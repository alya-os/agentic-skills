# post-deploy-404s

## Description
Deploy introduces new 404s. Routes deleted without redirects, drafts pushed live then unpublished, image paths changed without forwarding, sitemap updated without verifying every entry resolves.

## Symptoms
- Crawl after deploy finds 404s that didn't exist before
- Search Console reports a spike in 404 errors
- Internal links from primary navigation lead to dead pages
- Image src attributes point to renamed / removed files
- Old slugs return 404 instead of 301-redirecting to the new slug

## Root cause
Deploys that change URL structure or remove content without creating redirects or updating internal references.

## Independent verification
Run a crawl-diff: crawl the target before deploy (or use a known-good baseline crawl from the ledger), crawl after deploy, diff response codes per URL. Any URL that changed from 200/301 to 404/410 is a finding.

For internal links: enumerate every internal link href in the rendered HTML, fetch each, verify each resolves to 200.

## Common fix attempts that DON'T work
- Adding a redirect for the most-trafficked old URL only (long-tail still 404s)
- Adding a wildcard redirect that loops or misroutes
- Updating only the sitemap (does not fix internal links)

The fix that works: before any URL-changing deploy, generate the redirect map. After deploy, crawl and verify.

## Likely lenses
seo, developer
