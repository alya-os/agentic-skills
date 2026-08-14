# Style Presets

Concrete aesthetic directions for `--create` and `--refine` modes. Each preset defines typography, color, spacing, motion defaults, layout patterns, and overrides the dial defaults.

Use with: `--create --style soft`, `--refine amplify --style brutalist`, etc.

When no `--style` is specified, the skill uses the default dials and the user's stated direction. Presets are shortcuts for well-defined aesthetics.

---

## --style soft

**Vibe**: $150k agency, haptic depth, Apple/Linear-tier polish
**Dial defaults**: Variance 7, Motion 8, Density 3

### Typography
- **Display**: Geist, Clash Display, PP Editorial New, Plus Jakarta Sans
- **Body**: Same family at weight 400, or paired sans-serif
- **Sizing**: Massive — `text-4xl md:text-6xl tracking-tighter leading-none` for display
- **Banned**: Inter, Roboto, Arial, Open Sans, Helvetica

### Color
- **Backgrounds**: Deepest OLED black (`#050505`), warm creams (`#FDFBF7`), or silver-grey (`#F5F5F5`) — pick one per project
- **Accents**: Max 1, desaturated. No purple/blue AI gradient
- **Neutrals**: Tinted toward brand hue (chroma 0.01 in OKLCH)
- **Shadows**: Tinted to background hue, never pure black. Diffused: `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`

### Layout
- **"Double-Bezel" architecture**: Outer shell (`bg-black/5`, `ring-1 ring-black/5`, `p-1.5`, `rounded-[2rem]`) + inner core with its own background, inner highlight, and concentric radius
- **Macro-whitespace**: `py-24` to `py-40` between sections
- **Surfaces**: `rounded-[2.5rem]` for major containers
- **Cards**: Only when elevation communicates hierarchy
- **Banned layouts**: Edge-to-edge sticky navbars, symmetrical 3-column grids

### Motion
- **All transitions**: Custom cubic-bezier `(0.32, 0.72, 0, 1)` — never `linear` or `ease-in-out`
- **Spring physics**: `stiffness: 100, damping: 20` for interactive elements
- **Scroll entry**: `translate-y-16 blur-md opacity-0` → resolved over 800ms+ via `IntersectionObserver`
- **Staggered reveals**: All lists and grids enter sequentially
- **Magnetic buttons**: Pull toward cursor on hover (via `useMotionValue`, not `useState`)
- **Perpetual micro-animations**: Status dots pulse, search bars typewrite, icons float

### Components
- **Navigation**: Floating glass pill, detached from top (`mt-6 mx-auto w-max rounded-full`)
- **Buttons**: Rounded pills (`rounded-full px-6 py-3`) with nested icon circles
- **Eyebrow tags**: `rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em]` above headings
- **Icons**: Phosphor Light or Remix Line — ultra-light, precise lines

### Creative Arsenal
Pull from these when appropriate:
- Parallax Tilt Cards, Spotlight Border Cards, Holographic Foil
- Sticky Scroll Stack, Horizontal Scroll Hijack, Zoom Parallax
- Text Mask Reveal, Kinetic Marquee, Particle Explosion Buttons
- Bento Grid, Masonry, Split Screen Scroll

---

## --style minimal

**Vibe**: Notion/Linear editorial, warm monochrome, invisible motion
**Dial defaults**: Variance 5, Motion 3, Density 4

### Typography
- **Primary sans**: SF Pro Display, Geist Sans, Switzer, Helvetica Neue
- **Editorial serif** (headlines only): Lyon Text, Newsreader, Playfair Display, Instrument Serif — tight tracking (`-0.02em` to `-0.04em`), leading 1.1
- **Monospace**: Geist Mono, SF Mono, JetBrains Mono — for code, keystrokes, metadata
- **Body text**: Off-black `#111111` or `#2F3437`, never pure black. Line-height 1.6, max 65ch
- **Secondary text**: Muted gray `#787774`
- **Banned**: Inter, Roboto, Open Sans

### Color
- **Canvas**: Pure white `#FFFFFF` or warm bone `#F7F6F3` / `#FBFBFA`
- **Surfaces**: `#FFFFFF` or `#F9F9F8`
- **Borders**: `1px solid #EAEAEA` or `rgba(0,0,0,0.06)` — this is THE structural element
- **Accent colors**: ONLY desaturated, washed-out pastels for tags and inline backgrounds:
  - Pale Red: `#FDEBEC` (text `#9F2F2D`)
  - Pale Blue: `#E1F3FE` (text `#1F6C9F`)
  - Pale Green: `#EDF3EC` (text `#346538`)
  - Pale Yellow: `#FBF3DB` (text `#956400`)
- **Banned**: Primary-colored backgrounds for large sections, gradients, neon, glassmorphism

### Layout
- **Content width**: `max-w-4xl` to `max-w-5xl`
- **Massive vertical padding**: `py-24` or `py-32` between sections
- **Cards**: Border-only (`1px solid #EAEAEA`), radius `8px` to `12px`, padding `24px` to `40px`
- **No heavy shadows**: Ultra-diffuse only, < 0.05 opacity (practically invisible)
- **Bento grids**: Asymmetric CSS Grid, but clean and editorial

### Motion
- **Philosophy**: Present but invisible — quiet sophistication, not spectacle
- **Scroll entry**: `translateY(12px)` + `opacity: 0` over `600ms` with `cubic-bezier(0.16, 1, 0.3, 1)`
- **Hover**: Ultra-subtle shadow shift (`0 0 0` → `0 2px 8px rgba(0,0,0,0.04)` over 200ms)
- **Active**: `scale(0.98)` on buttons
- **Staggered**: `animation-delay: calc(var(--index) * 80ms)` — never mount everything at once
- **Background**: Optional slow-drifting radial gradient blob (`20s+`, `opacity: 0.02-0.04`, fixed, pointer-events-none)

### Components
- **Buttons**: Solid `#111111` bg, white text, radius `4px-6px`, no shadow
- **Tags**: Pill-shaped, `text-xs`, uppercase, wide tracking, pastel backgrounds
- **Accordions**: No container — items separated by `border-bottom: 1px solid #EAEAEA` with `+`/`-` toggle
- **Keyboard shortcuts**: `<kbd>` tags with border, light bg, monospace
- **Icons**: Phosphor Bold/Fill or Radix UI — slightly thicker stroke than soft preset
- **Banned**: `rounded-full` on large containers, emojis, thick icons, heavy drop shadows

---

## --style brutalist

**Vibe**: Swiss Industrial Print or Tactical Telemetry — raw, mechanical, declassified
**Dial defaults**: Variance 6, Motion 2, Density 8

Two sub-modes — pick one per project, never mix:

### Sub-mode: Swiss Industrial Print (Light)
- **Background**: `#F4F4F0` or `#EAE8E3` (matte unbleached paper)
- **Foreground**: `#050505` to `#111111` (carbon ink)
- **Accent**: `#E61919` or `#FF2A2A` (Aviation Red) — the ONLY accent color

### Sub-mode: Tactical Telemetry (Dark)
- **Background**: `#0A0A0A` or `#121212` (deactivated CRT, never pure `#000`)
- **Foreground**: `#EAEAEA` (white phosphor)
- **Accent**: Same red. Optional `#4AF626` (terminal green) for ONE single UI element only

### Typography (Both Modes)
- **Macro (Headers)**: Heavy sans — Neue Haas Grotesk Black, Archivo Black, Monument Extended
  - Scale: `clamp(4rem, 10vw, 15rem)` — massive
  - Tracking: `-0.03em` to `-0.06em` (extremely tight)
  - Leading: `0.85` to `0.95` (compressed)
  - Casing: EXCLUSIVELY UPPERCASE
- **Micro (Data)**: Monospace — JetBrains Mono, IBM Plex Mono, Space Mono, VT323
  - Scale: `10px` to `14px` fixed
  - Tracking: `0.05em` to `0.1em` (generous, simulating typewriter)
  - Casing: EXCLUSIVELY UPPERCASE
- **Textural** (rare): High-contrast serif (Playfair, EB Garamond) — subjected to halftone/dithering degradation

### Layout
- **Blueprint Grid**: Strict CSS Grid — elements anchored to tracks, never floating
- **Visible compartments**: Solid borders (`1px` or `2px`), full-width `<hr>` dividers
- **Bimodal density**: Extreme data density clusters alternating with vast negative space
- **Geometry**: `border-radius: 0` EVERYWHERE — 90-degree corners only
- **Banned**: Rounded corners, soft shadows, gradients, translucency

### Effects (CSS/SVG)
- **Halftone/1-bit dithering**: Dot-matrix patterns on images and large serif text
- **CRT scanlines** (dark mode): `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)`
- **Mechanical noise**: Low-opacity SVG static filter on DOM root
- **ASCII framing**: `[ SECTION ]`, `< TAG >`, `>>>`, `///`
- **Industrial markers**: `®`, `©`, `™` as geometric decorations, not legal text

### Components
- **No cards** — use grid compartments with visible borders
- **Semantic HTML**: `<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>` for technical content
- **Registration marks** and crosshairs (`+`) at grid intersections
- **Thick horizontal warning stripes** as section separators
- **Technical metadata**: `REV 2.6`, `UNIT / D-01`, randomized IDs

---

## --style editorial

**Vibe**: Magazine/newspaper layout, serif-forward, asymmetric grids
**Dial defaults**: Variance 8, Motion 4, Density 5

### Typography
- **Display**: High-contrast serif — Fraunces, Newsreader, Lora, Playfair Display
  - Massive scale, tight tracking, tight leading
  - Variable font animations on scroll/hover when appropriate
- **Body**: Clean sans-serif — Source Sans 3, Nunito Sans, DM Sans
  - Line-height 1.6, max 65ch, comfortable reading
- **Pull quotes**: Large italic serif with subtle color accent
- **Captions**: Small, uppercase, wide tracking

### Color
- **Warm neutrals**: Off-white backgrounds (`#FAFAF8`), warm grays
- **Ink-like text**: Deep charcoal, never pure black
- **Accent**: One editorial color — deep burgundy, forest green, or navy. Used sparingly for links, rules, and pull quotes
- **No bright colors**: Everything muted, considered, print-like

### Layout
- **Magazine grid**: Multi-column with variable widths, text wrapping around images
- **Full-bleed images**: Bleeding to edge, alternating with constrained text columns
- **Drop caps**: First letter of articles/sections enlarged as decorative element
- **Asymmetric columns**: Wide text + narrow sidebar, or 2:1 image-to-text ratios
- **Generous margins**: Print-inspired margins around text blocks
- **Pull quotes** breaking the grid as visual punctuation

### Motion
- **Restrained**: Scroll reveals and hover states only
- **Text-focused**: Outlined-to-fill transitions, variable font weight interpolation on scroll
- **Image reveals**: Subtle parallax, mask reveals on scroll entry
- **No perpetual animation**: Content is king, motion serves reading flow

### Components
- **Article cards**: Image-dominant, minimal chrome, date/category as metadata
- **Navigation**: Simple, horizontal, text-based — no floating pills
- **Footnotes & annotations**: Inline or margin-placed references
- **Dividers**: Thin rules, ornamental breaks, or large numbers/letters as section markers
