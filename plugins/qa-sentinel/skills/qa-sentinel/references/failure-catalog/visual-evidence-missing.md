# visual-evidence-missing

> The designer / replication-fidelity-drift / render-truth-drift lens produced a verdict (pass or fail) without capturing pixel-level screenshot evidence of the rendered page. Without a screenshot, the lens can only know what the HTML markup says — it cannot know what the user actually sees. Every false-confidence regression in this catalog category has the same fingerprint: HTML structurally matched a reference, screenshots would have revealed the gap immediately, no screenshots were taken.

## How to detect

The orchestrator inspects every finding AND every visual pass from designer / content-copy / replication-fidelity-drift / render-truth-drift verifiers before accepting it into the verdict. Anything without an `evidence_path` that resolves to a `.png` / `.jpg` / `.webp` on disk is inadmissible: the criterion goes to NOT CHECKED, never to pass, regardless of what the verifier concluded.

## Sub-patterns

### Sub-pattern A: structural diff substituted for visual diff

The lens counted `<nav> <a>` tags, `<img>` srcs, hero `.slide` count, JSON-LD scripts. All counts matched. Verdict: `pass`. But the **rendered output** had categories overlapping the hero on the reference and floating below it on the target — invisible to HTML inspection because the markup is the same; only the CSS positioning differs.

**Fix:** count diffs are a fast pre-check. They DO NOT replace screenshot inspection. Add a render step.

### Sub-pattern B: "I read the HTML, looks fine"

A vision-capable lens model has the ability to look at images but was never given any. The lens output references "matched layout" / "matched color" / "matched spacing" without citing a screenshot path. This is hallucinated certainty.

**Fix:** require `evidence_path` for every visual claim. Reject the finding if absent.

### Sub-pattern C: tooling not installed, lens skipped silently

Playwright / Chromium / Puppeteer not on the runner. Lens detected this, returned `status: ok, findings: []` instead of `status: skipped, reason: no-screenshot-tooling`. The aggregator marked the run as `pass`. Visual gaps shipped.

**Fix:** when no screenshot tooling is available, the lens MUST emit `status: skipped` with `reason: visual-evidence-tooling-missing`. The aggregator escalates this to a `tooling-missing` blocker, NOT a pass.

## How to verify the fix

For each lens flagged with `visual-evidence-missing`:

1. Re-run the lens with screenshot capture enabled.
2. Confirm `tmp/qa-sentinel/<run-id>/<page>-<viewport>-<source>.png` exists for both reference and target.
3. Confirm the lens output references those paths in `evidence_path` and articulates a visual delta (or lack thereof) that cites specific regions of the screenshot.

## Anti-pattern: counting-as-screenshots

`"observed_signature": "shape:nav=44-vs-44,img=16-vs-20"` is a structural signature, NOT a visual signature. The aggregator must distinguish these. A visual signature looks like `"pixel-diff:categories-y-offset:+120px"` — derived from comparing rendered geometries, not markup counts.

## Real-world example signatures

- `visual-evidence-missing:designer-lens:counted-only:no-screenshot`
- `visual-evidence-missing:replication-fidelity-drift:tooling-missing:playwright-not-installed`
- `visual-evidence-missing:render-truth-drift:claimed-pass-no-png`
