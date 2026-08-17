# Failure Catalog

52 abstract patterns observed repeatedly across many projects. Each entry has a stable filename (used as `catalog_entry` in lens findings) so the aggregator and ledger can group across runs.

These are project-agnostic by design. No client names, no specific URLs, no specific bug instances.

## Index

| Pattern | Lens(es) most likely to catch it |
|---|---|
| [about-page-cannibalization](about-page-cannibalization.md) | seo, content-copy |
| [adblock-blocked-conversion-ui](adblock-blocked-conversion-ui.md) | developer, business-conversion |
| [ai-slop-aesthetic](ai-slop-aesthetic.md) | designer, business-conversion |
| [broken-alternate-link](broken-alternate-link.md) | seo, developer |
| [cache-stale-verify](cache-stale-verify.md) | developer, seo |
| [cross-domain-intent-cannibalization](cross-domain-intent-cannibalization.md) | seo, content-copy |
| [cross-env-served-markup-drift](cross-env-served-markup-drift.md) | developer, seo, code-architect |
| [css-override-fights-production-js-init](css-override-fights-production-js-init.md) | developer, designer, code-architect |
| [fix-not-on-the-path](fix-not-on-the-path.md) | developer, code-architect |
| [fixture-unlike-production](fixture-unlike-production.md) | developer, code-architect |
| [ios-video-needs-playsinline](ios-video-needs-playsinline.md) | developer, designer, performance, accessibility |
| [catch-all-taxonomy-fallback](catch-all-taxonomy-fallback.md) | developer, product-manager |
| [client-side-content-void](client-side-content-void.md) | seo, developer |
| [cms-conditional-collision](cms-conditional-collision.md) | developer, performance |
| [composition-narrow-sample](composition-narrow-sample.md) | designer, product-manager |
| [contrast-ratio-fail](contrast-ratio-fail.md) | accessibility, designer |
| [editor-export-bloat](editor-export-bloat.md) | performance, designer |
| [inventory-dedup-by-wrong-key](inventory-dedup-by-wrong-key.md) | developer, product-manager |
| [queued-as-deferral](queued-as-deferral.md) | aggregator, all lenses |
| [retry-without-backoff-amplifies](retry-without-backoff-amplifies.md) | developer, performance, code-architect |
| [unknown-collapsed-to-default](unknown-collapsed-to-default.md) | developer, code-architect, product-manager |
| [visual-evidence-missing](visual-evidence-missing.md) | designer, replication-fidelity, render-truth |
| [external-sync-revert](external-sync-revert.md) | developer |
| [false-positive-generator](false-positive-generator.md) | code-architect, product-manager |
| [footer-below-fold-blind-spot](footer-below-fold-blind-spot.md) | designer, developer, accessibility |
| [helper-fn-not-deployed](helper-fn-not-deployed.md) | developer, code-architect |
| [inactive-by-default](inactive-by-default.md) | business-conversion, developer |
| [inline-script-interleave-broken](inline-script-interleave-broken.md) | developer, code-architect |
| [inline-script-stripped](inline-script-stripped.md) | developer, code-architect |
| [interactive-feature-not-exercised](interactive-feature-not-exercised.md) | developer, product-manager |
| [keyboard-navigation-trap](keyboard-navigation-trap.md) | accessibility |
| [metadata-contradiction](metadata-contradiction.md) | seo, content-copy |
| [migration-remnants](migration-remnants.md) | developer, seo, code-architect |
| [mobile-only-regression](mobile-only-regression.md) | designer, performance, accessibility |
| [multilayer-bug-class](multilayer-bug-class.md) | content-copy, developer, code-architect |
| [orphan-layout-after-removal](orphan-layout-after-removal.md) | designer, business-conversion |
| [post-deploy-404s](post-deploy-404s.md) | seo, developer |
| [rebuild-namespace-invention](rebuild-namespace-invention.md) | code-architect, designer |
| [redundant-nav-layering](redundant-nav-layering.md) | designer, product-manager |
| [regression-silent-failure](regression-silent-failure.md) | product-manager, code-architect |
| [render-truth-drift](render-truth-drift.md) | designer, developer |
| [replication-fidelity-drift](replication-fidelity-drift.md) | designer, content-copy, product-manager |
| [return-code-vs-body-error](return-code-vs-body-error.md) | developer |
| [state-persistence-loss](state-persistence-loss.md) | product-manager, business-conversion |
| [stray-char-broken-attribute-link](stray-char-broken-attribute-link.md) | developer, seo |
| [static-display-of-mutable-data](static-display-of-mutable-data.md) | product-manager, designer |
| [structural-grid-mismatch](structural-grid-mismatch.md) | designer, product-manager |
| [tone-inconsistency](tone-inconsistency.md) | content-copy |
| [touch-target-undersized](touch-target-undersized.md) | accessibility, designer |
| [translation-semantic-drift](translation-semantic-drift.md) | content-copy |
| [ui-language-mismatch](ui-language-mismatch.md) | content-copy, designer |
| [wp-wrapper-over-production-html](wp-wrapper-over-production-html.md) | developer, code-architect, designer |

## How to add a new pattern

When a finding repeats across two or more projects, promote it to a catalog entry:

1. Create `references/failure-catalog/<kebab-case-name>.md` with the standard structure (Description, Symptoms, Root cause, Independent verification, Common fix attempts that DON'T work, Likely lenses).
2. Add a row above.
3. Run `/bible add` if a knowledge-base skill is installed, so the pattern is searchable across projects.

## Catalog entry standard structure

```markdown
# <pattern-name>

## Description
One-paragraph description of what this failure looks like.

## Symptoms
- Bullet list of observable signals

## Root cause
What actually causes this, distinct from the symptoms.

## Independent verification
How to confirm the pattern via a channel different from the build agent's.

## Common fix attempts that DON'T work
What looks like a fix but isn't (signals to escalate via cross-run dedup).

## Likely lenses
Which lens(es) usually catch this.
```