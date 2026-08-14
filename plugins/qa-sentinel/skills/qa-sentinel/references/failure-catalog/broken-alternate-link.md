# broken-alternate-link

> A `<link rel="alternate">`, `<link rel="canonical">`, `<link rel="prev|next">`, or `<link rel="alternate" hreflang>` tag points to a URL that returns non-200 (403, 404, 500, redirect chain). The page itself loads fine; the broken pointer leaks into search results, RSS feeds, and crawler trust signals. Particularly painful for hreflang during staged multilingual rollouts where the EN/ES/etc. translations are not yet publishable but the alternate link advertises them anyway.

## How to detect

For every page in the sitemap:

1. Parse all `<link rel="alternate|canonical|prev|next" href="…">` from `<head>`.
2. For each `href`, fetch and check the final HTTP status (follow redirects, count hops).
3. Flag:
   - Final status not in {200, 304} → `broken-alternate-link:dead-target`
   - Redirect chain length > 2 → `broken-alternate-link:redirect-chain`
   - Cross-origin alternate where target host differs unexpectedly → `broken-alternate-link:host-drift`
   - Same `hreflang` value emitted on N pages with different `href` values (inconsistent alt mapping) → `broken-alternate-link:inconsistent-mapping`

## Sub-patterns

### Staged-rollout hreflang

A multilingual plugin (WPML, Polylang, GTranslate) advertises `hreflang="en"` pointing at `/en/` while `/en/` is still 403-protected by the host (staging-only access). Or the EN translation page is in draft state so the URL 404s while WPML still emits the alternate link.

**Fix:** strip the offending hreflang at `wp_head` priority 0 via output-buffer regex until the alternate URL returns 200. Re-enable per-language after launch.

### Canonical pointing to staging

The build agent copies a production canonical (`https://www.example.com/page/`) into staging meta. Staging returns the page fine, but `link rel="canonical"` advertises the production URL. Either (a) production has the same page and absorbs the SEO equity (acceptable), or (b) production 404s the URL (bad — crawler trust signal lost).

### Prev/next paginating off-the-end

A blog index emits `<link rel="next" href="/page/12/">` when only 11 pages exist. The next page 404s. WP core paginators usually handle this; custom paginators frequently don't.

## How to verify the fix

After patch:
1. Re-fetch each previously-broken alternate href and confirm 200.
2. Re-fetch the source page that emitted the alternate; confirm the broken pointer is gone (or now points to a 200).
3. If the fix is a `wp_head` filter or output buffer, verify it doesn't strip legitimate alternate links — diff before/after on a known-good page.

## Why this pattern is rarely caught by the developer

Browsers don't surface broken `<link rel="alternate">`. Lighthouse and PageSpeed don't crawl them. They only show up in:
- Google Search Console's "Coverage" report (post-indexing)
- Bing Webmaster Tools' "Crawl errors"
- Third-party crawlers (Screaming Frog, Sitebulb, Ahrefs)

Catching them pre-launch is qa-sentinel's job. Every replication / migration brief MUST include this check.

## Real-world example signatures

- `broken-alternate-link:hreflang-en-403:src=/bateaux/,target=/en/`
- `broken-alternate-link:canonical-to-prod-404:src=staging.x.com/page/,target=www.x.com/page/`
- `broken-alternate-link:prev-next-off-the-end:src=/blog/page/12/,total-pages=11`
