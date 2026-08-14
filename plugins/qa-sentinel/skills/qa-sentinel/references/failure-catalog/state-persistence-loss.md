# state-persistence-loss

## Description
User state (form input, scroll position, filter selection, auth) is wiped when it shouldn't be. Back-button takes user to a fresh page. Refresh erases progress. Filter changes don't survive navigation.

## Symptoms
- Filling a form, navigating away, navigating back: form is empty
- Scrolling halfway down a long list, clicking an item, hitting back: scroll position is at top
- Selecting filter facets, paginating: filters reset on page change
- Multi-step wizard: refreshing on step 3 takes user back to step 1
- Auth state appears valid but expires unexpectedly mid-session

## Root cause
State stored only in component memory or URL hash, not in URL query params, sessionStorage, localStorage, or server-side session. Page transitions discard the state.

## Independent verification
Walk the user journey end-to-end. At each transition (link click, back button, refresh, tab switch), capture the state. Any state that should persist but doesn't is a finding.

Check:
- Form state: type something, navigate away, navigate back, read the input value
- Scroll: scroll, click out, click back, read scrollY
- Filters: select facets, paginate, verify URL contains them and they're still applied
- Auth: log in, leave for 30 minutes, return, verify still logged in

## Common fix attempts that DON'T work
- Telling users "don't navigate away" (UX failure)
- Adding a confirm-before-leave dialog on every page (annoying)
- Storing state in component memory only (doesn't survive)

The fix that works: identify which state must persist across which transitions, store in the appropriate layer (URL params for filters / pagination, sessionStorage for ephemeral form state, server session for auth).

## Likely lenses
product-manager, business-conversion
