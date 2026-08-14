# redundant-nav-layering

## Description
The page stacks multiple navigation/context bands that repeat the same links, labels, or identity, pushing real content below the fold and making the hierarchy hard to read. Each band was added in isolation (global nav, then a breadcrumb strip, then a header card, then a tab bar) and nobody stepped back to see the cumulative vertical tax. Everything renders fine, so render checks pass, but the chrome-to-content ratio is poor and the user perceives it as cluttered or "not intuitive."

## Symptoms
- Two or more horizontal bars before any page content (global nav + breadcrumb + header card + tab bar)
- The same labels appear in multiple bands (e.g. "Dashboard / Brands" in both the top nav AND the breadcrumb)
- A large header card whose only content (title, a couple of stats) duplicates what the breadcrumb/nav already shows
- The primary content starts halfway down the viewport on desktop
- Each band is individually reasonable but collectively redundant

## Root cause
Incremental additions without a layout budget. Breadcrumbs, header cards, and tab bars each get added by different changes; no single pass evaluates total stacked chrome or de-duplicates repeated labels across bands.

## Independent verification
Count the horizontal bands above the first real content element at desktop width and note any label that appears in more than one band. More than ~2 chrome bands, or any label repeated across bands, is the signal. Capture a screenshot and measure where content begins relative to the fold. Confirm by asking: which band does each piece of information NEED to live in exactly once?

## Common fix attempts that DON'T work
- Shrinking each band slightly (still N bands, still redundant)
- Removing the breadcrumb entirely (loses wayfinding) instead of merging it
- Moving things around without removing duplication

The fix that works: consolidate to a minimal set (typically a global nav + one context bar that carries breadcrumb + title + actions + section tabs), and ensure each label/link appears in exactly one band.

## Likely lenses
designer, product-manager
