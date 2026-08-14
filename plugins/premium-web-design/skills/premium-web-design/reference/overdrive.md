# Overdrive — Technically Extraordinary Effects

Push interfaces beyond standard polish into technically impressive territory. This mode is for when "good" isn't enough — the interface needs to provoke a "how did they do that?" reaction.

**When to use**: Portfolio pieces, agency showcases, product launches, hero sections, creative experiments. NOT for admin dashboards, data-heavy tools, or interfaces where performance > impression.

**Prerequisites**: The interface should already be polished. Overdrive amplifies quality — it doesn't fix poor foundations.

---

## Context Gathering

Before adding effects, understand:
1. **Performance budget**: What's the target device? Mobile-first = conservative. Desktop showcase = go wild
2. **Audience expectation**: Developers expect technical polish. General users expect smooth, not flashy
3. **Framework**: React + Framer Motion? Vanilla + GSAP? WebGL? This determines what's possible
4. **Hero moment**: What's the ONE thing that should blow people away?

---

## Narrative Structure (do this BEFORE picking effects)

A cinematic site is a story told through scroll, not a collection of effects. Map the narrative arc first, then assign at most one signature effect per beat:

| Beat | Job | Typical section | Effect budget |
|------|-----|----------------|---------------|
| **Hook** | Stop the scroll, establish tone in 3 seconds | Hero | The ONE showpiece effect (this is where overdrive lives) |
| **Tension** | Make the problem felt | Problem/context | Restrained — motion supports reading, e.g. one scroll-linked reveal |
| **Resolution** | Show the answer with clarity | Solution/product | Purposeful — animation demonstrates the product (scroll-linked demo, before/after) |
| **Proof** | Build trust | Results, testimonials, logos | Minimal — trust content must be effortless to read (no scrolling testimonial boxes) |
| **Action** | Convert | CTA/pricing | One focused micro-interaction on the CTA itself |

**Rules:**
- Every animation must have a stated purpose you can name in one sentence: what does it help the user *understand, feel, or do*? If you can't name it, cut it.
- Effect intensity descends through the page: spectacle at the hook, clarity at the close. Reversing this (calm hero, chaotic pricing) kills conversion.
- The scroll journey reads as one continuous narrative — transitions between beats matter more than effects within them.
- For conversion-page section anatomy and the psychology of each scroll step, see [landing-structure reference](landing-structure.md).

---

## Effect Categories

### 1. Advanced Spring Physics
Go beyond basic `transition`. Implement physically-accurate spring systems:
- **Magnetic elements**: Buttons, cards, cursors that pull toward interaction points via `useMotionValue` + `useTransform` (NOT `useState`)
- **Inertial scrolling**: Decouple scroll from browser defaults for cinematic, weighted feel
- **Connected springs**: Elements that influence each other's position (drag one, others follow with dampened delay)
- **Framer Motion springs**: `type: "spring", stiffness: 100, damping: 20, mass: 1` — tweak `mass` for heavier/lighter feel

**CRITICAL**: Spring animations MUST be isolated in memoized Client Components. Never trigger parent re-renders.

### 2. Scroll-Driven Narratives
Transform scrolling into storytelling:
- **Sticky scroll stacks**: Cards stick to top and physically layer over each other
- **Horizontal scroll hijack**: Vertical scroll maps to horizontal gallery pan
- **Scroll-linked video/3D**: Frame rate tied to scroll position (GSAP ScrollTrigger)
- **SVG path drawing**: Vectors that trace themselves as user scrolls
- **Parallax depth layers**: Multiple layers moving at different rates (foreground fast, background slow)
- **Text reveal masks**: Large typography acts as window to video/animated background beneath
- **CSS `animation-timeline: scroll()`**: Native scroll-driven animations (Chrome 115+, no JS needed)

**Tools**: GSAP ScrollTrigger for complex choreography, Framer Motion `useScroll` for simpler effects.
**CRITICAL**: Never mix GSAP and Framer Motion in the same component tree. Pick one per section.

### 3. WebGL & Shader Effects
For maximum visual impact (use sparingly — heavy on GPU):
- **Mesh gradient backgrounds**: Organic, lava-lamp-like animated color blobs (Three.js or CSS `@property` hacks)
- **Image distortion on hover**: Vertex displacement shaders that warp images on cursor proximity
- **Particle systems**: Cursor trails, explosion effects on CTA clicks, ambient floating particles
- **Noise/grain overlays**: Procedural noise via fragment shaders (more performant than SVG filters)
- **Liquid transitions**: Page transitions that wipe like viscous fluid (GLSL shaders + Three.js)

**Performance**: Always provide a CSS-only fallback. Check `navigator.gpu` or use `matchMedia('(prefers-reduced-motion)')` to skip.
**Isolation**: WebGL canvases must be `position: fixed; pointer-events: none; z-index: -1` — background layer only.

### 4. Advanced Typography Effects
Make text itself the spectacle:
- **Variable font animation**: Interpolate weight, width, or slant on scroll/hover (`font-variation-settings`)
- **Text scramble/decode**: Matrix-style character cycling on load or hover
- **Kinetic marquee**: Infinite text bands that reverse/accelerate on scroll
- **Circular text paths**: SVG `<textPath>` on rotating circles
- **Split-character animation**: Each letter animated independently with stagger (`splitText` + GSAP or manual spans)
- **Outlined-to-fill transition**: Stroke-only text that fills with color on scroll entry

### 5. Interaction Spectacles
Micro-interactions elevated to macro impact:
- **3D tilt cards**: Parallax card tracking mouse position via `perspective` + `rotateX/Y`
- **Spotlight borders**: Card borders that illuminate dynamically under cursor (gradient follows mouse)
- **Directional hover**: Fill/reveal entering from the exact side the mouse enters
- **Particle explosion buttons**: CTAs that shatter into particles on click, then reassemble
- **Drag-and-throw physics**: Elements with momentum that can be flung across screen
- **Cursor-aware layouts**: Content that reorganizes or responds to cursor proximity

### 6. Layout Spectacles
Break conventional web layout expectations:
- **Dome/sphere galleries**: 3D gallery feeling like a panoramic space
- **Coverflow carousel**: 3D carousel with center-focused, edges-angled-back
- **Z-axis cascade**: Elements stacked like physical cards with slight rotation and overlap
- **Curtain reveal**: Hero section parting in the middle like a curtain on scroll
- **Infinite canvas**: Boundless grid draggable in any direction
- **Dynamic Island**: Pill-shaped UI that morphs to show different content/alerts

---

## Performance Rules (Non-Negotiable)

1. **Transform + opacity only** for CSS animations. WebGL gets its own GPU layer
2. **`will-change`** only on elements about to animate — never permanently
3. **60fps minimum** — profile in DevTools Performance tab before shipping
4. **Mobile fallback**: If effect can't run at 60fps on mid-range mobile, provide a simpler CSS-only version
5. **`prefers-reduced-motion`**: MUST disable all scroll-driven, parallax, and particle effects. Show static alternative
6. **Lazy initialization**: Heavy effects (WebGL, GSAP timelines) initialize on viewport entry, not page load
7. **Cleanup**: All `useEffect` hooks with animations MUST return cleanup functions (destroy timelines, dispose geometries)
8. **Grain/noise**: Always on `position: fixed; pointer-events: none` pseudo-elements, never scrolling containers

## Tool Selection

| Effect Type | Primary Tool | Alternative |
|---|---|---|
| UI spring physics | Framer Motion | React Spring |
| Scroll choreography | GSAP ScrollTrigger | Framer Motion `useScroll` |
| 3D/shaders | Three.js + React Three Fiber | Raw WebGL |
| Text splitting | GSAP SplitText | Manual DOM splitting |
| Scroll-driven CSS | `animation-timeline: scroll()` | IntersectionObserver polyfill |
| SVG animation | GSAP | Framer Motion SVG |

**CRITICAL**: Never mix GSAP and Framer Motion in the same component tree. Default to Framer Motion for UI interactions. Use GSAP exclusively for isolated full-page scrolltelling or canvas backgrounds.

---

## Pre-Flight Check

Before delivering overdrive code:
- [ ] Effects enhance the design direction, not distract from it
- [ ] 60fps on target devices (profile, don't guess)
- [ ] `prefers-reduced-motion` alternative provided
- [ ] WebGL/heavy effects have CSS-only fallback
- [ ] All effects isolated in their own Client Components (React)
- [ ] Cleanup functions in all useEffect hooks
- [ ] No GSAP + Framer Motion in same component tree
- [ ] Mobile has a degraded but still beautiful experience
- [ ] Loading state handles slow effect initialization gracefully
