# adblock-blocked-conversion-ui

## Description
A popup, modal, CTA, overlay, interstitial, or lead-capture element uses names that ad blockers target. Its CSS classes/ids or its JS/CSS asset filenames contain filter-list trigger tokens (popup, exit, cta, modal, interstitial, overlay, promo, newsletter, subscribe, optin, leadgen, banner, lightbox, exit-intent). EasyList/uBlock/AdBlock block the matching asset URLs and/or cosmetically hide the matching elements, so a large share of real visitors never see the element or it renders broken (script or stylesheet blocked). The element passes QA anyway because the QA browser has no ad blocker installed.

## Symptoms
- Element works in a headless/QA browser but is missing or broken for real users ("something is wrong, sometimes it doesn't show")
- Behavior differs by visitor and cannot be reproduced in a clean automated capture
- Network panel (with an ad blocker on) shows the element's JS/CSS asset blocked / never loaded
- Element's classes, ids, or filenames literally contain popup / exit / cta / modal / overlay / promo / newsletter / etc.

## Root cause
Ad-block filter lists (EasyList and friends) match both URLs and DOM selectors that look like advertising or interstitial markers. Marketing/conversion elements are frequently named exactly like the things filter lists target, so they get caught as collateral. A headless QA browser ships no ad blocker, so QA renders the element fine while a meaningful fraction of production traffic has it blocked.

## Independent verification
Verify on a channel that mirrors a real ad-blocking user, not a clean automated one:
1. Static scan: grep the element's classes, ids, and asset filenames against the trigger-token list. Any hit is a flag.
2. Live scan: load the page in a browser with uBlock Origin (EasyList enabled) and confirm (a) the element still renders and (b) each of its JS/CSS assets returns 200 (not blocked). A clean no-adblocker screenshot is NOT sufficient evidence for any conversion element.

## Common fix attempts that DON'T work
- Renaming only the file but leaving the trigger token in the CSS classes (cosmetic filters still hide it), or vice versa - both the URL and the selectors must be neutral
- Inlining the script/style to dodge URL blocking while keeping class names that cosmetic filters still hide
- Adding `!important` or z-index tweaks (the element is removed/hidden by the blocker, not merely covered)
- Testing only in a headless/automation browser, which never has an ad blocker

The fix that works: rename to neutral, non-marketing tokens (e.g. reach, invite, connect) for BOTH the asset filenames and the CSS classes/ids, then re-verify with an ad blocker enabled.

## Likely lenses
developer, business-conversion
