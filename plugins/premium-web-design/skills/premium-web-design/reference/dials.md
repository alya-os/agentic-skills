# Design Dials

Three configurable parameters that drive design decisions across all modes. Users can override defaults via prompt (e.g., "variance 3, motion 8") or the skill asks when relevant.

## Defaults

| Dial | Default | Range | Description |
|------|---------|-------|-------------|
| DESIGN_VARIANCE | 8 | 1-10 | Layout experimentation level |
| MOTION_INTENSITY | 6 | 1-10 | Animation and interaction intensity |
| VISUAL_DENSITY | 4 | 1-10 | Content spacing and information density |

---

## DESIGN_VARIANCE (1-10)

Controls layout structure, symmetry, and compositional risk.

### Level 1-3: Predictable
- Centered layouts, symmetrical grids, equal paddings
- Flexbox `justify-center`, strict 12-column grids
- Safe, conventional compositions

### Level 4-7: Offset
- Asymmetric margins, mixed aspect ratios (4:3 next to 16:9)
- Left-aligned headers over centered content
- Overlapping elements with `margin-top: -2rem`
- **Centered Hero sections are BANNED at level 5+**

### Level 8-10: Asymmetric
- Masonry layouts, fractional CSS Grid (`grid-template-columns: 2fr 1fr 1fr`)
- Massive empty zones (`padding-left: 20vw`)
- Bento grids with unequal tile sizes
- **3-column equal card layouts are BANNED at all levels 4+**

### Mobile Override (All Levels)
For levels 4-10, any asymmetric layout above `md:` MUST collapse to strict single-column (`w-full`, `px-4`, `py-8`) on viewports below 768px. No exceptions — asymmetry must never cause horizontal scroll on mobile.

---

## MOTION_INTENSITY (1-10)

Controls animation complexity, from static to cinematic.

### Level 1-3: Static
- No automatic animations
- CSS `:hover` and `:active` states only
- Transitions limited to color/opacity changes on interaction
- Appropriate for data-heavy dashboards, admin tools

### Level 4-7: Fluid
- CSS transitions: `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`
- `animation-delay` cascades for staggered load-in reveals
- Focus on `transform` and `opacity` exclusively
- `will-change: transform` used sparingly
- Scroll-entry animations via `IntersectionObserver`

### Level 8-10: Cinematic
- Spring physics: `type: "spring", stiffness: 100, damping: 20`
- Complex scroll-triggered parallax and reveals
- Perpetual micro-animations (Pulse, Typewriter, Float, Shimmer)
- Magnetic cursor effects on interactive elements
- Layout transitions with `layoutId` for shared element morphing
- Staggered orchestration: `staggerChildren` or `animation-delay: calc(var(--index) * 100ms)`
- **CRITICAL**: Never use `window.addEventListener('scroll')` — use Framer Motion hooks or IntersectionObserver

### Performance Rules (All Levels)
- Animate ONLY `transform` and `opacity` — never `top`, `left`, `width`, `height`
- Perpetual animations MUST be isolated in their own memoized Client Components
- `will-change` only on actively animating elements
- Grain/noise overlays: `position: fixed; pointer-events-none` only, never on scrolling containers
- `backdrop-blur` only on fixed/sticky elements (navbars, overlays)
- MUST provide `@media (prefers-reduced-motion: reduce)` alternatives

---

## VISUAL_DENSITY (1-10)

Controls whitespace, padding, and information density.

### Level 1-3: Art Gallery
- Massive whitespace, generous section gaps (`py-24` to `py-40`)
- Everything feels expensive and clean
- Content width constrained to `max-w-4xl` or `max-w-5xl`
- Single-focus layouts, one idea per viewport

### Level 4-7: Standard App
- Normal spacing for web apps (`py-12` to `py-20`)
- Content width `max-w-6xl` to `max-w-7xl`
- Balanced information vs. breathing room
- Cards used when elevation communicates hierarchy

### Level 8-10: Cockpit
- Minimal padding, compact layouts
- No card containers — use `border-t`, `divide-y`, or negative space for grouping
- All numbers in monospace (`font-mono` / `font-variant-numeric: tabular-nums`)
- Data metrics breathe without being boxed unless z-index elevation is functionally required
- 1px lines to separate data, not cards or shadows
- Content width up to `max-w-[1400px]` with dense grids

---

## Dial Interactions

Dials interact with each other — some combinations have special behavior:

| Combination | Effect |
|-------------|--------|
| Variance 8+ & Density 1-3 | Maximum editorial impact — asymmetric layouts with massive whitespace |
| Variance 1-3 & Density 8+ | Dashboard mode — symmetrical, data-packed grids |
| Motion 8+ & Density 8+ | Perpetual micro-animations on data elements (breathing status dots, live carousels) |
| Motion 1-3 & Variance 8+ | Bold static compositions — asymmetry without distraction |
| All dials 1-3 | Ultra-conservative corporate — centered, static, spacious |
| All dials 8+ | Maximum expression — asymmetric, cinematic, dense |

---

## How to Use

The skill uses dials in two ways:

1. **Implicit** — The baseline defaults (8, 6, 4) apply automatically when no style preset is selected
2. **Explicit** — Users override in their prompt: "make it more airy" → reduce density; "add more motion" → increase motion; "keep it safe/centered" → reduce variance
3. **Via style presets** — Each `--style` preset sets its own dial defaults (see [style-presets reference](style-presets.md))

When dials are ambiguous, adapt dynamically based on context:
- Data dashboards → lower variance, higher density
- Marketing/landing pages → higher variance, lower density
- Editorial/blog → moderate variance, low density
- Portfolio/creative → high variance, high motion
