# Idea Validation Prompts

Seven adversarial prompts for stress-testing a startup idea. Replace `[PLACEHOLDERS]` with intake data before running.

---

## PROMPT 1 - The Brutal Market Reality Check

**Persona:** Senior VC partner. Has seen 10,000 pitches. Funded 12.

```
Act as a senior VC partner who has seen 10,000 pitches and funded 12.
My startup idea is: [IDEA].

Give me the 5 most likely reasons this fails in year 1.
Be specific to this market - not generic startup advice.

Then, for each failure mode, tell me exactly what would need to be true
for that failure mode to NOT happen.
```

**What to look for:** If the founder cannot answer the "what would need to be true" part for even 3 of 5 failure modes - the idea has no viable path. Kill it.

**Signal Check criteria:**
- PASS: Founder has credible answers to 4-5 of the "what would need to be true" conditions
- CAUTION: Credible answers for 2-3 conditions
- FAIL: Credible answers for 0-1 conditions

---

## PROMPT 2 - The Angry Customer Simulator

**Persona:** Deeply frustrated version of the target customer.

```
You are a deeply frustrated version of my target customer.

My target customer is: [CUSTOMER - describe in detail: role, experience level,
geography, current tools, biggest daily frustrations].

You have tried every solution in this market and nothing works.
I am going to pitch you my idea: [IDEA].

React emotionally first - as this frustrated customer would.
Then tell me the ONE thing you would need to see before handing over your credit card.
```

**What to look for:** The emotional reaction surfaces whether the problem is a genuine hair-on-fire problem or a vitamin. The credit card condition is the minimum viable proof of value.

**Signal Check criteria:**
- PASS: Emotional reaction is visceral; credit card condition is specific and achievable
- CAUTION: Mild frustration; credit card condition is vague
- FAIL: Indifferent response; "I don't really need this"

---

## PROMPT 3 - The Pricing Stress Test

**Persona:** Skeptical buyer across 3 different pricing models.

```
My startup [IDEA] is targeting [CUSTOMER].

Give me 3 pricing models that could work for this business
(e.g., per-seat SaaS, usage-based, one-time fee, freemium, etc.).

For each model:
1. State the model and price point
2. Simulate a 60-second sales conversation where I pitch that price to a skeptical customer
3. Show exactly where the customer pushes back
4. Show what kills the deal
```

**What to look for:** Identify which model produces the least resistance and the most achievable objection handling. If all 3 models hit the same objection, that is a structural pricing problem.

**Signal Check criteria:**
- PASS: At least one model has clear path to close; objections are handleable
- CAUTION: All models generate price resistance but objections are addressable
- FAIL: All models generate fatal objections (budget, wrong buyer, no urgency)

---

## PROMPT 4 - The Existing Solution Destroyer

**Persona:** Rational defender of the status quo.

```
My startup idea is: [IDEA].

List every solution my target customer is using RIGHT NOW to solve this problem.
Include: paid software, spreadsheets, manual workarounds, doing nothing, paying an assistant.

For each existing solution, tell me exactly why a rational person would
choose THAT over my product on day one.

Do not give me spin. Be the rational devil's advocate.
```

**What to look for:** "There's no competition" is always wrong. The real question is whether the switching cost is surmountable. If the best existing solution is "just use a spreadsheet" and it genuinely works - you have a distribution problem, not a product problem.

**Signal Check criteria:**
- PASS: Existing solutions have clear, specific weaknesses the product addresses on day one
- CAUTION: Existing solutions are "good enough" but have pain points the product can exploit
- FAIL: Existing solutions outperform the product on day one for most customers

---

## PROMPT 5 - The Founding Team Fit Audit

**Persona:** Brutally honest advisor who has seen founders fail because of who they were, not what they built.

```
My co-founder team background: [TEAM_BG - describe all founders: work history,
domain expertise, technical ability, network, weaknesses].

Our startup idea is [IDEA] targeting [MARKET].

Give me an honest breakdown:
1. What is this team uniquely positioned to WIN at in this market?
2. What critical skills are completely missing from this team?
3. What type of person do we need to hire or partner with in the first 90 days
   to not fail because of a team gap?
```

**What to look for:** Founder-market fit matters more than most people admit. A great team in the wrong market loses to a good team in the right one. The missing hire in 90 days is often a distribution or domain expert.

**Signal Check criteria:**
- PASS: Team has clear unfair advantage; missing skills are hirable/partnerable
- CAUTION: Team has relevant skills but missing a critical domain piece
- FAIL: Team has no domain advantage and no clear path to acquiring it

---

## PROMPT 6 - The 18-Month Survival Simulation

**Persona:** Pessimistic CFO who has seen zero-fundraise companies die at month 14.

```
My startup is: [IDEA].

Assume we raise $0 and need to reach $10,000/month in revenue within 18 months.

Build a month-by-month breakdown (group into phases if needed) showing:
- What we need to DO each phase
- Key milestones that must be hit
- What kills us if we miss them
- Specific customer numbers required
- Revenue per customer assumption
- Primary acquisition channel and why

Do not be optimistic. Show the path where things go mostly right
but nothing goes perfectly.
```

**What to look for:** The $10K/month constraint forces real numbers. If the math only works at enterprise scale you cannot reach in 18 months bootstrapped - that is a funding dependency, not a business. That is not automatically fatal but must be acknowledged.

**Signal Check criteria:**
- PASS: Credible path to $10K MRR in 18 months with achievable customer/channel assumptions
- CAUTION: Path exists but requires things going unusually well in 2+ areas
- FAIL: Math does not work without fundraising or depends on unrealistic assumptions

---

## PROMPT 7 - The One-Sentence Test

**Persona:** Exhausted founder at 11pm, emailing a VC from their phone.

*Run this AFTER the other 6 prompts. The prior context informs it.*

```
Based on everything we have discussed about [IDEA], write 5 one-sentence
descriptions of this startup.

Each sentence must include:
- Who it is for (specific customer)
- What specific pain it eliminates
- Why this is the moment to build it (why now)

Write each one as something a tired, skeptical founder would send to a VC at 11pm.
Not polished. Not buzzword-heavy. True.
```

**What to look for:** If none of the 5 sentences are compelling - the positioning is broken. If one is clearly better than the others - that is the pitch. The "why now" is the most commonly missing piece.

**Signal Check criteria:**
- PASS: At least 2 sentences are genuinely compelling; "why now" is present and credible
- CAUTION: Sentences are clear but "why now" is weak or generic
- FAIL: All sentences feel generic or the customer/pain is too vague to be real

---

## PROMPT 8 - The Constructive Reframe (build-forward)

**Persona:** A pragmatic operator who has turned around weak ideas. Treats the 7 teardowns as raw material, not a verdict.

*Run this AFTER the scorecard. It uses all prior context. This is the build-forward half - the teardown earns the right to it.*

```
Based on everything we discussed about [IDEA] - especially the STRONGEST signal
(often the Prompt 2 credit-card moment) and every CAUTION/FAIL dimension - do NOT
re-litigate the weaknesses. Build forward instead:

1. Name the single strongest signal in the whole test and what it reveals about
   where the real value actually is.
2. Give me 2-3 ALTERNATE PATHS that route AROUND the risks. For each:
   - the reframe in one line
   - the wedge / first customer
   - the pricing-or-positioning that dodges the fatal objection from Prompts 3-4
   - why it is stronger than the original framing
3. Write "the stronger version of this idea" in one paragraph - the pivot I should
   actually build.
4. State what must be TRUE for the reframe to win, and the single first experiment
   I should run this week to test it.

Be concrete and specific to this market - no generic pivot advice.
```

**What to look for:** At least one path must genuinely dodge the fatal objections from Prompts 3-4. If none can, the teardown stands and that is the honest finding - say so plainly rather than inventing a hopeful pivot. Even then, name the nearest adjacent problem worth solving.

**Signal Check criteria:**
- PASS: >=1 alternate path clears the Prompt 3-4 objections and is concretely testable this week
- CAUTION: paths exist but each still carries one unresolved fatal objection
- FAIL: no route around the fatal objections - the idea, as scoped, is genuinely dead

---

## Scoring Reference

| Score | Verdict |
|-------|---------|
| 6-7 PASS | GO - move to customer discovery |
| 4-5 PASS | GO WITH CONDITIONS - list the conditions |
| 0-3 PASS | NO-GO - unless conditions are addressed first |

A single FAIL in prompts 1, 2, or 6 should trigger a serious conversation regardless of overall score.
