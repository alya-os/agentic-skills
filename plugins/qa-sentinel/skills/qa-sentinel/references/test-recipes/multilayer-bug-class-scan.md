# Recipe: multilayer-bug-class-scan

Catches `multilayer-bug-class`. When any single instance of a bug pattern is found (encoding error, label drift, geographic pin, deprecated brand name), scan ALL known storage layers for the same pattern.

## Inputs

- `pattern`: the canonical broken string (e.g., a malformed Unicode sequence, an old brand name, a city name that was supposed to be removed)
- `target_system`: WordPress, generic-database, filesystem, or mixed

## Steps

1. **Enumerate storage layers** for the target_system. Standard sets:
   - WordPress: `wp_posts.post_title`, `wp_posts.post_content`, `wp_posts.post_excerpt`, `wp_postmeta.meta_value` (across keys), `wp_options.option_value`, `wp_terms.name`, `wp_termmeta.meta_value`, theme template files, mu-plugin files, language files (`.mo`, `.po`)
   - Generic: app DB tables marked content-bearing, JSON content files, env-injected strings, build-time replacements, cache layers
2. **Use `scripts/multilayer_scan.py`** with the pattern. The script accepts `--pattern <regex>` and `--layer-set <wordpress|generic>` and returns a per-layer match count.
3. For each layer with matches, capture: layer name, match count, sample context (5 surrounding chars on each side), evidence_path to the dump.
4. Single-layer matches: not a finding (just normal usage). Multi-layer matches of the same pattern: confirmed `multilayer-bug-class`.

## Pass criteria

- Zero or one layer matched (single layer = could be intentional / sole authoritative)
- More than one layer matched → finding requiring full multi-layer fix

## Lenses this recipe feeds

- content-copy (label / brand / translation drift)
- developer (encoding / data corruption)
- code-architect (denormalization without sync mechanism)
