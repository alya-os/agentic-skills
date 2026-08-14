# mobile-only-regression

## Description
Layout, performance, or behavior breaks specifically at mobile viewport while desktop continues to work. Build agent verified at desktop only and missed it.

## Symptoms
- Card stretches to absurd height (sometimes thousands of pixels) on mobile due to inherited `min-height`
- Horizontal scroll appears on mobile but not desktop
- Touch target invisible or unreachable behind a sticky header
- Mobile menu does not open or closes immediately
- Performance metric (LCP, CLS) blows budget on mobile but passes on desktop
- Text wraps awkwardly only at narrow viewports
- Image / video player covers controls on mobile

## Root cause
Build agent only screenshotted or only tested at desktop dimensions. CSS rules that work at large widths fail at small widths.

## Independent verification
ALWAYS capture both desktop (1280×800) and mobile (390×844) screenshots. Apply the same rubric to each. Diff against any baseline mockups for both viewports.

Run Core Web Vitals capture in both viewports. Mobile thresholds are stricter for some metrics.

## Common fix attempts that DON'T work
- "It works on my phone" (single-device check; still misses other mobile widths)
- Adding a media query that doesn't address the root cause
- Hiding the broken element on mobile (regression in the other direction: feature gone on mobile)

The fix that works: every visual finding requires desktop AND mobile evidence. Per-iteration default in `/qa run`.

## Likely lenses
designer, performance, accessibility
