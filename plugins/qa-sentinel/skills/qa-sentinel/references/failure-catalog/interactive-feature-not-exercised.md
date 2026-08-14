# Failure pattern: interactive-feature-not-exercised

## What it looks like

The build agent reports a feature complete that REQUIRES JavaScript or a server roundtrip to function: a dynamic-content generator (codes, charts, signatures), a calculator, a modal trigger, a filter/facet control, a language switcher, an async form submit. The lens captures the page HTML, sees the trigger element (a button with the expected `data-` attribute, a container with the expected ID) and marks the feature present.

Days or weeks later the user notices the feature never actually fires. The generator never produces an image. The calculator outputs NaN. The modal trigger doesn't open anything because the JS handler wasn't bound. The filter URL changes but the result list doesn't update.

## Why HTML-only lenses miss it

Static markup reveals only the SHAPE of the feature: classes, data-attributes, IDs. It says nothing about whether the JS that hydrates the feature actually runs, whether the dynamic content renders, or whether the asset chain (script enqueued + path resolves + handler binds + endpoint reachable) is complete.

## How to detect

Each declared feature gets ONE exercise on a live page. The exercise table is type-driven, not name-driven:

| Control type | Exercise | Pass criterion |
|---|---|---|
| Dynamic content generator | Locate the generated element | Non-empty rendered content (image with `src`, svg with `viewBox`, text with characters) |
| Calculator / form-driven compute | Provide minimum valid inputs, blur or submit | Result region updated with a parseable, non-trivial value |
| Modal / dialog trigger | Click the trigger | Hidden attribute or display state flipped; focus moved inside |
| Filter / facet control | Activate one option | URL state changed AND visible result count or list changed |
| Tabbed / accordion content swap | Activate a non-default tab | Panel content visible; other panels hidden |
| Multi-state toggle (language, theme, currency) | Activate inactive state | Navigation OR live re-render to the alternate state |
| Async submit (form, vote, request) | Provide minimum valid inputs and submit | Network shows 2xx response AND UI confirms success or transition |

Each failure is `severity: critical` because the feature was claimed done. "Element is in the DOM" is not pass.

## Common root causes

- JS file enqueued under a stale handle name that conditional-load logic skipped.
- Shortcode renders the trigger but the supporting endpoint route was never registered.
- AJAX nonce missing, mismatched, or expired.
- Library (codec, charting, PDF, QR) referenced by the handler not loaded.
- Handler scope: DOM ready fires before the dynamic element is inserted.
- CSP blocks the inline handler or the third-party library origin.
- Build pipeline tree-shook the handler module as unused.

## Severity

P0 whenever the build agent marked the feature complete. Catching it after launch is much more expensive than catching it on the iteration that claimed completion.

## Sister patterns

- `inactive-by-default` — feature ships in a disabled-by-default state and no one flipped the toggle
- `helper-fn-not-deployed` — code-level analog (function defined but not loaded)
- `regression-silent-failure` — broader category
