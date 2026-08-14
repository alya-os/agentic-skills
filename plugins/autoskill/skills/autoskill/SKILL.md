---
name: autoskill
description: |
  Analyze coding sessions to detect corrections and preferences, then propose
  targeted improvements to the skills in your own workspace. Edits stay local:
  nothing is pushed to any upstream repo.

  Use when the user asks to "learn from this session", "update skills",
  "remember this pattern", or "improve this skill".
---

# Autoskill - Session Learning System

This skill analyzes coding sessions to extract durable preferences from corrections and approvals, then proposes targeted updates to Skills that were active during the session. It acts as a learning mechanism across sessions, ensuring Claude improves based on feedback.

The user triggers autoskill after a session where Skills were used. The skill detects signals, filters for quality, maps them to the relevant Skill files, and proposes minimal, reversible edits for review.

---

## When to Activate

**Trigger on explicit requests:**
- "autoskill", "learn from this session", "update skills from these corrections"
- "remember this pattern", "make sure you do X next time"

**Do NOT activate for:**
- One-off corrections or when the user declines skill modifications

---

## Signal Detection

Scan the session for:

### Corrections (highest value)
- "No, use X instead of Y"
- "We always do it this way"
- "Don't do X in this codebase"

### Repeated Patterns (high value)
- Same feedback given 2+ times
- Consistent naming/structure choices across multiple files

### Approvals (supporting evidence)
- "Yes, that's right"
- "Perfect, keep doing it this way"

### Ignore
- Context-specific one-offs ("use X here" without "always")
- Ambiguous feedback
- Contradictory signals (ask for clarification instead)

---

## Signal Quality Filter

Before proposing any change, ask:

1. Was this correction repeated, or stated as a general rule?
2. Would this apply to future sessions, or just this task?
3. Is it specific enough to be actionable?
4. Is this **new information** I wouldn't already know?

> **Only propose changes that pass all four.**

---

### What Counts as "New Information"

**Worth capturing:**
- Project-specific conventions ("we use `cn()` not `clsx()` here")
- Custom component/utility locations ("buttons are in `@/components/ui`")
- Team preferences that differ from defaults ("we prefer explicit returns")
- Domain-specific terminology or patterns
- Non-obvious architectural decisions ("auth logic lives in middleware, not components")
- Integrations and API quirks specific to this stack

**NOT worth capturing (I already know this):**
- General best practices (DRY, separation of concerns)
- Language/framework conventions (React hooks rules, TypeScript basics)
- Common library usage (standard Tailwind classes, typical Next.js patterns)
- Universal security practices (input validation, SQL injection prevention)
- Standard accessibility guidelines

> **If I'd give the same advice to any project, it doesn't belong in a skill.**

---

## Mapping Signals to Skills

Match each signal to the Skill that was active and relevant during the session:

| Signal Type | Action |
|-------------|--------|
| Signal relates to active Skill | Update that Skill's `SKILL.md` |
| 3+ related signals don't fit any active Skill | Propose a new Skill |
| Signal doesn't map to any Skill used | Ignore |

---

## Proposing Changes

For each proposed edit, provide:

```
File: path/to/SKILL.md
Section: [existing section or "new section: X"]
Confidence: HIGH | MEDIUM

Signal: "[exact user quote or paraphrase]"

Current text (if modifying):
> existing content

Proposed text:
> updated content

Rationale: [one sentence]
```

**Group proposals by file. Present HIGH confidence changes first.**

---

## Review Flow

Always present changes for review before applying. Format:

```markdown
## Autoskill Summary

Detected [N] durable preferences from this session.

### HIGH confidence (recommended to apply)
- [change 1]
- [change 2]

### MEDIUM confidence (review carefully)
- [change 3]

Apply high confidence changes? [y/n/selective]
```

**Wait for explicit approval before editing any file.**

---

## Applying Changes

When approved:

1. Edit the target file with minimal, focused changes
2. If git is available, commit with message: `chore(autoskill): [brief description]`
3. Report what was changed

**Script conventions**: Python scripts should use `uv` with inline dependencies (PEP 723), not bare `python3`.

---

## Constraints

| Rule | Description |
|------|-------------|
| No deletions | Never delete existing rules without explicit instruction |
| Additive preferred | Prefer additive changes over rewrites |
| Atomic changes | One concept per change (easy to revert) |
| Preserve structure | Maintain existing file structure and tone |
| Uncertain = MEDIUM | When uncertain, downgrade to MEDIUM confidence and ask |

---

## Workflow Diagram

```
Session Ends
     |
     v
[Scan for Signals] --> Corrections, Patterns, Approvals
     |
     v
[Quality Filter] --> Pass all 4 questions?
     |                      |
     | Yes                  | No
     v                      v
[Map to Skills]         [Ignore]
     |
     v
[Generate Proposals] --> HIGH / MEDIUM confidence
     |
     v
[Present for Review]
     |
     v
[User Approves?] --> y/n/selective
     |
     v
[Apply & Commit]
```

---

## Example Session

**User corrections during session:**
1. "No, we always use `@/lib/utils` for utility functions, not `@/utils`"
2. "Don't use `console.log` - we have a logger at `@/lib/logger`"
3. "Perfect, that's the right way to structure the API routes"

**Autoskill analysis:**

```markdown
## Autoskill Summary

Detected 2 durable preferences from this session.

### HIGH confidence (recommended to apply)

**Change 1:**
File: .claude/skills/frontend-design/SKILL.md
Section: new section: Project Conventions
Confidence: HIGH

Signal: "we always use `@/lib/utils` for utility functions, not `@/utils`"

Proposed text:
> ## Project Conventions
> - Utility functions: Always import from `@/lib/utils`, not `@/utils`

Rationale: Project-specific import path convention stated as universal rule.

---

**Change 2:**
File: .claude/skills/frontend-design/SKILL.md
Section: new section: Project Conventions
Confidence: HIGH

Signal: "Don't use `console.log` - we have a logger at `@/lib/logger`"

Proposed text:
> - Logging: Use `@/lib/logger` instead of `console.log`

Rationale: Project-specific logging convention explicitly stated.

Apply high confidence changes? [y/n/selective]
```
