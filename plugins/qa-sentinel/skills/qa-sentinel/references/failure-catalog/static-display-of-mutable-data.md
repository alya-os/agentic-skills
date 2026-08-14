# static-display-of-mutable-data

## Description
Data the user owns and would reasonably expect to manage is rendered read-only, with no affordance to add, edit, remove, or reorder it. The page "works" and the data is correct, so claim-and-render checks pass, but the user hits a wall the moment they try to change something. A sibling failure is the CRUD-completeness gap: a surface labeled "editor", "admin", "manage", or "settings" that supports only a subset of create/read/update/delete (e.g. per-row Save but no Add or Delete; a flat list with no search/filter/pagination that will not scale).

This is one of the highest-frequency "looks done but feels broken" gaps: an agent renders the data and stops, because rendering satisfies the literal claim ("show the competitors", "build the admin") while the implied verb (manage) is unmet.

## Symptoms
- Owned entities shown as static chips/badges/rows with no +Add, edit pencil, or ×remove control (competitors, tags, team members, keywords, models)
- A heading like "Competitors" / "Topics" / "Members" with content but zero interactive controls near it
- An "Editor" / "Admin" / "Manage X" surface that is update-only (no create, no delete) or read-only
- A list certain to grow (prompts, rows, records) with no search, filter, sort, or pagination
- "Save" buttons exist but there is no way to create the thing being saved in the first place
- The same data IS editable on one surface (e.g. a dedicated tab) but rendered dead on another (overview, brand page, dashboard) where the user also expects to act

## Root cause
The build claim was satisfied at the noun ("display the data") while the user's intent was the verb ("manage the data"). Read paths get built; the corresponding create/update/delete endpoints and their UI affordances are skipped or only partially wired. Often the endpoints already exist (used by one surface) and only the affordance is missing elsewhere.

## Independent verification
Do not just confirm the data renders. For every user-owned entity on the page, ask: can the user CREATE a new one, EDIT an existing one, and DELETE one, from a surface where they'd expect to? Drive it: click for an add control, look for edit/remove on hover, try the action and confirm it persists (re-fetch, not just optimistic UI). For any surface named editor/admin/manage/settings, enumerate which of C-R-U-D are actually reachable and exercise each. A surface that supports a subset must SAY so intentionally; silent omission is the finding. Cross-check: if the entity is editable elsewhere, the read-only surface is an affordance gap, not a missing feature.

## Common fix attempts that DON'T work
- Adding the data to the page again "more prominently" (still read-only)
- Pointing the user to a different page to edit (acceptable only if explicitly linked; usually the user expects to act in place)
- Wiring Create but not Delete (or vice-versa) and calling it done — re-fires the same finding next run
- An "admin" that only Saves edits to existing rows (the most common partial-CRUD trap)

The fix that works: expose the full verb the surface implies — add/edit/remove affordances in place, reusing the existing endpoints; for list surfaces that grow, add search/filter/pagination; for an admin, full CRUD or an explicit, documented subset.

## Likely lenses
product-manager, designer
