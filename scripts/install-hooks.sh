#!/bin/sh
# Install git hooks from scripts/hooks/ into .git/hooks/
set -e

# Verify we are inside a git repository
git rev-parse --is-inside-work-tree > /dev/null 2>&1 || { echo "Error: not inside a git repository."; exit 1; }

HOOKS_DIR="$(git rev-parse --show-toplevel)/scripts/hooks"
GIT_HOOKS_DIR="$(git rev-parse --show-toplevel)/.git/hooks"

for hook in "$HOOKS_DIR"/*; do
  name=$(basename "$hook")
  cp "$hook" "$GIT_HOOKS_DIR/$name"
  chmod +x "$GIT_HOOKS_DIR/$name"
  echo "Installed hook: $name"
done

echo "All hooks installed."
