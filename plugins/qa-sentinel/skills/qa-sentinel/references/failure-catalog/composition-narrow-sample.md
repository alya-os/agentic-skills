# composition-narrow-sample

## Description
A lens audits a multi-page CPT (services, products, locations, neighborhoods)
by sampling 1 or 2 posts and declaring the whole CPT verified. But layout bugs
often only manifest on specific compositions: hero-with-image vs hero-with-
gradient, page with form panel vs without, long title vs short title, single-
brand vs multi-brand product. The 1 sample passes; the unaudited 8 are broken.

## Symptoms
- « Service pages verified » based on 1 screenshot of refrigerator + 1 of
  dishwasher (both with similar hero compositions)
- A different service page in the same CPT has form overlapping a hero image,
  or a long title wrapping awkwardly, or a missing eyebrow eyebrow
- Layout bug surfaces in user testing weeks later: « it only happens on the
  washer page »

## Root cause
CPT sampling is treated like spot-checking a database table: « 1 row passed,
schema is verified ». But layout bugs are composition-dependent, not schema-
dependent. The composition of the sampled row masks variation.

## Independent verification
- For each multi-page CPT, sample at least 3 posts whose compositions DIFFER:
  - Hero composition (image-backed vs gradient vs no-hero)
  - Title length (short vs long, single-line vs multi-line)
  - Sidebar / form panel presence
  - Brand or category count (1 brand vs 10 brands listed)
- File a separate finding per sampled post (or pass-row per post).
- A coverage matrix row with `sample_count: 1` for a CPT with > 3 published
  posts is a P0 coverage gap, not a pass.

## Common fix attempts that DON'T work
- Picking « 1 representative » (no row is fully representative)
- Sampling 3 posts that all look the same (same composition = same bug masked)

## What does work
- Explicit composition-variance rule: pick samples that DIFFER in at least one
  composition axis (image vs no-image, long vs short title, etc.)
- Audit the full CPT for posts whose composition differs from the sampled set
- If automatable: scan every post for the specific bug pattern, not just visually

## Likely lenses
designer (primary), product-manager, developer
