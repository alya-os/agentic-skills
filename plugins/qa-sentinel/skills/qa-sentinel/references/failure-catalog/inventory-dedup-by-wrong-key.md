# inventory-dedup-by-wrong-key

> A dedup pass keyed on `post_title` (or `name`, `model`, `display_name`) trashed legitimately distinct inventory units. At dealerships (boats, cars, RVs, equipment) and at multi-warehouse retailers, **multiple physical units of the same model are normal** — they share the model name but differ on stock_id, color, year-on-floor, individual pricing, and serial number. Dedup MUST key on the canonical inventory primary key, not the human-readable title. This pattern surfaced on a boat-dealership inventory import: a title-based dedup trashed 27 of 299 units, including 4 distinct units of one model year that differed on stock_id, price, and colour.

## How to detect

Before running any dedup, the aggregator MUST verify:

1. **Per-group attribute variance**: for every "duplicate" group identified by the proposed key, list members and check whether at least one of `{stock_id, sku, serial_number, vin, asset_tag, color, price, year_of_arrival, location_id}` differs within the group. If ANY differ, the group is NOT a duplicate — those are distinct inventory units.
2. **Case-insensitive collision**: dedup keys must NEVER collapse `"REBEL XL"` and `"Rebel XL"`. Title casing variation is data noise, not a duplication signal. If the proposed key would collide these, switch to case-sensitive matching OR key on the inventory PK that's already case-normalized at the source.
3. **Brand-template uniformity**: title strings like `"2026 <Make> 16 <Model>"` are FACTORY MODEL NAMES, not unit identifiers. They will repeat as legitimate stock arrives. Dealer sites of any reasonable size will have multiple units of the same model on the lot simultaneously.

## How to choose the right dedup key

Priority order, top to bottom:

1. **Vendor/source-provided stable PK**: AutoTrader stock_id, AutoHebdo listing_id, manufacturer VIN/serial, dealer's internal inventory_id. These are the ground truth for "is this the same physical unit?"
2. **Composite key**: `(brand_slug, model_slug, year, stock_id)` — robust when the source feeds change schemas.
3. **Content fingerprint**: hash of (model + year + color + first 3 spec values + photo count). Useful for catching genuine import-bug duplicates where the same source row was imported twice (same stock_id repeated). Often this is what people MEAN when they say "dedupe by title".
4. **Title-only** — ONLY valid for genuine display-name duplicates within a non-inventory CPT (e.g. two `posts` with the same headline that an editor created in error). NEVER for inventory items.

## How to verify the fix

After any dedup operation on an inventory CPT:

1. Compare published-count before and after; subtract the expected number of TRUE duplicates (identical stock_id within the group) — that's the legitimate trash count.
2. For every group that was trashed, report the within-group variance on stock_id, price, color. ANY variance = the trash was wrong. Restore those posts.
3. Use `wp_trash_post()` (reversible) NEVER `wp_delete_post(force=true)` on the first pass. The post stays in trash and can be `wp_untrash_post()` if the dedup logic turns out to have been wrong.

## Anti-pattern: "we have 5 of these in stock so the data is wrong"

Inventory size IS the data. A dealer with 5 of the same model on the lot has 5 published listings, each with its own stock_id, its own gallery, its own price. Compressing them to one listing destroys the per-unit URLs that customers + Google have already crawled and bookmarked.

## Real-world example signatures

- `inventory-dedup-by-wrong-key:title-collision:dealership-import:27/299-trashed`
- `inventory-dedup-by-wrong-key:case-insensitive-name:REBEL-XL-vs-Rebel-XL`
- `inventory-dedup-by-wrong-key:model-uniformity:4-distinct-FALCON-16-units-treated-as-dupes`
