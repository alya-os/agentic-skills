# about-page-cannibalization

## Description
About / Entreprise / Team / À propos pages are the highest-risk class for
duplicate-content cannibalization between a subdomain (or sister site) and a
parent domain. Service pages have natural per-region variation; about pages
share the same team photos, the same mission paragraph, the same history,
verbatim. SEO lenses that scan « primary CPTs » (services, locations, products)
miss this entirely because about pages aren't in the focal list.

## Symptoms
- `<title>` and `<h1>` are identical or near-identical to parent-site about page
- First paragraph copy-pastes parent site verbatim
- Team photos with identical names, identical roles, identical alt text
- Mission/value paragraphs duplicate without variation
- Google Search Console shows the about page « competing » with parent site for
  brand + « about » queries — one of the two ranks but not both

## Root cause
About pages are off the radar because they're not « priority pages » for SEO.
Build agents and even QA lenses focus on commercial intent pages. The about
page gets created once, copy-pasted from a parent / template, never re-audited.

## Independent verification
- Crawl EVERY URL in the sitemap, not a hand-picked CPT list
- For each page, extract `<title>`, `<h1>`, first 200 words of `<main>` content
- Compare against the same fields on the parent / sister site (configurable via
  `parent_domain` field in the coverage matrix)
- Compute content-shingle similarity (8-word shingles, Jaccard). > 0.4 = flag.
- Pay special attention to URLs matching `/about/`, `/a-propos/`, `/entreprise/`,
  `/team/`, `/equipe/`, `/legal/`, `/privacy/`, `/terms/`

## Common fix attempts that DON'T work
- Adding a paragraph to the subdomain about page (overall similarity still high)
- Changing the H1 (body still nearly identical)
- Adding noindex to the subdomain page (loses SEO value entirely; doesn't
  address that the page is dead weight on the subdomain)

## What does work
- Rewrite the subdomain about page to focus on what's UNIQUE about the subdomain
  context (« this is our SEO guide site », « our local presence », etc.)
- Delete the subdomain about page and link to the parent's about page
- If both must exist, give them genuinely different angles
  (parent = company story; subdomain = team-by-region or service-team focus)

## Likely lenses
seo (primary), content-copy, code-architect
