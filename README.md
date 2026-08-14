# Agentic Skills

**Production Agent Skills for Claude Code, open-sourced by ALYA Labs.** Seven skills we run on real work every day: adversarial verification, deep research, interface design, brand systems, idea validation, and the two meta-skills that keep an agent improving and remembering.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-8-6d28d9.svg)](#the-skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin%20marketplace-c2410c.svg)](https://claude.com/claude-code)

---

## What this is

An **Agent Skill** is a modular folder of instructions, references, and scripts that Claude discovers and loads on demand, giving the model domain expertise it does not have out of the box.

This library is built and maintained by ALYA Labs, the AI research division of Index, a marketing technology company operating since 2010. Every skill here is one we run in production on client work. None of it is a demo.

There is no shortage of Claude Code skill collections. Most are prompt packs written by people who do not run anything on them. These were extracted from a live agentic operation, hardened against documented failure modes, then generalized.

---

## Install

```bash
# In Claude Code, add this marketplace:
/plugin marketplace add alya-os/agentic-skills

# Then install any skill:
/plugin install qa-sentinel
/plugin install deepdive
```

Each skill is self-contained. Install one, or install them all.

---

## The skills

### Verify and research

| Skill | What it does |
|-------|--------------|
| **[qa-sentinel](./plugins/qa-sentinel)** | A goal-anchored adversarial verifier for any work an agent declares done. Reconstructs the real acceptance criteria first, then tries to falsify the completion claim across nine expert lenses, with a living memory of past human overrides and a documented failure catalog. |
| **[deepdive](./plugins/deepdive)** | A recursive context-processing engine that prevents quality degradation (context rot) on complex, multi-source tasks. Decomposes inputs, processes them in focused sub-calls, cross-references the outputs, then audits for concept completeness. Includes a PRD-writing mode. |

### Make

| Skill | What it does |
|-------|--------------|
| **[premium-web-design](./plugins/premium-web-design)** | Create, refine, audit, or prototype frontend interfaces without the generic AI-slop look. 26 reference docs covering spatial design, typography, colour and contrast, motion, behavioural UX psychology, and a pre-launch audit gate. |
| **[brand-voice-generator](./plugins/brand-voice-generator)** | Generates reusable tone-of-voice and brand-system files (brand.json, tone-of-voice.md) that keep every downstream skill and agent on-brand. |
| **[idea-validation](./plugins/idea-validation)** | A fast 9-dimension pre-screen gate, then seven adversarial stress tests (VC reality check, angry customer, pricing, competitive teardown, team audit, 18-month survival, one-sentence pitch), then a conversion of the teardown into concrete pivots. |

### Stay in flow

| Skill | What it does |
|-------|--------------|
| **[autoskill](./plugins/autoskill)** | Watches your session for corrections and preferences, then proposes targeted edits to your own skills. Your agent gets better at your way of working. Edits stay local to your workspace. |
| **[handoff](./plugins/handoff)** | Captures session state (goal, progress, decisions, dead ends, changed files, next action) into a structured document so the next session resumes without context loss. |
| **[primer](./plugins/primer)** | Primes a fresh session with real project context: reads CLAUDE.md, README, entry points and config, then reports purpose, structure, key files, dependencies and configuration. The cheapest useful thing you can run at session start. |

---

## Why these are different

**1. They are proven, not proposed.** Each skill carries the scars of real production use: qa-sentinel's failure catalog is a list of specific ways agents have declared victory on broken work, written down after each one cost us real time.

**2. They compound.** `autoskill` learns from your corrections and rewrites your skills. `qa-sentinel` refuses to accept its own "done" without evidence. `handoff` preserves context across sessions. The longer you run the stack, the more it knows about how you work.

**3. They are measured.** ALYA Labs builds tools to measure AI, not just run it. `qa-sentinel` exists because "the agent said it finished" is not evidence. The same instinct drives our commercial research into GAIO(TM) (Generative Engine Optimization): measuring how, and how often, AI models actually cite a brand.

---

## What we did not publish, and why

This library was cut down from a larger internal marketplace. Three skills that would have padded the count were deliberately left out:

| Skill | Why it stayed private |
|-------|----------------------|
| `copywriting-mastery` | Built on a paid commercial training product we have no right to relicense. |
| `humanizer` | Derived from an excellent MIT upstream plus a share-alike pattern source. Use the original; we would rather contribute to it than repackage it. |
| `skill-creator` | Anthropic already publishes this one under Apache-2.0. Get it from them. |

We would rather ship seven skills we fully own than eleven with an asterisk. If a skill here is useful to you, you can use it commercially, fork it, and ship it without wondering whose material you inherited.

---

## From ALYA Labs

**ALYA Labs** is the AI research division of Index, a marketing technology company. We build agentic systems for marketing, sales, content, and analytics, and we open-source the horizontal pieces the whole community can use.

Our research focus is **GEO (Generative Engine Optimization)** and **GAIO(TM)**: measuring and improving brand visibility inside large language models, the way SEO measures visibility inside search engines.

- **[github.com/alya-os](https://github.com/alya-os)**: open-source releases from ALYA Labs
- **[Index](https://www.indexwebmarketing.com)**: the company these skills were forged in

---

## FAQ

**Are the skills free to use commercially?**  
Yes. MIT. The ALYA, ALYA Labs, GAIO(TM), and Index names and marks are not covered by that licence: see [TRADEMARKS.md](./TRADEMARKS.md).

**Did you write all of this yourself?**  
All seven skills are ALYA Labs' work. Where one builds on someone else's, it is credited in [NOTICE.md](./NOTICE.md) and inline. `idea-validation` adapts its pre-screen gate from Corey Haines' MIT-licensed makerskills.

**How is this different from other skill collections?**  
These run in production at a real company every day, they are hardened against documented failure modes, and two of them (`autoskill`, `qa-sentinel`) improve the rest of your setup over time rather than sitting static.

---

## License

[MIT](./LICENSE) (c) 2026 Index Web Marketing Inc. (ALYA Labs). Third-party credits in [NOTICE.md](./NOTICE.md), trademark notice in [TRADEMARKS.md](./TRADEMARKS.md).
