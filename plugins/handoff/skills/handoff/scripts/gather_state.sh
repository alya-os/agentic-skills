#!/usr/bin/env bash
# Gather git and environment state for handoff document generation.
# Output is plain text sections that the agent reads to populate the template.

set -euo pipefail

echo "=== BRANCH ==="
git branch --show-current 2>/dev/null || echo "(detached HEAD)"

echo ""
echo "=== LAST COMMIT ==="
git log -1 --format="%h %s" 2>/dev/null || echo "(no commits)"

echo ""
echo "=== UNCOMMITTED CHANGES ==="
git status --short 2>/dev/null || echo "(not a git repo)"

echo ""
echo "=== RECENT LOG (last 10) ==="
git log --oneline -10 2>/dev/null || echo "(no history)"

echo ""
echo "=== DIRTY FILE COUNT ==="
DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
echo "$DIRTY files with uncommitted changes"

echo ""
echo "=== STASH ==="
STASH_COUNT=$(git stash list 2>/dev/null | wc -l | tr -d ' ')
if [ "$STASH_COUNT" -gt 0 ]; then
  echo "$STASH_COUNT stashed entries:"
  git stash list
else
  echo "No stashes"
fi
