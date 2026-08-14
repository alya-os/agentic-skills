# ios-video-needs-playsinline

## Description
An autoplaying/inline `<video>` (background loop, hero, page-transition mask) has no `playsinline` attribute. On iOS (Safari AND Chrome-for-iOS, which is WebKit), the video is **forced fullscreen** the instant it plays — "the video opens up" over the page. If the file is heavy (4K / high-bitrate), the forced fullscreen decode can exhaust memory and **crash the tab** ("A problem repeatedly occurred" / "Can't open this page").

## Symptoms
- A background/decorative video takes over the whole screen on iPhone but is fine on desktop and Android
- Tab reloads or dies on iOS shortly after landing on the page
- Bug is iOS-specific (WebKit); Chrome/Firefox on desktop or Android never reproduce it
- The offending `<video>` lacks `playsinline` while sibling videos on the same site have it (a single missed element)

## Root cause
iOS only plays a `<video>` inline when it carries `playsinline` (and the legacy `webkit-playsinline` for older iOS). Without it, WebKit's default is fullscreen playback. `muted autoplay` alone is not enough — inline muted autoplay STILL requires `playsinline`. Heavy/4K sources make the resulting fullscreen decode a crash risk.

## Independent verification
- Grep the served markup for every `<video>` and every `<source>`; each autoplay/background video MUST have `playsinline webkit-playsinline` (plus `muted` for autoplay).
- Confirm at the DOM level on an iOS-emulated context: `video.playsInline === true` and `video.hasAttribute('playsinline')`. A runtime script may inject it — if that script errors (check the console), the attribute is absent at play time and the bug returns.
- Prefer real iOS / an iPhone device profile; a desktop-Chrome pass will NOT reproduce this class.

## Common fix attempts that DON'T work
- Adding `muted` only (inline autoplay still needs `playsinline`)
- Relying on a JS pass to add `playsinline` at runtime (fails silently if that script throws — put the attribute in the markup)
- Hiding the video on mobile via CSS (regression in the other direction: the visual is gone)

The fix that works: author `playsinline webkit-playsinline` directly on the `<video>` element in the template; and for heavy sources, serve a mobile-weight encoding. Verify the served markup after deploy.

## Likely lenses
developer, designer, performance, accessibility
