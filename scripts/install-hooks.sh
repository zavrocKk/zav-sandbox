#!/bin/sh
# Install git hooks from scripts/hooks/ into .git/hooks/
HOOKS_DIR="$(git rev-parse --show-toplevel)/scripts/hooks"
GIT_HOOKS_DIR="$(git rev-parse --show-toplevel)/.git/hooks"

for hook in "$HOOKS_DIR"/*; do
  name=$(basename "$hook")
  cp "$hook" "$GIT_HOOKS_DIR/$name"
  chmod +x "$GIT_HOOKS_DIR/$name"
  echo "Installed hook: $name"
done

echo "All hooks installed."
