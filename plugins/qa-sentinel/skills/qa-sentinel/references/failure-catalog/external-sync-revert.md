# external-sync-revert

## Description
A change is applied successfully, but a separate sync hook, deploy pipeline, or cron job silently reverts the change minutes or hours later. The agent reports success based on the immediate-after-deploy state.

## Symptoms
- Same change has been "fixed" multiple times in the ledger across runs
- Re-fetching the target hours after the deploy shows the change is gone
- Git history shows the file changing back to a prior state with no human author
- A scheduled job (CI sync, content sync, marketplace sync) overwrites the area being changed

## Root cause
The system has more than one source of truth for the same surface, and they reconcile on a schedule.

## Independent verification
Re-fetch the target with a cache-buster at three points: T+0, T+10min, T+1hr. If any later fetch shows reverted content, the pattern is confirmed.

Cross-reference the ledger: if the same `(test_id, observed_signature)` appears in multiple prior runs, this is a strong signal even before scheduling new fetches.

## Common fix attempts that DON'T work
- Re-applying the change (it just reverts again)
- Pinning the file (sync hooks often ignore file pins)
- Disabling the sync temporarily (re-enables on next deploy)

The fix that works: identify the upstream source of truth and update it there. If the upstream source is intentional, accept the change must live there.

## Likely lenses
developer (cross-run dedup catches this fast)
