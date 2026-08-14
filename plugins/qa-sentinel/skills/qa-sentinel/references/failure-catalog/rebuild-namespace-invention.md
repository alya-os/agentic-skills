# Failure pattern: rebuild-namespace-invention

## What it looks like

The brief is "rebuild this page on a new server / new theme / new framework, match production visually". The agent inspects the production HTML, then writes new code that *looks similar at first glance* but uses **new class names** (`bm-topbar` instead of production's `header header--desktop`, `bm-nav` instead of `navigation navigation--light`, `bm-footer-info` instead of `footer light`).

The first screenshot looks ~90% right. Subsequent screenshots drift further with every "fix" — colors shift, spacing rhythm breaks, nav casing flips, dropdowns lose their carets. The agent reports "fixing alignment" and "tightening spacing" weekly. Months in, the rebuild looks like a different site entirely.

## Why HTML-only lenses miss it

The page renders. The classes are valid CSS. The content is correct. A side-by-side screenshot at one viewport at one moment looks "close enough" because the agent picked the obvious colors and rough layout.

The drift is invisible to point-in-time review. It only shows up across iterations: every CSS rule the agent writes against the new namespace is a new debt that production's CSS already paid.

## How to detect

For any brief whose acceptance criteria mention "visual parity", "pixel-by-pixel", "mirror", "faithful reproduction", "rebuild on new server", or equivalent:

1. **Diff the class names** between the rebuild output and the production extraction. Take any major section — header, nav, footer, hero — and dump its outer-HTML from both. The class strings should be **identical**, not just visually similar. `class="header header--desktop hidden-sm-down light"` is not equivalent to `class="bm-topbar bm-topbar--scrolled"`.

2. **Read the rebuild's stylesheets**. If they declare rules against bespoke selectors (`.bm-*`, `.app-*`, `.theme-*`) instead of the production class names, every visual fix from here is the agent re-deriving styling that production's CSS already encodes.

3. **Read the rebuild's PHP/JSX templates**. Healthy reproduction looks like: production HTML with `<?php echo $dynamic_value; ?>` interpolated at the dynamic points. Unhealthy reproduction looks like: a fresh template emitting new class names, with PHP/JSX coordinating new markup.

## Common root causes

- Agent reads production HTML, summarizes it ("there's a topbar, a nav, a footer"), then writes new code from the summary rather than the literal HTML.
- Agent treats the production CSS as a black box and re-derives styles instead of loading the production stylesheets verbatim.
- Project conventions or design-system folder structure pulls the agent toward namespaced classes (`tw-`, `app-`, `theme-`) before checking if production CSS is reusable.
- The brief says "rebuild the look" and the agent reads "rebuild" as "redo from scratch" instead of "reproduce".

## The validated alternative pattern

`production-HTML-first rebuild` (see `test-recipes/production-html-first-rebuild.md`):

1. Snapshot production HTML byte-for-byte.
2. Localize CSS/JS/img/fonts assets (including inline `<style>` blocks from `<head>` — they hold critical overrides like `.navigation>a { text-transform: none }` that the linked stylesheets often DON'T have).
3. Build the new templates to emit the **exact production HTML structure** — same class names, same attribute order, same Font Awesome icons.
4. Back-fill ONLY dynamic bits with PHP/JSX (`<?php echo get_theme_mod('phone'); ?>`, `<?php wp_nav_menu(); ?>`).
5. Production CSS now drives the new templates without modification.

Result: zero CSS-namespace invention, zero drift over time, every "fix" is just a data fix.

## Sister patterns

- `replication-fidelity-drift` — the broader "rebuild doesn't match" pattern; this entry is the specific mechanism that causes it
- `helper-fn-not-deployed` — what happens when the production JS expects helpers the new namespace doesn't provide
- `inline-script-stripped` — partner failure when the noise filter also removes production's inline `<script>` configs

## Severity

P0 on any brief whose acceptance criteria include "match production" or equivalent. The cost grows with time — every iteration that adds bespoke styling deepens the divergence.

## Lens question to ask

> "Did the rebuild reuse production's class names byte-for-byte, or did it invent a new namespace? Dump the outer-HTML of three sections and grep both versions for `class=` — the strings should match."
