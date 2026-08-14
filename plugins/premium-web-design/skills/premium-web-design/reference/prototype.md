# GenUI Prototyper - Interactive HTML Design Handoffs

Build multiple interactive HTML prototypes in parallel, publish for stakeholder review, iterate on feedback. Specialized for ad creative management UIs but applicable to any data-rich dashboard prototype.

---

## When to Use

- Building interactive HTML mockups/handoffs for a product feature
- Creating multiple competing UI versions for comparison
- Prototyping ad management, creative audit, or campaign tools
- Any "design sprint" where you need 3-4 versions fast

**Trigger phrases:** "create UI versions", "design handoff", "GenUI prototype", "build HTML mockups", "interactive wireframe"

---

## Version Count & Token Budget

- **Default 3 versions**, 5 for a full sprint, up to ~7 only on an explicit "be comprehensive." More rarely changes the decision and wastes budget.
- Confirm the count with one quick question before fanning out, never spin up agents silently.
- One PARALLEL background agent per version; each writes its self-contained file to disk EARLY (then iterates) so a failure never loses a finished version.
- Every version stays on a DISTINCT, non-converging direction.

---

## Workflow

```
1. SPEC    - Understand the feature, data model, and user workflow
2. BUILD   - Launch parallel agents (one per version) to create HTML files
3. PUBLISH - Upload to FTP or local server for browser review
4. TEST    - Open in agent-browser, screenshot, verify interactions
5. ITERATE - Fix issues, rebuild versions based on feedback
6. REPEAT  - Until the design direction is locked
```

### Step 1: Spec Gathering

Before building, answer:
- **Who uses this?** (e.g., ad specialists, media buyers, account managers)
- **What's the core workflow?** (e.g., see ads > identify problems > pause/generate > export)
- **What data entities?** (e.g., campaigns > adgroups > creatives, with metrics)
- **What channels/platforms?** (each has different fields - see Channel Field Schemas below)
- **What AI integrations?** (e.g., your own named generation agents)

### Step 2: Parallel Agent Build

Launch one agent per version. Each agent gets:
- The full spec context
- A specific UI paradigm to follow
- Sample data (advertiser, campaigns, ads with French/English copy)
- Design rules (palette, typography, spacing, no-purple, etc.)
- The Channel Field Schemas section below

**Agent prompt template:**
```
Create /tmp/prototype-{concept}_v{N}.html -- single self-contained HTML file.

## Concept: {Paradigm Name}
{Description of the UI paradigm and how it organizes data}

## Features Required
{List from spec}

## Sample Data
{Advertiser name, campaigns, ad counts, channel mix}

## Design Rules
- {Palette, fonts, spacing}
- NO external CDN links (inline everything or use Unicode for icons)
- Use cr-* prefix for CSS classes (NEVER ad-* -- ad blockers kill them)
- All content as static HTML where possible, JS for interactions only
```

### Step 3: Publish

Use ftp-publisher skill to upload to review URL:
```bash
uv run .../upload.py -s snippets -l /tmp/file.html -r /internal/file.html
```

### Step 4: Browser Test

Use agent-browser to verify each version:
```bash
agent-browser open "https://url/file.html"
agent-browser screenshot /tmp/test.png
agent-browser snapshot -i  # Check interactive elements
agent-browser find text "Some Button" click  # Test interactions
```

### Step 5: Iterate

Common iteration patterns:
- "Collapsible doesn't work" -> Check JS event handlers, stopPropagation
- "Nothing shows" -> Check for ad-blocker-triggering class names
- "Layout broken" -> Check flex-wrap, min-width:0, overflow settings
- "Feels static" -> Add hover states, transitions (<300ms), loading shimmer

### Step 6: Judge & Synthesize (before handing back)

Don't dump N files on the user. Digest each version into a compact scorecard (distinctiveness · comprehension · density fit · motion discipline · port feasibility, /10 each) via a read-only pass per version so your own context stays lean. Then write a short SYNTHESIS: scored table, recommended winner with a one-paragraph rationale, and a "graft list" of the best ideas from the versions that lost.

---

## Proven UI Paradigms

Use these as starting points for different versions:

| Paradigm | Best For | Key Pattern |
|----------|----------|-------------|
| **Master/Detail Split** | Dense data, many fields per item | Left list (40%) + right adaptive detail (60%) |
| **Accordion Table** | Scannable overview + deep editing | Compact rows, click to expand channel-specific fields |
| **Channel Swim Lanes** | Multichannel comparison at a glance | Horizontal card strips per channel, scroll within |
| **Visual Card Catalog** | Image-heavy ads (Meta, Display, TikTok) | Gallery grid with cards, filtering, grouping |
| **Node/Topology Graph** | Relationships, shared angles, cross-channel | SVG nodes = creatives, edges = shared themes |
| **Vertical Tree** | Hierarchy drill-down | Advertiser > Channels > Campaigns > Creatives, top to bottom |
| **Radial Sunburst** | Budget/spend distribution | Concentric rings, sector size = proportional spend |
| **Command Center** | Real-time monitoring, workflow lifecycle | Kanban columns (Detect > Create > Deploy) + live feed |

---

## Channel Field Schemas

Each ad channel has completely different fields. UIs must adapt per channel.

### Google Search RSA
- 15 headlines (30 char each), pin positions (1/2/3/none)
- 4 descriptions (90 char each)
- Final URL, display path
- Preview: Google SERP mockup (H1 | H2 | H3 + D1)

### Google Demand Gen
- 5 headlines (40 char each)
- 5 descriptions (90 char each)
- Images: landscape (1200x628), square (1200x1200), portrait (960x1200)
- Brand name (25 char), link
- Video option (square/landscape/vertical, 5-30s)

### Google Performance Max
- 5 short headlines (30 char), 5 long headlines (90 char)
- 5 descriptions (90 char each)
- Images: landscape (1200x628), square (1200x1200), portrait (960x1200), logo (1200x1200), landscape logo (1200x300)
- Videos (YouTube links)

### Google Responsive Display
- 5 headlines (30 char), 1 long headline (90 char)
- 5 descriptions (90 char each)
- Images: landscape (1200x628), square (1200x1200), portrait (900x1600)
- Up to 5 YouTube video links

### Meta Feed (Facebook/Instagram)
- Square image required (1080x1080), landscape optional (1200x628)
- Headline (40 char)
- Primary text (125 char)
- Link description (30 char)
- CTA button (Shop Now, Learn More, Sign Up, etc.)
- Preview: Meta feed mockup (avatar, "Sponsored", image, headline, CTA)

### Meta Stories/Reels
- Vertical image or video (1080x1920, 9:16)
- Headline (40 char)
- Primary text (72 char for Reels)
- CTA button
- Preview: Full-screen vertical mockup

### TikTok
- Video (1080x1920, 9:16, 5-60s)
- Ad text (100 char)
- CTA button
- Display name
- Preview: TikTok For You page mockup

### LinkedIn
- Introductory text (150 char recommended, 255 max)
- Headline (70 char recommended, 200 max)
- Image (1200x627) or video
- CTA button

---

## Ad Blocker-Safe CSS Naming

**CRITICAL:** Never use CSS class names or IDs containing these patterns -- ad blockers will remove the elements:

| Blocked Pattern | Safe Alternative |
|----------------|-----------------|
| `ad-row`, `ad-card`, `ad-name` | `cr-row`, `cr-card`, `cr-name` |
| `adContainer`, `adList`, `adTable` | `crContainer`, `crList`, `crTable` |
| `ai-generated` | `agent-generated` |
| `banner`, `sponsor`, `promo` | `hero`, `partner`, `offer` |
| `ad-badge`, `ad-info` | `cr-badge`, `cr-info` |

Use `cr-` (creative) or `item-` or `entry-` prefixes throughout.

---

## Design Rules for Prototypes

### Always
- System fonts only (-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif)
- Spacing multiples of 8px
- 2 font sizes: 11-12px for data, 13-14px for UI elements
- Subtle transitions under 300ms
- No external CDN dependencies (inline everything)
- Icons: Unicode symbols or inline SVG, never external icon fonts
- All content rendered as static HTML (JS for interactions only)

### Never
- Purple in the palette (user preference)
- External CDN links (unpkg, cdnjs) -- they can block rendering or get blocked
- `ad-*` prefixed CSS classes (ad blockers)
- Heavy drop shadows, glossy gradients, over-animation
- JS-only rendering (page must show content with JS disabled)

### Color Palettes

**Light theme (spreadsheet/table UIs):**
```css
--bg: #fff; --bg-alt: #f8f9fa; --border: #e5e7eb;
--text: #111827; --text-sec: #6b7280;
--blue: #3b82f6; --green: #16a34a; --red: #dc2626; --amber: #d97706;
--google: #4285f4; --meta: #1877f2; --tiktok: #010101;
```

**Dark theme (graph/visualization UIs):**
```css
--bg: #0a0e14; --surface: #111827; --border: #1e293b;
--text: #f1f5f9; --text-sec: #94a3b8;
--teal: #14b8a6; --cyan: #06b6d4; --blue: #3b82f6;
```

---

## Metrics Display Pattern

Combine metrics into a single compact cell with period-over-period deltas:

```
CTR 2.4% +0.3  |  1.2K clicks +5%  |  8 conv +2
```

- Green text + up arrow = improvement
- Red text + down arrow = decline
- Gray = no change or no data

---

## Audit Signal Patterns

Three creative audit triggers to show in the UI:

| Signal | Visual | Meaning |
|--------|--------|---------|
| **Single-Ad Risk** | Red badge/glow | Adgroup has only 1 active creative |
| **7-Day Rule** | Amber badge | CTR below benchmark for 7+ consecutive days |
| **Local Minima** | Orange badge | One ad has >80% delivery share |

Present as inline badges or row tints, not floating overlays.

---

## Competitor Integration Pattern

Competitors are INPUT, not part of the main data view:
- Collapsible panel or separate tab labeled "Competitor Library"
- Show competitor ad cards with: name, copy preview, channel badge
- "Use as Inspiration" button feeds the angle into your generation agent
- Never show competitor ads mixed with your own ads in the main view

---

## Export as RESULT Pattern

Export/preview actions are the OUTPUT of the generation workflow, not a sidebar:
- Generate -> Preview (SERP/Feed mockup) -> Approve/Reject -> Export
- Export formats: Google Ads Editor CSV, Meta Bulk CSV, Push to API, Screenshot for Client
- Show in a results section or as action buttons on approved creatives

---

## Proposal & Pitch Deck Narrative Structure

**When building marketing proposals, sales presentations, or budget recommendations, NEVER data-dump. Follow this narrative arc:**

### Mandatory Section Order

| # | Section | Purpose | Example Heading |
|---|---------|---------|-----------------|
| 1 | **Title / Cover** | Project name, stakeholders, date, confidentiality | "Projet 2X — Arvika Bike Rack" |
| 2 | **The Question** | Frame the client's core question | "La question posée par [client]" |
| 3 | **Baseline** | Current state with real numbers | "Point de départ — 2025" |
| 4 | **The Objective** | Target state, framed as ambitious but achievable | "L'objectif — Doubler les ventes" |
| 5 | **Methodology** | How the analysis was conducted | "Notre méthodologie" |
| 6 | **Findings / Constraints** | What we discovered (obstacles + opportunities) | "Constats & contraintes identifiés" |
| 7 | **Budget Structure** | Split: Investment (one-time) vs Recurring (each cycle) | "Structure du budget" |
| 8 | **Channel Allocation** | Detailed per-channel table with CPA, units, revenue | "Plan d'allocation par canal" |
| 9 | **Services & Operations** | Non-media costs (content, analytics, web) | "Services, création et opérations" |
| 10 | **ROI Scenarios** | Multiple scenarios: direct > excl. one-time > +LTV > +referral | "ROI projeté, LTV et effet de référence" |
| 11 | **Proof Points** | Real past data proving the thesis (e.g., influencer 10x ROI) | "La preuve par les chiffres" |
| 12 | **Comparison Table** | Side-by-side old vs new with delta column | "Comparatif 2025 vs 2026" |
| 13 | **The Ask** | Explicit budget number, broken into 2-3 buckets | "La demande au conseil" |
| 14 | **Next Steps** | 4-6 numbered concrete actions post-approval | "Prochaines étapes" |
| 15 | **People / Credits** | Real names, roles, company — not generic address | "Merci — [names + roles]" |

### Key Rules

- **Every section gets a lead subtitle** explaining WHY it matters (one line, italic, lighter color)
- **Budget MUST be split** into Investment (contributes beyond period) vs Dépenses récurrentes (consumed each cycle)
- **Call out key insights inline** in data sections: "Constat clé : X représente 28% du budget mais génère 53% des unités"
- **ROI presented as progressive scenarios** — not a single flat number
- **Name real people** in closing (presenter, client contact, stakeholder with roles)
- **Use middot separators** for punchy labels: "Vidéos de qualité · photos produit · copy"
