---
name: idea-validation
version: 1.2.1
description: "Startup idea validation framework that opens with a fast 9-dimension serial-founder PRE-SCREEN (Problem, Audience, Wedge, Monetization, Moat, Portfolio-fit, Distribution, Energy-fit, Opportunity-cost) yielding a cheap Build / Sleep-on-it / Pass gate, then - only if it passes - runs 7 brutal adversarial stress-test prompts (VC reality check, angry customer simulation, pricing stress test, competitive teardown, founding team audit, 18-month survival sim, one-sentence pitch test). Produces a scored go/no-go validation report saved to disk, then converts the teardown into constructive alternate paths / pivots (not only a takedown). Use whenever a user wants to validate, stress-test, pressure-test, gut-check, sanity-check, kill-or-build, OR find a stronger version / pivot of a startup idea, business idea, product concept, side project, or new venture, even if they don't explicitly ask for 'validation'. Triggers on phrases like 'is this a good idea', 'should I build', 'thinking about starting', 'considering launching', 'tell me why this won't work', 'rip my idea apart', or any pre-commitment idea review for founders, PMs, or operators."
---

# Idea Validation

## Overview

This skill validates a startup idea in two stages. **Phase 0** is a fast, cheap 9-dimension serial-founder pre-screen that renders a three-way Build / Sleep-on-it / Pass gate BEFORE any expensive work - so a weak idea is caught in minutes, not after a full teardown. Only if Phase 0 passes (or the user overrides) does the skill run its **7 adversarial validation prompts**, each designed to surface a different failure mode. By the end, you will have a go/no-go recommendation with specific evidence from each stress test. Then - critically - it converts that teardown into **constructive alternate paths**: the strongest signal and every Caution/Fail become concrete pivots, so the founder leaves with a stronger version of the idea, not just a body count. The teardown earns the reframe; it is not the deliverable.

**Designed for:** Founders, PMs, and operators who want brutal honesty before committing resources.
**Future integration:** gstack by YCombinator (multi-agent validation pipeline).

> Phase 0 pre-screen adapted from Corey Haines / makerskills `business-brainstorm`.

---

## Workflow

### Step 0: Intake

Before running any prompts, collect the following from the user. If already provided, extract from context.

| Field | Variable | Example |
|-------|----------|---------|
| Core idea (1-2 sentences) | `IDEA` | "AI scheduling tool for independent tattoo artists" |
| Target customer (detailed) | `CUSTOMER` | "Solo tattoo artists, 5-15 years experience, urban markets, booked 2-3 weeks out" |
| Founding team background | `TEAM_BG` | "Ex-Shopify PM + full-stack dev, no tattoo industry experience" |
| Target market | `MARKET` | "Independent tattoo artists, US/Canada" |

Once collected, confirm with the user and proceed to **Phase 0**.

---

### Phase 0: The 9-Dimension Pre-Screen (cheap gate, runs FIRST)

Before spending the deep-dive teardown, run a fast serial-founder pre-screen. Score the
idea across 9 dimensions with a quick verdict each, then render a three-way gate. This is a
few minutes of work that decides whether the expensive 7-persona teardown is worth running.

**The gate model (read this first):** the gate verdict is driven by the **4 CORE dimensions**
(Problem, Audience, Monetization, Moat). The **5 strategic lenses** (Wedge, Distribution,
Portfolio-fit, Energy-fit, Opportunity-cost) are **ADVISORY** in Phase 0 - they inform the
one-line rationale and the biggest-unknown call, but none of them hard-vetoes the gate. (In
particular, Energy-fit is advisory here, not a veto. It becomes a documented modifier later,
in Step 8.) The lenses carry forward and become scored modifiers in the Step 8 final verdict.

Full dimension definitions and the "name it or mark UNKNOWN" discipline live in
`references/prescreen-dimensions.md` - read it before scoring. Also check for a
`portfolio.local.md` (see `references/portfolio.local.example.md`, which is an illustrative
EXAMPLE only and is never auto-loaded); if a real `portfolio.local.md` is present, load it to
ground Portfolio-fit and Opportunity-cost in the founder's real properties. If absent, mark
those two UNKNOWN rather than guessing - even inside an Index / ALYA repo.

**The discipline:** for each dimension, either name a concrete specific answer or mark it
UNKNOWN. Do NOT pad with plausible assumptions - a wall of confident guesses is exactly what
this gate exists to catch.

Produce a **Pre-Screen Scorecard**:

```
PRE-SCREEN: [IDEA SLUG]
=====================================
CORE (drives the gate)
1. Problem           [PASS / CAUTION / FAIL / UNKNOWN]  - real, acute, large enough
2. Audience          [PASS / CAUTION / FAIL / UNKNOWN]  - nameable, reachable, has budget
4. Monetization      [PASS / CAUTION / FAIL / UNKNOWN]  - value capture + unit economics
5. Moat              [PASS / CAUTION / FAIL / UNKNOWN]  - stops a copycat in 6 months
-------------------------------------
STRATEGIC LENSES (advisory in Phase 0; scored modifiers in Step 8)
3. Wedge             [PASS / CAUTION / FAIL / UNKNOWN]  - minimum viable offer into workflow
7. Distribution      [PASS / CAUTION / FAIL / UNKNOWN]  - how the first 100 hear about you
6. Portfolio fit     [PASS / CAUTION / FAIL / UNKNOWN]  - compounds vs fragments focus
8. Energy fit        [PASS / CAUTION / FAIL / UNKNOWN]  - energized vs chasing shiny
9. Opportunity cost  [PASS / CAUTION / FAIL / UNKNOWN]  - what high-leverage work it displaces
-------------------------------------
GATE: [BUILD / SLEEP ON IT / PASS]
-------------------------------------
ONE-LINE RATIONALE: ...
BIGGEST UNKNOWN TO RESOLVE: ...
```

**Gate logic** (judgment, not arithmetic; driven by the 4 CORE dimensions only - the 5
strategic lenses are advisory here and never hard-veto the gate. See the reference for the
full rule):
- **BUILD** - all 4 core dimensions (Problem, Audience, Monetization, Moat) are PASS (Problem
  and Audience must be PASS), with at most ~1 UNKNOWN or CAUTION among the four. Proceed to
  Step 1.
- **SLEEP ON IT** - promising shape but 2+ core dimensions are UNKNOWN or CAUTION. Recommend
  naming the unknowns first; offer the user the choice to override and run the teardown anyway.
- **PASS** - Problem or Audience is FAIL, or 3+ core dimensions are UNKNOWN/FAIL. Not worth the
  teardown as scoped. Say so plainly and name the one dimension that would have to change.

**Status semantics:** UNKNOWN is an honest gap (unscored, but it counts toward the "how many
unknowns" thresholds above); a core UNKNOWN is never silently treated as a PASS. CAUTION means
the answer exists but is soft or risky - two or more CAUTION/UNKNOWN core dimensions push the
gate down from BUILD to SLEEP ON IT.

**Only BUILD proceeds automatically to Step 1.** For SLEEP ON IT or PASS, STOP and present the
gate verdict, then WAIT for the user - ask one explicit yes/no question ("Override the [SLEEP ON
IT / PASS] gate and run the full teardown anyway? yes / no"). Do not run Step 1 until the user
answers yes. If the user overrides, the override AND the Phase-0 gate verdict it overrode are
both recorded in the saved report (see Step 10). Nothing in this pre-screen is thrown away - all
9 dimension verdicts carry forward into the Step 8 final scorecard as a preserved Phase-0 block.

---

### Step 1-7: Run Each Validation Prompt

Run each prompt **in character** - do not break the persona. See `references/prompts.md` for the full prompt text with placeholders.

After each prompt response, add a brief **Signal Check** (2-3 sentences):
- What is the strongest signal from this test?
- Pass / Caution / Fail for this dimension
- One thing the founder must answer before moving forward

**Prompts summary:**

| # | Name | Persona | Tests |
|---|------|---------|-------|
| 1 | Brutal Market Reality Check | Senior VC partner | Year-1 failure modes |
| 2 | Angry Customer Simulator | Deeply frustrated target customer | Emotional buy-in + credit card moment |
| 3 | Pricing Stress Test | Skeptical buyer in 3 sales scenarios | Willingness to pay |
| 4 | Existing Solution Destroyer | Rational incumbent defender | Day-1 switching cost |
| 5 | Founding Team Fit Audit | Honest advisor | Skills gaps + first hire |
| 6 | 18-Month Survival Simulation | Pessimistic CFO | Zero-fundraise path to $10K MRR |
| 7 | One-Sentence Test | Exhausted founder at 11pm | Pitch clarity |
| 8 | Constructive Reframe | Pragmatic turnaround operator | Build-forward alternate paths (run in Step 9) |

---

### Step 8: Final Verdict

After all 7 prompts, produce a **Validation Scorecard**. It has three parts: (a) a preserved
**Phase-0 block** carrying forward all 9 Phase-0 dimension verdicts verbatim (so a fatal
Phase-0 Problem or Audience FAIL remains a first-class artifact even after an override); (b)
the 7 persona dimensions scored from the teardown; and (c) the 5 strategic lenses, updated
with anything the teardown revealed - so no dimension surfaced in Phase 0 is lost:

```
VALIDATION SCORECARD: [IDEA SLUG]
=====================================
PHASE-0 CARRIED FORWARD (verbatim from the pre-screen - not re-scored here)
 GATE VERDICT: [BUILD / SLEEP ON IT / PASS]   (+ OVERRIDDEN: yes/no, by user)
 CORE:   Problem [.]  Audience [.]  Monetization [.]  Moat [.]
 LENSES: Wedge [.]  Distribution [.]  Portfolio fit [.]  Energy fit [.]  Opportunity cost [.]
   ([.] = PASS / CAUTION / FAIL / UNKNOWN as scored in Phase 0)
=====================================
CORE (7-persona teardown)
 1. Market Reality Check      [PASS / CAUTION / FAIL]   (Prompt 1)
 2. Customer Emotional Buy-in [PASS / CAUTION / FAIL]   (Prompt 2)
 3. Pricing Viability         [PASS / CAUTION / FAIL]   (Prompt 3)
 4. Competitive Moat          [PASS / CAUTION / FAIL]   (Prompt 4)
 5. Team Fit                  [PASS / CAUTION / FAIL]   (Prompt 5)
 6. Survival Path             [PASS / CAUTION / FAIL]   (Prompt 6)
 7. Pitch Clarity             [PASS / CAUTION / FAIL]   (Prompt 7)
-------------------------------------
SCORE: X/7  (drives the GO / GO WITH CONDITIONS / NO-GO verdict)
-------------------------------------
STRATEGIC LENSES (carried from Phase 0, updated by the teardown - modifiers only)
 8. Wedge                     [PASS / CAUTION / FAIL / UNKNOWN]  - minimum viable entry point
 9. Portfolio fit             [PASS / CAUTION / FAIL / UNKNOWN]  - compounds vs fragments focus
10. Energy fit                [PASS / CAUTION / FAIL / UNKNOWN]  - founder durability over years
11. Opportunity cost          [PASS / CAUTION / FAIL / UNKNOWN]  - what building this starves
-------------------------------------
VERDICT: [GO / GO WITH CONDITIONS / NO-GO]
-------------------------------------
TOP 3 RISKS:
1. ...
2. ...
3. ...

TOP CONDITIONS (if GO WITH CONDITIONS):
1. ...
2. ...
```

The X/7 core score sets the base verdict (see Scoring Reference in `references/prompts.md`).
The strategic lenses are judgment modifiers: a FAIL on Portfolio fit, Energy fit, or
Opportunity cost can pull a marginal GO down to GO WITH CONDITIONS even when the core 7
pass, because an idea that fragments focus, drains the founder, or starves a higher-leverage
bet is not worth building on core merits alone. (CAUTION on a lens is a soft flag noted in
the risks/conditions; UNKNOWN on a lens is carried as an open question, never scored as a
pass.)

**Distribution is NOT a separate modifier here.** The Phase-0 Distribution score was a quick
pre-screen only; it is SUPERSEDED by Prompt 6's go-to-market evidence (customer count, ARPU,
CAC, channel), which is already scored in the CORE "Survival Path" row. Do not add Distribution
back as an independent lens modifier - that would double-count go-to-market. Its Phase-0 verdict
still appears verbatim in the preserved Phase-0 block above for continuity.

---

### Step 9 - Constructive Paths (the build-forward half)

A teardown that ends at the scorecard has failed. Run **PROMPT 8 (Constructive Reframe)** to turn the analysis into forward motion. Produce:

- **THE STRONGEST SIGNAL:** name the single most visceral signal (often Prompt 2's credit-card moment) and what it reveals about where the real value lives.
- **2-3 ALTERNATE PATHS** that route AROUND the Caution/Fail dimensions - each with: the reframe in one line, the wedge / first customer, the pricing-or-positioning that dodges the fatal objection from Prompts 3-4, and why it's stronger.
- **THE STRONGER VERSION:** one paragraph - the pivot the founder should actually build.
- **FIRST EXPERIMENT:** what must be true for the reframe to win, and the one test to run this week.

Even a NO-GO gets this: name the nearest viable pivot. The only idea that gets no constructive path is one where PROMPT 8 cannot find a single route around the fatal objections - and that itself is the finding.

---

### Step 10: Save Results

Save the full session (the Phase-0 pre-screen scorecard AND its gate verdict, all 7 prompts + the Step 8 scorecard + constructive paths) as a Markdown file the founder can keep, share, or revisit. If a SLEEP ON IT or PASS gate was overridden to run the teardown, the report MUST record both the original Phase-0 gate verdict and the fact that the user overrode it (who and why, if stated). Default to the current working directory so the report survives reboots. `/tmp` is ephemeral and a real validation deserves a durable home:

```
./idea-validation-[idea-slug].md
```

Where `idea-slug` is the idea name lowercased with hyphens (e.g., `tattoo-scheduler`).

If the user has indicated a project or notes directory (e.g., `~/founder-notes/`, an active client folder), save there instead. Use the Write tool and confirm the final path to the user so they know exactly where to find it.

---

## Key Rules

- **Phase 0 gates the deep dive.** Run the 9-dimension pre-screen first. The gate is driven by the 4 CORE dimensions (Problem, Audience, Monetization, Moat); the 5 strategic lenses (including Energy-fit) are advisory in Phase 0 and never hard-veto the gate. Only a BUILD gate proceeds automatically to the teardown; SLEEP ON IT and PASS require an explicit user override - STOP, ask one yes/no question, and wait for the answer before running Step 1. Record any override (and the verdict it overrode) in the saved report. Do not burn the expensive 7-persona teardown on an under-formed idea.
- **Name it or mark UNKNOWN** in Phase 0. Never pad a dimension with a plausible assumption to make the idea look readier than it is - honest gaps are the point.
- **Never break persona** during prompts 1-7. The adversarial framing is intentional.
- **Don't soften responses.** A FAIL is a FAIL. Sugar-coating defeats the purpose.
- **Do use** specific market details in every response - generic startup advice is useless here.
- **Prompt 2 is the most skipped** - push the user not to skip it. The discomfort is the signal.
- **Prompt 6 must include real numbers**: customer count, ARPU, CAC estimate, channel.
- **The teardown is not the deliverable.** Prompts 1-7 earn the right to Step 9. A validation is only complete when it hands back constructive alternate paths, including for NO-GO verdicts (the nearest viable pivot).

## Reference Files

- `references/prescreen-dimensions.md` - The 9 Phase-0 dimensions, the "name it or mark UNKNOWN" discipline, and the Build / Sleep-on-it / Pass gate logic (pre-screen adapted from Corey Haines / makerskills `business-brainstorm`)
- `references/portfolio.local.example.md` - Convention + template for the optional user-provided `portfolio.local.md` that grounds Portfolio-fit and Opportunity-cost in real properties
- `references/prompts.md` - Full prompt text with `[PLACEHOLDER]` variables for each of the 7 prompts
