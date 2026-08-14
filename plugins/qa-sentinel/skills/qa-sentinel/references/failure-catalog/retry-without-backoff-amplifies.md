# retry-without-backoff-amplifies

## Description
Failure handling that increases load on the failing dependency. A retry with no delay, a refresh triggered by a read, a health check that fires more often when unhealthy, a cache that is only repopulated by the request that found it empty. Harmless while the dependency is healthy; under stress it converts a slowdown into an outage, because the retries ARE the expensive operation that just failed.

Worst when the failure leaves no record: if a failed attempt does not update the "last attempted" marker, every subsequent caller starts another.

## Symptoms
- Retry logic with no delay, no jitter and no ceiling
- A refresh, warm or sync triggered from a read path, so load scales with readers rather than with change
- Failure handling that records the error but not the attempt
- Concurrency guarded by an in-process flag while several processes run
- Load on a dependency that rises as the dependency slows

## Independent verification
Make the dependency SLOW rather than dead — a proxy delay, a paused container — and count outbound calls per minute against the healthy baseline. The count must go down, not up. Then check a caller cannot force past the gate, and that the guard survives more than one process (kill one, confirm the other still holds).

## Common fix attempts that DON'T work
- A fixed retry delay with no ceiling and no streak counter (still constant load through a long outage)
- An in-process "already refreshing" flag where several processes run
- Raising the timeout, which lengthens each attempt without reducing their number
- Disabling the retry entirely, which usually means the cache silently never updates again

The fix that works: record the attempt (not just the failure), enforce a floor between attempts, back off exponentially on a streak with a ceiling so recovery is still automatic, and keep the guard in shared storage.

## Likely lenses
developer, performance, code-architect
