# cache-stale-verify

## Description
Build agent verifies a deploy by fetching the target immediately after deploying. The CDN, page cache, or browser cache returns the pre-deploy version. The agent reports success based on stale data.

## Symptoms
- Agent says "deployed and verified"; user later sees old content
- HTTP response Age header shows the resource was served from cache
- Re-fetching with a cache-busting query parameter returns different content
- Edge / CDN cache TTL is longer than the agent's verification window

## Root cause
Caches at multiple layers (browser, CDN, page-cache plugin, reverse proxy) return cached responses. Build agents typically don't bust caches before verifying.

## Independent verification
After any deploy, fetch with a random cache-buster: `curl -A "qa-sentinel" "<url>?_nc=$(date +%s%N)"`. Then fetch a second time without the buster, after the expected cache TTL. Both fetches must return the new content.

If `Age` header is present and non-zero, the response was cached. If `X-Cache: HIT` appears, same.

## Common fix attempts that DON'T work
- Adding a `?v=` parameter that doesn't actually vary (some caches strip query params)
- Calling a "purge cache" endpoint without verifying purge completion
- Trusting the CDN's "purged" response without re-fetch
- Verifying via a different domain (admin, staging) that doesn't use the production cache

The fix that works: verify with a unique cache-buster, then verify again after the documented TTL passes.

## Likely lenses
developer, seo
