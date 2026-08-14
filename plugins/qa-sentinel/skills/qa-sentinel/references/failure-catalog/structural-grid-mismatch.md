# Failure pattern: structural-grid-mismatch

## What it looks like

The build reproduces a reference interface but ships a different grid structure: reference has an N-column primary content grid, build renders M. Reference shows logos in a 5+5 array; build wraps to 3+3+4. Reference fits 8 category tiles in one row; build folds to 4+4. Every card renders. Colors and typography are close. The lens reads "the grid is present" and passes. The user opens the staging URL next to the reference and immediately sees the structural mismatch.

## Why HTML-only lenses miss it

Inspecting markup never reveals computed column count. `gridTemplateColumns` is a CSS-computed value; it depends on viewport, `auto-fit`, `minmax()`, and parent width. Two pages that produce visually different grids can have identical markup.

## How to detect

Measure on the live page at the same viewport as the reference (typically 1280×800 desktop, 390×844 mobile):

```js
const grid = document.querySelector('<grid-selector>');
const cs = getComputedStyle(grid);
const cols = cs.gridTemplateColumns.split(' ').filter(Boolean).length;
const cardCount = grid.children.length;
const rows = Math.ceil(cardCount / cols);
// Compare: ref_cols vs build_cols, ref_rows vs build_rows
```

When a reference is in scope, the designer lens MUST measure both sides and report the deltas as findings.

## Common root causes

- `repeat(auto-fit, minmax(280px, 1fr))` resolves to a different count when the build's container max-width or padding differs from the reference.
- Reference uses an explicit `repeat(N, 1fr)`; build picked `auto-fit` and the container is too narrow.
- Build copied the markup but rebuilt the CSS from scratch and picked different breakpoints.
- Container has a `flex-wrap: wrap` that triggers at a different threshold than the reference.

## Severity

P0 when the brief is "pixel-by-pixel" / "rebuild on new server" / "faithful reproduction". P1 when the brief is "modern reskin" but the difference still violates the spec.

## Sister patterns

- `replication-fidelity-drift` — broader category covering all axes of replication divergence (palette, typography, ordering, component shape, interactivity), not just grids
- `orphan-layout-after-removal` — when removing an element produced an unbalanced grid
