# metadata-contradiction

## Description
Different surfaces for the same page contradict each other. Title says one thing, h1 says another, og:title says a third. Crawlers and social previews show the wrong text. Users get inconsistent signals.

## Symptoms
- Page title (`<title>`) does not match h1
- og:title does not match page title
- Twitter card title is generic ("Home") while page is specific
- Canonical URL points elsewhere (often a default or staging URL)
- hreflang lists language pairs that don't reciprocate (lang A points to B, B doesn't point back)
- Breadcrumb structured data lists pages that don't exist

## Root cause
Templates that source metadata from different fields than the visible content. Default values not overridden. Multiple authoring surfaces (CMS, theme, plugin) write to different metadata fields.

## Independent verification
Fetch the rendered HTML. Extract every metadata surface (`<title>`, `<h1>`, `og:*`, `twitter:*`, `link[rel=canonical]`, JSON-LD). Compare. Any mismatch on the same conceptual field is a finding.

For hreflang: fetch each language version, build the matrix, verify reciprocity.

## Common fix attempts that DON'T work
- Updating the title field in the CMS (often only updates `<title>`, not og:title)
- Setting a sitewide og:title default (overrides page-specific intent)
- Manually patching one of the surfaces (others remain wrong)

The fix that works: identify the single source of truth for the page's title / description / canonical. Make all other surfaces derive from it.

## Likely lenses
seo, content-copy
