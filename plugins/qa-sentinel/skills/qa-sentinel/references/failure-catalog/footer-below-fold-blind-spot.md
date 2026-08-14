# footer-below-fold-blind-spot

## Description
Designer / accessibility / SEO lenses capture « full-page screenshots » but only
visually evaluate the hero / above-the-fold region. Real bugs hide in middle
sections and the footer area: broken leadgen forms, sticky CTAs in wrong
position, third-party widgets that survived hide-CSS attempts, footer markup
overlapping, social icons missing, copyright text wrong year, language toggles
broken, dead links.

## Symptoms
- A lens declares « screenshot captured, looks good » with full-page PNG saved
  but only the top third was actually inspected
- Sitewide form/widget bugs (AI assistant icon, chatbot, abandoned testing
  banners) visible on every page but missed
- Footer columns misaligned on mobile, copyright row missing on certain page
  templates
- Bottom-of-page CTAs misaligned, with stale wording the rest of the site fixed

## Root cause
« Took a full-page screenshot » is treated as equivalent to « evaluated the full
page ». Multi-thousand-pixel PNGs are too tall to absorb at once; the eye reads
the hero, decides « looks fine », closes the file.

## Independent verification
- For every captured screenshot, the lens MUST file SEPARATE findings (or
  separate pass marks) for THREE positions:
  1. Hero / above-the-fold
  2. Middle content (~50% scroll)
  3. Footer + bottom CTA blocks
- Optionally capture viewport-only screenshots at scroll positions 0%, 50%,
  90% for explicit verification.
- For sitewide elements (footer, sticky CTA, language switcher, leadgen-mini),
  sample on at least 3 different page templates to catch template-specific
  breakage.

## Common fix attempts that DON'T work
- Adding « scroll down » to the prompt (still only one screenshot)
- Making the screenshot bigger (eye still skips middle and bottom)

## What does work
- Explicit per-position findings in the structured lens output
  (`region: above_fold | middle | footer`)
- Multiple viewport-position screenshots (page.evaluate to scroll, screenshot,
  scroll, screenshot)
- Sitewide-element matrix: row per element, column per page template, mark
  visible/correct/broken

## Likely lenses
designer (primary), developer, accessibility
