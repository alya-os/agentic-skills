# Data-Dense & Application UI (dashboards, tables, admin, CRM, settings)

Enterprise-grade application UI is a **different lane** from the bold, distinctive marketing work the rest of this skill optimizes for. Here the goal is legibility, orchestration, and low cognitive load — not memorability.

> **Lane reconciliation (read first).** The skill's anti-AI-slop rules (no Inter/Roboto, break the grid, asymmetry, one bold direction) are for **creative/marketing surfaces** (landing pages, heroes, campaigns). For **data-dense application surfaces**, invert the emphasis: a single clean sans (Inter, SF Pro, DM Sans, Plus Jakarta Sans is *fine and correct* here), a strict grid, tight rhythm, restraint. Don't apply "editorial asymmetry" to a data table. Pick the lane by surface: is this a *page to be admired* or a *tool to be operated*?

The three laws below separate amateur dashboards from professional ones. Then the component-craft specs make them concrete.

---

## Law 1 — Data drives the UI (contextual component architecture)

The nature of the data dictates the component. Never pour data into a generic table by default.

- **Categorical → badges/chips, not text.** A column with a constrained set of values (status: Active/Pending/Error; department: HR/Sales/Eng) renders as semantic color-coded badges, not plain strings. Instant visual grouping.
- **Numbers → right-aligned.** Text reads left-to-right; numbers compare by place value. Right-align all numeric/financial columns so ones/tens/hundreds line up and magnitudes scan without effort. Tabular figures (`font-variant-numeric: tabular-nums`) for alignment.
- **People → avatars, not names.** The brain processes faces faster than text. Replace user/employee names with an avatar (fallback: initials in a colored circle) so "who did what" is instant.
- **Time-series → timeline or roll-up, not a table.** An activity log or event history is time-delineated — a flat table is the wrong component. Use a **Timeline** component, or place a summary chart (bar/spark) directly above the table to roll the data up before the user reads rows. (For the chart itself, reach for the `dataviz` skill if available.)
- **Truncate, don't wrap.** Long strings get `text-overflow: ellipsis` (+ a tooltip with the full value) so row heights stay uniform and the table breathes. Wrapping distorts the grid.
- **De-emphasize inactive rows.** Inactive/resolved/deactivated items drop to lower opacity so the eye is drawn to active, actionable data.
- **Color carries data, never decorates.** Red is reserved for urgent/critical/error only. A colored cell must *mean* something.

## Law 2 — Progressive disclosure (temporal hierarchy)

Hierarchy isn't only static weight (size, contrast) — it's **when** the user sees a thing. Aggressively hide secondary/tertiary features; reveal precisely when needed.

- **De-clutter the default state.** A config panel (e.g. Share settings) doesn't earn permanent real estate — tuck it behind one explicit button that opens a clean pop-over/modal.
- **Hover for secondary/destructive row actions.** Don't put Edit/Delete on every row — that's clutter. Hide them; reveal an ellipsis menu or icon row on row-hover only. Keeps the baseline pristine. (Provide a keyboard/focus-visible equivalent — hover-only actions are inaccessible otherwise; see the a11y note below.)
- **Spectrum of explicitness.** Every element gets a place on the visibility scale by frequency of use: *highly explicit* (a global "Add new" always visible) → *low explicit* (a copy-to-clipboard icon that only materializes on cell hover).
- **Hierarchy inside hidden states too.** In a pop-over, the primary action (invite search box) sits at top; secondary actions (permissions, remove) are minimized.
- **Mobile/touch disclosure.** Swipe gestures over crowding a list item with buttons (Apple Reminders pattern): flag/details/delete hidden until swipe.
- **Sequenced onboarding, never a 6-bullet welcome modal.** Users dismiss text walls instantly. Show one contextual tooltip pointing at the first action; reveal the next only after they complete it. (Ties to the [psychology reference](psychology.md) — Goal Gradient.)

## Law 3 — Invisible UI (the orchestration you don't see)

The junior tell is designing only the static "happy" state. Premium feel lives in the interactive/hidden layer.

- **Micro-indicators for hidden depth.** A subtle corner triangle = a comment exists on this cell; a copy overlay that fades in over a metric invites interaction without clutter.
- **Tooltips are mandatory.** The #1 amateur giveaway is their absence. Every icon, truncated string, and ambiguous column header/metric gets a descriptive hover tooltip — this is what lets the UI stay clean (icons over labels) without sacrificing comprehension. Tooltips must be keyboard-reachable, not hover-only.
- **State management IS design.** The UI = tables + buttons + the drawers, slide-out panels, error states, success toasts, empty states, and non-intrusive "new feature" pops you don't immediately see. Design all of them, not just the layout.

---

## Component-craft specs (concrete, enforceable)

### Spacing — the 4/8-point grid
Every margin, padding, and gap is a multiple of 4 (prefer the 8-step scale): `4, 8, 12, 16, 20, 24, 32, 40, 48, 64`. No 13px-here-27px-there guessing.
- **Relational spacing signals grouping.** Title↔subtitle tight (`8`); text block↔button wider (`16`); card↔next section large (`48`–`64`). Distance encodes relationship (Gestalt proximity).

### Typography discipline (application lane)
- One clean sans family for the whole app.
- ≤ 5–6 sizes: `12` metadata · `14` body · `16` subheader · `20` header · `24`+ hero metric.
- Line-height scales inversely with size: large headers tight (`110–120%`), body loose (`140–150%`).

### Color & semantics
- One primary brand color; a lightened tint for backgrounds, a darkened shade for active states.
- Reserve semantics strictly: **red = danger/delete only · green = success/active · amber = warning · blue = neutral info.** Never decorative.

### Dark mode (depth without shadows)
- Light mode builds depth with shadows; **dark mode builds it with lightness.** Base near-black (`#121212`), cards a step lighter (`#1E1E1E`), higher surfaces lighter still. Elevation = lighter, not darker.
- Kill heavy borders — remove or make faint (`rgba(255,255,255,0.08–0.1)`).

### Shadows (light mode)
Diffused and nearly transparent, never a harsh dark outline: low Y-offset, large blur, very low opacity — e.g. `box-shadow: 0 10px 40px rgba(0,0,0,0.08)`. Layer two (a tight contact shadow + a soft ambient one) for realism.

### Image/text overlays
Text over an image is unreadable raw — interpose a linear-gradient scrim (black→transparent) or `backdrop-filter: blur()` to guarantee contrast (target WCAG AA on the final composite).

### The five component states (every interactive element)
| State | Treatment |
|-------|-----------|
| Default | baseline |
| Hover | subtle bg shift or slight elevation |
| Active/Pressed | physical push — `scale(0.98)`, shadow removed |
| Disabled | opacity ~50%, `cursor: not-allowed`, non-focusable |
| Loading | label swaps for a centered spinner; width locked to avoid layout jump |

Inputs additionally need **Focus** (colored ring, always `:focus-visible`) and **Error** (red border + red helper text beneath).

### Affordances & signifiers
Clickable things must broadcast it. A segmented/pill control: active segment gets a distinct bg + shadow; inactive text grays out. Use a monochrome SVG icon set (Phosphor, Lucide) — never emoji.

### Icon & button proportions
- **Icon alignment:** match the icon's box/line-height to the adjacent text's line-height (e.g. a 24px icon in a 24px box beside 16px text) so it sits on the optical baseline.
- **2:1 button padding:** horizontal padding ≈ double the vertical (`px-6 py-3`) for proportioned buttons.

### Feedback micro-interactions
Confirm actions explicitly. "Copy link" → a small green "Copied!" badge slides up and fades out, not just a quiet color change. Pair these with the `motion-library` skill (98+ reusable animations) when it's available rather than hand-rolling every keyframe. Respect `prefers-reduced-motion`.

---

## Accessibility (non-negotiable, applies to all of the above)
- Hover-only affordances (row actions, tooltips) MUST have a keyboard/`:focus-visible` path — hover alone excludes keyboard and touch users.
- Color is never the sole carrier: pair every semantic color with text/icon (a "Pending" badge says *Pending*, not just amber). Colorblind- and print-safe.
- Badges/status meet contrast on their tint; de-emphasized rows still clear AA.
- Tooltips reachable by keyboard and dismissible; not the only place critical info lives.

## Applying during a build
1. Classify the surface: **operate** (this doc) vs **admire** (the creative DO/DON'T + style presets). Don't cross the wires.
2. For each column/element, ask "what IS this data?" → pick the component (badge / avatar / right-aligned number / timeline / chart) before styling.
3. Put every action on the explicitness spectrum; hide the rare ones.
4. Build all states + the invisible layer (tooltips, empties, toasts, errors), not just the static view.
5. Lock spacing to the grid; verify contrast and keyboard paths last.
