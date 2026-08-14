# Test recipe: production-HTML-first rebuild verification

## When to invoke this recipe

The brief says one of:
- "rebuild this site on a new theme / new server / new framework"
- "match production visually" / "pixel-by-pixel" / "faithful reproduction"
- "port this WordPress site to v2 of the theme"
- "lift-and-shift" or "migrate without touching content"

The verified pattern this recipe checks for was validated end-to-end on a WordPress + WooCommerce + WPML site (~20 preview pages deployed). The reviewer accepted this pattern only after rejecting an earlier attempt that shipped copied HTML and CSS with PHP bolted on behind it.

## The 8-step rebuild pipeline (what to expect)

### 1. Snapshot production HTML

Fetch production HTML byte-for-byte via headless Chrome `--dump-dom` (CloudFront, Akamai, and most CDN bot-detection layers block `curl` directly). Save as `parity-reference/raw-production.html`.

```bash
/usr/bin/google-chrome --headless --disable-gpu --no-sandbox \
    --user-agent="Mozilla/5.0 ..." --virtual-time-budget=15000 \
    --dump-dom https://www.example.com/ > raw-production.html
```

### 2. Localize CSS / JS / IMG / FONTS

Walk the HTML's `<link rel=stylesheet>`, `<script src>`, `<img src>`, `srcset`, inline `style="url(...)"`, and `<style>` block `url(...)` refs. Download each asset to `assets/{css,js,img,fonts}/<flat-filename>__<hash>.<ext>` and rewrite paths to be relative.

Result: an `index.html` that opens locally and renders identically to production, offline.

### 3. Extract inline `<style>` blocks → overrides.css

Production HTML often has inline `<style>` blocks in `<head>` that contain critical CSS rules NOT in the linked stylesheets. Example: `.header--desktop .navigation>.menu-item>a { text-transform: none; color: var(--color-primary); }` — without this rule the nav renders UPPERCASE while production renders Title-case.

Pull every non-`parity-overrides` inline `<style>` body into `assets/css/overrides.css` and enqueue it AFTER the linked stylesheets so its rules win.

### 4. Localize external CDN URLs (post-pass)

After step 2 there will still be external URLs surviving in the bundle — CDN-hosted brand SVGs, hero images, font files behind Cloudflare's `/cdn-cgi/image/<transforms>/` rewriter. Walk the bundle a second time with a regex matching `cdn-convertus.com`, `*-cdn-static.com`, `wp-content/themes/<vendor-theme>/assets/`, etc. Strip Cloudflare's `/cdn-cgi/image/<params>/` prefix so different-sized variants of the same asset collapse to one local file. Refetch + rewrite.

### 5. Noise filter (analytics only, NEVER inline scripts)

Strip ONLY `<script src="...">` tags whose URL matches a known analytics domain (`googletagmanager.com`, `nr-data.net`, `hotjar.com`, `optimizely`). **Never decompose inline `<script>` blocks** — they hold runtime config (`var globalVars`, `var loadFontsArr`, `var CMSettings`, `var translatedStrings`, `dataLayer.push(...)`) that production JS reads. See `failure-catalog/inline-script-stripped.md`.

### 6. Server-side back-fill (WordPress example)

Build a side-by-side theme that emits the production HTML byte-for-byte. Same class names. Same attribute order. Same Font Awesome icon classes. Same `convertus-data-id` attributes. PHP interpolates ONLY the dynamic values:

```php
<a href="tel:<?php echo esc_attr($phone); ?>" class="header__info-single--phone">
    <?php echo esc_html($phone); ?>
</a>
```

NOT:

```php
<a href="tel:<?php echo $phone; ?>" class="bm-topbar__phone">
    <span class="bm-topbar__phone-number"><?php echo $phone; ?></span>
</a>
```

See `failure-catalog/rebuild-namespace-invention.md` for why the second form is a P0 bug.

### 7. Editability via companion mu-plugin

Register CPTs + Customizer fields via a COMPANION mu-plugin (not the theme's `functions.php`) so the editable surface loads regardless of which theme is active. This decouples editability from theme activation — the dealership / editor can edit content immediately while the new theme is still being validated, without risking inventory/WC breakage.

Hook `save_post_<cpt>` + `customize_save_after` to a server-side rebuilder that splices the editable `<section>` blocks of the static bundle in-place via PHP `include` + output buffer.

### 8. Generic `/preview` route

Mu-plugin matches `/<slug>2` URLs on `init` priority 0 and serves `/wp-content/uploads/<slug>2/index.html` with `X-Robots-Tag: noindex, nofollow`. Easy iteration without touching the live theme; reversible at any moment.

---

## Variant: Production-HTML-as-PHP-template (validated 2026-05-22)

> **Category**: WordPress QA / Interface-Replicating QA — high-fidelity reproduction & assessment.
>
> This variant supersedes the static-bundle approach above when the user requirement is **"same site as production, on clean URLs, no `/preview` routes, no `readfile()` of HTML files"**. Validated end-to-end on a dealership site rebuild (18 page templates).

### When to pick this variant over the bundle approach

| Signal | Pick variant |
|---|---|
| User says "no preview URL, clean URLs only" | yes |
| User says "DONT render html files" or "no readfile" | yes |
| Each canonical URL should look distinct (home vs about vs contact) | yes — each gets its own `.php` template |
| Static-bundle preview is acceptable for demo | no — use Steps 1-8 above |

### The recipe (5 steps, end-to-end)

#### V1. Snapshot full production HTML per canonical URL

For each canonical URL the rebuild must serve, capture the ENTIRE `<html>...</html>` via headless Chrome `--dump-dom`. Not just `<main>`. The `<head>` contains critical inline `<style>` blocks (e.g., `.navigation>a { text-transform: none }`) that linked stylesheets DON'T have. The `<header>`/`<nav>`/`<footer>` markup must be preserved verbatim.

```bash
/usr/bin/chromium --headless --disable-gpu --no-sandbox \
    --virtual-time-budget=15000 \
    --dump-dom "https://www.example.com/about/" \
    > parity-reference-about/index.html
```

#### V2. Embed as a per-URL PHP template

Each canonical URL gets its own `page-templates/<slug>.php` containing production's full HTML verbatim. **NO `get_header()` / `get_footer()` wrappers** — production HTML already has its own `<header>`, `<nav>`, `<footer>`. Only these PHP injections are allowed inside the production HTML body:

| Injection | Where | Why |
|---|---|---|
| `<?php wp_head(); ?>` | immediately after `<head ...>` | WP plugin scripts (Yoast, WPML, etc.) |
| `<?php wp_footer(); ?>` | immediately before `</body>` | admin bar + plugin scripts |
| `<?php echo esc_attr(implode(" ", get_body_class())); ?>` | mixed into existing `<body class="...">` attr | WP body classes |

```php
<?php /* Template Name: About */ ?>
<!DOCTYPE html>
<html lang="en">
<head>
<?php wp_head(); ?>
<!-- production's exact <head> contents, untouched -->
...
</head>
<body class="page page-template <?php echo esc_attr(implode(' ', get_body_class())); ?>">
<!-- production's exact <header>, <main>, <footer>, scripts -->
...
<?php wp_footer(); ?>
</body>
</html>
```

#### V3. Asset URL strategy — pick ONE, be consistent

- **Option A: Production-CDN passthrough** — keep production CSS/JS/image URLs as-is (`https://www.example.com/wp-content/...`, `https://*-cdn-static.com/...`). Production serves the assets directly. Faster to ship, no local asset copy.
- **Option B: Localize** — download all assets to `theme/assets/{css,js,img,fonts}/` and rewrite paths via `<?= THEME_URI ?>/assets/X`. Slower to ship, but bundle is self-contained and survives if production goes down.

**Never mix.** Mixing A + B leads to 404 chaos (some assets resolve, others 404, hard to debug). Decide upfront.

#### V4. Internal-link rewrite (production → staging)

Production page links like `https://www.example.com/about/` should resolve to `/about/` so navigating the rebuild stays on the rebuild. Use a regex with **negative lookahead** to SKIP `/wp-content/`, `/app/`, `/cdn-cgi/` paths (those are assets, not pages):

```python
# Rewrite page links, skip asset paths
rewrite_re = re.compile(
    r'https://www\.example\.com(?!/(?:wp-content|app|cdn-cgi))(/[^"\'\s]*)'
)
html = rewrite_re.sub(r'\1', html)
```

#### V5. WP page seeding (idempotent)

Seed one WP page per canonical slug + assign the template via `_wp_page_template` post-meta:

```php
$pages = [
    'about'   => ['template' => 'page-templates/about.php',   'title' => 'About'],
    'contact' => ['template' => 'page-templates/contact.php', 'title' => 'Contact'],
    // ...
];
foreach ($pages as $slug => $cfg) {
    $existing = get_page_by_path($slug, OBJECT, 'page');
    $id = $existing ? $existing->ID : wp_insert_post([
        'post_name' => $slug, 'post_title' => $cfg['title'],
        'post_type' => 'page', 'post_status' => 'publish',
    ]);
    update_post_meta($id, '_wp_page_template', $cfg['template']);
}
update_option('show_on_front', 'page');
update_option('page_on_front', get_page_by_path('home')->ID);
```

### Why this variant beats parallel reimplementations

- **Zero CSS-class invention.** Production CSS targets production HTML — they're a matched pair. Inventing `app-home-categories` requires writing parallel CSS that re-invents production styling. Production CSS reused verbatim = zero parallel maintenance.
- **All JS interactivity works** because production's exact `<script>` emission ORDER and inline configs (TinySlider, lazy-load, Vue, jQuery init) are preserved.
- **Reversible**: removing the variant is `rm page-templates/<slug>.php` + remove template assignment. No surgery.
- **Per-page divergence allowed**: home looks like home, contact looks like contact, about looks like about — each PHP file is independent.

### Anti-patterns (CALL THESE OUT IF SEEN)

These were tried during the validated session and explicitly REJECTED by the user. The lens should refuse the rebuild if any of these appears:

- ❌ Wrapping production HTML with `get_header()` / `get_footer()` — emits the rebuild theme's header instead of production's → visual mismatch. See `failure-catalog/wp-wrapper-over-production-html.md`.
- ❌ Extracting just `<main>` — loses head + header + footer + critical inline `<style>` blocks.
- ❌ Adding CSS overrides for production class names (`.slider_widget-*`, `.button_block_widget-*`, `.about_widget-*`) to "fix" production styling — production CSS+JS handles rendering correctly; if it appears broken, the root cause is asset URL, missing JS init, or stale cache — **not the CSS rules themselves**. See `failure-catalog/css-override-fights-production-js-init.md`.
- ❌ Stripping inline `<script>` tags — loses runtime config globals → cascading `TypeError "undefined"`. See `failure-catalog/inline-script-stripped.md`.
- ❌ Concatenating multiple inline scripts into one bundle — loses INLINE+EXTERNAL interleave order → carousels / runtime stacks fail to init. See `failure-catalog/inline-script-interleave-broken.md`.
- ❌ Regenerating production HTML from a build pipeline instead of capturing as-is — pipeline introduces bugs (misclassified CSS-in-JS folder, unrewritten `/app/` paths, missing assets).
- ❌ Using wp-admin Theme File Editor on WP Engine — silently rejects saves; always SFTP + verify md5.
- ❌ Mixing localized + production-CDN asset URLs — pick A or B, never both.

### Verification checklist (additions for this variant)

In addition to the 7-step checklist below, run:

8. **Per-template existence**: `wp post list --post_type=page --fields=ID,post_name,meta_value` should show each canonical slug assigned to a DISTINCT `_wp_page_template` value. If all pages share one template, the variant was abandoned mid-way.
9. **No-wrapper check**: `grep -E '(get_header|get_footer)\s*\(' page-templates/*.php` should return ZERO. Any hit means production HTML got wrapped — see `failure-catalog/wp-wrapper-over-production-html.md`.
10. **No-override check**: `grep -E '\.(slider_widget|button_block_widget|about_widget)' theme/assets/css/overrides.css` (and any custom CSS) should return ZERO. Any hit means custom CSS is fighting production CSS — see `failure-catalog/css-override-fights-production-js-init.md`.
11. **Asset-URL consistency**: `grep -c 'src="https://www\.<prod-domain>' page-templates/*.php` vs `grep -c 'src="<?= THEME_URI ?>' page-templates/*.php` — exactly ONE of these counts should be zero (CDN-only OR localized-only, never mixed).

### Lens questions added by this variant

> 7. Did the rebuild capture FULL `<html>...</html>` byte-for-byte, or just `<main>`?
> 8. Does each canonical URL serve its OWN per-page template (`_wp_page_template`), or are they all sharing one?
> 9. Are there ZERO `get_header()` / `get_footer()` calls inside production-HTML templates?
> 10. Are there ZERO CSS overrides for production CMS class names (`.slider_widget-*`, `.button_block_widget-*`, etc.)?
> 11. Are asset URLs all-CDN OR all-localized — never mixed?

---

## Verification checklist (what the lens runs)

Run all of these against any rebuild claiming "matches production":

1. **Class-name byte-diff**: Dump outer-HTML of header, nav, footer, hero from both production and rebuild. The `class="..."` strings should be identical. Diff with `diff -u` and reject any meaningful divergence.

2. **Inline-script count**: Count inline `<script>` blocks in production HTML vs rebuild HTML. A drop ≥3 indicates the noise filter ate them. See `failure-catalog/inline-script-stripped.md`.

3. **Script interleaving check**: Sequence-label every `<script>` tag (INLINE/EXTERNAL) in order, both sides. Compare sequences. Mismatch → see `failure-catalog/inline-script-interleave-broken.md`.

4. **Browser console check**: Open the rebuild in a real browser (Playwright). Count JS errors and PageErrors. Production = 0 functional errors. Rebuild = 0 functional errors. Any `X is not defined`, `Cannot read properties of undefined`, or `TypeError` is a finding.

5. **Visual diff**: Headless screenshot at 1440×900 and 390×844 (mobile). Side-by-side with production extraction. Flag layout drift, image absence, broken carousels, empty brand grids, blank promo cards.

6. **Editability test**: Edit one field via WP Customizer or CPT post. Re-fetch the preview URL. The new value should appear without external CLI rebuild. If not, the rebuild-on-save hook is missing.

7. **External URL audit**: `grep -E "https?://[a-z0-9.-]*(cdn-|tadvantage-|akamai|cloudfront)"` in the served bundle. Production-side CDN URLs should be ZERO after step 4. Any remaining external is a failure to localize.

## Gotchas catalog

Each of these was hit on the validated session — document so future rebuilds avoid them:

- **`get_theme_mod($key, $default)` runs `$default` through `sprintf()`**. URL defaults with `%20` encoded spaces blow up `Unknown format specifier "?"`. Fix: pass empty string as default, fall back via `?:` operator. See `failure-catalog/customizer-default-sprintf-blowup.md` (TODO).

- **`safe_name()` hash accumulation**. Naïve `<basename>__<hash>.<ext>` filename generation, when fed an already-hashed input, produces `<basename>__<hash1>__<hash2>__...__<hash25>.<ext>` → 256+ char filename → OS errno 36 "File name too long". Fix: strip pre-existing `__<8hex>` suffixes before adding a new hash.

- **WPE varnish/page cache is sticky**. `wp cache flush` only clears object cache, not the HTTP page cache layer. Use `WpeCommon::purge_varnish_cache_all()` via PHP, OR set a `wordpress_logged_in_*` cookie to bypass varnish, OR detect cache hits via response header `x-cache: HIT` vs `MISS`.

- **`get_template_part()` double-load on active-theme + companion-loader**. When BOTH the old active theme AND the new theme-as-companion have a same-named template part (e.g., `template-parts/footer-info.php`), `get_template_part()` loads from the active theme AND the companion filter also includes the new one → rendered twice. Fix: use direct `include` (`defined('NEW_THEME_DIR') ... include "$dir/template-parts/footer-info.php"`) instead of `get_template_part()` in the new theme's `header.php` / `footer.php`.

- **`wp_remote_get()` from inside `php-exec` deadlocks on WPE worker pool**. The php-exec holds one PHP-FPM worker; the loopback HTTP request needs another; if WPE has 1-2 workers configured the request hangs 10+ seconds. Symptom: cURL error 28 timeout when actual page render completes in <100ms. Test via external `curl` from a different machine to confirm.

## Sister recipes

- `visual-baseline-diff` — point-in-time screenshot comparison; pairs well with this recipe but doesn't catch drift over iterations
- `design-vs-deployed-diff` — comp vs live diff; orthogonal to production-HTML rebuild
- `multilayer-bug-class-scan` — broader cross-pattern audit; this recipe is one specific case

## Lens questions this recipe enables

> 1. Did the rebuild reuse production's class names byte-for-byte, or did it invent a new namespace? (`rebuild-namespace-invention`)
> 2. Are inline `<script>` configs preserved or stripped? (`inline-script-stripped`)
> 3. Is the script INTERLEAVING order preserved or flattened? (`inline-script-interleave-broken`)
> 4. Is editability via WP entities (Customizer + CPTs) hooked to auto-rebuild on save?
> 5. After step 4 of the pipeline, are there any remaining external CDN URLs in the served bundle?
> 6. Does the rebuild's preview URL render identically to production at desktop + mobile, with zero browser console errors?
