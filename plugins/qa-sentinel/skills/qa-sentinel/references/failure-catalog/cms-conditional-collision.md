# cms-conditional-collision

> Built-in CMS conditional functions (WordPress: `is_home()`, `is_front_page()`, `is_singular()`, `is_woocommerce()`, `is_archive()`; Drupal hook contexts; Shopify template scopes) can return TRUE on a page that the developer mentally categorizes differently. The conditional fires correctly per its documentation; the developer's mental model is wrong. The result: meta tags, asset enqueues, body classes, and template branches resolve to the wrong path, and no error surfaces because the conditional did not fail — it just matched a context the developer did not anticipate.

## The two canonical sub-patterns

### Sub-pattern A: `is_home()` / `is_front_page()` ambiguity

WordPress separates "home" (the blog index) and "front page" (`page_on_front`). When `show_on_front=page` AND `page_for_posts` is set, the page assigned as the "Posts page" makes `is_home()` return TRUE. Any meta-emission, SEO, hero-render, or content-routing logic gated by `if (is_front_page() || is_home())` fires on **both** the homepage AND the assigned Posts page. If the Posts page is a custom inventory archive (e.g. `/bateaux/`, `/products/`, `/listings/`), it inherits the homepage's meta description, OG tags, hero image, and JSON-LD.

**Detection:** for every page where the SEO lens flags duplicate meta-description vs. the homepage, check `get_option('page_for_posts')`. If the duplicate page's ID matches, the cause is `is_home()` collision, not authoring laziness.

**Fix recipe:** the inventory/archive branch in the SEO emitter MUST be evaluated BEFORE the `is_front_page() || is_home()` branch. Use a custom query var (`bm_inventory_archive`) OR a URI-path regex as the gate, not the WP conditionals.

### Sub-pattern B: `is_woocommerce()` on non-store CPTs that share the `product` post type

When a custom data type is stored in the `product` post type for convenience (boats, vehicles, real-estate listings, courses, anything that needs WooCommerce taxonomies but is NOT a store product), `is_woocommerce()` returns TRUE on its singular template. Any `wp_dequeue_*` gated by `if (!is_woocommerce())` skips those pages, and the full WC asset stack (photoswipe, blocks, cart-fragments, WC blocks CSS, source-buster, js-cookie, jquery-blockui) loads on what the developer thinks is a clean custom page.

**Detection:** count `<link rel="stylesheet">` + `<script src=>` on a "custom CPT" singular page vs the documented theme spec. If the count exceeds the spec by 5+ and the extras are all `wc-*` / `woocommerce-*` / `photoswipe`, this pattern is the cause.

**Fix recipe:** introduce a tighter guard — e.g. `bm_is_boat()`, `bm_is_listing()` — that returns TRUE on the custom-typed posts and FALSE on real store products. Use `(!is_woocommerce() || $is_custom_typed)` instead of `!is_woocommerce()`.

## How to detect the broader pattern

Any time a feature gate uses ONLY a built-in CMS conditional, audit:

1. List every page the conditional matches per its docs.
2. List every page in the live sitemap.
3. Diff: pages where the developer believes the conditional is FALSE but it's TRUE = potential collision.
4. Render those pages and inspect the gated feature: did the wrong branch fire?

This pattern is responsible for at least one P0 finding per WordPress / WooCommerce migration the qa-sentinel has audited.

## How to verify the fix

After tightening the conditional:
- Re-fetch the colliding page(s) and confirm the previously-leaking branch is now silent.
- Re-fetch the page(s) the gate WAS meant to protect and confirm THEIR branch still fires.
- Do NOT trust a single-page recheck; the fix can break the adjacent context.

## Anti-pattern: "just check the URL"

`if (str_starts_with($_SERVER['REQUEST_URI'], '/special-page/'))` works but is fragile. WPML adds `/fr/`, mobile adds `/m/`, AMP adds `/amp/`, REST adds `/wp-json/wp/v2/…`. The robust gate uses both a query var AND a URI fallback, with the URI as the safety net for unflushed rewrite rules.

## Real-world example signatures

- `cms-conditional-collision:is_home-on-posts-page:dup-meta-desc=/bateaux/`
- `cms-conditional-collision:is_woocommerce-on-custom-cpt:asset-leak-count=22,leaked=wc-*+photoswipe`
- `cms-conditional-collision:is_singular-on-virtual-archive:wrong-template-fallback`
