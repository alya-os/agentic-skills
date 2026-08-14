---
name: primer
description: Prime Claude with full project context at the start of a new session. Reads CLAUDE.md, README.md, and key project files, then summarizes the project structure, purpose, goals, key files, dependencies, and configuration. Use at session start to catch Claude up to speed on any project. Triggers on requests like "prime the context", "catch up on this project", "read the project", "prime yourself", "/prime", or any request to understand the codebase before starting work.
---

# Primer

## Workflow

1. Read `CLAUDE.md` if it exists — this is the primary source of AI instructions and project conventions
2. Read `README.md` to understand the project purpose and setup
3. Explore key files:
   - Entry points (e.g., `index.js`, `main.py`, `app.py`, `src/index.ts`)
   - Config files (e.g., `package.json`, `pyproject.toml`, `.env.sample`, `docker-compose.yml`)
   - Any other files that seem central to the project based on the directory structure
4. Report back with a concise summary covering:
   - **Project purpose and goals**
   - **Project structure** — top-level directories and what they contain
   - **Key files** and their roles
   - **Important dependencies**
   - **Important configuration** — env vars, secrets, external services
