# Failure pattern: css-override-fights-production-js-init

> **Category**: WordPress QA / Interface-Replicating QA — high-fidelity reproduction & assessment.

## What it looks like

An interface-replicating rebuild loads production CSS verbatim. A section "looks broken" in the rebuild (carousel slides stacked vertically instead of in a viewport, lazy-loaded images stay invisible, hero section has zero height, brand grid renders flat instead of horizontally-scrolling). The agent diagnoses this as "production CSS has wrong rules" and adds an overrides stylesheet like:

```css
.slider_widget-11 .slider__single { left: 0 !important; position: relative !important; }
.button_block_widget-7 { display: flex !important; }
.about_widget-3 .about__image { width: 100% !important; height: auto !important; }
.lazy-background { background-image: url(...) !important; }
.tns-item { display: inline-block !important; }
```

After deploying overrides, the section renders. Ship it. A week later, ANOTHER section breaks in a similar way — different widget instance, same root cause. The override file grows weekly. Eventually overrides start fighting each other (`!important` vs `!important`), the rebuild looks subtly different from production at every viewport, and "fix the styling" becomes a permanent backlog item.

## Why HTML-only lenses miss it

The page renders. The CSS is valid. Screenshots at one viewport look ~90% right after the override is added. The lens sees "agent fixed a styling bug" and moves on.

The real failure is invisible at the CSS layer: production CSS was correct all along — it was waiting for production JS to initialize. The carousel's first slide has `left: -800px` and `position: absolute` because TinySlider sets `left: 0` on the active slide at runtime. The lazy-background div is empty because the lazy-load observer hadn't promoted `data-src` to `src` yet. The brand grid is flat because the carousel-init script for `.brand-tile-list` hadn't been called.

The override hard-codes the post-init state into CSS. Now the section renders without the JS — but it ALSO renders that way after the JS runs, causing subtle flicker, layout snap, or "first slide stuck visible" bugs.

## How to detect

1. **Grep the overrides file for production CMS class names**:
   ```bash
   grep -nE '\.(slider_widget|button_block_widget|about_widget|tns-|lazy-background|owl-|swiper-)' \
       theme/assets/css/*.css theme/assets/css/overrides.css 2>/dev/null
   ```
   In an interface-replicating rebuild this should return ZERO hits. Any match is a finding.

2. **Compare DevTools "computed styles" between production and rebuild** for the broken element BEFORE running JS:
   ```bash
   # Disable JS in DevTools, reload production and rebuild side-by-side.
   # If both look broken in the same way → CSS is identical, JS init is what's missing.
   # If production looks fine and rebuild doesn't → asset URL is wrong or override is masking.
   ```

3. **Check browser console for missing init**: open the broken page, look for the JS function call that initializes the widget. For TinySlider: `tns({...})` should appear in console traces. For lazy-load: the `IntersectionObserver` for `.lazy-background` should be present.

4. **Compare `<script>` count between production and rebuild** (per the inline-script-stripped pattern). A missing inline `<script>` config block can silently disable the init the override is now masking.

5. **Inspect asset URLs**: if a CSS file 404s (open Network tab, filter CSS, look for red entries), the override may be "compensating" for the missing styles rather than fixing them.

## Common root causes

- Agent sees a broken section, jumps straight to CSS overrides, never asks "is the JS that styles this element running?"
- Production CSS includes a rule like `.slider_widget-11 .slider__single:not(.tns-slide-active) { left: -100% }` that DEPENDS on TinySlider adding `.tns-slide-active` to the visible slide. If TinySlider never inits (because the inline config was stripped, OR because jQuery didn't load, OR because the carousel root selector mismatch), every slide stays at `left: -100%` → all-blank carousel. Override `left: 0 !important` makes ALL slides visible simultaneously → broken in a new way.
- Asset URL for production CSS is wrong (e.g., `/wp-content/themes/<old-theme>/...` 404s in rebuild) so the production rules never load, and the override is "filling in" what the missing CSS would have done.
- Stale browser/Varnish cache serves old version of the override file or old CSS bundle, so the agent thinks the override is working when really it's the cached old behavior.

## The validated fix

Strip every override targeting production CMS class names. Diagnose the actual root cause:

| Symptom | Real cause | Real fix |
|---|---|---|
| Carousel renders all slides stacked | TinySlider never inits | Find which inline `<script>` carries `tns({...})` call; preserve it; verify jQuery and TinySlider lib are loaded BEFORE the call. |
| Lazy-background div has no image | IntersectionObserver never promotes `data-src` → `src` | Preserve production's lazy-load inline `<script>`; OR add a one-liner that DOM-ready promotes all `data-src` to `src` eagerly (lose lazy benefit but get rendering). |
| Brand tile grid renders flat | Carousel-init script for `.brand-tile-list` missing | Find the inline `<script>` block that initializes the brand carousel; preserve it. |
| Section has zero height | Production CSS depends on a JS-added class (e.g., `.is-loaded`) | Find what adds that class at runtime; either preserve the JS or eagerly add the class at render. |

After the JS init runs as production intended, production CSS renders correctly. ZERO override needed.

## Sister patterns

- `inline-script-stripped` — the most common upstream cause (stripped inline config breaks the JS init the override is now masking).
- `inline-script-interleave-broken` — even with inline scripts preserved, wrong execution order breaks init.
- `rebuild-namespace-invention` — broader "rebuild diverges from production" pattern.
- `wp-wrapper-over-production-html` — partner WP-specific pattern (wrapping production HTML with `get_header`/`get_footer` then "fixing" the visual mismatch with CSS).

## Severity

P1. The page renders so static visual checks pass, but the rebuild is brittle: every new section becomes a new override; overrides fight each other; the rebuild slowly drifts from production over months. Cost is debt-on-debt and unbounded growth of the override file.

## Lens question to ask

> "Do the rebuild's custom CSS files target any production CMS class names (`.slider_widget-*`, `.button_block_widget-*`, `.about_widget-*`, `.tns-*`, `.lazy-background`)? If yes, the override is masking a JS-init failure rather than fixing a real CSS bug. Strip the overrides and find what JS init is missing."
