# Failure pattern: inline-script-stripped

## What it looks like

A "rebuild matches production" effort downloads the production HTML, then runs it through a noise filter that strips analytics/tracker scripts. The filter regex matches `<script>` tags containing strings like `googletagmanager`, `newrelic`, `hotjar`, `gtm` — but it matches them in **inline** `<script>` blocks too, not just `<script src="...">` references.

The bundle ships. The page renders. But interactive JS is broken: hero carousel stays blank, lazy-loaded images don't appear, mega-menu hover doesn't trigger, language switcher dropdown opens but its config is missing. Console fills with `loadFontsArr is not defined`, `CMSettings is not defined`, `globalVars is not defined`, `showCookieBanner is not defined`.

## Why HTML-only lenses miss it

The HTML structure is correct. The CSS loads. The external `<script src="...convertus.min.js">` files load. The agent reports "stripped trackers per privacy requirement" and the screenshot looks ~80% right (header + footer render fine; only image-dependent and JS-config-dependent areas are broken).

A point-in-time visual check at one viewport may not catch it if the carousel auto-rotated past the broken slide, OR if lazy-loading was disabled in headless screenshots.

## How to detect

1. **Open browser devtools console on the rebuild.** Count JS errors. Production has zero functional errors. The rebuild should have zero functional errors. Reference errors (`X is not defined`) at runtime almost always mean an inline config block was stripped.

2. **Diff the inline `<script>` blocks** between production HTML and rebuild HTML:
   ```bash
   # Production
   grep -oE '<script[^>]*>(?!<)' production.html | grep -v 'src=' | wc -l
   # Rebuild
   grep -oE '<script[^>]*>(?!<)' rebuild.html | grep -v 'src=' | wc -l
   ```
   A drop of ≥3 inline scripts is suspicious. Production CMSes often emit 10-30 inline config blocks (`var loadFontsArr = [...]`, `var globalVars = {...}`, `dataLayer.push({...})`).

3. **Open `view-source` on a working browser tab pointed at the rebuild.** Search for the lowercase variable names production's runtime expects: `var loadFontsArr`, `var CMSettings`, `var globalVars`, `var translatedStrings`. Each missing one is a finding.

## Common root causes

- Noise filter matches by substring in the script body, not by `src=` URL: `if ('newrelic' in $script_body) decompose()` will strip the inline `(function(){var NREUM=...})()` init block AND the inline `var globalVars = {...}` block if it happens to contain a tracker reference.
- Agent assumes any tracker keyword in JS = data leak; in reality, the inline blocks define **globals that the SAME production JS** (which we're keeping) reads at runtime.
- Filter operates on text-match instead of DOM attribute match.

## The validated fix

Strip ONLY `<script src="...">` tags whose URL substring matches a known analytics domain (`googletagmanager.com`, `nr-data.net`, `hotjar.com`, `optimizely`). NEVER decompose inline `<script>` blocks. They don't make external requests on their own — they define data that the JS we're keeping consumes.

```python
NOISE = ("googletagmanager.com", "google-analytics.com", "newrelic",
         "nr-data.net", "hotjar", "optimizely", "facebook.net",
         "doubleclick", "bat.bing")
for sc in soup.find_all("script"):
    src = sc.get("src") or ""
    if src and any(n in src.lower() for n in NOISE):
        sc.decompose()
    # NEVER strip based on sc.string content
```

## Sister patterns

- `rebuild-namespace-invention` — the broader "rebuild drifts from production" pattern
- `inline-script-interleave-broken` — even when inline scripts ARE preserved, bundling them into one file loses execution-order interleaving
- `helper-fn-not-deployed` — analogous failure when PHP function definitions are missing

## Severity

P1 (high). The page renders, so static checks pass. But all dynamic interactivity is silently broken — hero carousels, lazy-loaded images, menu hover states, cookie banner, language switcher. Visitors see a worse experience than production while every console error pings the customer's analytics about silent failures.

## Lens question to ask

> "Did the rebuild preserve production's inline `<script>` blocks? Open browser console on the rebuild and screenshot any `X is not defined` errors. Compare inline script counts between production and rebuild."
