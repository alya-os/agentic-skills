# Recipe: workflow-replay

Catches `regression-silent-failure`, `state-persistence-loss`, and `inactive-by-default` on user journeys. Replays each journey extracted from the workflow-discovery output end-to-end.

## Inputs

- `journeys`: list of user journeys produced by `scripts/workflow_discover.py` from CLAUDE.md / README.md / PRD
- `target_url` or `app_root`: where to start each journey

## Steps

For each journey:

1. Open the starting URL in `agent-browser`.
2. Walk the steps as documented. Common patterns:
   - "User does X" → click / type / submit per the doc
   - "Then Y happens" → assertion: capture state and verify expected change
   - "Verify Z" → final assertion
3. At each transition, capture: page URL, scroll position, form state, auth state, network requests fired since previous step.
4. Compare captured state against expected outcomes from the doc.
5. After completing the journey, exercise back-button behavior and refresh-mid-flow behavior. Verify state survives appropriately (`state-persistence-loss` check).
6. For form-submission journeys: actually submit. Verify the receiving system received the data (DB row, email, notification, downstream API call). Verify the form's `is_active=1` server-side AND the submit handler succeeded (`inactive-by-default` check).

## Pass criteria

- Every journey completes without error
- Every assertion in the journey passes
- State persists across documented transitions
- Form submissions reach their destination

## Lenses this recipe feeds

- product-manager (primary)
- business-conversion (form journeys)
- accessibility (keyboard-only replay variant)
