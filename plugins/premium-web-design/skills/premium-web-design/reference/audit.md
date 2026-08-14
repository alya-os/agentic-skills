Run a complete interface audit in two phases. This is a read-only mode — produce reports, not code changes.

Each phase produces a numerical score for objective measurement and before/after comparison.

**First**: Review the design principles and anti-patterns from the main SKILL.md DON'T guidelines.

---

## Quick Review Pass (proactive — apply to ANY UI work, not just --audit)

Before or during any UI creation/review, run this 30-second lens. It is the always-on layer inherited from the premium-web-design skill; the full two-phase audit below is the deep version.

**The 3-second comprehension test** — if a user sees this section for 3 seconds, can they answer:
- [ ] **What** is this product/feature?
- [ ] **Who** is it for?
- [ ] **Why** should they care?

If no → refactor messaging and visual hierarchy before touching aesthetics.

**Clarity spot-checks** (fix immediately when spotted):

| Element | Check | Action if missing |
|---------|-------|------------------|
| Headline | No jargon, speaks user's language | Replace technical terms with plain language |
| Problem/Solution | Pain point clearly established | Add "before/after" or problem statement |
| Differentiation | Unique value in one sentence | Add what makes this different |
| Target audience | Crystal clear who this is for | Narrow messaging to a specific persona |
| AI slop tells | Scan against [ai-slop reference](ai-slop.md) | Fix per its checklist |

---

## Phase 1: Technical Audit — "Est-ce que ça marche bien ?"

Run systematic quality checks across these dimensions:

### 1. Accessibility (A11y)
- **Contrast issues**: Text contrast ratios < 4.5:1 (or 7:1 for AAA)
- **Missing ARIA**: Interactive elements without proper roles, labels, or states
- **Keyboard navigation**: Missing focus indicators, illogical tab order, keyboard traps
- **Semantic HTML**: Improper heading hierarchy, missing landmarks, divs instead of buttons
- **Alt text**: Missing or poor image descriptions
- **Form issues**: Inputs without labels, poor error messaging, missing required indicators

### 2. Performance
- **Layout thrashing**: Reading/writing layout properties in loops
- **Expensive animations**: Animating layout properties (width, height, top, left) instead of transform/opacity
- **Missing optimization**: Images without lazy loading, unoptimized assets, missing will-change
- **Bundle size**: Unnecessary imports, unused dependencies
- **Render performance**: Unnecessary re-renders, missing memoization

### 3. Theming
- **Hard-coded colors**: Colors not using design tokens
- **Broken dark mode**: Missing dark mode variants, poor contrast in dark theme
- **Inconsistent tokens**: Using wrong tokens, mixing token types
- **Theme switching issues**: Values that don't update on theme change

### 4. Responsive Design
- **Fixed widths**: Hard-coded widths that break on mobile
- **Touch targets**: Interactive elements < 44x44px
- **Horizontal scroll**: Content overflow on narrow viewports
- **Text scaling**: Layouts that break when text size increases
- **Missing breakpoints**: No mobile/tablet variants

### 5. Anti-Patterns (CRITICAL)
Check against ALL the **DON'T** guidelines in the main skill. Look for AI slop tells and general design anti-patterns. Consult [ai-slop reference](ai-slop.md) for the detailed checklist.

### Phase 1 Score: Technical Quality (0-20)

Score each dimension 0-4 (0=critical failures, 1=major issues, 2=several problems, 3=minor issues, 4=excellent):

| Dimension | Score (0-4) |
|-----------|-------------|
| Accessibility | /4 |
| Performance | /4 |
| Theming | /4 |
| Responsive Design | /4 |
| Anti-Patterns | /4 |
| **Total** | **/20** |

**Score bands**: 0-5 Critical (fundamental issues) · 6-9 Poor (major overhaul) · 10-13 Acceptable (significant work) · 14-17 Good (targeted fixes) · 18-20 Excellent (minor polish)

---

## Phase 2: Design Critique — "Est-ce que ça look bien ?"

Evaluate the interface as a design director would:

### 1. AI Slop Detection (CRITICAL)
**This is the most important check.** Does this look like every other AI-generated interface from 2024-2025?

Review against ALL the **DON'T** guidelines — they are the fingerprints of AI-generated work. Check for the AI color palette, gradient text, dark mode with glowing accents, glassmorphism, hero metric layouts, identical card grids, generic fonts, and all other tells.

**The test**: If you showed this to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

### 2. Visual Hierarchy
- Does the eye flow to the most important element first?
- Is there a clear primary action? Can you spot it in 2 seconds?
- Do size, color, and position communicate importance correctly?
- Is there visual competition between elements that should have different weights?

### 3. Information Architecture
- Is the structure intuitive? Would a new user understand the organization?
- Is related content grouped logically?
- Are there too many choices at once? (cognitive overload)
- Is the navigation clear and predictable?

### 4. Communication Clarity
- Does the interface pass the 3-second test? (What/Who/Why immediately clear)
- Is there a single primary CTA per section?
- Does the messaging speak the user's language, not internal jargon?
- Is the value proposition specific, not vague? Consult [communication reference](communication.md)

### 5. Emotional Resonance
- What emotion does this interface evoke? Is that intentional?
- Does it match the brand personality?
- Would the target user feel "this is for me"?

### 6. Composition & Balance
- Does the layout feel balanced or uncomfortably weighted?
- Is whitespace used intentionally or just leftover?
- Is there visual rhythm in spacing and repetition?
- Does asymmetry feel designed or accidental?

### 7. Typography as Communication
- Does the type hierarchy clearly signal what to read first, second, third?
- Is body text comfortable to read? (line length, spacing, size)
- Do font choices reinforce the brand/tone?

### 8. Color with Purpose
- Is color used to communicate, not just decorate?
- Does the palette feel cohesive?
- Are accent colors drawing attention to the right things?

### 9. States & Edge Cases
- Empty states: Do they guide users toward action?
- Loading states: Do they reduce perceived wait time?
- Error states: Are they helpful and non-blaming?
- Success states: Do they confirm and guide next steps?

### 10. Microcopy & Voice
- Is the writing clear and concise?
- Does it sound like the right human for this brand?
- Are labels and buttons unambiguous?

### Phase 2 Score: Design Quality (0-40)

Score using Nielsen's 10 Usability Heuristics. Each scored 0-4 (0=violated everywhere, 1=major violations, 2=several issues, 3=minor issues, 4=exemplary):

| Heuristic | Maps to | Score (0-4) |
|-----------|---------|-------------|
| 1. Visibility of system status | States & Edge Cases (#9) | /4 |
| 2. Match between system and real world | Communication Clarity (#4) | /4 |
| 3. User control and freedom | Information Architecture (#3) | /4 |
| 4. Consistency and standards | Visual Hierarchy (#2) | /4 |
| 5. Error prevention | States & Edge Cases (#9) | /4 |
| 6. Recognition rather than recall | Information Architecture (#3) | /4 |
| 7. Flexibility and efficiency of use | Composition & Balance (#6) | /4 |
| 8. Aesthetic and minimalist design | AI Slop Detection (#1) | /4 |
| 9. Help users recognize, diagnose, recover from errors | Microcopy & Voice (#10) | /4 |
| 10. Help and documentation | Communication Clarity (#4) | /4 |
| **Total** | | **/40** |

**Score bands**: 0-11 Critical · 12-21 Poor · 22-31 Fair · 32-35 Good · 36-40 Excellent

### Persona-Based Testing

After scoring, evaluate the interface through 5 user archetypes. Select 2-3 personas most relevant to the interface type.

**Alex — Impatient Power User**
Tests: keyboard shortcuts, bulk actions, onboarding bypass, information density.
Red flags: forced tutorials, no shortcuts, slow workflows, unnecessary confirmation dialogs.
*Best for: dashboards, admin tools, developer tools, productivity apps.*

**Jordan — Confused First-Timer**
Tests: discoverability, labeled icons, plain language, help access, clear CTAs.
Red flags: unexplained jargon, icon-only navigation, no getting-started guidance, hidden features.
*Best for: landing pages, onboarding flows, consumer apps, marketing sites.*

**Sam — Accessibility-Dependent**
Tests: keyboard-only navigation, screen reader compatibility, WCAG AA (4.5:1), focus management.
Red flags: missing focus rings, `outline: none` without replacement, unlabeled images, keyboard traps, color-only indicators.
*Best for: any public-facing interface, government/enterprise, healthcare, education.*

**Riley — Deliberate Stress Tester**
Tests: edge cases, error recovery, state persistence, boundary inputs, concurrent actions.
Red flags: silent failures, lost form data, broken back-button, no undo, unhandled empty/overflow states.
*Best for: forms, e-commerce checkout, multi-step wizards, data-heavy interfaces.*

**Casey — Distracted Mobile User**
Tests: one-handed use, thumb-zone placement, state persistence across interruptions, 44px touch targets.
Red flags: small tap targets, no state persistence, lost scroll position, horizontal overflow, pinch-to-zoom disabled.
*Best for: mobile-first apps, responsive sites, PWAs, any interface used on-the-go.*

**Selection guide**: Landing pages → Jordan + Riley + Casey. Dashboards → Alex + Sam. E-commerce → Riley + Casey + Jordan. Internal tools → Alex + Sam + Riley.

---

## Generate Audit Report

Structure the report in two clear parts:

### Anti-Patterns Verdict
**Start here.** Pass/fail: Does this look AI-generated? List specific tells. Be brutally honest.

### Part 1: Technical Findings

#### Executive Summary
- Total issues found (count by severity)
- Most critical issues (top 3-5)

#### Detailed Findings by Severity

For each issue:
- **Location**: Component, file, line
- **Severity**: Critical / High / Medium / Low
- **Category**: Accessibility / Performance / Theming / Responsive
- **Description**: What the issue is
- **Impact**: How it affects users
- **WCAG/Standard**: Which standard it violates (if applicable)
- **Recommendation**: How to fix it
- **Suggested command**: Which premium-web-design mode or dev-front-system mode to use

### Part 2: Design Critique

#### Overall Impression
A brief gut reaction — what works, what doesn't, and the single biggest opportunity.

#### What's Working
Highlight 2-3 things done well. Be specific about why.

#### Priority Issues
The 3-5 most impactful design problems, ordered by importance:

For each:
- **What**: Name the problem clearly
- **Why it matters**: How this hurts users or undermines goals
- **Fix**: Concrete suggestion
- **Suggested command**: Which premium-web-design refine mode to use (--polish, --animate, --colorize, etc.)

#### Questions to Consider
Provocative questions that might unlock better solutions.

### Recommendations by Priority
1. **Immediate**: Critical blockers to fix first
2. **Short-term**: High-severity issues (this sprint)
3. **Medium-term**: Quality improvements (next sprint)
4. **Long-term**: Nice-to-haves and optimizations

**CRITICAL**: Be direct — vague feedback wastes time. Be specific — "the submit button" not "some elements". Prioritize ruthlessly — if everything is important, nothing is.

---

## Quick-Scan Checklist (Comprehensive)

A rapid 100-point scan for common issues. Check each category systematically before writing the full report.

### Typography (10 points)
- [ ] Browser default or Inter font everywhere?
- [ ] Headlines lack presence (small, loose tracking, high line-height)?
- [ ] Body text wider than ~65 characters?
- [ ] Only Regular (400) and Bold (700) weights used?
- [ ] Numbers in proportional font instead of tabular figures?
- [ ] Missing letter-spacing adjustments on headers/labels?
- [ ] All-caps subheaders everywhere?
- [ ] Orphaned single words on last line?
- [ ] Serif font used on dashboard/software UI?
- [ ] More than 2-3 font families?

### Color & Surfaces (12 points)
- [ ] Pure `#000000` used?
- [ ] Oversaturated accents (>80% saturation)?
- [ ] More than one accent color?
- [ ] Mixed warm and cool grays?
- [ ] Purple/blue "AI gradient" aesthetic?
- [ ] Generic `box-shadow` (pure black, too strong)?
- [ ] Flat design with zero texture?
- [ ] Perfectly even linear gradients?
- [ ] Inconsistent lighting direction across shadows?
- [ ] Random dark sections in a light mode page?
- [ ] Empty flat sections with no visual depth?
- [ ] Gray text on colored backgrounds?

### Layout (15 points)
- [ ] Everything centered and symmetrical?
- [ ] Three equal card columns as feature row?
- [ ] Using `h-screen` instead of `min-h-[100dvh]`?
- [ ] Complex flexbox percentage math instead of CSS Grid?
- [ ] No max-width container (content stretches edge-to-edge)?
- [ ] Cards of equal height forced by flexbox?
- [ ] Uniform border-radius on everything?
- [ ] No overlap or depth (elements flat next to each other)?
- [ ] Symmetrical top/bottom padding (bottom often needs more)?
- [ ] Dashboard with mandatory left sidebar?
- [ ] Missing whitespace (design doesn't breathe)?
- [ ] Buttons not bottom-aligned in card groups?
- [ ] Feature lists at different Y positions across columns?
- [ ] Inconsistent vertical rhythm in side-by-side elements?
- [ ] Mathematical alignment that looks optically wrong?

### Interactivity & States (11 points)
- [ ] No hover states on buttons?
- [ ] No active/pressed feedback?
- [ ] Instant transitions with zero duration?
- [ ] Missing focus ring for keyboard navigation?
- [ ] No loading states (or generic circular spinner)?
- [ ] No empty states?
- [ ] No error states?
- [ ] Dead `#` links?
- [ ] No active page indicator in navigation?
- [ ] Animations using layout properties instead of transform/opacity?
- [ ] Missing `prefers-reduced-motion` support?

### Content (12 points)
- [ ] Generic names ("John Doe", "Jane Smith")?
- [ ] Fake round numbers (`99.99%`, `50%`)?
- [ ] Placeholder company names ("Acme Corp")?
- [ ] AI copywriting clichés ("Elevate", "Seamless", "Unleash")?
- [ ] Exclamation marks in success messages?
- [ ] "Oops!" error messages?
- [ ] Passive voice in messaging?
- [ ] All blog post dates identical?
- [ ] Same avatar for multiple users?
- [ ] Lorem Ipsum anywhere?
- [ ] Title Case On Every Header?
- [ ] Emojis in UI text?

### Components (10 points)
- [ ] Generic card look (border + shadow + white bg)?
- [ ] Always one filled button + one ghost button?
- [ ] Pill-shaped "New"/"Beta" badges?
- [ ] Accordion FAQ (instead of side-by-side or searchable)?
- [ ] 3-card carousel testimonials with dots?
- [ ] 3-tower pricing table without clear tier emphasis?
- [ ] Modals for simple actions?
- [ ] Avatar circles exclusively (no squircles)?
- [ ] Sun/moon dark mode toggle?
- [ ] Footer link farm with 4+ columns?

### Iconography (5 points)
- [ ] Lucide/Feather icons exclusively?
- [ ] Cliché metaphors (rocket=launch, shield=security)?
- [ ] Inconsistent stroke widths across icons?
- [ ] Missing favicon?
- [ ] Stock "diverse team" photos?

### Code Quality (7 points)
- [ ] Div soup (no semantic HTML)?
- [ ] Inline styles mixed with CSS classes?
- [ ] Hardcoded pixel widths?
- [ ] Missing alt text on images?
- [ ] Arbitrary z-index values (`9999`)?
- [ ] Commented-out dead code?
- [ ] Import hallucinations (packages not in dependencies)?

### Strategic Omissions (6 points)
- [ ] No legal links (privacy, ToS)?
- [ ] No "back" navigation (dead ends)?
- [ ] No custom 404 page?
- [ ] No form validation?
- [ ] No "skip to content" link?
- [ ] No cookie consent (if required)?

### Fix Priority Order
When issues are found, fix in this order for maximum visual impact with minimum risk:
1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing/oversaturated colors
3. **Hover and active states** — makes interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliché patterns for modern alternatives
6. **Add loading, empty, and error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

---

## Pre-Launch Performance Gate

Run this gate before any site ships — mandatory for animated/scroll-driven sites, where effects are the #1 cause of Core Web Vitals failures. Measure with Lighthouse (mobile, throttled) and real-device testing, not desktop DevTools alone.

### Core Web Vitals thresholds (hard numbers)

| Metric | Pass | Needs work | Fail |
|--------|------|-----------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5-4.0s | > 4.0s |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |
| **INP** (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |

### Animation-specific checks
- [ ] Only `transform` and `opacity` animated (no layout properties)
- [ ] Heavy effects (WebGL, GSAP timelines, particles) lazy-initialize on viewport entry, not page load
- [ ] `will-change` only on elements about to animate, removed after
- [ ] 60fps verified in DevTools Performance tab on a mid-range mobile profile
- [ ] `prefers-reduced-motion` disables scroll-driven, parallax, and particle effects
- [ ] Hero animation does not delay LCP (animate after content paints, or animate the LCP element with opacity only)
- [ ] Entrance animations don't cause CLS (reserve space; animate in place, not into layout)

### Asset & delivery checks
- [ ] Images: modern formats (AVIF/WebP), responsive `srcset`, explicit width/height, lazy loading below the fold
- [ ] Fonts: `font-display: swap` (or `optional` for non-critical), subset, preload the one critical font, max 2 families
- [ ] JS: code-split by route/section; animation libraries loaded only where used; no render-blocking scripts
- [ ] Compression: Brotli/gzip on; assets minified; video posters + `preload="none"` on below-fold media
- [ ] Caching: long-lived immutable cache headers on hashed assets; HTML short-cache
- [ ] Third-party scripts deferred and audited (each one must justify its weight)

### SEO & a11y sanity (pre-launch)
- [ ] Content renders without JS (or SSR/prerender in place) — critical for crawlers and AI answer engines
- [ ] One `<h1>`, logical heading order, meta title/description, canonical, OG tags
- [ ] Keyboard path through the whole page; focus visible; skip-to-content link
- [ ] Custom 404, legal links, favicon

**Verdict format**: PASS / CONDITIONAL PASS (list the conditions) / FAIL (list blockers in fix-priority order).
