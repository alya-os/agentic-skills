# touch-target-undersized

## Description
Interactive elements (buttons, links, checkboxes, icon buttons) are smaller than 44×44 px on mobile viewports. Users mis-tap. One-handed use becomes impossible. Conversion drops.

## Symptoms
- Icon-only buttons (close, menu, share) under 44px
- Inline links in body text on mobile (no padding makes them sub-44 even if the text appears tappable)
- Pagination "next/previous" buttons squeezed
- Checkboxes and radio buttons visible but unlabeled-and-untouchable
- Multiple links so close together they overlap on touch

## Root cause
Designs created at desktop scale; mobile spacing not increased. CSS that uses fixed-px sizes for interactive elements without `min-height: 44px; min-width: 44px;` on mobile.

## Independent verification
Render the target at mobile viewport (390×844). For every interactive element, measure computed width × height (use `agent-browser` to inject a one-line script that lists `getBoundingClientRect()` for `button, a, input, label, [role=button]`).

Any interactive element with width or height < 44px on mobile is a finding.

## Common fix attempts that DON'T work
- Adding hover states (mobile has no hover)
- Making icons bigger but not the tap area (visual change without functional fix)
- Adding more padding only on hover / focus (still small for first tap)

The fix that works: enforce `min-height: 44px; min-width: 44px;` on all interactive elements at mobile breakpoint.

## Likely lenses
accessibility, designer
