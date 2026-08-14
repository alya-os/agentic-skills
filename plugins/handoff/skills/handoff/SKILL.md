---
name: handoff
description: |
  Capture session state into a structured handoff document so the next Claude
  session (or another human) can resume without context loss. Generates a
  Markdown file with goal, progress, decisions, dead ends, changed files, and
  recommended first action.

  Use when: user says "handoff", "session summary", "save session state",
  "wrap up", "create handoff", "context for next session", "end of session",
  "pass the baton", or asks to capture work-in-progress for later continuation.
  Also use proactively when a long session is ending and significant uncommitted
  decisions or in-progress work exist.
argument-hint: "What will the next session be used for? (optional - tailors the handoff)"
---

# Handoff - Session State Capture

Generate a structured handoff document that lets the next session resume
without re-discovery. Prioritize **non-obvious context** -- decisions, dead
ends, and gotchas that cannot be recovered from `git log` or file reads alone.

---

## Workflow

### 1. Gather state automatically

Run `scripts/gather_state.sh` to collect git branch, last commit, dirty files,
recent log, and environment snapshot. Read the output to populate the template.

```bash
bash <skill_path>/scripts/gather_state.sh
```

### 2. Interview the session (context window scan)

Scan the current conversation for:

| Signal | Maps to section |
|--------|-----------------|
| User's original request or plan | **Goal** |
| Completed tool calls / commits | **Completed** |
| Open TODOs, unfinished tasks | **In Progress / Next Steps** |
| "I chose X because Y", rejected alternatives | **Key Decisions** |
| Approaches tried then abandoned | **Dead Ends** |
| Files created / edited / deleted | **Files Changed** |
| Agent spawns, MCP calls, CRM updates | **External State Changes** |
| Warnings, blockers, risks mentioned | **Context for Next Session** |
| Skills/plugins used or obviously needed next | **Suggested Skills** |

**Purpose tailoring**: if the user passed arguments, treat them as a description
of what the NEXT session will focus on and weight the document accordingly (a
"next session = deploy" handoff prioritizes Current State and external access
details over Dead Ends; a "next session = continue feature X" handoff goes deep
on In Progress and Key Decisions).

### 3. Find the existing handoff FIRST (default: update, not create)

**Never ask whether one exists -- look.** Search `handoffs/` for a handoff covering
this thread and match on substance, not just filename: the topic slug, the branch,
the repo, and the files touched. Read the newest two or three candidates before
deciding.

```bash
ls -t handoffs/*.md | head -20
grep -ril "<repo|feature|component keyword>" handoffs/ | head
```

**If one covers this thread, UPDATE it in place.** Keep its filename, so every
existing link to it still resolves:

- append a dated `## Session {YYYY-MM-DD}` block with the new work
- revise **Current State** and **Next Steps** to be true as of now
- move anything finished out of Next Steps and into Completed
- leave earlier sessions' Dead Ends and Key Decisions intact; they are the value

**Create a new file only when the work genuinely starts a new thread.** When you
do, add a `## Related` section linking the handoffs it continues from, and add a
back-link line in each of those. A thread that has split into standalone files
nobody can find is the failure mode this step exists to prevent.

### 4. Write or update the handoff file

Create the file at: `handoffs/handoff-{YYYY-MM-DD}_{HH-MM}_{topic-slug}.md`

The `{topic-slug}` is a 2-4 word kebab-case summary of the session's primary
goal. Derive it from the Goal section. Keep it short enough to scan in a
directory listing.

Examples:
- `handoff-2026-03-22_21-45_fullstack-seo-pipeline.md`
- `handoff-2026-03-28_02-15_alya-signal-tracking.md`
- `handoff-2026-03-31_03-45_billing-engine.md`

If the `handoffs/` directory doesn't exist in the project root, create it.

Use the template in `references/template.md`. Fill every section. If a section
has nothing to report, write "None" -- do not omit sections.

### 5. Update the index

Maintain `handoffs/INDEX.md`: one row per active thread -- topic, current handoff
path, last updated, one-line status. Update the row you touched, or add one. The
index is how a thread gets found next time; without it a directory of standalone
files is unsearchable and every session starts another one.

| Thread | Handoff | Updated | Status |
|---|---|---|---|
| {topic} | [{filename}](handoff-....md) | {YYYY-MM-DD} | {one line} |

### 6. Summarize to user

After writing the file, print a short confirmation with the file path and the
"Recommended first action" line so the user can verify it before closing.

---

## Guidelines

- **Be specific with file paths** -- always use paths relative to project root
- **Capture "why" over "what"** -- the diff shows what changed; the handoff
  explains why and what alternatives were rejected
- **Dead Ends are the highest-value section** -- they prevent the next session
  from wasting tokens on approaches that already failed
- **External State Changes** -- if MCP tools modified HubSpot, Google Docs,
  sent emails, created calendar events, etc., list them. These cannot be
  inferred from git
- **Depth over brevity -- never truncate to hit a length.** Capture every decision,
  measurement, number, error string and rejected alternative the session produced. A
  handoff that omits a detail to stay short has failed at its only job. Long is fine;
  vague is not.
- **Quote the specifics** -- exact figures, timings, error text, command output,
  `file:line`. "The query was slow" is worthless; "12.6s for the full list, 46.96s for
  the cursor because that column is unindexed" is the handoff.
- **Timestamp decisions** -- if a decision was made partway through the session
  after initial work went a different direction, note that
- **Reference other artifacts by path AND carry the conclusion** (PRDs, plans,
  specs, reports, commits, diffs). A bare path makes the next session re-derive what
  this one already knew; give the finding and the path to its evidence.
- **Redact sensitive information** -- no API keys, passwords, tokens, or client
  PII in the handoff body; name the variable or credential location, never the
  value
