# inactive-by-default

## Description
Build agent creates a form, component, feature, or content item via API. The API defaults the active / published / enabled flag to false. Agent verifies "the item exists" but never verifies "the item is active". User-facing surface shows nothing.

## Symptoms
- Form created via API responds with success and an ID
- Visiting the page where the form should appear: form is missing or shows "no form found"
- Database row for the item exists but `is_active=0`, `status=draft`, `published=false`, or similar
- Item appears in admin / dashboard but not on the public frontend

## Root cause
Most API methods default new items to inactive / unpublished as a safety measure. Build agent treats "API returned 200" as "user can see it".

## Independent verification
After creating any item via API, immediately verify on the public-facing surface. For forms: render the host page, check the form is visible AND submittable AND the submit handler works.

For posts / pages: render the public URL and verify the content appears.

For database-backed items: query the active / published flag directly.

## Common fix attempts that DON'T work
- Re-creating the item (creates another inactive item)
- Toggling visibility through a different API (often sets a different flag)
- Verifying via admin panel (admins see drafts; users don't)

The fix that works: explicitly set the active / published flag in the create call AND verify on the public surface.

## Likely lenses
business-conversion, developer
