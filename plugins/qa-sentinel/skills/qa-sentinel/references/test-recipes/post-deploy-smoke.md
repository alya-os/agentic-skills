# Recipe: post-deploy-smoke

A fast-pass recipe to run after any deploy. Catches the most common immediate failures before deeper lenses run.

## Inputs

- `target_url`: the deployed URL or set of URLs
- `expected_signature`: a short string the deploy is supposed to add or change (used as ground truth for "did the change land")

## Steps

1. **HTTP availability** - fetch each URL with `curl -sS -o /dev/null -w "%{http_code}" <url>`. Expect 200 or 30x to a 200. Anything else is a finding.
2. **Cache-busting fetch** - fetch each URL with a unique cache-buster: `?_nc=$(date +%s%N)`. Compare the body to a non-busted fetch. If they differ, the cache served stale content (`cache-stale-verify`).
3. **Body inspection** - search the rendered HTML for `expected_signature`. If absent, the change did not land or did not deploy.
4. **Body error scan** - grep response body for `"status":"error"`, `"errors":[`, `Fatal error`, `Notice:`, `Warning:`. Any match is a finding (`return-code-vs-body-error`).
5. **Console + network capture** - open in `agent-browser`, capture console errors and network failures. Any console error of severity ≥ "error" or any 4xx/5xx network request is a finding.
6. **Mobile parity** - capture both desktop and mobile screenshots. Verify expected_signature is visible on both.

## Pass criteria

All six steps pass cleanly.

## Lenses this recipe feeds

- developer
- seo (cache + body inspection)
- product-manager (signature verification)
