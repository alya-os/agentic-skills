# translation-semantic-drift

## Description
EN and FR (or any language pair) versions of the same content convey different meaning, instructions, or emphasis. Not a translation error per se; the EN and FR pages tell different stories.

## Symptoms
- EN headline emphasizes feature X; FR headline emphasizes feature Y
- EN CTA says "Start free trial"; FR equivalent says "Demander une démo"
- Quebec French content uses France-French terms (`courriel` vs `email`, `magasiner` vs `faire les courses`) inconsistently
- Tone formal in EN, casual in FR (or vice versa)
- Bullet points ordered differently between languages
- Stats or numbers don't match (USD vs CAD, miles vs km without proper conversion)

## Root cause
Translation done out-of-context, by different people / tools, or with different briefs. No reconciliation pass.

## Independent verification
Extract paragraph-level content from both versions. Place side-by-side. Compare semantic content (not literal). Flag drift.

For Quebec French: reference the user's project locale settings. Use `tu` informally if the project's brand voice file specifies it.

For numeric data: cross-reference. Currency, units, dates must match (in their respective formats: 12/05/2026 vs 2026-05-12 vs 12 mai 2026).

## Common fix attempts that DON'T work
- Re-running an MT engine on the EN to produce a "matching" FR (loses the manual edits)
- Updating only the surface that's "wrong" (other surface may be intentional)

The fix that works: identify the source-of-truth language; treat translation as a bilingual edit, not a one-way translate. Reconciliation pass on every content change.

## Likely lenses
content-copy
