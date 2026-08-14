# stray-char-broken-attribute-link

## Description
A server-side template concatenates a stray character into an HTML attribute value, producing a malformed attribute. The classic form is a PHP close-tag typo `?>>"` (an extra `>` after `?>`, landing inside the quotes), which renders `href="/page/>"`. The page still parses and returns 200, but the link is broken: clicking it requests `/page/%3E` and 404s. Casual source or diff review misses the single stray character; it only surfaces by rendering the page and testing the actual link targets. It commonly hits ONE copy-pasted item in a repeated component (recommendation cards, nav, related-posts, galleries) while the siblings are fine.

## Symptoms
- A link that looks correct in source but 404s when clicked
- A rendered URL ending in `>` or `%3E`, or an attribute value with a trailing stray char before the closing quote
- One card/link in a repeated component broken while the others work
- The PAGE returns 200 (so a status-only check passes) but the LINK does not resolve

## Root cause
A template output typo: an extra character inside a quoted attribute, most often `?>>"` (PHP close tag plus a stray `>`) or unescaped/mis-concatenated output. The surrounding HTML remains well-formed enough to parse, so the page loads and returns 200 - masking the broken attribute.

## Independent verification
Do not eyeball the source and do not trust the page's 200. Render the page and HEAD-test the ACTUAL `href` target of every link; a target that 404s (or a URL containing `>`/`%3E`) is the signature. In any repeated link component, test EVERY item, not one. In source, grep templates for `?>>"` and for attribute values with a stray char before the closing quote (`href="...>"`), and distinguish the legitimate tag-closer `<?php ... ?>>` (the `>` closes the tag, no quote after) from the bug `?>>"` (the `>` sits inside the quotes).

## Common fix attempts that DON'T work
- Reviewing the diff visually - the single stray character is trivially missed
- Testing only one item of a repeated list - the bug is often in a single copy-pasted card
- Trusting the page's 200 status - the page 200s while the link 404s
- Flagging external client-logo links that 403 to a bot UA (anti-bot false positive; fine in a real browser) or `href="#"` placeholders (dead but intentional) as this bug

## Likely lenses
developer, seo
