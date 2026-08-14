---
name: deepdive
description: |
  Recursive context processing for information-dense tasks. Prevents quality
  degradation ("context rot") by probing sources with a persistent REPL and
  entropy profiling, decomposing based on empirical analysis, processing
  through focused sub-agents, and verifying coverage iteratively.

  Inspired by Zhang, Kraska & Khattab, "Recursive Language Models"
  (arXiv:2512.24601v2, Jan 2026), adapted for Claude Code's tool
  architecture. This is a practical approximation, not an implementation
  of the paper's Algorithm 1.

  REPL integration adapted from claude_code_RLM (MIT license).
  Entropy profiling adapted from minrlm (MIT license).

  Use when: processing multiple source documents, writing long-form output
  from sources, doing deep research across many inputs, the AI "cuts corners"
  or "misses details," user says /deepdive, "go deeper," "be thorough,"
  "don't skip anything," "process everything," "read all of these," "don't
  miss anything," or provides 3+ source files for synthesis.
---

# DeepDive v3 -- Recursive Context Engine

## The Problem

**Context rot**: LLM output quality degrades as input length and task
complexity increase. Three failure modes compound:

1. **Compaction loss** -- Summarizing inputs discards details the model
   cannot recover later. Early sources lose representation in later output.
2. **Autoregressive wrap-up** -- The model "feels done" before covering
   everything. Later sections get progressively shallower.
3. **Attention dilution** -- With many inputs in the prompt, the model forms
   surface impressions and generates from those instead of re-examining sources.

The result: output that reads well but silently drops 40-70% of source
concepts. Users say "it's cutting corners" or "it missed X from source Y."

## Three Invariants (Non-Negotiable)

### 1. Sources live in the environment, NEVER in the root prompt

The root agent sees only metadata, entropy maps, and REPL probe results.
Full content is read only by sub-agents processing specific slices via
Read with offset/limit.

**Why**: Loading all sources into the prompt creates lossy impressions
during the initial read. The model then generates from impressions instead
of re-examining the material.

### 2. Output assembled from variables, NEVER autoregressed in one shot

Each output chunk is produced by an independent sub-agent and written to
the workspace as a file. The final result is assembled programmatically.

**Why**: Autoregressive generation has no concept of coverage completeness.
File-based assembly guarantees every chunk exists before declaring completion.

### 3. Recursion is symbolic (code/tools), NEVER verbalized

Use the Agent tool in programmatic patterns to process every input. Never
say "and similarly for the remaining sources" -- every iteration must execute.

**Why**: When the model verbalizes sub-tasks, it controls how many actually
run and will often shortcut. Programmatic loops via Agent tool are
deterministic.

## The Algorithm

```
INIT -> PROBE -> PLAN -> EXECUTE -> VERIFY -> DECIDE
                                                 |
                              loop back ---------+-- or finalize -> ASSEMBLE
```

### INIT -- Create Workspace and Initialize REPL

Create a persistent workspace and initialize the REPL for each source.

1. Create workspace:
   ```bash
   WORKSPACE=$(mktemp -d /tmp/deepdive-XXXXXX)
   echo "Workspace: $WORKSPACE"
   ```

2. Resolve the skill path. Check `<skill_path>/scripts/rlm_repl.py` exists.
   The REPL script provides persistent Python state with helpers: `peek`,
   `grep`, `chunk_indices`, `write_chunks`, `add_buffer`.

3. Initialize the REPL for each source:
   ```bash
   python3 <skill_path>/scripts/rlm_repl.py --state $WORKSPACE/repl_src0.pkl \
     init /abs/path/to/source0.md
   ```
   Each source gets its own state pickle so probes do not cross-contaminate.

4. Write `$WORKSPACE/state.json`:
   ```json
   {
     "sources": [
       {"path": "/abs/path/file.md", "lines": 842, "bytes": 34201,
        "type": "markdown", "repl_state": "$WORKSPACE/repl_src0.pkl"}
     ],
     "iteration": 0,
     "phase": "init"
   }
   ```

### PROBE -- Entropy Profiling + REPL Analysis

Two-stage probe: first get a compression-based entropy map (fast, mechanical),
then use the REPL to investigate what the entropy map reveals.

#### Stage 1: Entropy Profiling

Run `scripts/entropy_probe.py` on each source. This computes zlib
compression ratios across micro-chunks (500 chars), aggregates them into
macro-sections, and flags spikes (regions with distinctively unique content
vs repetitive boilerplate).

```bash
python3 <skill_path>/scripts/entropy_probe.py /abs/path/source.md \
  --sections 20 --out $WORKSPACE/entropy_src0.json
```

If the script does not exist, approximate with the REPL:

```bash
python3 <skill_path>/scripts/rlm_repl.py --state $WORKSPACE/repl_src0.pkl \
  exec <<'PY'
import zlib, json
micro = 500
n = len(content)
ratios = []
for i in range(n // micro):
    raw = content[i*micro:(i+1)*micro].encode('utf-8', errors='replace')
    ratios.append(round(len(zlib.compress(raw, 1)) / max(len(raw), 1), 3))
# Aggregate into 20 sections
per_sec = max(len(ratios) // 20, 1)
sections = []
for s in range(20):
    seg = ratios[s*per_sec:(s+1)*per_sec if s < 19 else len(ratios)]
    if seg:
        sections.append({
            "section": s, "char_start": s*per_sec*micro,
            "char_end": min((s+1)*per_sec*micro, n),
            "max_ratio": max(seg), "median_ratio": sorted(seg)[len(seg)//2]
        })
print(json.dumps(sections, indent=2))
PY
```

**Interpreting the entropy map**:
- Higher compression ratio = more unique/diverse content (information-dense)
- Lower compression ratio = more repetitive/boilerplate
- Spikes indicate regions to focus sub-agent attention on
- Uniform distribution means content complexity is consistent

Save entropy results to `$WORKSPACE/entropy_src{N}.json`.

#### Stage 2: REPL Probing

Use the persistent REPL to investigate structure and content patterns.

```bash
# Scout beginning and end
python3 <skill_path>/scripts/rlm_repl.py --state $WORKSPACE/repl_src0.pkl \
  exec -c "print(peek(0, 3000))"
python3 <skill_path>/scripts/rlm_repl.py --state $WORKSPACE/repl_src0.pkl \
  exec -c "print(peek(len(content)-3000, len(content)))"

# Search for structural patterns
python3 <skill_path>/scripts/rlm_repl.py --state $WORKSPACE/repl_src0.pkl \
  exec <<'PY'
import re, json
headings = grep(r'^#{1,6}\s+', max_matches=50)
print(json.dumps([h['match'].strip() for h in headings], indent=2))
PY

# Investigate a high-entropy spike region
python3 <skill_path>/scripts/rlm_repl.py --state $WORKSPACE/repl_src0.pkl \
  exec -c "print(peek(14000, 17000))"  # spike at section 7
```

**Iterate probes until decomposition strategy is clear.** There is no fixed
count. The entropy map tells you WHERE to look; the REPL tells you WHAT
is there. Stop when you know enough to plan line-range assignments.

Store final probe results in `$WORKSPACE/probe_results.json`.

### PLAN -- Decomposition from Entropy + Probe Results

Build a decomposition plan grounded in data, not previews.

1. Read `$WORKSPACE/probe_results.json` and all `entropy_src{N}.json` files.

2. Assign subtasks to specific line-ranges. Use probe-discovered structure
   (headings, sections, data boundaries) as natural split points. Weight
   sub-agent attention toward entropy spikes -- these contain the most
   distinctive information and are most likely to be lost by compression.

3. Write `$WORKSPACE/plan.json`:
   ```json
   {
     "subtasks": [
       {
         "id": "chunk_1",
         "description": "Extract problem definition from spec",
         "sources": [
           {"path": "/path/file.md", "start_line": 1, "end_line": 120}
         ],
         "entropy_note": "spike at chars 2000-4000, focus on unique constraints",
         "output_format": "structured analysis",
         "depends_on": []
       }
     ],
     "coverage_map": {
       "/path/file.md": [[1, 120, "chunk_1"], [121, 300, "chunk_2"]]
     }
   }
   ```

4. Verify every source line-range appears in at least one subtask. Gaps in
   the coverage_map must be filled before proceeding.

### EXECUTE -- Spawn Sub-Agents

For each subtask, spawn a sub-agent using the Agent tool. Use the Haiku
model for cost efficiency.

**Sub-agent prompt structure:**

```
You are completing ONE subtask for a recursive context engine. Be
exhaustive -- extract every relevant detail from your assigned input
region. Do not summarize. Do not skip edge cases, constraints, or details.

SUBTASK: {description}
OUTPUT FORMAT: {format}
ENTROPY NOTE: {entropy_note}

Read the file {path} using Read tool with offset={start_line} and
limit={end_line - start_line}. Process ONLY that region. Pay special
attention to any region flagged as high-entropy -- it contains
distinctive content that is easy to lose in summarization.

If your assigned content exceeds ~15K tokens and contains distinct
sub-sections, you may recurse: create a sub-workspace, probe, plan,
and spawn your own sub-agents. Maximum recursion depth: {max_depth - 1}.
At depth 0, process directly.

Return your result as JSON:
{
  "chunk_id": "{id}",
  "relevant": [
    {"point": "...", "evidence": "short quote or paraphrase", "confidence": "high|medium|low"}
  ],
  "missing": ["what you could not determine from this chunk"],
  "gaps": ["cross-references to other chunks that may be needed"]
}
```

Rules:
- Run independent subtasks in parallel (multiple Agent tool calls).
- Each sub-agent reads ONLY its assigned line-range via Read with
  offset and limit.
- Write each output to `$WORKSPACE/chunks/chunk_{id}.md`.
- Default max_depth: 2. For inputs > 100K tokens total, consider depth 3.

### VERIFY -- Cross-Reference Overlapping Chunks

After all subtasks complete, check for consistency.

1. Build a source-overlap graph: which chunks share source material or
   have logical dependencies? Read `$WORKSPACE/plan.json` to identify
   overlapping source regions and dependency relationships.

2. For each pair of chunks that share sources or have dependencies,
   spawn a verification sub-agent:
   ```
   Compare these two output sections. Check for:
   - Contradictions (same concept described differently)
   - Gaps (information in source region not reflected in either chunk)
   - Missing cross-references (chunk A mentions X, chunk B should reference it)

   SECTION A: {read chunk_a from workspace}
   SECTION B: {read chunk_b from workspace}

   Output a JSON list of issues, or empty list if consistent.
   ```

3. Write all issues to `$WORKSPACE/verify_issues.json`.

**Why pairwise on overlapping chunks, not just adjacent**: When chunk 7
references the same source region as chunk 2, contradictions can emerge
that sequential adjacency checks would miss.

### DECIDE -- The Iteration Loop

Evaluate quality and decide whether to loop or finalize.

1. Read all workspace state:
   - `probe_results.json` and `entropy_src{N}.json`
   - `plan.json`
   - `chunks/*.md`
   - `verify_issues.json`

2. Evaluate:
   - Unresolved verification issues?
   - Coverage heuristic suggests gaps? (See "Coverage Heuristic" below.)
   - Chunks suspiciously thin relative to their source region size?
   - Sub-agents that failed or produced truncated output?
   - High-entropy regions inadequately represented in output?

3. If issues exist AND iteration budget remains (default: 3 loops max):
   - Adapt the plan: re-split problematic chunks, reassign sources.
   - Re-execute only the affected subtasks.
   - Re-verify affected pairs.
   - Write decision to `$WORKSPACE/decisions/decision_{iteration}.json`.
   - Increment iteration counter and loop back to EXECUTE.

4. If satisfied OR budget exhausted:
   - Proceed to ASSEMBLE.
   - If budget exhausted with remaining issues, log them as known gaps.

### ASSEMBLE -- Produce Final Output

1. Read all chunks from `$WORKSPACE/chunks/` in plan order.
2. Concatenate with appropriate headers, transitions, and structure.
3. Report:
   - Coverage heuristic result and any known gaps (see below).
   - Iterations taken.
   - Entropy spikes and whether they are represented in output.
   - Unresolved issues, if any.
4. Write final output to the user's specified path.
5. Clean up: `rm -rf $WORKSPACE`.

## Coverage Heuristic

An LLM-based fuzzy check comparing source concepts against output concepts.
Not a mathematical guarantee -- the extraction itself is an LLM task subject
to recall limits. Report the ratio as a heuristic indicator.

1. For each source, spawn a sub-agent to extract all key concepts as a flat
   bullet list. Do the same for the assembled draft.
2. Diff the lists. Concepts in sources but not in output are gaps.
3. Below 80% coverage: trigger another DECIDE loop. Above 80%: report and proceed.

If `scripts/concept_auditor.py` exists:
```bash
uv run <skill_path>/scripts/concept_auditor.py \
  --sources file1.md file2.md --output draft.md
```

## REPL Quick Reference

Persistent Python REPL (`scripts/rlm_repl.py`, from claude_code_RLM, MIT).
State persists in pickle files. Each source gets its own `--state` path.

**Commands**: `init <path>` | `exec -c "code"` | `exec <<'PY'...PY` |
`status` | `reset` | `export-buffers <path>`

**Injected into exec environment**:
- `content` (str), `context` (dict), `buffers` (list)
- `peek(start, end)` -- slice content
- `grep(pattern, max_matches=20, window=120)` -- regex search with context
- `chunk_indices(size, overlap)` -- compute (start, end) spans
- `write_chunks(out_dir, size, overlap, prefix)` -- write chunks to disk
- `add_buffer(text)` -- append to buffers

## Entropy Quick Reference

Compression-based density profiling (from minrlm, MIT). Splits text into
500-char micro-chunks, compresses each with zlib, reports ratio per section.

| Ratio range | Meaning | Action |
|-------------|---------|--------|
| 0.3 - 0.5 | Repetitive/boilerplate | Process quickly |
| 0.5 - 0.7 | Average complexity | Standard processing |
| 0.7 - 1.0 | High unique content | Focus sub-agent attention here |
| Spike | Well above median | Assign granular chunks, verify first |

## Recursive Depth

| Total input tokens | max_depth |
|--------------------|-----------|
| < 15K              | 1         |
| 15K - 100K         | 2         |
| 100K - 500K        | 3         |
| > 500K             | 3 (larger chunks) |

Pass `max_depth - 1` to sub-agents. At 0, process directly.

## Task Modes

### PRD/Spec
Use `deepdive-prd` sub-skill if available. PROBE for requirements,
stakeholders, constraints, success criteria. Cross-reference against
existing specs and capability inventories to catch gaps.

### Research & Competitive Analysis
Decompose by source, add synthesis pass for themes and contradictions.
For competitive analysis, assign one sub-agent per competitor to prevent
cross-contamination. Verify phase catches conflicting claims.

### Document Analysis
Decompose by logical unit. Entropy spikes often mark analytically
interesting sections.

### Code Review & Refactoring
Decompose by file/module. Cross-reference interfaces and error handling.
For large refactors (10+ files), entropy profiling identifies the dense
or tricky files that need focused attention. Verify phase catches
interface mismatches across modules.

### Marketing & Content Production
Process multiple sources (brand guides, analytics, research papers,
competitor data, client briefs) into high-fidelity marketing outputs.
Key applications:
- **Client onboarding**: Digest all client materials without losing the
  priority buried on page 12 of the brand guide
- **RFP responses**: Every requirement addressed, none silently dropped
- **SEO content planning**: Cross-reference keyword data + competitor
  content + client brief + search intent
- **Case studies**: Project data + client feedback + analytics + emails
  processed exhaustively
- **White papers / thought leadership**: 5+ academic or industry sources
  with coverage verification
- **Newsletter curation**: Entropy profiling finds novel content vs
  rehashes across 20+ weekly articles

### Migration & Integration Planning
Process old system docs + new framework docs + constraints. REPL probing
finds edge cases in legacy documentation. Coverage heuristic ensures no
constraint is missed.

### Multi-Client Reporting
Process analytics from multiple client accounts. Each client gets a
dedicated sub-agent to prevent data cross-contamination.

### Autonomous Quality Pipeline
DeepDive serves as the engine for "Factual-Rich" version generation in
multi-version quality loops. When research agents gather 5+ sources
before content generation, DeepDive processes ALL sources with coverage
verification, ensuring the output is provably grounded in research
rather than model impressions. The coverage heuristic (>80%) provides
an anti-hallucination guarantee that regular prompting cannot offer.

## When to Use / When NOT to Use

**Use when**:
- 3+ sources, > 8K tokens total
- Source fidelity matters (RFPs, proposals, audits, research-backed content)
- Pairwise cross-referencing needed (competitive analysis, multi-API integration)
- User reports shallow output or "it missed X from source Y"
- Generating the "Factual-Rich" version in a multi-version quality loop
- Client onboarding with brand guide + analytics + campaign history
- Large codebase refactors or migrations (10+ files, multiple doc sources)
- Any task where silent 40-70% concept loss is unacceptable

**Skip when**:
- Short context (< 4K tokens)
- Speed over completeness (social media posts, quick replies, status updates)
- Creative writing where source fidelity is not the goal
- Generating "Light" versions designed to be fast, not exhaustive
- Single-source tasks where a direct Read is sufficient

## Scripts

Check existence before invoking. If absent, run the algorithm manually.

| Script | Purpose |
|--------|---------|
| `scripts/rlm_repl.py` | Persistent REPL |
| `scripts/entropy_probe.py` | Standalone entropy profiler |
| `scripts/concept_auditor.py` | Coverage heuristic |
| `scripts/rce_engine.py` | Full recursive engine |

## Fallback

If REPL or sub-agents fail: log failure, fall back to single-pass, append
"Generated without recursive verification -- coverage not verified."

## Quality Checklist

- [ ] Every source line-range assigned to at least one subtask
- [ ] Entropy spikes covered by focused subtasks, not lumped into large chunks
- [ ] No chunk reads as generic summary -- each has source-specific details
- [ ] Coverage heuristic run and reported (with caveats)
- [ ] No unresolved contradictions between chunks
- [ ] Output could not have been produced without the specific sources
- [ ] Workspace cleaned up after assembly

## Attribution

- **REPL**: Adapted from claude_code_RLM (MIT). Persistent pickle REPL and
  helpers (peek, grep, chunk_indices, write_chunks, add_buffer).
- **Entropy**: Adapted from minrlm (MIT). zlib compression-ratio approach
  from `compute_entropy_profile`.
- **Recursive decomposition**: Inspired by Zhang, Kraska & Khattab,
  "Recursive Language Models" (arXiv:2512.24601v2, Jan 2026). Practical
  approximation, not an implementation of Algorithm 1.
- **VERIFY/audit phases**: Original to DeepDive. Not present in
  claude_code_RLM or minrlm.
