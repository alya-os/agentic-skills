# return-code-vs-body-error

## Description
HTTP request returns status 200 (or process returns exit code 0). Build agent treats this as success. The response body actually contains an error: `{"status": "error", "message": "..."}` or `{"errors": [...]}`. Failure was reported in-band; agent ignored it.

## Symptoms
- Process exit code 0 but stderr or stdout contains "Error:", "Failed:", "Exception:"
- HTTP 200 with `"success": false` in JSON body
- HTTP 200 with non-empty `errors` array in JSON body
- HTTP 200 with HTML response containing "An error occurred"
- API returns success structure but missing the expected created-resource ID

## Root cause
Build agent assumes the transport layer is the source of truth for success. Many APIs (especially older WP / PHP-style endpoints) return 200 with embedded error fields.

## Independent verification
Always parse the response body. Check for known error indicators:
- Top-level `success`, `status`, `error`, `errors`, `ok` fields
- HTTP body shape that doesn't match the expected schema
- Non-empty error arrays even if a top-level success field is true
- Missing required fields in the expected response

For shell processes: capture stderr separately and grep for error indicators even on exit 0.

## Common fix attempts that DON'T work
- Increasing timeout (timeout is not the issue)
- Retrying (gets the same in-band error again)
- Trusting "if I got a response it must be working" (the response IS the error)

The fix that works: every API call inspects the body, not just the status code. Every shell call inspects stdout / stderr, not just the exit code.

## Likely lenses
developer
