# Failure pattern: inline-script-interleave-broken

## What it looks like

A rebuild correctly preserves production's inline `<script>` blocks (avoiding `inline-script-stripped`). But the rebuild also wants to enqueue them via `wp_enqueue_script()` or its equivalent, so it concatenates all the inline blocks into a single bundled file (e.g., `inline-config.js`) and enqueues it before the external `<script src="...">` tags.

The bundle loads. The HTML structure is correct. The CSS renders. But the carousel still doesn't init, the lazy-load still doesn't fire, the language switcher still doesn't open. Console shows: "TypeError: Cannot read properties of undefined (reading 'init')" or similar.

The cause: production's body emits scripts in a specific **interleaved order**. Inline block A defines `globalVars`. External script B reads `globalVars` and registers a callback. Inline block C (further down the body) calls the callback with arguments. Inline block D defines `tinySlider` init data. External script E reads it and starts the carousel.

When all the inline blocks are bundled into one upfront load, blocks A and D fire BEFORE external scripts B and E register their handlers. The carousel init data is set, but nothing's listening yet. Blocks C runs but the callback isn't registered. Result: silent JS deadlock.

## Why HTML-only lenses miss it

`view-source` of the rebuild looks fine. Inline scripts are present. External scripts are present. The order of script tags in the markup matches production's order at the top level. The breakage is at execution-time — the relative ordering between inline `<script>` BLOCK B and external `<script src=C>` is what production interleaves, and the rebuild has flattened.

A point-in-time screenshot may catch it (blank hero, empty brand circles, blank promo backgrounds) but only if the lens looks at those specific elements. Headless screenshots with insufficient `--virtual-time-budget` will mask the failure as "JS hasn't run yet".

## How to detect

1. **Diff the script emission order** between production and rebuild. Walk through every `<script>` in `<head>` and `<body>` in order and label each as INLINE-{seq} or EXTERNAL-{filename}. The labels and their interleaving should match. Specifically:

   ```bash
   python3 -c "
   from bs4 import BeautifulSoup
   for f in ['production.html', 'rebuild.html']:
       html = open(f).read()
       soup = BeautifulSoup(html, 'lxml')
       for s in soup.find_all('script'):
           src = s.get('src')
           print(f'{f[:4]:5} {\"EXT\" if src else \"INL\"} {src or s.string[:60] if s.string else \"\"}')"
   ```

   Look for sequences where production has INLINE→EXT→INLINE→EXT but rebuild has INLINE→INLINE→INLINE→EXT→EXT→EXT (all bundled).

2. **Open browser console on the rebuild**. Errors like `Cannot read properties of undefined`, `X.init is not a function`, `TypeError in callback`, or `expected handler not registered` strongly indicate execution-order mismatch.

3. **Check for visible non-functional widgets**: hero carousels stuck on slide 1, blank lazy-load placeholders, dropdowns that open visually but don't populate, language switchers that submit forms but don't redirect. Each is a likely interleaving failure.

## Common root causes

- Agent extracts inline scripts to "bundle them properly" via `wp_enqueue_script()` — a well-meaning attempt at WP idiom that violates the script's load-order assumptions.
- Agent treats inline scripts as independent units instead of as a step-by-step setup script for the external bundles.
- Build pipeline minifies/concatenates inline scripts into a single asset early without checking that production's runtime needs them interleaved.

## The validated fix

In WordPress, use **`wp_add_inline_script($handle, $body, 'before'|'after')`** to attach each inline block to the SPECIFIC external script it interleaves around:

```php
wp_register_script('convertus-main', '.../main.convertus.min.js', ['jquery']);
wp_add_inline_script('convertus-main', $inline_block_setting_globals, 'before');
wp_add_inline_script('convertus-main', $inline_block_calling_init, 'after');
wp_enqueue_script('convertus-main');
```

Each `wp_add_inline_script` call preserves position relative to its handle's enqueue order. The browser sees the exact `<script>BLOCK</script><script src=X></script><script>AFTER</script>` interleaving production has.

The static-bundle alternative (preserve production's body byte-for-byte as a static HTML file): production order is preserved by construction.

## Sister patterns

- `inline-script-stripped` — the noise filter ate the inline blocks entirely
- `rebuild-namespace-invention` — broader rebuild drift; this is the JS sibling
- `helper-fn-not-deployed` — analogous failure for PHP function definitions

## Severity

P1. Page renders, CSS works, but interactivity (carousels, lazy-loads, dropdowns, menus) is silently broken. Same blast radius as `inline-script-stripped` but with a more confusing diagnosis path because inline scripts ARE present in the rebuild — just in the wrong execution slot.

## Lens question to ask

> "Walk through every `<script>` tag in production and rebuild in order. Do the INLINE/EXTERNAL sequences match? If the rebuild bundled inline blocks into one early load, what was production's intended interleaving order — and is anything depending on it visibly broken (carousel blank, lazy-load not firing, dropdown not populating)?"
