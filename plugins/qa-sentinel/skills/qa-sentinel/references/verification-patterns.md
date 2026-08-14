# Verification Patterns

The "never trust the build agent" rules. Every lens applies these.

## Rule 1: Independent channel

Always pick a transport tier different from the channel the build agent reported success on.

| Build agent used | QA verifies via |
|---|---|
| REST API | SFTP fetch + grep, OR wp-cli, OR direct DB |
| wp-cli | REST + browser console |
| SSH / SFTP | REST + agent-browser |
| Browser screenshot | curl + grep + log inspection + DB |
| MCP tool | direct API call + body inspection |
| Local dev render | deployed-target render |

Rationale: every channel has its own failure modes. Same-channel verification finds same-channel-only successes. Cross-channel verification finds the truth.

## Rule 2: Body always

Never trust status codes alone. Always parse the response body. HTTP 200 with `{"status": "error"}` is failure (`return-code-vs-body-error`). Process exit 0 with stderr containing "Failed" is failure.

## Rule 3: Cache busting

After any deploy, fetch with a unique cache-buster (`?_nc=$(date +%s%N)`). If the cache-busted response differs from the non-busted response, the cache lied. Re-verify after the documented TTL.

## Rule 4: Mobile required

Visual findings require BOTH desktop and mobile evidence. Desktop-only verification misses `mobile-only-regression`.

## Rule 5: Multi-layer scan when bug-class found

When any single instance of a bug pattern is found (encoding error, label drift, broken link), scan all known storage layers for the same pattern. Use `scripts/multilayer_scan.py`. This catches `multilayer-bug-class` before it hits production.

## Rule 6: Evidence on disk

Every finding requires `evidence_path` pointing to a real artifact. Self-attestation without artifacts is rejected. The artifact (screenshot, log excerpt, fetched HTML, diff image, JSON dump) is what makes the finding reproducible.

## Rule 7: Reproducibility tagging

Every finding has a `reproducibility` field: `deterministic`, `flaky`, or `unverified`. Findings tagged `flaky` or `unverified` cannot exceed `minor` severity until they're upgraded to `deterministic` via re-run.

## Rule 8: Cross-run dedup

If the same `(test_id, observed_signature)` appears in any prior ledger run for this project, escalate immediately. We've seen this exact failure before. The build agent should not be trusted to fix it autonomously.

## Rule 9: Helper deployed

When a build claims new code, fetch the deployed bundle / file via the channel different from the deploy channel. Grep for the symbol. Local working ≠ deployed working.

## Rule 10: Verify form is_active

When a build claims a form / component / item is created, verify on the public-facing surface AND verify the active flag is true server-side. Default-inactive is a documented failure class.

## Rule 11: No silent loop runaway

The loop's safety circuits (convergence, repeat-finding, destructive-fix count-invariant, human pulse, budget sense) are mandatory and never silently disabled. See `loop-protocol.md`.
