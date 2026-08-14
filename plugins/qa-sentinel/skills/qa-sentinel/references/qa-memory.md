# QA Memory — the living ledger of human overrides

This is the skill's learning organ. Every time a human overrules a verdict ("you passed this but X was broken", "you missed Y", "stop, there should be 299"), the lesson is captured HERE as a structured entry — never as another rule paragraph welded into SKILL.md. The v0.x era proved that prompt accretion does not transfer (16 scar-tissue commits in 11 days; the same failures recurred anyway). Retrieval at run start is what transfers.

## Two tiers

| Tier | File | Scope | Written by |
|------|------|-------|-----------|
| Project memory | `.claude/qa-memory.md` in the project under test | Project-specific lessons (this site's fragile surfaces, this client's standards) | `/qa learn` + automatic capture during runs |
| Skill memory | this file's SEED ENTRIES + `references/failure-catalog/` | Cross-project patterns | Promotion: when a project lesson generalizes, add a catalog entry (via autoskill//evolve) |

## Run-start protocol (mandatory)

1. Read the project's `.claude/qa-memory.md` (if present) IN FULL.
2. Skim the seed entries below + the failure-catalog README index.
3. For each acceptance criterion, ask: which past overrides are relevant here? Cite the entry ID in the verification plan ("per QM-2, gallery media gets a full-denominator HEAD sweep").

## Capture protocol (`/qa learn`, or automatic when a human contradicts a verdict)

Append to the project's `.claude/qa-memory.md`:

```markdown
## QM-<n> | <date> | <one-line title>
- **Human said**: <verbatim or close paraphrase of the correction>
- **We had reported**: <what the verdict claimed>
- **Root cause**: <why the verification missed it — wrong channel, narrow sample, no denominator, goal not modeled>
- **Rule going forward**: <one falsifiable check that would have caught it>
- **Generalize?**: yes → propose failure-catalog entry | no → project-specific
```

Never argue with an override. Record it, re-verify with the new rule, and thank the human input by never needing it twice.

## Seed entries (paid for in real incidents, May 2026)

## QM-1 | 2026-05-19 | Structural counts are not visual parity
- **Human said**: "i am unsatisfied... we're still far from the same site (4 columns, menu color)"
- **We had reported**: "✅ Visual reproduction of production layout" after 5 passes
- **Root cause**: verified markup shape, never compared rendered pixels at matching viewports
- **Rule going forward**: replication verdicts require screenshot pairs at 1440 AND 390 + computed-style checks on brand-critical elements (doctrine §2, §6)
- **Generalize?**: yes → `render-truth-drift`, `structural-grid-mismatch`

## QM-2 | 2026-05-24 | The denominator was 1,575 and nobody checked it
- **Human said**: (different agent found it) 154/299 products had broken gallery images, 5 days after QA passed
- **We had reported**: clean passes across 5 iterations
- **Root cause**: no criterion stated the full media surface; sampling never swept the catalog denominator
- **Rule going forward**: every countable surface in the criteria gets a full-denominator sweep (HEAD-check all media, render-check all N items) or an explicit NOT-CHECKED disclosure
- **Generalize?**: yes → narrow-sample family in catalog

## QM-3 | 2026-05-20 | A rule in the prompt did not make screenshots happen
- **Human said**: "find a solution you are not taking screenshots at all !?"
- **We had reported**: designer findings without screenshot evidence (one day AFTER the mandatory-screenshots rule landed)
- **Root cause**: rule lived in a wall of prose; no structural gate
- **Rule going forward**: a visual claim without an on-disk screenshot pair is INADMISSIBLE — the verdict section must show the evidence index before any visual criterion can read pass
- **Generalize?**: yes → `visual-evidence-missing`

## QM-4 | 2026-05-19 | The fix loop deleted 27 real products
- **Human said**: "stop, there should be 299 boats"
- **We had reported**: a dedup fix as progress (title-based dedup collapsed distinct stock units sharing a title)
- **Root cause**: no count-invariant guard on destructive fixes
- **Rule going forward**: any fix that deletes/merges/reduces data declares its count invariant BEFORE running ("299 before → 299 after expected") and halts the loop on violation
- **Generalize?**: yes → `inventory-dedup-by-wrong-key`

## QM-5 | 2026-05-20 | Stalling disguised as politeness
- **Human said**: "WHY is it still WAITING FOR NEXT TARGETS, PROCEED!?"
- **We had reported**: "Next targets (queued)" at iteration end
- **Root cause**: completion-seeking — presenting a plan instead of executing it
- **Rule going forward**: queued work IS the work; the only valid reasons to stop are a safety circuit or a staged irreversible-destructive action
- **Generalize?**: yes → `queued-as-deferral`

## QM-6 | 2026-05-18 | Category coverage missed
- **Human said**: "you missed several categories" (credit-card categories, on a services-guide site)
- **We had reported**: coverage complete
- **Root cause**: coverage computed over lens/process completion, not over the site's actual category tree
- **Rule going forward**: enumerate the real content tree (sitemap, taxonomy, data files) and diff coverage against it
- **Generalize?**: yes → coverage-denominator principle (goal-reconstruction step 3)

## QM-7 | 2026-07-06 | Partial-view diagnosis — concluding from a truncated read
- **Human said**: "something is off, Ghaith confirmed to me he is setup" (after I reported Ghaith was NOT on the morning-brief roster)
- **We had reported**: "Ghaith is missing slack_user_id" — from a `grep ... | head -5` that truncated ABOVE his `identities:` block (line 112 in his file vs line 24 in the shorter file I compared against). Same day, the deployed Slack agent confabulated a "session schedule evaporated" root cause for the same miss, from a symptom it could not actually inspect.
- **Root cause**: concluding from a partial/indirect view instead of the authoritative source, then stating it with confidence. Two flavors: truncated command output (mine) and narrating a cause for a layer you can't see (the agent's).
- **Rule going forward**: (1) when an authoritative query exists, RUN it — don't infer (`morning_brief.py --list` is the roster; never grep user files for membership). (2) Never truncate the read that backs a conclusion — `head -N` is for scanning, never for "X is absent". (3) When asked WHY at a layer you cannot inspect, label explanations as hypotheses and say what you can't see — never a confident fabricated cause, never a fix built on a guess.
- **Generalize?**: yes → this IS doctrine §1 (full denominator) applied to diagnosis; a verifier that concludes "absent/missing/none" from a partial view has produced an inadmissible finding.
