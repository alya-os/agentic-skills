# catch-all-taxonomy-fallback

> A migration / seed script bulk-imported N entries into a custom taxonomy but used a single fallback term for everything, instead of classifying per-entry. The taxonomy has 10 registered terms; 9 have count=0 and 1 has count=N. Every filter UI on the site that depends on that taxonomy returns empty results for the 9 unused terms. The site looks complete from the admin (entries exist, taxonomy exists) but the front-end is broken in ways that don't surface until a user clicks a category filter.

## How to detect

1. List every custom taxonomy registered for content post types (skip `category` and `post_tag` unless those are the audit subject).
2. For each taxonomy, query term-count distribution: `SELECT t.slug, tt.count FROM wp_term_taxonomy tt JOIN wp_terms t ON tt.term_id=t.term_id WHERE tt.taxonomy='<name>'`.
3. Flag taxonomies where ONE term has count ≥ 80% of total assigned entries AND ≥3 other registered terms have count = 0.
4. Cross-check: pick the most-used term, click through the front-end filter for it (`?cat=<term>` or `/category/<term>/`), confirm it returns the bulk count. Click a count=0 term's filter and confirm it returns empty.
5. If the empty results are user-facing AND no UI suppresses the empty term's link (e.g. it still appears in the category nav or filter sidebar), file the finding.

## Sub-patterns

### Single-tag bulk seed

Migration script's classifier was a stub: `return ['default-cat']`. Surface symptom: front-end filter dropdown lists 10 categories but 9 of them say "0 boats" / "0 listings" / "Aucun résultat".

### Lossy taxonomy mapping

Source CMS had a richer taxonomy than the target's term registry. Classifier ran but unrecognized source terms all fell through to a `'other'` / `'misc'` / `'plaisance'` bucket. Surface symptom: same as above, plus the catch-all term is non-zero and weirdly large.

### Brand/manufacturer field empty

The brand taxonomy is registered, has 10 terms, but every post has the brand taxonomy assignment EMPTY. The brand was stored in the post title (`"2026 BENETEAU Flyer 10"`) but the seed script never extracted it. Filter UI shows the 10 brand checkboxes but every one returns zero.

## How to verify the fix

After running a re-categorization mu-plugin or one-shot script:
1. Re-query term-count distribution. Spread should now show ≥3 non-zero terms, none ≥70% of total.
2. Front-end click-through: hit each filter URL, confirm card count matches the term count. Account for pagination — if a term has count=88 but the archive paginates at 24/page, the first-page card count IS expected to be 24, not 88.
3. Term `count` field is denormalized and OFTEN STALE after `wp_set_object_terms()`. Run `wp_update_term_count_now()` after the writes before reading counts back. See `cache-stale-verify.md`.
4. WP Engine page cache will serve the OLD filter-result page. Verify with cache-bust query string AND `Cache-Control: no-cache` header (see `cache-stale-verify.md` / SKILL.md "cache-aware verification" rule).

## Anti-pattern: trust admin term counts pre-flush

Editing terms in `wp-admin` shows the cached `term_taxonomy.count`. After a bulk `wp_set_object_terms`, that count is stale until `wp_update_term_count_now()` fires OR an admin page reload triggers WP's lazy count update. A QA pass that reads counts directly via REST or via `get_terms()` before flushing returns counts that don't match the just-written term assignments. Always flush before reading.

## Real-world example signatures

- `catch-all-taxonomy-fallback:bulk-seed:tax=bm_boat_category,used=1/10,catch-all-pct=100`
- `catch-all-taxonomy-fallback:lossy-mapping:tax=product_cat,catch-all=other,catch-all-pct=82`
- `catch-all-taxonomy-fallback:empty-brand:tax=bm_boat_brand,assignments=0/299`
