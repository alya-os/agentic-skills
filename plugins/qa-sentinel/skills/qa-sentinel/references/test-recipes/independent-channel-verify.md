# Recipe: independent-channel-verify

The foundational verification primitive. Implements the "never trust the channel the build agent reported success on" rule.

## Inputs

- `claim`: the build agent's "I did X" statement
- `claim_channel`: the transport tier the build agent used (REST, wp-cli, SSH, SFTP, browser, MCP, etc.)
- `target`: the URL or resource the claim is about

## Steps

1. **Pick a different channel** from `claim_channel`:
   - If claim_channel is REST → verify via SFTP fetch + grep, OR via wp-cli, OR via direct DB query
   - If claim_channel is wp-cli → verify via REST + browser console, OR via SFTP
   - If claim_channel is SSH/SFTP → verify via REST + agent-browser
   - If claim_channel is browser → verify via curl + grep + log inspection
   - If claim_channel is MCP → verify via direct API call + body inspection
2. **Verify via that channel**. The exact action depends on the claim:
   - "I deployed file X" → SFTP fetch X, diff against local source
   - "I updated meta Y" → REST GET, parse, check Y
   - "I created form Z" → render the host page, verify form is rendered AND `is_active=1` in DB
   - "I cleared cache" → curl with cache-buster, then curl without; both must return new content
   - "I fixed bug W" → reproduce the original bug repro steps; verify it no longer reproduces
3. **Inspect the response body even on success status** (`return-code-vs-body-error`). 200 with `"status":"error"` is a failure.
4. **Capture evidence to disk**: the verification artifact (fetched file, parsed response, screenshot, log excerpt) goes to `tmp/qa-sentinel/<run-id>/` and the path becomes the finding's `evidence_path`.

## Pass criteria

- The independent channel confirms the claim
- The response body has no error indicators
- The artifact on disk matches the expected post-action state

## Lenses this recipe feeds

- developer (primary; this recipe IS the developer lens's verification rule)
- All other lenses use this principle whenever a build-agent claim must be checked
