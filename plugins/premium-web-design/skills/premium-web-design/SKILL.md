---
name: premium-web-design
description: Create, refine, audit, or prototype frontend interfaces with high design quality. Use when building web components, pages, landing pages, artifacts, or applications, improving existing UI (polish, animate, colorize, simplify), auditing or reviewing ANY interface for premium design patterns and AI-slop indicators, or building interactive HTML prototypes and design handoffs, or generating multiple distinct design directions/versions to compare (proactively offer this, default 3-5, when the direction is not locked). Apply proactively to any UI work (hero sections, feature cards, onboarding, dashboards, wireframes, mockups) to ensure it immediately communicates what, who, and why with premium, non-generic execution. Generates creative, polished code that avoids generic AI aesthetics.
argument-hint: "[--create | --refine | --audit | --prototype | --onboard] [--landing] [--style soft|minimal|brutalist|editorial]"
user-invocable: true
---

Create, refine, audit, or prototype frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Design Dials
> *Consult [dials reference](reference/dials.md) for full specifications and dial interactions.*

Three parameters drive all design decisions. Defaults apply unless overridden by user or by a `--style` preset:

| Dial | Default | Range | Description |
|------|---------|-------|-------------|
| DESIGN_VARIANCE | 8 | 1-10 | Layout experimentation (1=symmetric, 10=asymmetric chaos) |
| MOTION_INTENSITY | 6 | 1-10 | Animation complexity (1=static, 10=cinematic spring physics) |
| VISUAL_DENSITY | 4 | 1-10 | Content spacing (1=art gallery airy, 10=cockpit dense) |

Adapt dynamically from user prompts: "make it more airy" → lower density; "add motion" → raise motion; "keep it safe" → lower variance.

## Behavioral UX Psychology (core mechanic)
> *Consult [psychology reference](reference/psychology.md) for the full principle-by-principle guide, code patterns, and the ethics guardrail.*

Persuasion is **structural**, not cosmetic — it lives in defaults, step order, progress state, framing, and adjacency, not in a banner color. For any surface with a conversion goal (signup, upgrade, onboarding, checkout, form), design the behavior, not just the look:

| Principle | One-line mechanic |
|-----------|-------------------|
| **Smart Defaults** | Never ship a blank form — pre-select the common choice; a default reads as a trusted recommendation |
| **Goal Gradient** | Progress bars/steppers never start at 0% — credit completed steps so the user opens at 20–30% |
| **Reciprocity** | Deliver core value (a partial result) *before* any signup wall; the gate saves/unlocks, it doesn't block |
| **Endowment (IKEA)** | Reverse onboarding — let them build/customize first; ask for email *after*, button says "Continue" not "Sign Up" |
| **Loss Aversion** | Frame around what's at risk, not just what's gained — show the concrete thing they'd lose |
| **Contrast / Anchoring** | Never show a price alone — place it beside a larger anchor; express upsells as a % of the cart |

**Rules of use:** pick the 1–3 principles that fit the surface (don't stack all six — that reads as manipulation). Bake them into component logic and state, not decoration. **Every technique must pass the ethics guardrail** in the reference: no fake scarcity, no fabricated losses, no pre-checked consent, no dark patterns. If it only works by misleading the user, do not build it.

## Two Lanes: Admire vs Operate
Pick the lane by surface before applying any guideline — the two need opposite instincts:

- **Admire** (landing pages, heroes, campaigns, marketing) → the bold/distinctive lane. Apply the creative DO/DON'T below, the `--style` presets, asymmetry, a memorable point of view, and the AI-slop test.
- **Operate** (dashboards, data tables, admin, CRM, settings, analytics, any data-dense application UI) → the disciplined-legibility lane. Follow the [data-dense UI reference](reference/data-dense-ui.md): data-drives-the-UI, progressive disclosure, invisible UI, the 4/8-pt grid, five component states, mandatory tooltips. **Auto-trigger this reference** (no flag needed) whenever the deliverable is a dashboard, table, admin panel, CRM, settings screen, or data grid.

> The lanes deliberately conflict (e.g. "ban Inter / break the grid" for Admire vs "one clean sans / strict grid" for Operate). That's intentional — don't apply Admire instincts to a data table, or Operate restraint to a hero. The reference explains the reconciliation.

## Mode Selection

### Create modes
- **--create** *(or no flag)* → Create a frontend interface
- **--create --style [preset]** → Create with a specific aesthetic direction. See [style presets](reference/style-presets.md)
  - `--style soft` — $150k agency, haptic depth, cinematic motion (Apple/Linear tier)
  - `--style minimal` — Notion/Linear editorial, warm monochrome, invisible motion
  - `--style brutalist` — Swiss Industrial Print or Tactical Telemetry, raw mechanical
  - `--style editorial` — Magazine layout, serif-forward, asymmetric grids
- **--create --landing** → Create a conversion-focused marketing/landing page. Follow [landing-structure reference](reference/landing-structure.md) for section anatomy and scroll psychology; pair with a copywriting skill for the copy and apply the [psychology reference](reference/psychology.md) (Reciprocity, Social Proof, Anchoring). Combines with `--style`. Auto-trigger when the deliverable is a landing page, product page, or campaign page even without the flag
- **--onboard** → Create onboarding flows and first-time user experiences. Follow [onboard reference](reference/onboard.md); design the behavior with the [psychology reference](reference/psychology.md) (Goal Gradient + Endowment + Smart Defaults are the onboarding trifecta)
- **--prototype** → Build multiple interactive HTML prototypes in parallel for stakeholder review. Follow [prototype reference](reference/prototype.md)

The `--style` flag works with any mode: `--refine amplify --style soft`, `--create --style brutalist`, etc. When no style is specified, use the default dials and the user's stated direction.

### Design Multiplication (proactive multi-version generation)

When a surface's direction isn't locked yet, generating SEVERAL distinct versions to compare beats committing to one. This is the highest-leverage early-stage use of the skill.

**Auto-detect** the intent (no flag needed) when the user says: "options", "a few directions", "variations", "explore", "concepts", "mockups to choose from", "which looks better", "versions", "A/B" — or is scoping a NEW surface.

**When detected, ASK ONE lightweight question before spending tokens** (never fan out silently):
> "Want multiple design directions to compare, or commit to one? If multiple, how many (default 3)?"

**Budget discipline (token-maxxing, not token-burning):**
- Default **3** versions; **5** for a real design sprint; exceed 5 (up to ~7) only when the user says "be comprehensive."
- Each version commits FULLY to a DISTINCT direction, no convergence (the `--style` presets — soft / minimal / brutalist / editorial — are ready-made distinct lanes).
- Run versions as PARALLEL background agents (one per direction); each writes its self-contained file to disk EARLY so a mid-run failure never loses a finished version.
- Keep the orchestrator's context lean: judge from a compact per-version scorecard, don't re-read every full file.
- Close with a SYNTHESIS: scored comparison, recommended winner, and a "graft list" of the best ideas from the losers.

Follow [prototype reference](reference/prototype.md) for the full fan-out, judge, synthesize workflow.

### Mirror mode (faithful reproduction of an existing site the user owns)

- **--mirror** → Reproduce an existing site the user is migrating to a new server / CMS. The success metric is `diff(extraction-screenshot, live-screenshot) ≈ ∅`, not "fits the brand palette".

**Auto-trigger signals.** Default to mirror mode (even without the explicit `--mirror` flag) when the user says: "pixel by pixel", "identical to", "copy of the current site", "faithful reproduction", "rebuild on new server", "migrate the existing site", "reproduction visuelle fidèle", "exactly the same as production" — AND/OR an extraction snapshot is present in `tmp/<client>-extraction-*/`, `clients/<client>/_extraction-snapshot/`, or any folder containing `manifest.json` + `02-pages/<locale>/<slug>/page.html`.

**Mirror-mode workflow (FIRST decision before writing any HTML/CSS):**

1. Start from the extracted HTML, not a blank template. Locate the page-type sources under `<extraction_root>/02-pages/<locale>/<slug>/page.html`.
2. Identify the dynamic blocks that need CMS replacement (inventory listings, cart, user state, dynamic counts, search results). Replace ONLY those blocks with template includes or shortcodes that emit the same DOM structure.
3. Rewrite asset URLs (CDN paths → self-hosted paths) but keep CSS class names and DOM structure byte-for-byte identical to the source.
4. Keep the original site's CSS files as-is on the new server; only add an override stylesheet for the deltas the user explicitly requested.
5. Smell-tests during build (any one of these means you are in the wrong mode, not mirror):
   - You are picking fonts → wrong mode
   - You are picking colors → wrong mode
   - You are choosing a layout → wrong mode
   - You are adding emoji or letter-circle fallbacks for missing icons → wrong mode (sideload the real icons from the extraction first)
   - You are designing template parts named `home-categories.php`, `home-hero.php`, etc. with bespoke markup → wrong mode (the extraction already has these)
6. Verification: capture a screenshot of the live build and visually diff it against the extraction screenshot. Any structural divergence is a P0 build defect.

### When mode is unclear

Ask the user: "Is this a faithful copy of an existing site you're migrating, or a fresh design from scratch?" Default to mirror when in doubt — mirror-then-iterate is cheaper than design-then-redo.

### Evaluate mode (read-only — produces reports, not code)
- **--audit** — Complete interface audit in two phases: technical quality scan (a11y, performance, theming, responsive) then design critique (hierarchy, communication, emotional resonance, AI slop). Uses the [comprehensive quick-scan checklist](reference/audit.md) (100+ points), plus a pre-launch performance gate (Core Web Vitals thresholds) for anything about to ship. Follow [audit reference](reference/audit.md). This mode is a self-review; for the authoritative "is it actually shippable" gate, hand off to `qa-sentinel` (`/qa run`) — it verifies against the real goal and its designer lens runs the deterministic `slop_lint` AI-slop linter as an independent channel. Do this before treating any build as done.

**Proactive Quick Review (always on)**: even outside `--audit`, apply the Quick Review Pass from the [audit reference](reference/audit.md) to any UI being created or touched — the 3-second what/who/why comprehension test and AI-slop spot-checks. This is the former premium-web-design behavior, now built in.

### Refine mode (improve existing UI)
- **--refine** — Improve an existing interface. Modify existing code — don't recreate from scratch.

If `--refine` is used without sub-options, use AskUserQuestion to ask:

"What do you want to improve? (pick one or more)

- **polish** — Alignment, spacing, consistency, states
- **animate** — Purposeful animations and micro-interactions
- **colorize** — Inject strategic color into flat designs
- **amplify** — More contrast, drama, presence
- **soften** — Tone down while keeping quality
- **delight** — Moments of joy and personality
- **wording** — UX copy, labels, microcopy
- **simplify** — Strip to essence, remove complexity
- **overdrive** — Technically extraordinary effects (shaders, spring physics, scroll-driven)"

**Shortcut**: Power users can skip the question with `--refine polish animate`.

Once sub-options are selected, follow the corresponding references:
- polish → [polish reference](reference/polish.md)
- animate → [animate reference](reference/animate.md)
- colorize → [colorize reference](reference/colorize.md)
- amplify → [intensity reference](reference/intensity.md) (amplify section)
- soften → [intensity reference](reference/intensity.md) (soften section)
- delight → [delight reference](reference/delight.md)
- wording → [wording reference](reference/wording.md)
- simplify → [simplify reference](reference/simplify.md)
- overdrive → [overdrive reference](reference/overdrive.md)

## Design Context

**Always look for an existing brand system BEFORE choosing any palette, typeface, or visual direction.** Check, in order:

1. A `## Design Context` section in the project's `CLAUDE.md`
2. A brand guide supplied in-conversation (the user pasting colours, fonts, logo rules)
3. `_company.yml`, `documentation/*brand*`, `documentation/*SELLING_POINTS*`, `brand.json` / `brand-system.md` / `tone-of-voice.md` (the `brand-voice-generator` output)
4. Existing branded artefacts to mine when no guide is written down: client decks, an existing site, a logo file. A deck with base64-embedded logos yields both the real assets and the real voice.

- **If found** → Load it and follow it.
- **If absent** → Suggest `/dev-front-system --init`. Proceed without it if they prefer.

### A real brand system OVERRIDES this skill's aesthetic DON'Ts

The DON'T list below (no Inter, no cyan-on-dark, no dark-mode-with-accent, and so on) describes the **defaults AI reaches for when it has no brand to follow**. It is not a ban on colours and fonts that real companies legitimately own.

When the client's brand mandates something on that list, **the brand wins**. Ignoring a documented brand to satisfy a generic heuristic is the actual error, and it produces work the client cannot ship.

Apply the anti-slop discipline to **execution** instead:

| Situation | Wrong response | Right response |
|---|---|---|
| Brand font is Inter | Substitute a "better" font | Use Inter. Earn distinction through scale, spacing, and hierarchy |
| Signature colour is a cyan / neon | Swap it for something tasteful | Use it. Read the brand's stated *feel* and avoid the lazy rendering of it |
| Brand is dark-themed | Force a light theme | Build the dark theme well: layered surfaces, tinted neutrals, one accent |

Read the brand's own adjectives and let them decide the rendering. A guide that says "light, geometric, tech-forward" with a cyan accent means **cyan as an accent on a light field**, not cyan glowing on black, even though both are "on brand" by colour alone. That distinction is where the slop actually lives.

Use the real assets, not approximations: pull the actual logo file rather than typesetting the wordmark, and quote the brand's real sentences rather than inventing positioning in its voice.

---

## Design Direction

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Style preset or custom tone**: If `--style` was specified, load the corresponding preset from [style presets](reference/style-presets.md) and apply its typography, color, layout, motion, and component rules. If no preset, pick a clear direction — or choose from: soft (agency/premium), minimal (editorial/workspace), brutalist (industrial/data), editorial (magazine/serif). Other directions work too: retro-futuristic, organic, playful, art deco, etc.
- **Dial calibration**: Adjust DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY based on context. Style presets set their own defaults (see [dials reference](reference/dials.md)).
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Brief fidelity across iterations

On multi-round design work the failure mode is rarely a bad round. It is **requirement drift**: fixing the newest complaint while silently dropping a constraint from an earlier one.

Keep an explicit ledger of every stated constraint from the original brief and carry it forward untouched: named conversion mechanics, named audiences, scope boundaries, must-include content, forbidden elements.

**Never rename the user's named mechanic.** If they said "waitlist", the button says join the waitlist. Inventing a cleverer label is not a copy improvement, it is dropping a requirement while appearing to work. The same holds for a named audience, a named framework, or a named page type.

Before delivering any revision, re-verify the **whole ledger**, not only the item you were last asked about. A round that satisfies the newest note and breaks an older one is a regression, and the user experiences it as not being listened to.

Signals you have drifted: the user prefixes a correction with "as I said", "again", or "like I told you", or repeats a constraint they already gave. Treat those words as evidence of a dropped requirement, not as new information.

---

## Deliverable Integrity

A page that renders on your machine and breaks on theirs is not delivered. Two failures cause almost all of it:

**1. Self-contained means self-contained.** Any HTML handed over as a standalone file (attachment, artifact, paste-into-CMS block, preview link) must carry its own assets. A relative `src="assets/logo.png"` breaks the moment the HTML travels without the folder, and it will travel without the folder.

- Inline images as `data:` URIs, or inline SVG. Generate the base64 with a script so it never passes through your own output.
- Keep the embedded copy small (size it for its rendered dimensions, not the source file).
- Before delivering, grep the file for `src="assets/`, `src="./`, `href="./`, and any other relative reference. The count must be zero.
- If an asset genuinely must stay external, say so explicitly in the handover and ship the asset alongside.

**2. Every element earns its place.** Chrome that speaks to nobody is worse than empty space, because it costs attention and says the page was assembled rather than written. Audit each element against: *which reader wants this, and what do they do differently for having read it?*

Common offenders: corporate parentage lines in the header ("An X product, delivered by Y"), badges nobody asked for, restated headings, decorative counters, and legends explaining a graphic that should not need one. Move parentage to the footer, or cut it.

**3. Real navigation and a real footer are content, not furniture.** For a page replacing or extending a live site, mirror the site's actual menu (fetch it, do not invent it) and give the footer real destinations. Legal links (terms, privacy) are frequently a contractual requirement from an API or connector agreement, not a nicety. Ask which apply, and use the live URLs.

---

## Frontend Aesthetics Guidelines

> **These DON'Ts describe AI defaults, not banned design.** If the project has a documented brand system (see [Design Context](#design-context)), the brand overrides every DON'T below. Apply the discipline to how you execute the brand, not to whether you follow it.

### Typography
> *Consult [typography reference](reference/typography.md) for scales, pairing, and loading strategies.*

Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font.

**DO**: Use a modular type scale with fluid sizing (clamp)
**DO**: Vary font weights and sizes to create clear visual hierarchy
**DON'T**: Use overused fonts—Inter, Roboto, Arial, Open Sans, system defaults
**DON'T**: Use monospace typography as lazy shorthand for "technical/developer" vibes
**DON'T**: Put large icons with rounded corners above every heading—they rarely add value and make sites look templated

### Color & Theme
> *Consult [color reference](reference/color-and-contrast.md) for OKLCH, palettes, and dark mode.*

Commit to a cohesive palette. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

**DO**: Use modern CSS color functions (oklch, color-mix, light-dark) for perceptually uniform, maintainable palettes
**DO**: Tint your neutrals toward your brand hue—even a subtle hint creates subconscious cohesion
**DON'T**: Use gray text on colored backgrounds—it looks washed out; use a shade of the background color instead
**DON'T**: Use pure black (#000) or pure white (#fff)—always tint; pure black/white never appears in nature
**DON'T**: Use the AI color palette: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds
**DON'T**: Use gradient text for "impact"—especially on metrics or headings; it's decorative rather than meaningful
**DON'T**: Default to dark mode with glowing accents—it looks "cool" without requiring actual design decisions
**DON'T**: Use more than one accent color—pick one, commit to it; multiple accents create visual noise
**DON'T**: Use emojis anywhere in UI—BANNED. Use proper icons (Phosphor, Radix) or clean SVG

### Layout & Space
> *Consult [spatial reference](reference/spatial-design.md) for grids, rhythm, and container queries.*

Create visual rhythm through varied spacing—not the same padding everywhere. Embrace asymmetry and unexpected compositions. Break the grid intentionally for emphasis.

**DO**: Create visual rhythm through varied spacing—tight groupings, generous separations
**DO**: Use fluid spacing with clamp() that breathes on larger screens
**DO**: Use asymmetry and unexpected compositions; break the grid intentionally for emphasis
**DON'T**: Wrap everything in cards—not everything needs a container
**DON'T**: Nest cards inside cards—visual noise, flatten the hierarchy
**DON'T**: Use identical card grids—same-sized cards with icon + heading + text, repeated endlessly
**DON'T**: Use the hero metric layout template—big number, small label, supporting stats, gradient accent
**DON'T**: Center everything—left-aligned text with asymmetric layouts feels more designed
**DON'T**: Use the same spacing everywhere—without rhythm, layouts feel monotonous
**DON'T**: Use 3-column equal card grids—the most generic AI layout. Use 2-column zig-zag, asymmetric grid, bento, or horizontal scroll
**DON'T**: Use `h-screen` for full-height sections—use `min-h-[100dvh]` to prevent iOS Safari viewport jumping

### Visual Details
**DO**: Use intentional, purposeful decorative elements that reinforce brand
**DON'T**: Use glassmorphism everywhere—blur effects, glass cards, glow borders used decoratively rather than purposefully
**DON'T**: Use rounded elements with thick colored border on one side—a lazy accent that almost never looks intentional
**DON'T**: Use sparklines as decoration—tiny charts that look sophisticated but convey nothing meaningful
**DON'T**: Use rounded rectangles with generic drop shadows—safe, forgettable, could be any AI output
**DON'T**: Use modals unless there's truly no better alternative—modals are lazy

### Motion
> *Consult [motion reference](reference/motion-design.md) for timing, easing, and reduced motion. When the `motion-library` skill is installed, pull from it first — 98+ proven, reusable animations (goo/metaball, liquid, 3D, cursor, scroll, feedback, lists) beat hand-rolling keyframes. Optional, not required.*

Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions.

**DO**: Use motion to convey state changes—entrances, exits, feedback
**DO**: Use exponential easing (ease-out-quart/quint/expo) for natural deceleration
**DO**: For height animations, use grid-template-rows transitions instead of animating height directly
**DON'T**: Animate layout properties (width, height, padding, margin)—use transform and opacity only
**DON'T**: Use bounce or elastic easing—they feel dated and tacky; real objects decelerate smoothly

### Interaction
> *Consult [interaction reference](reference/interaction-design.md) for forms, focus, and loading patterns.*

Make interactions feel fast. Use optimistic UI—update immediately, sync later.

**DO**: Use progressive disclosure—start simple, reveal sophistication through interaction (basic options first, advanced behind expandable sections; hover states that reveal secondary actions)
**DO**: Design empty states that teach the interface, not just say "nothing here"
**DO**: Make every interactive surface feel intentional and responsive
**DON'T**: Repeat the same information—redundant headers, intros that restate the heading
**DON'T**: Make every button primary—use ghost buttons, text links, secondary styles; hierarchy matters

### Responsive
> *Consult [responsive reference](reference/responsive-design.md) for mobile-first, fluid design, and container queries.*

**DO**: Use container queries (@container) for component-level responsiveness
**DO**: Adapt the interface for different contexts—don't just shrink it
**DON'T**: Hide critical functionality on mobile—adapt the interface, don't amputate it

### UX Writing
> *Consult [ux-writing reference](reference/ux-writing.md) for labels, errors, and empty states.*

**DO**: Make every word earn its place
**DON'T**: Repeat information users can already see

---

## Communication Clarity
> *Consult [communication reference](reference/communication.md) for messaging tables and user flow principles.*

Any user encountering a section for the first time should immediately grasp: **What** this is, **Who** it's for, **Why** they should care. This is the 3-second test.

**DO**: Frame benefits positively, one primary CTA per section, speak the user's language
**DON'T**: Use internal jargon, have multiple equally-weighted CTAs, lead with sign-up/paywall before showing value

## Premium Patterns
> *Consult [premium patterns reference](reference/premium-patterns.md) for detailed patterns and resources.*

Five patterns that elevate UI from generic to premium: subtle interactions & animations, custom illustrations for empty states, immediate sensory feedback, consistent & thoughtful iconography, and continuous design taste training.

---

## The AI Slop Test
> *Consult [ai-slop reference](reference/ai-slop.md) for the detailed checklist with fixes.*

**Critical quality check**: If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

A distinctive interface should make someone ask "how was this made?" not "which AI made this?"

Review the DON'T guidelines above—they are the fingerprints of AI-generated work from 2024-2025.

---

## Implementation Principles

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices across generations.

### Constraint-Driven Language

Use precise constraints, not vague directives. **"Subtle"** is the most powerful keyword for preventing over-engineered AI output.

| Instead of... | Say... |
|---|---|
| "improve the design" | "refine the design, keep layouts consistent and animations subtle" |
| "add animations" | "subtle fade-up on enter, 200ms ease-out, staggered 50ms" |
| "make it better" | "tighten spacing, reduce visual noise, match this reference's density" |

### Build Section-by-Section

Never generate an entire page in one pass. Build section by section, verify each against the style guide before proceeding.

---

## Related Skills (optional — use if installed, never required)

These are independent skills. This skill works fully on its own; reach for one only when the task calls for it and it happens to be available. No hard dependency — if a skill is absent, proceed without it.

| When the work involves... | Consider | Instead of |
|---------------------------|----------|------------|
| Animations / motion / `overdrive` | **`motion-library`** — 98+ proven, reusable UI animations (goo/metaball, liquid, 3D, cursor, scroll, feedback) | hand-rolling every keyframe |
| Charts, dashboards, KPI/metric surfaces | **`dataviz`** — accessible chart engine + design system (JSON spec → light/dark HTML with a table-twin) | ad-hoc chart markup |
| Empty-state illustrations, hero imagery, image resize/crop/reframe | **`art`** — local resize/crop + subject-aware crops + AI image generation | emoji or placeholder boxes |
| Faithful pixel-level reproduction of an existing interface | **`interface-mirror`** — six-axis replication-fidelity scoring | eyeballing the diff (this skill's `--mirror` mode covers the build; `interface-mirror` scores fidelity) |
| Landing/marketing copy | **a copywriting skill** — AIDA/PAS/StoryBrand frameworks | generic marketing prose |
| Project design system / tokens / `## Design Context` | **`dev-front-system`** — the companion; `/dev-front-system --init` seeds the context this skill reads | improvising tokens per build |
| Verifying a build before you call it "done" / ship | **`qa-sentinel`** (`/qa run`) — goal-anchored adversarial gate; its designer lens runs a deterministic AI-slop linter (`slop_lint.py`) then judges against the goal | trusting your own "looks finished" |

Remember: Claude is capable of extraordinary creative work. Don't hold back--show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
