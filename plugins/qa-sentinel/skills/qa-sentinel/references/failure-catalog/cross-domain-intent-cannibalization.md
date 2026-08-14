# cross-domain-intent-cannibalization

## Description
Two pages on different domains (typically a subdomain + its parent site, or
two sister sites in the same network) compete for the same search intent.
The catch: their **body content can be genuinely unique** — they fail every
Jaccard-style duplicate-content check — but they still cannibalize each other
in SERPs because their **H1 / title / URL pattern target the same keyword
+ entity** (same city, same service, same brand).

This is distinct from `about-page-cannibalization`, which catches verbatim
body duplication. This pattern catches intent collisions that look unique to
a body-shingle scan but still split rankings, dilute internal authority, and
confuse Google about which URL should rank.

## Symptoms
- Subdomain has unique narrative content ("Kirkland is a West Island
  municipality with high-end appliance concentration…") but parent has
  generic template content ("Our repair technicians can quickly go to Kirkland
  to get your home appliances working good as new")
- H1 on subdomain: "Réparation d'électroménager à Kirkland". H1 on parent:
  "Réparation d'électroménagers à Kirkland". Near-identical title intent.
- Both URLs target the same primary keyword + location: `/locations/<city>/`
  on subdomain vs. `/reparation-electromenagers/<city>/` on parent
- Google Search Console shows one page ranking briefly, then the other —
  positions flip every few weeks. Combined impressions are split.
- Body Jaccard < 0.2 (passes `about-page-cannibalization` rule), yet GSC data
  shows the cannibalization clearly

## Root cause
The build agent (or QA lens) is configured to scan **internal** duplicates
only. The `parent_domain` field in the coverage matrix may exist but be empty,
or the cannibalization rule may only fire when body-Jaccard exceeds a
threshold — which never triggers for genuinely-rewritten content.

Cannibalization is **not** purely a content-duplication problem. Two pages
with 100 % unique bodies still cannibalize if they:
1. Target the same primary keyword phrase (cosine-similar H1 or `<title>`)
2. Address the same entity (same city, same service, same brand, same combo)
3. Have similar URL slug semantics (e.g., both contain `kirkland`)

## Independent verification
1. Fetch the **parent domain's** sitemap_index.xml (or sitemap.xml). Recursively
   enumerate every sub-sitemap (post-, page-, category-, etc.).
2. Extract all URLs. Group by trailing slug (e.g., `kirkland`, `beaconsfield`).
3. For each subdomain page, compute the trailing slug. Find any parent URL
   whose slug matches OR contains the subdomain slug.
4. For matched pairs: fetch H1 + `<title>` from both. Compute:
   - **H1 token-set ratio** (sorted token overlap, dedup, case-folded, accent-folded)
   - **Title token-set ratio** (same)
   - If H1 OR title token-set ratio ≥ 0.75 → **flag intent cannibalization**
5. Independent transport: fetch with `curl -A "Googlebot"` AND `agent-browser`.
   Some templates inject the H1 only via JS — both transports must see the same H1.

Example token-set ratio check:
```
H1 subdomain: "Réparation d'électroménager à Kirkland"
  tokens (folded, sorted, deduped): {a, d, electromenager, kirkland, reparation}
H1 parent:    "Réparation d'électroménagers à Kirkland"
  tokens (folded, sorted, deduped): {a, d, electromenagers, kirkland, reparation}
intersection = 4 of 5 = 0.80  →  FLAG
```

## Common fix attempts that DON'T work
- Adding `<meta name="robots" content="noindex">` to the subdomain page —
  destroys the subdomain's local SEO value entirely and signals to Google
  that the parent should rank, which may not be the business intent.
- Adding `<link rel="canonical" href="parent-url">` from subdomain →
  parent — same issue, also can fail when domains differ at organizational
  level.
- Rewriting the subdomain body further — body uniqueness was never the
  problem. The H1 + title + slug pattern still collide.
- Adding more local landmarks to the subdomain body — same root cause
  remains.

## What does work
**Pick one site as the canonical for each intent.** Then either:

**Option A — Subdomain wins the city pages:**
1. Set the parent's `/reparation-electromenagers/<city>/` and
   `/en/appliance-repair/<city>/` pages to `noindex,follow` via a server-side
   filter (NOT meta — server header is more reliable; meta gets cached).
2. Add `<link rel="canonical" href="https://subdomain.example.com/locations/<city>/">`
   on each parent city page. Verifies via independent curl fetch.
3. 301 the parent city pages to the subdomain equivalents AFTER 30-60 days
   of consolidated signal (let Google reprocess noindex first).

**Option B — Parent wins the city pages:**
1. Subdomain city pages become differentiated from parent intent: shift H1
   from "Réparation d'électroménager à Kirkland" to
   "Guide d'entretien d'électroménagers — secteur Kirkland"
   (different intent: guide content vs. service intent).
2. Subdomain canonical points to subdomain page (self-referencing). Parent
   canonical points to parent page. Intent split is now meaningful.

**Option C — Service-area page on parent + neighborhood-specific on subdomain:**
1. Parent keeps `/reparation-electromenagers/<region>/` for top-level metros.
2. Subdomain has `/quartiers/<neighborhood>/` (Plateau-Mont-Royal, Saint-Henri)
   that the parent doesn't cover. Intent is genuinely different.

Whatever the choice, the rule is: **one URL per intent across the network.**

## Independent transport (mandatory)
- Fetch with `curl -A "Googlebot"` — what crawler sees
- Fetch with `agent-browser` — what user sees post-JS
- For the parent: fetch from a different network / VPN tier where possible
  to bypass any CDN edge caching that might serve different responses.

## Likely lenses
seo (primary), content-copy, business-conversion (because the wrong page
ranking erodes conversion intent — generic-template page ranking instead of
local-narrative page = lower conversion rate)
