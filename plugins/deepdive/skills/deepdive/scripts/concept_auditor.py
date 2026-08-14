#!/usr/bin/env -S uv run python
# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""Concept Completeness Auditor for Recursive PRD Writer.

Multi-pass extraction + validated coverage matching. Reports heuristic
coverage estimates with confidence levels and gap repair suggestions.

Usage:
    uv run concept_auditor.py --sources s1.md,s2.md --prd output.md
"""
from __future__ import annotations

import argparse, json, os, re, sys, time
from pathlib import Path
import anthropic

EXTRACTION_PROMPT = (
    "Extract ALL key concepts, requirements, constraints, technical terms, "
    "and specific details from this document. Return as a JSON array of "
    "strings, where each string is a concise concept (3-10 words). Be "
    "exhaustive -- include every distinct idea, not just main themes."
)
MATCHING_PROMPT = (
    "You are comparing two concept lists to determine coverage.\n\n"
    "SOURCE CONCEPTS (the ground truth that must be covered):\n{source_concepts}\n\n"
    "PRD CONCEPTS (what the document actually contains):\n{prd_concepts}\n\n"
    "For each source concept, determine if it is covered by ANY PRD concept, "
    "even if worded differently. Semantic equivalence counts as covered.\n\n"
    "Return a JSON object with exactly two keys:\n"
    '  "covered": array of source concept strings that ARE represented in the PRD\n'
    '  "missing": array of source concept strings that are NOT represented\n\n'
    "IMPORTANT: Every source concept must appear in exactly one of these arrays.\n"
    "Return ONLY valid JSON, no other text."
)
SECTION_SUGGEST_PROMPT = (
    "Given this PRD document and these missing concepts, suggest which PRD "
    "section each concept should be added to. Return a JSON array of objects "
    'with keys "concept" and "suggested_section".\n\n'
    "PRD (first 3000 chars):\n{prd_preview}\n\n"
    "Missing concepts:\n{missing}\n\n"
    "Return ONLY valid JSON, no other text."
)
MAX_RETRIES = 3
BACKOFF_BASE = 2


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Concept completeness auditor (heuristic)")
    p.add_argument("--sources", required=True, help="Comma-separated source file paths")
    p.add_argument("--prd", required=True, help="Path to the generated PRD file")
    p.add_argument("--model", default="claude-haiku-4-5-20251001", help="Model for extraction")
    p.add_argument("--threshold", type=float, default=0.85, help="Minimum coverage ratio")
    p.add_argument("--output-json", default=None, help="Optional path to write JSON results")
    return p.parse_args()


def read_file(path: str) -> str:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    return p.read_text(encoding="utf-8")


def parse_json_response(raw: str) -> object:
    """Parse JSON from LLM response, handling fences, preamble, bullet fallback."""
    text = raw.strip()
    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        text = m.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    for i, ch in enumerate(text):
        if ch in ("[", "{"):
            try:
                return json.loads(text[i:])
            except json.JSONDecodeError:
                continue
    lines = [l.strip().lstrip("-*").strip().strip('"').strip("'")
             for l in text.splitlines() if l.strip().startswith(("-", "*"))]
    if lines:
        return lines
    raise ValueError(f"Could not parse JSON from response: {text[:200]}")


def call_model(client: anthropic.Anthropic, model: str, prompt: str, content: str) -> str:
    """Call model with retry + exponential backoff on transient errors."""
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.messages.create(
                model=model, max_tokens=4096,
                messages=[{"role": "user", "content": f"{prompt}\n\n---\n\n{content}"}],
            )
            return resp.content[0].text
        except (anthropic.APIConnectionError, anthropic.RateLimitError,
                anthropic.InternalServerError) as exc:
            if attempt == MAX_RETRIES - 1:
                raise
            wait = BACKOFF_BASE ** (attempt + 1)
            print(f"  Retry {attempt+1}/{MAX_RETRIES} after {wait}s: {exc}", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError("Unreachable")


def extract_concepts_once(client: anthropic.Anthropic, model: str, text: str) -> list[str]:
    raw = call_model(client, model, EXTRACTION_PROMPT, text)
    result = parse_json_response(raw)
    if not isinstance(result, list):
        raise ValueError(f"Expected list, got {type(result)}")
    return [str(c) for c in result]


def extract_concepts(client: anthropic.Anthropic, model: str, text: str) -> list[str]:
    """Two independent extraction passes; return the union."""
    return sorted(set(extract_concepts_once(client, model, text))
                  | set(extract_concepts_once(client, model, text)))


def match_batch_once(
    client: anthropic.Anthropic, model: str,
    source_batch: list[str], prd_concepts: list[str],
) -> tuple[set[str], set[str]]:
    prompt = MATCHING_PROMPT.format(
        source_concepts=json.dumps(source_batch), prd_concepts=json.dumps(prd_concepts),
    )
    raw = call_model(client, model, prompt, "")
    result = parse_json_response(raw)
    if not isinstance(result, dict):
        raise ValueError(f"Expected dict, got {type(result)}")
    return set(result.get("covered", [])), set(result.get("missing", []))


def validated_match(
    client: anthropic.Anthropic, model: str,
    source_concepts: list[str], prd_concepts: list[str], batch_size: int = 20,
) -> tuple[list[str], list[str], list[str]]:
    """Multi-pass validated matching. Returns (covered, missing, uncertain)."""
    all_covered: set[str] = set()
    all_missing: set[str] = set()
    all_uncertain: set[str] = set()
    for i in range(0, len(source_concepts), batch_size):
        batch = source_concepts[i:i + batch_size]
        cov1, mis1 = match_batch_once(client, model, batch, prd_concepts)
        cov2, mis2 = match_batch_once(client, model, batch, prd_concepts)
        agreed_covered = cov1 & cov2
        agreed_missing = mis1 & mis2
        uncertain = set(batch) - agreed_covered - agreed_missing
        all_covered |= agreed_covered
        all_missing |= agreed_missing
        all_uncertain |= uncertain
    # Validation: catch silently dropped concepts
    total = len(source_concepts)
    accounted = len(all_covered) + len(all_missing) + len(all_uncertain)
    if accounted != total:
        print(f"  WARNING: {accounted} accounted vs {total} total ({total-accounted} "
              "unaccounted, added to uncertain)", file=sys.stderr)
        all_uncertain |= set(source_concepts) - all_covered - all_missing - all_uncertain
    return sorted(all_covered), sorted(all_missing), sorted(all_uncertain)


def suggest_sections(
    client: anthropic.Anthropic, model: str, prd_text: str, missing: list[str],
) -> dict[str, str]:
    if not missing:
        return {}
    prompt = SECTION_SUGGEST_PROMPT.format(
        prd_preview=prd_text[:3000], missing=json.dumps(missing),
    )
    items = parse_json_response(call_model(client, model, prompt, ""))
    if isinstance(items, list):
        return {it["concept"]: it["suggested_section"] for it in items if isinstance(it, dict)}
    return {}


def build_source_map(src_map: dict[str, list[str]], concepts: list[str]) -> list[dict]:
    result = []
    for concept in concepts:
        source = "unknown"
        for name, cs in src_map.items():
            if concept in cs:
                source = name
                break
        result.append({"concept": concept, "source": source})
    return result


def main() -> None:
    args = parse_args()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    client = anthropic.Anthropic()
    source_paths = [s.strip() for s in args.sources.split(",") if s.strip()]

    # Step 1: Multi-pass extraction from each source
    all_src: dict[str, list[str]] = {}
    for path in source_paths:
        name = Path(path).name
        try:
            concepts = extract_concepts(client, args.model, read_file(path))
            all_src[name] = concepts
            print(f"  Extracted {len(concepts)} concepts from {name} (2-pass union)", file=sys.stderr)
        except Exception as exc:
            print(f"  WARNING: Failed to process {name}: {exc}", file=sys.stderr)
    if not all_src:
        print("ERROR: No source concepts extracted.", file=sys.stderr)
        sys.exit(1)
    union = sorted({c for cs in all_src.values() for c in cs})

    # Step 2: Multi-pass extraction from PRD
    prd_text = read_file(args.prd)
    prd_concepts = extract_concepts(client, args.model, prd_text)
    print(f"  Extracted {len(prd_concepts)} concepts from PRD (2-pass union)", file=sys.stderr)

    # Step 3: Validated multi-pass matching
    covered, missing, uncertain = validated_match(client, args.model, union, prd_concepts)
    total = len(union)
    con_ratio = len(covered) / total if total else 1.0
    opt_ratio = (len(covered) + len(uncertain)) / total if total else 1.0
    agree_pct = (len(covered) + len(missing)) / total * 100 if total else 100.0
    confidence = "HIGH" if agree_pct >= 95 else ("MEDIUM" if agree_pct >= 80 else "LOW")

    # Step 4: Gap repair suggestions
    sec_map = suggest_sections(client, args.model, prd_text, missing)
    missing_det = build_source_map(all_src, missing)
    for item in missing_det:
        item["suggested_section"] = sec_map.get(item["concept"], "Unknown section")
    uncertain_det = build_source_map(all_src, uncertain)

    # Verdict
    thr = args.threshold
    if con_ratio >= thr:
        verdict = "LIKELY PASS"
    elif opt_ratio >= thr:
        verdict = "LIKELY PASS (marginal -- uncertain concepts could tip either way)"
    else:
        verdict = "LIKELY FAIL"

    # Report
    cp, op = con_ratio * 100, opt_ratio * 100
    mp = len(missing) / total * 100 if total else 0
    up = len(uncertain) / total * 100 if total else 0
    print(f"\n=== CONCEPT AUDIT REPORT (HEURISTIC) ===\n")
    print(f"Sources analyzed: {len(all_src)}")
    print(f"Extraction passes: 2 per source (union)")
    print(f"Matching passes: 2 per batch (intersection)\n")
    print(f"Total source concepts: {total}")
    print(f"PRD concepts: {len(prd_concepts)}\n")
    print(f"Coverage breakdown:")
    print(f"  Covered (both passes agree):   {len(covered):>4} ({cp:.1f}%)")
    print(f"  Missing (both passes agree):   {len(missing):>4} ({mp:.1f}%)")
    print(f"  Uncertain (passes disagree):   {len(uncertain):>4} ({up:.1f}%)")
    print(f"\nConfidence: {confidence} (passes agree on {agree_pct:.1f}% of concepts)\n")
    if missing_det:
        by_sec: dict[str, list[dict]] = {}
        for item in missing_det:
            by_sec.setdefault(item["suggested_section"], []).append(item)
        print("MISSING CONCEPTS (grouped by suggested section):")
        for section, items in sorted(by_sec.items()):
            print(f"  -> {section}")
            for it in items:
                print(f'     [{it["source"]}] "{it["concept"]}"')
        print()
    if uncertain_det:
        print("UNCERTAIN CONCEPTS (manual review recommended):")
        for it in uncertain_det:
            print(f'  [{it["source"]}] "{it["concept"]}"')
        print()
    print(f"VERDICT: {verdict} (coverage {cp:.1f}%-{op:.1f}% vs threshold {thr*100:.1f}%)")
    print(f"  Note: True coverage is between {cp:.1f}% (conservative) and {op:.1f}% (optimistic)")

    if args.output_json:
        output = {
            "source_concepts": all_src, "prd_concepts": prd_concepts,
            "covered": covered, "missing": missing_det, "uncertain": uncertain_det,
            "coverage_conservative": round(con_ratio, 4),
            "coverage_optimistic": round(opt_ratio, 4),
            "agreement_pct": round(agree_pct, 1),
            "confidence": confidence, "verdict": verdict, "threshold": thr,
        }
        Path(args.output_json).write_text(json.dumps(output, indent=2), encoding="utf-8")
        print(f"\nFull results written to {args.output_json}")
    sys.exit(0 if "PASS" in verdict else 1)


if __name__ == "__main__":
    main()
