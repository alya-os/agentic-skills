# cross-env-served-markup-drift

## Description
A bug reproduces in one environment (staging) but not another (production), and the investigation stalls because everyone assumes the two environments run the same code. They don't. Staging is usually a clone taken at some past date; a later production hotfix never propagated back to it, so the *served* markup/assets differ even though the source repo "should" be identical.

## Symptoms
- "It only happens on staging / only on the old site / only on the client's copy"
- Source files look identical, or nobody has actually compared the *rendered* output between the two hosts
- The broken environment is a clone (staging cloned from prod, a duplicated site, a restored backup)
- A single attribute, script tag, asset version, or DOM node present in one env is missing in the other

## Root cause
Environments diverge over time. A fix applied directly to production (or via a plugin/patch that was never committed) leaves the clone behind. The mental model "same repo = same output" is false the moment one env got a change the other didn't.

## Independent verification
Do NOT reason from the source you assume is deployed. **Fetch the SERVED HTML from BOTH environments (cache-busted, real browser UA) and diff the actual element in question** — attributes included, whitespace-normalized. `curl -sL "$A" | tr -d '\n'` and the same for `$B`, then compare the specific node. The diff is the answer; the source tree is a hypothesis. Confirm at the DOM-property level too (a runtime script may add/remove attributes the raw HTML doesn't show).

## Common fix attempts that DON'T work
- Editing the source repo and assuming the broken env now matches (it may not deploy from that repo, or not auto-deploy)
- Re-testing without ever diffing the two served outputs
- Blaming caching without checking whether the *markup itself* differs

The fix that works: patch the lagging environment to parity with the known-good one (verify the served markup after), and flag that the clone drifted so the repo mirror gets reconciled.

## Likely lenses
developer, seo, code-architect
