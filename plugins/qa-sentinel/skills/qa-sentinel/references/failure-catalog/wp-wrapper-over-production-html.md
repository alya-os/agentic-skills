# Failure pattern: wp-wrapper-over-production-html

> **Category**: WordPress QA / Interface-Replicating QA — high-fidelity reproduction & assessment.

## What it looks like

The brief is "rebuild this WordPress site to match production, page-for-page". The agent captures the production HTML correctly, but when embedding it into a per-page PHP template, it wraps the production HTML with `get_header()` and `get_footer()` (because that's "the WordPress way"). The resulting page emits the REBUILD theme's `<header>` + production's `<header>` stacked on top of each other (and the same for the footer at the bottom).

Symptoms:
- Two visually different headers stacked — one from the rebuild theme, one from production HTML.
- Two `<body>` tags in the served HTML (the rebuild theme's `header.php` opens a `<body>` and the embedded production HTML opens another).
- Nav appears twice, sometimes with different menus (rebuild theme's WP menu vs production's static markup menu).
- Scripts and styles double-load.
- Browser console shows `Multiple <body> elements found` warnings.
- `view-source:` shows two `<!DOCTYPE html>` declarations.

## Why HTML-only lenses miss it

A point-in-time screenshot at one viewport can look "approximately right" because both headers usually render in roughly the same area — the eye reads it as "thick header". Visual regression tools flag a height difference but don't articulate the root cause. The HTML technically parses (browsers tolerate multiple `<body>` tags via error recovery), and individual sections look correct in isolation.

## How to detect

1. **Grep the templates**:
   ```bash
   grep -nE '(get_header|get_footer)\s*\(' theme/page-templates/*.php
   ```
   In an interface-replicating rebuild this should return ZERO. Any hit is a finding.

2. **Count `<body>` and `<!DOCTYPE>` in served HTML**:
   ```bash
   curl -s https://staging.example.com/about/ | grep -c '<!DOCTYPE'
   curl -s https://staging.example.com/about/ | grep -cE '<body[^a-z]'
   ```
   Both should be exactly 1. A count of 2 is the smoking gun.

3. **Visual side-by-side**: open production and rebuild at 1440×900. If the rebuild looks taller at the top (extra header band) or bottom (extra footer band), inspect the DOM and look for two `<header>` peers in `<body>`.

4. **Open DevTools → Elements**: search for `<header` in the DOM tree. Production page has ONE top-level `<header>`. The broken rebuild has TWO.

## Common root causes

- Agent defaults to WordPress idiom: "page templates ALWAYS call `get_header()` and `get_footer()`". This is true for WordPress-native themes — but FALSE for interface-replicating rebuilds where the embedded HTML already provides those.
- Agent extracts only `<main>` from production HTML (assuming WP will provide the chrome), then realizes the chrome doesn't match production, then keeps both.
- Template was copy-pasted from a starter theme that includes `get_header()` boilerplate, and the agent forgot to delete those lines after pasting in production HTML.

## The validated fix

A per-page template that embeds production HTML byte-for-byte should look like this — **no `get_header()`, no `get_footer()`**:

```php
<?php /* Template Name: About */ defined('ABSPATH') || exit; ?>
<!DOCTYPE html>
<html lang="en">
<head>
<?php wp_head(); ?>
<!-- production's exact <head> contents preserved here -->
...
</head>
<body class="<?php echo esc_attr(implode(' ', get_body_class())); ?>">
<!-- production's exact <header>, <main>, <footer>, scripts -->
...
<?php wp_footer(); ?>
</body>
</html>
```

The only allowed PHP injections are:
- `<?php wp_head(); ?>` after `<head>` (WP plugin scripts: Yoast, WPML, admin bar styles).
- `<?php wp_footer(); ?>` before `</body>` (admin bar + plugin scripts).
- `<?php echo esc_attr(implode(' ', get_body_class())); ?>` mixed into the existing `<body class="...">` attr (WP body classes).

Everything else stays untouched.

## Sister patterns

- `rebuild-namespace-invention` — broader "rebuild diverges from production" pattern; this is the WP-specific symptom.
- `css-override-fights-production-js-init` — the partner pattern when the rebuild then tries to "fix" the visual mismatch with CSS instead of removing the wrapper.
- `inline-script-stripped` — partner failure when noise filter also eats production's inline `<script>` configs.

## Severity

P0 on any interface-replicating WordPress rebuild. The rebuild visibly looks wrong to the user (doubled headers/footers are immediately obvious), and every CSS override the agent adds afterward to "compensate" deepens the divergence and the debt.

## Lens question to ask

> "Does the rebuild's page template include `get_header()` / `get_footer()` calls? Grep for them. If found, the production HTML is being wrapped in the rebuild theme's chrome — remove the wrappers and embed the full `<html>...</html>` verbatim instead."
