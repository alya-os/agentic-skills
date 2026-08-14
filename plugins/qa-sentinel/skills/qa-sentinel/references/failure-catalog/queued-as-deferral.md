# queued-as-deferral

> The sentinel produced a list of "queued / next-pass / follow-up" items at the END of its report and stopped. The items were not ambiguous, did not require new user input, and had clear fix recipes already named — they were simply parked on a follow-up backlog as if the run were over. This is autonomy-rule violation: queued work IS the work. The sentinel must execute the queued items in the same pass, in parallel where possible, until a safety circuit fires.

## How to detect

The aggregator scans the final user-facing report for trailing phrasings:

- `Next targets (queued)`
- `Will report back when…`
- `Want me to … next pass?`
- `Queued for follow-up`
- `Will do X in the next iteration`
- `Should I … first?` (when no irreversible action is at stake)
- `Want me to install Y next time?`

If any of these appear in the report AND the items underneath are not blocked by:

(a) An irreversible destructive action requiring user consent (deletion of production data, force-push to main, public messages, account changes), OR
(b) Genuine ambiguity in user intent that has no convergence-favoring default,

then the report is flagged as `queued-as-deferral` and the verdict is `partial-coverage`, not `pass`. The user did not invoke qa-sentinel to receive a backlog; they invoked it to receive verified work product.

## Sub-patterns

### Sub-pattern A: queued screenshots / queued visual fixes

The sentinel identifies a visual delta (e.g. "category tiles use wrong design pattern"), names the fix recipe, then defers ACTUAL execution to "next pass." The fix is mechanically determinable and reversible — there is no reason to defer.

**Fix:** execute the fix in the same iteration. If the fix touches code already modified earlier in the pass, apply on top.

### Sub-pattern B: queued tooling install

The sentinel hits a missing tool, declines to install it, then queues "Should I install Y first?" The user invoked the sentinel; they consented to installs by invoking it. Install proceeds without asking.

**Fix:** install the tool. If install fails, follow the tooling-fallback chain in SKILL.md. Only after all fallbacks are exhausted file `tooling-missing` as a real blocker.

### Sub-pattern C: queued sub-findings

The sentinel produced a P0 finding, fixed half of it, and queued the rest as "F-N next." The rest of the finding shares the same fix file, the same diff context, and the same lens that flagged it. Splitting it across passes wastes the cache warmup and the user's time.

**Fix:** complete the finding in one iteration. The atomicity rule (one finding per iteration) refers to ONE entry in the findings array, not one micro-step of a fix.

## How to verify the fix

After re-running the iteration:
- The final report contains NO trailing "queued" / "next pass" / "follow-up" language unless an irreversible action is staged with a request for consent.
- Every finding from the discovery scan is either `closed`, `stalled` (with documented stall reason), or actively being worked in the current iteration.
- The aggregator does not flag the report with `queued-as-deferral`.

## Anti-pattern: "but I wanted the user to confirm"

The user's invocation of qa-sentinel IS the confirmation. The skill is invoked to take action, not to negotiate scope item-by-item. The only reason to pause for explicit consent is the irreversibility / public-action / data-loss criteria in the autonomy rule. Scope confirmation is not on that list.

## Real-world example signatures

- `queued-as-deferral:visual-fix:F-120 F-121 F-122 listed as queued`
- `queued-as-deferral:tooling-install:playwright-install-deferred-after-first-error`
- `queued-as-deferral:sub-findings:half-finding-completed-rest-queued`
