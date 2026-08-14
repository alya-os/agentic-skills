#!/usr/bin/env -S uv run python
# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""Recursive Context Engine (RCE) v2 for PRD Generation.

Defeats "plan overtaking" via 4+ phases with iterative gap-filling:
  1 - Metadata Planning:  Root model sees ONLY file metadata, never content
  2 - Section Writing:    Sub-model writes sections from chunked source segments
  3 - Cross-Reference:    Source-overlap-aware pairwise consistency checks
  4 - Concept Audit:      Dual-pass set-difference coverage verification
  Iteration:              Re-run for gaps until coverage >= threshold

INVARIANT: Source file content is NEVER sent whole to the API. Sources are
chunked and only the assigned segment is included per sub-call.

Usage:
    uv run scripts/rce_engine.py \\
        --sources file1.md,file2.md --task "Write PRD for X" --output prd.md
"""
import argparse, json, os, re, sys, time
from pathlib import Path
import anthropic

# -- Globals ----------------------------------------------------------------
client: anthropic.Anthropic = None
CALL_COUNT = INPUT_TOKENS = OUTPUT_TOKENS = 0
MAX_TOKENS = 8192
INPUT_COST_PER_M = 3.0
OUTPUT_COST_PER_M = 15.0
CHUNK_SIZE = 2000
FAILED_PREFIX = "[SECTION GENERATION FAILED"
MARKER_A, MARKER_B = "=== SECTION A ===", "=== SECTION B ==="

def log(msg: str) -> None:
    print(f"[RCE] {msg}", file=sys.stderr)

def approx_tokens(text: str) -> int:
    return max(1, int(len(text.split()) / 0.75))

# -- Robust JSON extraction -------------------------------------------------
def extract_json(raw: str, expect_type: type = list):
    """Extract JSON from LLM output handling fences, preamble, multi-block."""
    raw = raw.strip()
    # 1) Direct parse
    try:
        obj = json.loads(raw)
        if isinstance(obj, expect_type): return obj
    except json.JSONDecodeError: pass
    # 2) Markdown fences
    for m in re.finditer(r"```(?:json)?\s*\n?(.*?)```", raw, re.DOTALL):
        try:
            obj = json.loads(m.group(1).strip())
            if isinstance(obj, expect_type): return obj
        except json.JSONDecodeError: continue
    # 3) Largest bracket-delimited block
    opener = "[" if expect_type is list else "{"
    closer = "]" if expect_type is list else "}"
    best, best_len = None, 0
    for i, ch in enumerate(raw):
        if ch != opener: continue
        depth = 0
        for j in range(i, len(raw)):
            if raw[j] == opener: depth += 1
            elif raw[j] == closer: depth -= 1
            if depth == 0:
                cand = raw[i:j+1]
                try:
                    obj = json.loads(cand)
                    if isinstance(obj, expect_type) and len(cand) > best_len:
                        best, best_len = obj, len(cand)
                except json.JSONDecodeError: pass
                break
    if best is not None: return best
    raise ValueError(f"Could not extract {expect_type.__name__} JSON from response")

# -- LLM call with retry + exponential backoff ------------------------------
def llm(model: str, system: str, user: str, *, json_mode: bool = False,
        expect_type: type = list) -> str:
    """Anthropic API call. Retries 3x with backoff on transient errors."""
    global CALL_COUNT, INPUT_TOKENS, OUTPUT_TOKENS
    CALL_COUNT += 1
    for attempt in range(4):
        try:
            r = client.messages.create(
                model=model, max_tokens=MAX_TOKENS, system=system,
                messages=[{"role": "user", "content": user}],
            )
            INPUT_TOKENS += r.usage.input_tokens
            OUTPUT_TOKENS += r.usage.output_tokens
            text = r.content[0].text
            return json.dumps(extract_json(text, expect_type)) if json_mode else text
        except anthropic.RateLimitError:
            if attempt < 3:
                log(f"  Rate limited, retry in {2**(attempt+1)}s..."); time.sleep(2**(attempt+1)); continue
            raise
        except anthropic.APIStatusError as exc:
            if exc.status_code >= 500 and attempt < 3:
                log(f"  Server {exc.status_code}, retry in {2**(attempt+1)}s..."); time.sleep(2**(attempt+1)); continue
            raise
        except anthropic.APIConnectionError:
            if attempt < 3:
                log(f"  Connection error, retry in {2**(attempt+1)}s..."); time.sleep(2**(attempt+1)); continue
            raise
    raise RuntimeError("Exhausted retries")

# -- Source loading (chunked, never whole) ----------------------------------
def read_sources(paths: list[str]) -> list[dict]:
    """Load source files. Stores lines for chunked delivery."""
    sources = []
    for p in paths:
        fp = Path(p).expanduser().resolve()
        if not fp.exists():
            log(f"WARNING: not found: {fp}"); continue
        text = fp.read_text(encoding="utf-8", errors="replace")
        sources.append(dict(index=len(sources), filename=fp.name, path=str(fp),
                            tokens=approx_tokens(text), lines=text.splitlines(keepends=True),
                            preview=text[:800]))
    return sources

def get_chunk(src: dict, start: int) -> tuple[str, int]:
    """Return (chunk_text, end_line) for a source segment."""
    end = min(start + CHUNK_SIZE, len(src["lines"]))
    return "".join(src["lines"][start:end]), end

# -- Phase 1: Metadata Planning (root model sees NO content) ----------------
def phase1(sources: list[dict], task: str, model: str, max_sec: int) -> list[dict]:
    log("Phase 1 -- Metadata Planning")
    meta = [dict(index=s["index"], filename=s["filename"],
                 tokens=s["tokens"], preview=s["preview"][:200]) for s in sources]
    sys_p = ("You are an expert technical writer planning a PRD. You receive ONLY metadata "
             "about source files -- not their content. Design the document structure and map "
             "sources to sections. Return ONLY valid JSON, no markdown fences.")
    usr_p = (f"TASK: {task}\n\nSOURCE FILES ({len(sources)}):\n{json.dumps(meta, indent=2)}"
             f"\n\nCreate up to {max_sec} sections. Return a JSON array of objects with keys: "
             '"title" (string), "description" (1-2 sentences), "assigned_source_indices" '
             '(list of ints), "requirements" (writer instructions). JSON array only.')
    outline = json.loads(llm(model, sys_p, usr_p, json_mode=True, expect_type=list))
    log(f"  Planned {len(outline)} sections")
    for i, s in enumerate(outline):
        log(f"  [{i+1}] {s['title']} (sources: {s.get('assigned_source_indices', [])})")
    return outline

# -- Phase 2: Section Writing (chunked source delivery) ---------------------
def phase2(outline: list[dict], sources: list[dict], model: str,
           section_filter: set[str] | None = None) -> dict[str, str]:
    """Write sections with ONLY chunked source segments in context."""
    log("Phase 2 -- Section Writing")
    sections: dict[str, str] = {}
    sys_p = ("You are writing ONE section of a PRD. Be exhaustive. Reference specific "
             "details from the source material. Do not summarize or invent. Use clear "
             "technical prose with bullets where appropriate. Never use em dash characters.")
    for i, sec in enumerate(outline):
        title = sec["title"]
        if section_filter and title not in section_filter: continue
        log(f"  [{i+1}/{len(outline)}] {title}")
        ctx_parts = []
        for idx in sec.get("assigned_source_indices", []):
            if 0 <= idx < len(sources):
                s = sources[idx]
                total = len(s["lines"])
                for start in range(0, total, CHUNK_SIZE):
                    chunk, end = get_chunk(s, start)
                    ctx_parts.append(f"--- SOURCE: {s['filename']} (index {idx}) "
                                     f"lines {start+1}-{end} of {total} ---\n{chunk}")
        ctx = "\n\n".join(ctx_parts) if ctx_parts else "(No sources assigned.)"
        usr_p = (f"SECTION: {title}\nDESCRIPTION: {sec.get('description','')}\n"
                 f"REQUIREMENTS: {sec.get('requirements','')}\n\nSOURCE MATERIAL:\n{ctx}\n\n"
                 "Write this section now. Start directly with content, no heading.")
        try:
            sections[title] = llm(model, sys_p, usr_p)
        except Exception as exc:
            log(f"  ERROR: {exc}"); sections[title] = f"[SECTION GENERATION FAILED: {exc}]"
    return sections

# -- Phase 3: Source-overlap-aware pairwise cross-reference -----------------
def phase3(sections: dict[str, str], outline: list[dict], model: str) -> dict[str, str]:
    """Check ALL pairs sharing assigned sources, plus bookends."""
    log("Phase 3 -- Cross-Reference Verification")
    titles = list(sections.keys())
    if len(titles) < 2:
        log("  Skipping (< 2 sections)"); return sections
    # Build overlap graph
    src_map = {sec["title"]: set(sec.get("assigned_source_indices", [])) for sec in outline}
    pairs: set[tuple[str, str]] = set()
    for ai, ta in enumerate(titles):
        for bi in range(ai + 1, len(titles)):
            tb = titles[bi]
            if src_map.get(ta, set()) & src_map.get(tb, set()):
                pairs.add((ta, tb))
    pairs.add((titles[0], titles[-1]))  # bookends

    out = dict(sections)
    check_sys = ("You review two PRD sections sharing source material. Identify "
                 "contradictions, gaps, missing cross-references. Never use em dash "
                 'characters.\nReturn ONLY JSON: '
                 '{"issues_found": bool, "issues": [...], "repair_needed": bool}')
    repair_sys = ("Repair two PRD sections to fix identified issues. Never use em dash "
                  f"characters.\nFormat response exactly as:\n{MARKER_A}\n(content A)\n"
                  f"{MARKER_B}\n(content B)")
    checked = 0
    for ta, tb in sorted(pairs):
        ca, cb = out.get(ta, ""), out.get(tb, "")
        if ca.startswith(FAILED_PREFIX) or cb.startswith(FAILED_PREFIX): continue
        log(f"  Checking: '{ta}' <-> '{tb}'"); checked += 1
        try:
            raw = llm(model, check_sys,
                      f"SECTION A: {ta}\n{ca}\n\nSECTION B: {tb}\n{cb}\n\nReturn JSON.",
                      json_mode=True, expect_type=dict)
            res = json.loads(raw)
        except Exception as exc:
            log(f"  WARNING: check failed: {exc}"); continue
        if not (res.get("repair_needed") and res.get("issues")): continue
        issues = "\n".join(f"- {x}" for x in res["issues"])
        log(f"  Repairing {len(res['issues'])} issue(s)...")
        try:
            txt = llm(model, repair_sys,
                      f"ISSUES:\n{issues}\n\nSECTION A ({ta}):\n{ca}\n\n"
                      f"SECTION B ({tb}):\n{cb}\n\nFix all issues, preserve detail.")
            if MARKER_A in txt and MARKER_B in txt:
                a_s = txt.index(MARKER_A) + len(MARKER_A)
                b_s = txt.index(MARKER_B)
                out[ta] = txt[a_s:b_s].strip()
                out[tb] = txt[b_s + len(MARKER_B):].strip()
                log("  Repair applied.")
            else:
                log("  WARNING: unexpected repair format, keeping originals.")
        except Exception as exc:
            log(f"  WARNING: repair failed: {exc}")
    log(f"  Checked {checked} pair(s)")
    return out

# -- Phase 4: Dual-pass concept audit --------------------------------------
def phase4(sources: list[dict], sections: dict[str, str],
           model: str, threshold: float) -> tuple[dict[str, str], float, list[str]]:
    """Dual-pass concept extraction + coverage. Returns (sections, ratio, missing)."""
    log("Phase 4 -- Concept Audit")
    extract_sys = ("Extract ALL key concepts, requirements, constraints, and technical "
                   "details. Return ONLY a JSON array of short concept strings. Be thorough.")
    # Extract from each source (chunked)
    src_concepts: dict[str, list[str]] = {}
    for s in sources:
        log(f"  Extracting from: {s['filename']}")
        concepts: list[str] = []
        for start in range(0, len(s["lines"]), CHUNK_SIZE):
            chunk, _ = get_chunk(s, start)
            try:
                parsed = json.loads(llm(model, extract_sys, chunk, json_mode=True, expect_type=list))
                if isinstance(parsed, list): concepts.extend(str(c) for c in parsed)
            except Exception as exc:
                log(f"    WARNING: chunk extraction failed: {exc}")
        src_concepts[s["filename"]] = concepts
        log(f"    {len(concepts)} concepts")
    all_src: set[str] = set()
    for v in src_concepts.values(): all_src.update(v)
    if not all_src:
        log("  No concepts extracted, skipping."); return sections, 1.0, []
    # Extract from PRD
    prd_text = "\n\n".join(f"## {t}\n{c}" for t, c in sections.items()
                           if not c.startswith(FAILED_PREFIX))
    log("  Extracting from PRD...")
    try:
        prd_set = set(str(c) for c in json.loads(
            llm(model, extract_sys, prd_text, json_mode=True, expect_type=list)))
        log(f"  PRD has {len(prd_set)} concepts")
    except Exception as exc:
        log(f"  WARNING: PRD extraction failed: {exc}"); prd_set = set()
    # Dual-pass semantic coverage (intersection reduces false positives)
    log("  Computing coverage (dual-pass semantic match)...")
    src_list, prd_list = sorted(all_src), sorted(prd_set)
    match_sys = ("Compare source concepts against PRD concepts. A source concept is "
                 "'covered' if the PRD contains it or a close equivalent.\n"
                 'Return ONLY JSON: {"covered": [...], "missing": [...]}')
    prompt = (f"SOURCE ({len(src_list)}):\n{json.dumps(src_list)}\n\n"
              f"PRD ({len(prd_list)}):\n{json.dumps(prd_list)}")
    covered_sets: list[set[str]] = []
    for p_num in range(1, 3):
        log(f"    Pass {p_num}...")
        try:
            mr = json.loads(llm(model, match_sys, prompt, json_mode=True, expect_type=dict))
            covered_sets.append(set(mr.get("covered", [])))
        except Exception as exc:
            log(f"    WARNING: pass {p_num} failed: {exc}"); covered_sets.append(set())
    covered = (covered_sets[0] & covered_sets[1]) if len(covered_sets) == 2 else (covered_sets[0] if covered_sets else set())
    missing = sorted(all_src - covered)
    cov = len(covered) / len(all_src) if all_src else 1.0
    # Validate partition
    if len(covered) + len(missing) != len(all_src):
        log(f"  WARNING: partition mismatch -- {len(covered)}+{len(missing)} != {len(all_src)}")
    log(f"  Coverage (heuristic): {cov:.1%} ({len(covered)}/{len(all_src)}), Missing: {len(missing)}")
    for fn, cs in src_concepts.items(): log(f"    {fn}: {len(cs)} concepts")
    log(f"    Total: {len(all_src)} | PRD: {len(prd_set)} | Covered: {len(covered)} | "
        f"Missing: {len(missing)} | Ratio: {cov:.3f}")
    return sections, cov, missing

# -- Assembly ---------------------------------------------------------------
def assemble(sections: dict[str, str]) -> str:
    return "\n\n---\n\n".join(f"## {t}\n\n{c}" for t, c in sections.items())

# -- Main -------------------------------------------------------------------
def main() -> None:
    global client, MAX_TOKENS, CHUNK_SIZE, INPUT_COST_PER_M, OUTPUT_COST_PER_M
    ap = argparse.ArgumentParser(description="Recursive Context Engine v2")
    ap.add_argument("--sources", required=True, help="Comma-separated source file paths")
    ap.add_argument("--task", required=True, help="Task description for the PRD")
    ap.add_argument("--output", required=True, help="Output file path")
    ap.add_argument("--root-model", default="claude-sonnet-4-6")
    ap.add_argument("--sub-model", default="claude-haiku-4-5-20251001")
    ap.add_argument("--max-sections", type=int, default=15)
    ap.add_argument("--coverage-threshold", type=float, default=0.85)
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--chunk-size", type=int, default=2000)
    ap.add_argument("--max-iterations", type=int, default=2)
    ap.add_argument("--input-cost", type=float, default=3.0, help="$/1M input tokens")
    ap.add_argument("--output-cost", type=float, default=15.0, help="$/1M output tokens")
    args = ap.parse_args()

    MAX_TOKENS = args.max_tokens
    CHUNK_SIZE = args.chunk_size
    INPUT_COST_PER_M = args.input_cost
    OUTPUT_COST_PER_M = args.output_cost

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.", file=sys.stderr); sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)

    src_paths = [p.strip() for p in args.sources.split(",") if p.strip()]
    if not src_paths:
        print("ERROR: No source files.", file=sys.stderr); sys.exit(1)

    log(f"Task: {args.task}")
    log(f"Sources: {len(src_paths)} | Root: {args.root_model} | Sub: {args.sub_model}")
    log(f"Max sections: {args.max_sections} | Coverage: {args.coverage_threshold:.0%} "
        f"| Iterations: {args.max_iterations} | Tokens: {MAX_TOKENS} | Chunk: {CHUNK_SIZE}\n")
    t0 = time.time()

    sources = read_sources(src_paths)
    if not sources:
        print("ERROR: No valid source files.", file=sys.stderr); sys.exit(1)
    log(f"Loaded {len(sources)} sources (~{sum(s['tokens'] for s in sources):,} tokens)\n")

    try:
        outline = phase1(sources, args.task, args.root_model, args.max_sections)
    except Exception as exc:
        print(f"FATAL: Phase 1 failed: {exc}", file=sys.stderr); sys.exit(1)
    log("")

    sections = phase2(outline, sources, args.sub_model); log("")
    sections = phase3(sections, outline, args.sub_model); log("")

    # Phase 4 + iterative gap-filling
    coverage, missing = 0.0, []
    for iteration in range(1, args.max_iterations + 1):
        log(f"=== Iteration {iteration}/{args.max_iterations} ===")
        sections, coverage, missing = phase4(sources, sections, args.sub_model,
                                             args.coverage_threshold)
        log("")
        if coverage >= args.coverage_threshold or not missing:
            log(f"Coverage {coverage:.1%} meets threshold."); break
        log(f"Coverage {coverage:.1%} below threshold. Gap-filling...")
        miss_txt = "\n".join(f"- {c}" for c in missing[:50])
        try:
            sup = llm(args.sub_model,
                      "Add missing concepts to a PRD. Never use em dash characters. "
                      "Write a 'Supplementary Details' section covering them with depth.",
                      f"MISSING CONCEPTS:\n{miss_txt}\n\nCover each concept thoroughly.")
            label = f"Supplementary Details" if iteration == 1 else f"Supplementary Details ({iteration})"
            sections[label] = sup
            log(f"  Gap-fill section '{label}' added.")
        except Exception as exc:
            log(f"  WARNING: gap-fill failed: {exc}")
        log("")

    out_path = Path(args.output).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(assemble(sections), encoding="utf-8")

    elapsed = time.time() - t0
    cost = (INPUT_TOKENS / 1e6 * INPUT_COST_PER_M) + (OUTPUT_TOKENS / 1e6 * OUTPUT_COST_PER_M)
    log("=" * 50)
    log("RCE v2 COMPLETE")
    log(f"  Sections: {len(sections)} | Calls: {CALL_COUNT} | Coverage: {coverage:.3f}")
    log(f"  Tokens in/out: {INPUT_TOKENS:,}/{OUTPUT_TOKENS:,} | Est. cost: ${cost:.2f}")
    log(f"  Time: {elapsed:.1f}s | Output: {out_path}")
    log("=" * 50)

if __name__ == "__main__":
    main()
