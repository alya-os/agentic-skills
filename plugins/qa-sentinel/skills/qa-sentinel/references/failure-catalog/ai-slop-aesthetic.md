# ai-slop-aesthetic

## Description
Interface visually screams "AI-generated". Generic layouts, generic palette, generic type, generic motion. Looks competent at a glance but lacks intentionality. Hurts brand differentiation and trust.

## Symptoms
- Glassmorphism applied to multiple elements
- Gradient text on dark backgrounds
- Identical 3-column equal card grids
- Hero stat layout with 3-4 metric chips
- Cyan-on-dark accent palette
- Inter or Roboto with no other typographic decisions
- Oversized rounded corners + heavy drop shadow on every card
- Sparkline graphs without axis labels or scale
- Marketing illustrations of floating geometric shapes
- "Modal as default" interaction pattern
- Dark hero with abstract mesh-gradient background
- Stock-photo people facing a laptop

## Root cause
Default outputs from generative tools (image, code, layout) trend to a global mean shaped by training data. Without intentional design choices, the output regresses to that mean.

## Independent verification
Two channels, in order:

1. **Deterministic pre-filter (fast, repeatable).** Run the slop-lint script on the built HTML/CSS:
   ```bash
   uv run scripts/slop_lint.py <file.html | dir | --url URL>
   ```
   It mechanically counts the fingerprints below and exits non-zero at >= 3 (`--json` for machine output). This is a **static/lab signal**, not a verdict: it catches the mechanical tells and gives you `rule -> where`. Works best on self-contained HTML/CSS (premium-web-design output, mirror rebuilds); for Tailwind/React lint the rendered page via `--url`. External `<link>` stylesheets are not fetched (the report says so).
2. **Judgment (the lens decides).** Capture a desktop and mobile screenshot and apply the AI-slop checklist in `references/lenses/designer.md`. The script flags candidates; the designer lens renders the verdict against the user's actual goal (per the metric-honesty doctrine, never present the script's static count as the finished measurement).

If three or more fingerprints are present (by either channel), the pattern is confirmed.

## Common fix attempts that DON'T work
- Swapping cyan for a different accent color (the structural slop remains)
- Adding more elements (more chips, more cards) (worsens it)
- Changing one font family (the layout grammar is the issue, not the type)
- Making it darker or more "premium" (often adds glassmorphism)

The fix that works: re-architect the layout grammar. Asymmetry, distinctive visual hooks, intentional typographic scale, restraint with motion.

## Likely lenses
designer, business-conversion (slop hurts conversion via trust loss)
