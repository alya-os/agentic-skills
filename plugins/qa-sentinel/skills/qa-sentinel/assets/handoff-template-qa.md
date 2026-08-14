# QA-Sentinel Failure Handoff

**Generated**: {{timestamp}}
**Run ID**: {{run_id}}
**Project**: {{project}}
**Target**: {{target}}

## Why this handoff

`/qa run` terminated without a passing verdict. Reason: **{{loop_terminated_reason}}**.

This handoff captures everything needed for the next session to resume without re-discovering the same problems.

## Verdict

- **Status**: {{verdict}}
- **Iterations run**: {{iteration_count}}
- **Coverage**: {{coverage_pct}}%
- **Lenses with fallback**: {{fallbacks_used}}
- **Lenses skipped**: {{lenses_skipped}}

## Findings (grouped by failure-catalog entry)

{{#findings_by_catalog}}
### {{catalog_entry}}

{{#findings}}
- **{{finding_id}}** [{{priority}}] caught by: {{caught_by}}
  - Expected: {{expected}}
  - Observed: {{observed}}
  - Evidence: {{evidence_paths}}
  {{#conflict}}
  - **Conflict**: {{causality}}
  {{/conflict}}
  {{#suggested_fix_class}}
  - Suggested fix class: {{suggested_fix_class}}
  {{/suggested_fix_class}}
{{/findings}}
{{/findings_by_catalog}}

## Dead ends (do not re-attempt without new information)

{{#dead_ends}}
- **{{test_id}}** with signature `{{observed_signature}}`: this exact failure has been seen before in run {{prior_run_id}}. Cross-run dedup tripped. Likely external-sync-revert or systemic.
{{/dead_ends}}

## Recommended next action

Based on the loop-termination reason:

{{#if loop_terminated_reason == "signature-dedup"}}
The build agent produced the same broken result two iterations in a row. **Do not** invoke the build agent again with the same prompt. Investigate the failing surface manually, identify the structural reason the fix isn't taking, then re-prompt with explicit guidance.
{{/if}}

{{#if loop_terminated_reason == "cross-run-dedup"}}
This exact failure has been seen before. Likely cause: external-sync-revert (a sync hook overwrites the change), or a systemic bug class not addressable by the build agent alone. Consult the prior run ledger and the catalog entry for the matching pattern.
{{/if}}

{{#if loop_terminated_reason == "confidence-decay"}}
Iterations stopped producing new observations. The build agent is stuck. Try a different agent, a different prompt, or a different fix strategy entirely.
{{/if}}

{{#if loop_terminated_reason == "cost-cap"}}
Hit the token-spend ceiling. Decide whether to allocate more budget or pivot strategy. The unfinished findings are listed above; prioritize P0 / P1 first.
{{/if}}

{{#if loop_terminated_reason == "human-stop"}}
You stopped the loop. Findings up to that point are listed above.
{{/if}}

## Artifact locations

- Run ledger: `.claude/qa-ledger/{{project}}/{{date}}.jsonl`
- Run evidence: `tmp/qa-sentinel/{{run_id}}/`
- Coverage matrix used: `.claude/qa-plan-{{matrix_timestamp}}.md`
- Skill inventory snapshot: `.claude/qa-skill-inventory.json`

## Resume command

```
/qa report   # to see the structured failure report again
/qa plan     # to rebuild the matrix with current state
/qa run      # to re-run from the current state
```
