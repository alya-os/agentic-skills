# Goal Reconstruction — derive the acceptance criteria before anything runs

The May 2026 catastrophe in one line: five QA passes delivered 31 generic-quality fixes and declared ✅ while the actual mission ("identical to production") was failing on 4-column grids, menu colors, and a broken QR reader. The verdict was rendered against quality dimensions instead of the goal. This phase is the fix, and it is MANDATORY before any verification work.

## Procedure

1. **Collect the mission sources** (priority order):
   1. The user's own words — this session and recent corrections. What the human says they want OUTRANKS every document.
   2. The build agent's handoff / completion claim (what exactly is being claimed done?)
   3. Spec/PRD/brief files; for replication briefs, the reference URL or extraction snapshot
   4. CLAUDE.md / README user journeys (see `workflow-discovery-guide.md`)
   5. Git diff since last verified state (what actually changed = what needs verification)

2. **Write the acceptance criteria** — 3-10 falsifiable statements that, if all true, mean the mission is accomplished. Each criterion must be *testable by observation*, not by reading code. Translate vague missions:
   - "identical to production" → "at 1440/390 viewports, page X renders visually equivalent to reference (screenshot pair); grid column counts match; nav/footer link counts match; every interactive feature (list them) works when triggered; full catalog (N items — state N) renders with intact media"
   - "the feature is done" → "user journey X completes end-to-end on the live target; edge case Y behaves as spec'd; no regressions on adjacent surface Z"
   - "deployed" → "new content serves through ALL cache layers; old content gone; no 404s on the changed routes"

3. **Quantify the surfaces.** State the denominator for everything countable: N pages, N products, N images, N locales, N features. A criterion without a denominator becomes a narrow-sample false pass (the 51.5%-broken-gallery lesson: nobody stated "all 1,575 gallery images load").

   For a **website** target the denominator includes the set of distinct **TEMPLATES**, not just the page the human named: home, listing/archive, single item, contact, 404, plus each active language. Templates are shared, so a defect found on one usually lives on several, and a defect on an unvisited template is invisible. Auditing the homepage and reporting sitewide is a narrow-sample false pass. Enumerate the templates from the nav you already discovered and name every one you did not visit in NOT CHECKED (QM-blog-template-unvisited: a homepage-only audit shipped 1.06:1 title contrast and a broken pagination control on `/blog/`).

4. **One clarifying question maximum.** If the mission is genuinely ambiguous, ask ONE question, then proceed with your best-reasoned criteria, stated explicitly so the human can correct them.

5. **Print the criteria list at the top of the run.** The verdict (see SKILL.md) is rendered against THIS list, criterion by criterion. Anything verified beyond the list is bonus; anything on the list left unverified is disclosed as NOT CHECKED — never silently dropped.

## Anti-patterns this phase exists to kill

- Verifying generic quality dimensions while the stated mission fails (the ✅-with-wrong-layout incident)
- Coverage math computed over process steps ("9/9 lenses ran") instead of over criteria and surfaces
- Accepting the build agent's framing of "done" instead of the human's framing of the goal
