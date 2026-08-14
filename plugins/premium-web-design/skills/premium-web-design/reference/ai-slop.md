# AI Slop Indicators & How to Fix Them

Detailed guide for identifying and fixing design anti-patterns that signal template-generated, rushed, or low-effort interfaces. Complements the DON'T guidelines in the main skill.

---

## Visual Anti-Patterns

### Heavy Drop Shadows
**Problem:** Overly dramatic drop shadows on cards, buttons, and elements.
**Fix:** Use subtle shadows sparingly. Consider light borders or background color changes instead.
```
BAD:  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
GOOD: box-shadow: 0 1px 3px rgba(0,0,0,0.1);
```

### Clashing Color Palettes
**Problem:** Colors that don't harmonize, often from randomly selecting "vibrant" colors.
**Fix:** Use established color theory. Limit primary brand colors to 2-3, with neutrals filling the rest.

**Tools:** Coolors.co, Adobe Color, Tailwind CSS Colors

### Generic Gradient Buttons
**Problem:** Glossy, overly-styled buttons with multiple gradients and reflections.
**Fix:** Flat or subtle gradient buttons with clear states (hover, active, disabled).

```
Base: Solid color, subtle border-radius
Hover: Slight color darkening or lightening
Active: Visual press effect (translate or shadow reduction)
Focus: Clear outline for accessibility
```

### Inconsistent Visual Styles
**Problem:** Mixing design styles between sections (rounded cards + sharp rectangles).
**Fix:** Establish a design system early:
- Border radius: Pick 1-2 values (e.g., 4px small, 8px cards)
- Spacing: Use multiples of 4 or 8
- Typography: Max 2-3 font families

### Overly Complex Custom Fonts
**Problem:** Decorative or unusual fonts for body text or headings.
**Fix:** Stick to modern system fonts or well-tested web fonts. Prioritize readability.

**Safe choices:** System fonts, Inter, Manrope, Space Grotesk, Plus Jakarta Sans

### Tiny, Illegible Screenshots
**Problem:** Product screenshots or demos too small, too fast, or too complex.
**Fix:** Show zoomed-in, focused views of key features. Use annotations or highlights.
- Focus on one feature at a time — don't show the entire dashboard
- Use annotations — arrows, highlights, or callouts to draw attention
- Slow down videos — give users time to absorb information
- Always use 2x or 3x resolution for screenshots

### Misused or Missing Logos
**Problem:** Product logo tiny, missing, or overshadowed by partner logos.
**Fix:** Product logo = most prominent branding element. Partners go in footer.

### Over-Animation
**Problem:** Everything moves, bounces, or slides excessively.
**Fix:** Keep most animations under 300ms. Honor `prefers-reduced-motion`.

---

## Messaging Anti-Patterns

### Internal Jargon
```
BAD:  "MCP-enabled infrastructure for LLM orchestration"
GOOD: "Connect AI models to your tools and data"
```

### Vague Value Propositions
```
BAD:  "Transform Your Workflow"
GOOD: "Send personalized emails to 10,000 customers in minutes"
```

### Negative Framing
```
BAD:  "Stop wasting time on manual data entry"
GOOD: "Automate data entry and focus on strategy"
```

---

## The AI Tells — Forbidden Patterns

Specific patterns that instantly signal AI-generated work. These are BANNED unless the user explicitly requests them.

### Typography Tells
- **Inter font** — The #1 AI default. Use Geist, Outfit, Cabinet Grotesk, Satoshi, or Plus Jakarta Sans instead
- **Oversized H1 that screams** — Control hierarchy with weight and color, not just massive scale
- **Serif on dashboards/software UI** — Serif fonts are for editorial/creative contexts only

### Color Tells
- **Pure black `#000000`** — Use off-black: Zinc-950, `#0a0a0a`, or tinted dark
- **Pure white `#FFFFFF` for backgrounds** — Use warm `#FAFAF8`, `#F9FAFB`, or tinted white
- **Purple/blue neon gradient** — The "AI aesthetic". Replace with neutral bases + single considered accent
- **Oversaturated accents (>80% saturation)** — Desaturate to blend elegantly with neutrals
- **Multiple accent colors** — Pick ONE. Remove the rest
- **Mixed warm and cool grays** — Stick to one gray family, tinted consistently

### Layout Tells
- **3-column equal cards** — The most generic AI layout. Use 2-column zig-zag, asymmetric grid, bento, or horizontal scroll
- **Centered hero with text over dark image** — Use asymmetric split: text left/right, background with subtle stylistic fade
- **Everything centered** — Left-aligned text with asymmetric layouts feels more designed
- **`h-screen` for full-height** — Use `min-h-[100dvh]` to prevent iOS Safari viewport jumping
- **Cards everywhere** — Not everything needs a container. Use spacing and alignment

### Content Tells
- **Generic names** — "John Doe", "Jane Smith", "Sarah Chan" are banned. Use creative, realistic-sounding names
- **Fake round numbers** — `99.99%`, `50%`, `$100.00` → Use organic data: `47.2%`, `$87.50`
- **Startup slop names** — "Acme", "Nexus", "SmartFlow". Invent premium, contextual brand names
- **AI copywriting clichés** — "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve", "Tapestry", "In the world of..." — Write plain, specific language
- **Lorem Ipsum** — Never. Write real draft copy
- **Broken Unsplash links** — Use `https://picsum.photos/seed/{context}/800/600` or SVG placeholders

### Component Tells
- **Emojis anywhere in UI** — BANNED. Use proper icons (Phosphor, Radix) or clean SVG
- **Lucide/Feather icons exclusively** — Default AI icon choice. Differentiate with Phosphor, Heroicons, or custom sets
- **Default shadcn/ui** — Must customize radii, colors, shadows to match project aesthetic
- **Generic circular spinner** — Use skeleton loaders matching layout shape
- **Sun/moon toggle for dark mode** — Use dropdown, system preference, or settings integration

### Motion Tells
- **Bounce/elastic easing** — Dated and tacky. Use exponential easing (ease-out-quart/quint/expo)
- **`ease-in-out` or `linear`** — Use custom cubic-bezier curves
- **Animating `width`/`height`/`top`/`left`** — Only `transform` and `opacity`
- **No `prefers-reduced-motion` support** — Affects ~35% of adults 40+. Always provide alternatives

---

## Quick Audit Checklist

- [ ] Heavy drop shadows? → Lighten or remove
- [ ] Colors clash or lack harmony? → Use a color palette tool
- [ ] Buttons overly glossy or gradient-heavy? → Simplify
- [ ] Visual style inconsistent? → Establish design system
- [ ] Custom fonts hard to read? → Switch to proven web fonts
- [ ] Screenshots/demos unclear? → Zoom in and focus
- [ ] Product logo missing or tiny? → Make it prominent
- [ ] Too much animation? → Reduce to purposeful motion only
- [ ] Messaging uses jargon? → Translate to user language
- [ ] Value proposition vague? → Be specific about what it does and for whom
