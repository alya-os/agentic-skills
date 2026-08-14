# Recipe: visual-baseline-diff

Catches `regression-silent-failure` and `mobile-only-regression` on visual surfaces. Compares pixels against a known-good baseline at both desktop and mobile viewports.

## Inputs

- `target_url`: the page to verify
- `baseline_dir`: directory containing `<name>.desktop.png` and `<name>.mobile.png` (or fetch most recent green from `tmp/qa-sentinel/<last-green-run-id>/`)

## Steps

1. Use `agent-browser` to open the target at 1280×800. Take a full-page screenshot. Save to `tmp/qa-sentinel/<run-id>/<name>.desktop.png`.
2. Repeat at 390×844 mobile viewport. Save as `<name>.mobile.png`.
3. Diff each capture against the corresponding baseline using `scripts/screenshot_diff.py`. The script outputs a per-region diff percentage and a visual diff image.
4. Threshold: any region with >5% pixel difference is a finding. Whole-image diff >2% is a finding. Adjust thresholds per project if needed.
5. For each diff finding, classify:
   - Layout shift (likely `regression-silent-failure`)
   - Missing element (likely build-output regression)
   - Mobile-only difference (`mobile-only-regression`)
   - AI-slop drift (designer lens cross-check)

## Pass criteria

- Zero layout shifts >2% whole-image
- Zero missing-element regions
- Mobile and desktop both within thresholds

## Lenses this recipe feeds

- designer
- product-manager (regression detection)
- accessibility (visual contrast regressions)
