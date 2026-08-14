# Failure pattern: render-truth-drift

## What it looks like

A theme or app declares CSS rules that reference design tokens (custom properties, SASS variables, Tailwind tokens). The rule files load correctly, the markup carries the correct class names, but a missing dependency in the asset pipeline (unenqueued manifest stylesheet, shadowed `:root` block, importmap mis-resolution, missing parent-theme load) makes every token resolve to its initial value. Backgrounds render `transparent`, brand colors render as user-agent default, dimensions sized via tokens collapse to `0px` or `auto`.

The HTML is correct. The CSS file with the rules is correct and loaded. `view-source` looks right. `getComputedStyle(navEl).backgroundColor` is `rgba(0, 0, 0, 0)` but the source-of-truth rule says `background: var(--brand-primary)` and the brand primary is `#0a1f44`.

## Why HTML-only lenses miss it

Reading the captured HTML reveals no problem. The agent enqueued the CSS file, the rules exist when curl'd. The pass criterion ("rule shipped to the browser") is met. The render criterion ("rule applied with the declared value") is not.

## How to detect

On a live rendered page, query computed styles of brand-critical elements and cross-check against the declared design system:

```js
const root = getComputedStyle(document.documentElement);
const navBg = getComputedStyle(document.querySelector('<primary-nav-selector>')).backgroundColor;
const declared = root.getPropertyValue('<design-token-name>');
// FAIL when declared !== '' but navBg === 'rgba(0, 0, 0, 0)'
// FAIL when declared === '' (variable not registered — manifest not enqueued)
```

Repeat for every brand-critical class the project declares: primary navigation, primary CTA, active-state indicator, dark-section heading, brand-logo image. Each non-zero declared rule resolving to a transparent/empty/default computed value is one finding.

## Common root causes

- The manifest stylesheet that declares `:root { --tokens }` is not enqueued; only the consumer stylesheets are loaded.
- A child theme overrides the parent's enqueue without re-registering the manifest.
- A plugin filter unsets the manifest handle late in the cascade.
- The token consumer stylesheet loads before its producer due to dependency-array order.
- A build pipeline tree-shakes the design-token CSS out as unused.

## Sister patterns

- `helper-fn-not-deployed` — analogous failure for PHP/JS code (the symbol is referenced but the file containing the definition was never loaded)
- `metadata-contradiction` — two source-of-truth files declare conflicting values
- `regression-silent-failure` — broader category for "deployed but inert"

## Severity

P0 whenever the affected element is brand-critical (navigation, primary CTA, hero, footer chrome). The page renders but ships visually broken; static checks pass; only computed-style verification catches it.
