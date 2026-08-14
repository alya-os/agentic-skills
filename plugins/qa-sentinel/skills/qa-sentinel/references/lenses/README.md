# Lens Selection Rules

`/qa run` selects which lenses to fan out per project type. Defaults below; if uncertain, run all 9.

## Always-on lenses (every run, every project type)

- **developer** - every project has runtime concerns (errors, network, security headers)
- **accessibility** - every UI matters; a11y is non-optional
- **code-architect** - every code change must be simple, elegant, and reuse patterns

These three are the minimum. `/qa run` always fans out to at least these three even if all others are skipped.

## Conditional lenses

| Trigger | Lenses to add |
|---|---|
| Visual UI / landing page / marketing page / dashboard | `designer`, `performance` |
| Indexable site / public web target | `seo`, `content-copy` |
| Marketing / sales / conversion-oriented page | `business-conversion`, `content-copy` |
| Spec-driven feature work (PRD exists) | `product-manager` |
| Bilingual / multilingual target | `content-copy` (with translation parity check) |
| Production deploy (any target marked production) | `performance` |
| Form-bearing page | `business-conversion` (CTA + friction), `accessibility` (a11y) |

If `/qa plan` cannot determine the project type, fall back to **all 9 lenses**.

## Lens activation logic (pseudocode)

```python
selected = {"developer", "accessibility", "code-architect"}

if has_visual_ui or is_landing_page or is_dashboard:
    selected |= {"designer", "performance"}

if is_indexable_web:
    selected |= {"seo", "content-copy"}

if is_marketing_page or is_sales_page:
    selected |= {"business-conversion", "content-copy"}

if has_prd_or_spec:
    selected |= {"product-manager"}

if is_bilingual:
    selected |= {"content-copy"}

if is_production_deploy:
    selected |= {"performance"}

if has_forms:
    selected |= {"business-conversion", "accessibility"}

if not selected_unambiguously:
    selected = ALL_NINE_LENSES
```

## Lens skip rules

A lens is skipped (returns `status: "skipped"`) only when:

- Its entire `preferred_chain` is unavailable in the skill inventory AND
- No fallback artifact can be produced (rare: only when `agent-browser` itself is missing for visual lenses, or no diff is available for code lenses)

Skipped lenses are counted as coverage gaps and surfaced in the final report.

## Per-iteration scope (auto-loop)

In subsequent loop iterations:

- **Default**: re-run only lenses that produced findings in the previous iteration
- **Every 3rd iteration**: full re-fanout to catch new regressions introduced by fixes
- **On confidence-decay escalation**: full re-fanout one final time before terminating

## Reading order

When `/qa run` fans out, the orchestrator launches all selected lenses in parallel via the `Task` tool, with all calls in a single message containing multiple tool blocks. Each subagent reads its own lens file (`references/lenses/<lens>.md`) before starting. Lens files are self-contained.
