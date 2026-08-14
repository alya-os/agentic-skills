# Workflow Discovery Guide

Adapted from the `ultimate_validate_command.md` pattern. Real user workflows from project docs become E2E recipes in the coverage matrix. This is what makes the QA sentinel project-specific instead of generic.

## Where to look

In priority order:

1. `README.md` → "Usage", "Quickstart", "Examples", "How it works" sections
2. `CLAUDE.md` / `AGENTS.md` → workflow-pattern descriptions, common operations
3. `docs/` → user guides, tutorials
4. `PRD*.md`, `specs/` → user-stories formatted as scenarios
5. Code comments at module-entry points (e.g., FastAPI route docstrings, React top-level component comments)

## What a workflow looks like

A workflow is any text describing a sequence of user actions and expected outcomes:

- "User does X → then Y → then Z"
- "1. Click X. 2. Type Y. 3. See Z."
- "Send a POST to /endpoint → receive {result: ...} → verify the database row was created"
- "Run `command --flag` → output appears at /path → file is uploaded to S3"

## Three levels of E2E (per `ultimate_validate_command.md`)

For each workflow, classify into:

1. **Internal APIs** - what the project tests itself (commands execute, DB queries succeed)
2. **External integrations** - what the workflow depends on outside the project (CLIs, third-party APIs, services)
3. **Complete user journey** - start-to-finish from the user's perspective, ending in a real-world outcome

Coverage at all three levels is the goal. A workflow that covers only internal APIs leaves external-integration risk unchecked.

## Extraction algorithm

`scripts/workflow_discover.py` applies this:

1. Read each priority source.
2. Find sections with imperative-mode language ("Click", "Run", "Send", "Create", "Verify", "Open", "Type").
3. Group consecutive imperative sentences into a candidate journey.
4. For each candidate, identify:
   - Starting condition (URL, command, state)
   - Ordered steps
   - Expected outcomes per step
   - Final assertion / success criterion
5. Classify the journey level (internal / external / complete).
6. Score the journey for QA importance (how often is it cited? does the README put it in the first 100 lines? does it touch a payment / form / auth flow?).
7. Output the top N journeys (default N=10) for the coverage matrix.

## Output format

```yaml
journeys:
  - name: "<short-stable-name>"
    source: "<file-path:line>"
    level: "internal-api|external-integration|complete-journey"
    importance: <1-10>
    starting_state:
      url: "<url or null>"
      command: "<command or null>"
      preconditions: ["<text>", ...]
    steps:
      - action: "<imperative>"
        expected: "<outcome>"
    final_assertion: "<text>"
```

These journeys feed the `workflow-replay.md` recipe and become rows in the coverage matrix routed to the product-manager lens.

## Edge cases

- **Project has no docs** → no journeys to extract; `/qa plan` falls back to URL-only and crawl-based discovery
- **Docs exist but workflows aren't structured as steps** → extract verb-noun pairs as informal journeys; lower importance score
- **Multiple conflicting journey descriptions** (README says one thing, PRD says another) → use higher-priority source per the input-understanding priority order; flag the discrepancy as a finding
