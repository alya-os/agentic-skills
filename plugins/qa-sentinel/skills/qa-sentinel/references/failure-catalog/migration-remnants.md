# migration-remnants

## Description
Migration from one tooling, framework, or pattern to another left orphaned artifacts behind. Old CSS selectors, dead JavaScript bundles, dangling references in templates, deprecated API endpoints, sitemap entries pointing to removed routes.

## Symptoms
- Selectors in CSS for elements that no longer exist (e.g., `.old-search-widget`)
- Script tags loading bundles for removed features
- 404s in the network panel for resources the app no longer needs
- Comments / TODOs referencing the previous tooling
- Database tables / rows from the old system not cleaned up
- Sitemap or RSS feed lists URLs that 404
- Two ways to do the same thing in code; only one is current

## Root cause
Migration shipped the new path but did not clean up the old. Often "we'll clean up later" that never happens.

## Independent verification
Crawl the deployed target with `seo-audit`. Catch 404s on assets and pages. Grep deployed CSS / JS bundles for selectors / symbols that match the old tooling. Cross-reference git history for the migration commit and what it removed (or didn't).

For database remnants: query for orphaned rows in tables marked deprecated.

## Common fix attempts that DON'T work
- Moving the cleanup to a separate ticket "for later" (later never comes)
- Pretending the orphans don't matter (they accumulate weight, security surface, confusion)

The fix that works: every migration includes the cleanup as a hard requirement before "done". Ledger across runs catches accumulated remnants.

## Likely lenses
developer, seo, code-architect
