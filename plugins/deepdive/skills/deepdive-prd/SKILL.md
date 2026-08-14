---
name: deepdive-prd
description: >
  PRD and spec writing mode for the deepdive v3 recursive engine. Provides
  section templates, source-to-section mapping, and PRD-specific quality
  criteria. Triggers on /deepdive prd, "write a PRD," "create a spec from
  sources," "the PRD keeps failing," or "spec is not deep enough."
---

# DeepDive PRD - Sub-Skill

Extends the `deepdive` parent skill (v3) with PRD-specific templates, section mappings, and quality gates. All generic recursion logic lives in the parent skill - this file only provides the PRD configuration layer.

## PROBE Phase Override

During PROBE, use `scripts/entropy_probe.py` (if available) to identify high-information regions in source specs before decomposition. This replaces naive line-count splitting with entropy-weighted region detection. For REPL-driven exploration, use `scripts/rlm_repl.py` (if available) to interactively query sources.

Use the PRD section templates in `references/prd_templates.md` to guide outline planning. Select the best-fit template based on source signals:

| Source Signal | Template |
|---------------|----------|
| API specs, schemas, infra diagrams | Technical PRD |
| User research, mockups, OKRs, business cases | Product PRD |
| Academic papers, benchmarks, algorithm pseudocode | Research-to-Engineering PRD |
| Mixed signals | Hybrid - pick best-fit sections from each template |

The root model receives ONLY file metadata (names, token counts, previews) plus probe results and the selected template's section list. It maps sources to sections and returns a JSON outline.

## EXECUTE Phase Override

Each section sub-agent (via `agents/deepdive-subcall.md`) receives:

1. The template's **description** for that section (from `prd_templates.md`)
2. The template's **requirements** column as writer instructions
3. ONLY the source files mapped to that section (no cross-contamination)

Sub-agents write exhaustively against their assigned sources. They do not summarize - they extract and organize.

## VERIFY Phase - Quality Criteria

PRD-specific thresholds passed to the concept auditor (`scripts/concept_auditor.py`). See `references/quality_rubric.md` for full scoring details.

| Dimension | Minimum | Weight |
|-----------|---------|--------|
| Concept Coverage | >= 85% | 30% |
| Depth Score | >= 3/5 | 20% |
| Cross-Reference Density | >= 5 refs | 10% |
| Source Fidelity | >= 4/5 | 25% |
| Actionability | >= 3/5 | 15% |

If any dimension fails, the engine triggers a targeted recursion pass on the failing dimension before finalizing. Two or more failures trigger a full re-entry from EXECUTE.

## Scripts Reference

- `scripts/rce_engine.py` - Recursive context engine orchestrator (all phases)
- `scripts/concept_auditor.py` - Coverage heuristic and gap detection
- `scripts/entropy_probe.py` - Entropy-weighted region detection for specs (v3)
- `scripts/rlm_repl.py` - Interactive REPL for source exploration during PROBE (v3)

## Template and Rubric References

- `references/prd_templates.md` - Section templates for Technical, Product, and Research-to-Engineering PRDs
- `references/quality_rubric.md` - Full scoring rubric with composite calculation and gate decisions
