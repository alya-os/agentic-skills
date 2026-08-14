# Failure pattern: replication-fidelity-drift

## What it looks like

The brief is replication ("pixel by pixel", "faithful copy", "rebuild on new server", "looks identical to <URL>"). The build agent produced something that LOOKS similar — same general shape, similar palette, similar typography — but is not a copy. Section order is shuffled. Grid column counts differ. The brand palette is approximated but not matched. Custom icons became emoji fallbacks. Hand-tuned spacing became default Tailwind/Bootstrap rhythm. The visitor cannot articulate what is wrong, but it does not feel like the original.

This is a CATEGORY of drift, not a specific bug. It surfaces as one or more concrete failures along six axes:

1. **Structural layout** — grids, sections, breakpoints, ordering (covered by `structural-grid-mismatch`)
2. **Brand palette** — rendered computed colors vs the reference's computed colors (covered by `render-truth-drift` when token resolution fails; replication-fidelity-drift when the rebuild used different tokens entirely)
3. **Typography stack** — resolved font-family, weight, scale, leading
4. **Section ordering** — top-to-bottom block sequence per page type
5. **Component shape** — card aspect ratios, badge placement, hover states, border radius
6. **Interactive parity** — same controls, same outcomes, same keyboard behaviour as reference (covered by `interface-mirror` skill when present)

## Why HTML-only lenses miss it

Each axis is invisible to markup inspection. Section order matches by class name; only render measurement reveals the visual order. Palette matches by token name; only computed-style sampling reveals what the user sees. Component shape matches by selector; only rendered geometry reveals the proportions.

A lens that reads HTML and reports "all sections present" is right about presence and wrong about fidelity.

## How to detect

When the brief is replication and a reference is in scope (live URL, extraction snapshot, or saved-from-web archive), run the six-axis diff:

- Capture reference + build at matching viewports (desktop 1280×800 + mobile 390×844)
- Per axis, measure on both sides and compute the delta
- Per page type, sum the per-axis drift into an overall fidelity score
- Replication briefs target ≥ 90% overall fidelity. Below that, file findings per drifted axis.

The `interface-mirror` skill packages this measurement into a structured report. When `interface-mirror` is available in the user's skill inventory, the designer lens delegates the measurement to it.

### Structural-count pre-check (runs BEFORE the six-axis diff)

Before the (expensive) computed-style + geometry measurement runs, do a cheap HTML-shape diff. This catches gross missing-content / missing-structure deltas in seconds:

| Metric | How to measure |
|---|---|
| Top-level `<nav> <a>` count | Count anchors inside `<nav>` for header navigation |
| Footer `<a>` count | Count anchors inside `<footer>` |
| `<img>` src count | Exclude 1×1 tracking pixels, beacons, analytics images |
| Hero/carousel slide count | Count siblings matching `.slide`, `.swiper-slide`, `.slick-slide`, `[data-slide-index]`, OR N+1 hero images in a row inside the hero container |
| Top-level `<section>` / direct-child of `<main>` | Section ordering |
| JSON-LD count + schema-type list | `<script type="application/ld+json">` |
| Alternate-link count + target URLs | `hreflang`, `canonical`, `prev`, `next` |
| Stylesheet + script counts | `<link rel="stylesheet">` + `<script src=>` (catches dequeue leaks) |

A count delta ≥1 on any metric is P0. The structural-count pre-check is mandatory on every replication brief — running the six-axis diff without it means the lens may produce a "looks-OK" pass on a target that is missing entire sections (e.g., a 1-slide hero vs a reference's 4-slide carousel, or a 33-link header vs a reference's 44-link mega-menu). See SKILL.md "Hard Rule: reference-shape diff fires BEFORE any lens fanout".

## Common root causes

- Build agent inferred the design from the build agent's own theme spec, not from the reference (the QA failure mode this skill exists to catch)
- Reference's CSS used computed values that the rebuild cannot reproduce without the same custom-properties chain
- Build agent treated the reference as inspiration, not as ground truth
- Designer lens was never given the reference path and silently used the build's own spec as the baseline

## Severity

P0 for any replication brief. P1 when the brief explicitly permits modernization (e.g., "modern reskin preserving brand").

## Sister patterns

- `structural-grid-mismatch` — narrow case for one axis
- `render-truth-drift` — narrow case for the palette axis when tokens fail to resolve
- `interactive-feature-not-exercised` — interactivity axis specifically
- `ai-slop-aesthetic` — when the rebuild defaulted to generic design instead of the reference's identity
