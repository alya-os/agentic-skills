# false-positive-generator

## Description
A QA process flags a finding that turns out to be non-reproducible, environment-dependent, or a misunderstanding of acceptable behavior. Repeated false positives erode trust in QA reports and cause real findings to be ignored.

## Symptoms
- Finding only reproduces under conditions outside the documented scope (slow 3G, specific OS, locale)
- Finding contradicts the explicit spec or PRD
- Finding flags an intentional design choice as a bug
- Finding's "evidence" is a screenshot taken at the wrong viewport or with a flaky network state
- Reproducibility field is marked `flaky` or `unverified` but severity is `critical`

## Root cause
Lens executed without sufficient guardrails on environment, scope, or reference truth.

## Independent verification
Re-run the lens with strict, documented preconditions. If the finding does not reproduce, mark as non-reproducible and DOWNGRADE severity to `minor` or remove. Update the lens's prompt template if a class of false positives recurs.

## Common fix attempts that DON'T work
- Tightening severity thresholds (does not address the root cause)
- Suppressing the lens (loses real findings)
- Adding "ignore" rules per finding (rule list grows unbounded)

The fix that works: improve the lens's preconditions and reproducibility check. Require `evidence_path` to point to a fully-reproducible artifact. Mark `reproducibility` accurately.

## Likely lenses
code-architect (when a finding turns out to be over-defensive code), product-manager (when a finding contradicts the spec)
