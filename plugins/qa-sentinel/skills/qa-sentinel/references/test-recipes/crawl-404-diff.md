# Recipe: crawl-404-diff

Catches `post-deploy-404s` and `migration-remnants`. Compares response codes for the full URL set before and after a change.

## Inputs

- `target_site`: the site to crawl
- `baseline_crawl`: path to a prior known-good crawl summary (or fetch the most recent green from the ledger)

## Steps

1. If `seo-audit` is available, run a Screaming Frog crawl with size capped per the skill's pre-crawl sizing logic. Save the response_codes_all.csv and internal_all.csv outputs to `tmp/qa-sentinel/<run-id>/`.
2. If `seo-audit` is unavailable, fetch the sitemap.xml, extract URLs, fetch each with `curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n"` to a manifest file.
3. Diff the response-code manifest against the baseline. Output:
   - URLs that went from 200/301 to 404/410 → critical findings (`post-deploy-404s`)
   - URLs that went from 200 to 301 → check if redirect target is correct
   - New URLs in the post-deploy crawl absent from baseline → log but not a finding
4. For each 404, attempt to resolve as the most likely renamed URL. If a likely match exists, the finding includes "suggested redirect" guidance.

## Pass criteria

- Zero new 404s/410s
- Zero broken internal links
- Sitemap entries all resolve to 200/301-to-200

## Lenses this recipe feeds

- seo
- developer
