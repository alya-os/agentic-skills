# orphan-layout-after-removal

## Description
When a previously-present UI element is removed (form panel, image, sidebar,
CTA), the remaining layout often looks unbalanced because surrounding rules
still reserve space, alignment, or visual weight that depended on the removed
element. A build agent that just removes the element rarely re-balances what's
left.

## Symptoms
- Hero where text is now centered but stretches full width awkwardly
- Two-column layout collapsed to one column without re-centering the survivor
- Empty white space where a card / form / image used to live
- Visual weight imbalance: e.g. 80% of hero is empty gradient
- Survivor element drifts to one side because flex/grid rules still assume a partner
- Heading sits alone with no nearby focal point, looks like a draft

## Root cause
CSS class names like `has-X` or `has-Y` are added conditionally when X is
present. When X is removed, the parent class is removed but other rules
(grid-template-columns, text-align, padding, justify-content) were authored
assuming the survivor would carry visual weight or have a partner.

## Independent verification
- Capture a baseline screenshot BEFORE the removal (or fetch from `assets/baselines/`).
- After the removal, eyeball the same viewport at 1280×800: is there a focal element?
- Where does the eye land in the first 2 seconds? If the answer is « nowhere obvious », flag.
- Compare visual weight distribution to a competent reference site in the same vertical.

## Common fix attempts that DON'T work
- Just removing the element (no rebalance)
- Adding `text-align: center` on the survivor (still feels empty)
- Adding `max-width` without re-centering or rebalancing surrounding sections

## What does work
- Rebalance survivors: re-center, add a focal element (image, illustration, supporting card)
- Reduce the section's vertical padding so the empty space doesn't dominate
- Promote a secondary element (testimonial, badge, social proof) to fill the gap
- Use the negative space intentionally (large H1 + plenty of breathing room) rather than letting it look orphaned

## Likely lenses
designer (primary), business-conversion, product-manager
