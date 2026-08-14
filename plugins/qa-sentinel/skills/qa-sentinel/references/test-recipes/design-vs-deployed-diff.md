# Recipe: design-vs-deployed-diff

Catches deployment that drifted from the design comp / mockup / brief. Compares the rendered output against the source-of-truth design files.

## Inputs

- `target_url`: the deployed page
- `design_files`: directory or list of design comps (PNG, JPG, PDF, Figma export)
- `coverage_areas`: which sections of the design map to which sections of the page (hero, features, footer, etc.)

## Steps

1. Capture deployed screenshots at the viewports the designs were created for (typically desktop 1440×900 and mobile 375×812 - match design file metadata).
2. For each `coverage_area`, crop both the design and the deployed screenshot to the relevant region.
3. Compare against design intent on these dimensions:
   - **Color tokens**: extract dominant colors via simple histogram from both crops; flag drift > 5% on any swatch
   - **Spacing scale**: measure gaps between major elements; flag drift > 8px
   - **Typography hierarchy**: identify h1/h2/body in both; flag mismatched sizes or weights
   - **Layout grammar**: are sections in the same order, same proportions? A grid that became a stack on desktop is a finding.
   - **Elements present**: any element in the design that's missing in the deploy is a finding; the reverse (extra elements in deploy) is also flagged for review
4. For each diff, pick a severity:
   - Color / spacing drift within a few percent → minor
   - Hierarchy or layout-grammar mismatch → major
   - Missing element from the design → major
   - Wholly-different section → critical (design contract broken)

## Pass criteria

- All `coverage_areas` match within tolerance
- No missing or wholly-different elements

## Lenses this recipe feeds

- designer
- product-manager (design IS spec)
