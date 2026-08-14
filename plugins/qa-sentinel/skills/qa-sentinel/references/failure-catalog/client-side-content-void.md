# client-side-content-void

## Description
Server returns an empty or minimal HTML container. JavaScript fetches data and populates the DOM client-side. To a crawler with no JS execution, the page appears empty.

## Symptoms
- `curl <url>` returns HTML with no h1, no body content, no schema markup
- `curl` HTML shows a `<div id="root"></div>` or similar empty mount point
- Search Console reports indexed pages with low coverage
- Schema.org structured data missing from raw HTML
- Page renders fine in a browser but is invisible to old crawlers

## Root cause
Single-page-app pattern without server-side rendering or static pre-render. Often a deliberate architectural choice for app-like experiences but wrong for content / marketing pages.

## Independent verification
Always diff `curl -A "Googlebot" <url>` against the rendered DOM (`agent-browser` after page-load). The diff IS the finding.

If primary content (h1, body copy, JSON-LD, internal links to important pages) appears only after the diff, the pattern is confirmed.

## Common fix attempts that DON'T work
- Adding more meta tags (doesn't change body content)
- Adding a `<noscript>` fallback with marketing copy (Googlebot DOES execute JS now, but intermittently; relying on `<noscript>` is fragile)
- Adding JSON-LD to a script tag without the surrounding content (Google requires the content to back the schema)

The fix that works: server-side render the route, or add a static pre-render step at build time. Hybrid frameworks (Next.js, Astro, Nuxt) make this routine.

## Likely lenses
seo, developer
