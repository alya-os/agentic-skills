# tone-inconsistency

## Description
Same product or brand spoken about in different voices on different surfaces. Hero is casual, features are technical, pricing is corporate, footer is jargon-heavy. The reader feels they are reading three different products.

## Symptoms
- Voice shifts mid-page (casual hero → technical feature list → corporate pricing)
- Same noun referred to with different terms across the site (the product, the platform, the solution, the engine)
- Calls-to-action swing between informal ("Get started") and formal ("Request a demonstration")
- Microcopy in errors ("Oops! Something went sideways") clashes with the brand's professional voice
- Translation versions adopt different tones from each other

## Root cause
Multiple authors, multiple tools, no consistent voice file. Or AI-generated copy with no brand-voice constraint at generation time.

## Independent verification
Read the page top-to-bottom as one piece. Note voice shifts. Cross-reference with brand-voice file if one exists. Apply a copywriting skill tone classifier if available.

For bilingual: compare EN and FR voice; if EN is professional-friendly and FR reads as formal-distant, that's drift.

## Common fix attempts that DON'T work
- Editing one section to "match" the others (which one is right?)
- Running everything through one tool (often produces fresh inconsistencies)
- Calling it "creative variety" (variety is intentional; inconsistency is not)

The fix that works: explicit brand-voice file as ground truth; every surface evaluated against it; inconsistencies flagged at authoring time.

## Likely lenses
content-copy
