# /qa loop — the Ralph loop that actually runs

Sustained find→fix→verify iteration for big pieces of work. The v0.x shell driver (`qa-ralph.sh`, fresh `claude -p` subprocesses, JSON state files) was never executed once in production; what DID work was the orchestrated in-session loop with fresh-context subagents. This protocol formalizes that working pattern.

## Architecture

The MAIN session is the loop driver (it holds the goal model and the ledger). Each iteration uses FRESH-CONTEXT background agents so drift cannot accumulate — the Ralph property, on primitives that exist:

```
ITERATION N:
  1. FIND   — spawn background verifier agent(s) (fresh context): the acceptance
              criteria + qa-memory excerpts + doctrine pointers + "falsify done".
              They return findings with evidence paths. (Parallel, ownership-split
              by surface when multiple.)
  2. TRIAGE — orchestrator dedupes vs the run ledger (concept-level, not string-
              level), prioritizes P0→P2, plans fixes. Destructive-fix gate here.
  3. FIX    — spawn fixer agent(s) with ownership-locked file sets, each prompt
              carrying the finding, its evidence, and the count invariants.
  4. VERIFY — spawn a fresh verifier (NEVER the fixer, NEVER reuse the finder's
              context) on the fixed surfaces via an independent channel.
  5. LEDGER — append iteration results to `tmp/qa-sentinel/<run-id>/ledger.md`
              (open/fixed/stalled per finding, evidence paths, tokens-ish estimate).
  6. LOOP   — continue unless a circuit fires.
```

State lives in `tmp/qa-sentinel/<run-id>/ledger.md` (human-readable markdown, not JSON machinery): criteria status table + findings list + iteration log. If the session dies, a new session resumes from the ledger.

## Safety circuits (judgment rules, enforced by the orchestrator)

1. **Convergence** — no NEW findings and no state change on open findings for 2 consecutive iterations → stop, report stalled set.
2. **Repeat-finding** — the same finding (same root cause, judged at concept level) reopens after being fixed twice → stop touching it, escalate with both fix attempts documented.
3. **Destructive-fix gate** — any fix that deletes, merges, or reduces data MUST declare its count invariant before running ("299 products before → 299 after") and verify it immediately after. Violation = halt the entire loop, report, wait for human. (QM-4: a dedup "fix" deleted 27 real boats.)
4. **Human pulse** — every 5 iterations OR on any P0 verdict change, print a one-line status (open/fixed/stalled counts, criteria progress, rough spend). Do NOT stop to wait for a reply — continue unless told otherwise. The pulse is a kill-switch opportunity, not a permission request.
5. **Budget sense** — if cumulative spend is clearly disproportionate to remaining criteria value (judgment, not a chars/4 formula), stop and report what's left vs what it costs.

## Per-finding stall

After each fix attempt, judge honestly: did the observation change? If two attempts produce identical observations, or no new fix vector exists, mark `stalled` with both attempts documented and move on. Stalled ≠ failed-silently: stalled findings appear in the verdict's NOT-RESOLVED section.

## Autonomy stance

The loop is invoked to act. Queued work IS the work — execute it this iteration, not "next pass". Stopping to ask is valid ONLY for: (a) staged irreversible destructive actions (circuit 3), (b) genuinely ambiguous intent with no convergence-favoring default. "Continue?" is never a valid question — continue until a circuit fires. (QM-5.)

**Continuous improvement without human intervention (QM-qa-loop-continuous).** `/qa loop` does not stop the moment defects hit zero. Separate two convergence bars:
- **Correctness convergence** — no defects against the acceptance criteria. Reaching it does NOT end the loop; it *promotes* it.
- **Improvement convergence** — after correctness holds, the loop keeps iterating autonomously to *raise the bar*: each round a fresh-context agent asks "what is the next most valuable improvement to this surface?" (polish, responsive edge, a11y, perf, copy, consistency with siblings), proposes it, applies it, and verifies it on the independent channel — same find→fix→verify→ledger machinery, now sourcing its own work-list instead of a defect list.

The loop only ends on a real circuit: **budget sense** (circuit 5 — improvement value clearly below cost), **improvement convergence** (2 iterations produce no improvement worth the spend), a repeat/stall, a staged destructive action, or an explicit human stop. Never idle-stop with "defects are zero, awaiting instructions" — that is the exact hand-back the human invoked the loop to avoid. The human pulse (circuit 4) still prints every 5 iterations as a kill-switch opportunity; it is never a permission request.

## Exit

On ANY exit (complete, converged, circuit-fired): write the final verdict (SKILL.md format) + invoke the `handoff` skill with `assets/handoff-template-qa.md` when findings remain open. The next session resumes from the ledger, not from scratch.
