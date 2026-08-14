# editor-export-bloat

> A vector asset exported from a design tool (Adobe Illustrator, Inkscape, Sketch, Figma) ships with tool-private metadata, unused `<defs>`, hidden layers, and clip-path stubs that inflate file size 100–500× the rendered cost. A 920 KB brand SVG with four visible `<path>` elements and zero embedded raster is the canonical case. Lighthouse and "page weight" lenses flag the symptom; the catalog entry names the cause so the fix recipe is correct.

## How to detect

| Signal | Threshold | Mechanism |
|---|---|---|
| SVG > 50 KB | hard flag | Compare `Content-Length` of every `*.svg` against this floor |
| Zero embedded raster | required | `<image>` count = 0 AND `base64,` substring count = 0 |
| Adobe Illustrator export marker | strong indicator | `xmlns:i="http://ns.adobe.com/AdobeIllustrator"` OR `Generator: Adobe Illustrator` in comment |
| Figma export marker | indicator | `data-figma-name` / `<!-- Created with Figma -->` |
| Sketch export marker | indicator | `xmlns:sketch=` |
| `<defs>` size > 60% of total | indicator | Compute byte ratio of `<defs>…</defs>` block |

If any TWO signals trigger, file the finding with `catalog_entry: editor-export-bloat`. Do not require all signals — pure-path bloat without an editor marker still qualifies.

## How to verify the fix

The fix is mechanical: `npx svgo@3 --multipass <file>`. Verify by:

1. Re-fetch the file via HTTPS (with cache-bust query string — see `cache-stale-verify.md`).
2. Confirm `Content-Length` dropped by ≥80%.
3. Confirm visual fidelity: render both originals + optimized side-by-side at the layout's target dimensions. Flag any visible regression.
4. Re-run the homepage / inventory / archive that references the asset; confirm no console errors about missing IDs (SVGO can drop `id=""` attributes referenced by `<use href="#…">`).

## Anti-pattern: optimize-in-place without backup

When the asset lives in `/wp-content/uploads/` (WordPress) or another CMS media library, the optimized version OVERWRITES the original. Always download the original first to `/tmp/<asset>-pre-opt.svg`. Two reasons:

1. If the optimization breaks a referenced `<use href>`, the rollback is one `sftp put`.
2. The original is what the build agent was working from. If the bug shows up on retest after optimization, the comparison artifact is the un-optimized file.

## Distinction from `cache-stale-verify`

`editor-export-bloat` is the bug. `cache-stale-verify` is the false-pass when an optimized upload appears not to be live because Cloudflare / WPE Edge is still serving the old 920 KB asset. Always cite both when both apply.

## Real-world example signatures

- `editor-export-bloat:adobe-illustrator:size=920781,paths=4,defs-ratio=0.97`
- `editor-export-bloat:figma:size=180000,paths=12,defs-ratio=0.45`
- `editor-export-bloat:generic:size=210000,paths=8,defs-ratio=0.78` (editor unknown, bloat pattern present)
