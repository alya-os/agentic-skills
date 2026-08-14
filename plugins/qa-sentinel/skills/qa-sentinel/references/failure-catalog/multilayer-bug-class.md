# multilayer-bug-class

## Description
A bug class (encoding error, label drift, geographic pin, language leak) lives in multiple storage layers simultaneously. Build agent fixes one layer, verifies that layer, declares done. Other layers remain broken.

## Symptoms
- Same string visible-but-wrong in multiple places: heading, meta description, og:title, schema, breadcrumb, sitemap
- Encoding corruption fixed in `wp_posts` but persisting in `wp_postmeta` and `wp_options`
- Brand name updated in CMS but old name still in JSON-LD, alt text, image filenames
- City pin removed from h1 but present in 8 other surfaces (footer, tooltip, breadcrumb, schema, etc.)
- Translation updated in primary content but old version cached in i18n table

## Root cause
The same conceptual data is denormalized across multiple tables / files / surfaces, often for performance or rendering reasons. Each surface needs its own fix.

## Independent verification
When any single instance of a bug class is found, scan ALL known storage layers for the same pattern. Use `scripts/multilayer_scan.py` with the canonical string pattern. WordPress storage layers: `wp_posts.post_title`, `wp_posts.post_content`, `wp_posts.post_excerpt`, `wp_postmeta.meta_value` (multiple keys), `wp_options.option_value`, theme template files, mu-plugin files.

For non-WordPress: enumerate all data stores (DB, JSON files, env-injected strings, build-time replacements) and grep each.

## Common fix attempts that DON'T work
- Fixing one layer and verifying that layer (the canonical failure)
- Running a global find/replace without knowing all the layers (misses encoded variants)
- Trusting the CMS's "save once, propagate" claim

The fix that works: enumerate layers explicitly, apply the fix to each, verify each layer independently.

## Likely lenses
content-copy, developer, code-architect (this pattern is the common cause of `helper-fn-not-deployed` recurring across files)
