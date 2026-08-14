# contrast-ratio-fail

## Description
Text or critical UI elements fail WCAG AA contrast (4.5:1 body, 3:1 large text or non-text UI). Often introduced by dark-mode swaps, hover/focus states, or "premium" greys.

## Symptoms
- Body text on the actual rendered background fails 4.5:1
- Hover state has lower contrast than the resting state
- Dark mode introduces new contrast violations not present in light mode
- Placeholder text in inputs is unreadably grey
- "Disabled" state used for an enabled element

## Root cause
Color decisions made against an idealized background (white) or a single mode, not against the actual rendered background across all states and modes.

## Independent verification
Use axe-core via `agent-browser` (catches most cases). Manually verify hover/focus states. Capture screenshots in light AND dark mode (if dark mode exists). Spot-check text on imagery / gradients / overlays.

For components on photographic backgrounds, contrast must be measured against the worst pixel of the background overlap.

If `agent-browser` is not available, measure via the Claude-in-Chrome MCP rather than degrading to fetched HTML (markup carries no contrast information, so an HTML-only pass is NOT CHECKED, never a pass). See `references/lenses/accessibility.md` for the measurement snippet. A page builder that styles meta/excerpt colours but leaves the title colour unset is a frequent source: the heading inherits the theme default and lands on a dark section.

## Common fix attempts that DON'T work
- Adding a text-shadow to "boost" contrast (doesn't pass automated checks; user research shows it hurts)
- Lowering opacity to "soften" text (lowers effective contrast)
- Using a slightly-different grey (often still fails by a few decimal points)

The fix that works: pick colors against the actual rendered background, target 7:1 on critical text (passes AAA, has headroom for hover variations).

## Likely lenses
accessibility, designer
