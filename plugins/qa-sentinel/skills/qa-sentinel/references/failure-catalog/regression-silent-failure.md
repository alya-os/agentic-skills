# regression-silent-failure

## Description
Feature still "works" but worse than before. UI flickers during load. Pagination loads but order is inconsistent. Sort persists when it shouldn't. Animation runs but at 15fps. No error is thrown; no log line written; nothing that would fail a binary assertion. Quality degraded silently.

## Symptoms
- User-perceptible UX regression (jank, flicker, stutter)
- Functional degradation that passes binary "did it work" tests
- Performance metric got worse but stayed within "acceptable" bounds
- Animation timing changed but new timing also "works"
- State management quirks (back button, scroll restore, filter persistence) degraded

## Root cause
Tests check binary outcomes; humans perceive quality. Without baseline-vs-current comparisons on quality metrics, regressions hide.

## Independent verification
Compare the current state against a baseline from the ledger. For visual: pixel diff against last-passing screenshots. For perf: compare LCP/FID/CLS against last-passing metrics. For interaction: replay user journey and capture the timing / state at each step.

If the current state is measurably worse than baseline (even if both pass binary tests), it's a finding.

## Common fix attempts that DON'T work
- Adding a binary assertion (the regression already passes binary)
- Lowering the perf budget to accommodate (this is normalization of failure)
- Calling it "subjective" (it's measurable; baselines exist)

The fix that works: maintain quality baselines (screenshots, perf metrics, interaction timings) per release. Compare every deploy against the most recent green baseline.

## Likely lenses
product-manager, code-architect, designer, performance
