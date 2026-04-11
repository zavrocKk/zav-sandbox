#!/bin/bash
# PR Body Check — Vérifie que le body de PR est substantiel avant merge

PR_BODY="${1:-}"
TEMPLATE_FILE=".github/pull_request_template.md"

if [ -z "$PR_BODY" ]; then
  echo "❌ PR body vide — description obligatoire"
  echo "   Utiliser le template : $TEMPLATE_FILE"
  exit 1
fi

# Normaliser (trim + collapse whitespace)
BODY_NORM=$(echo "$PR_BODY" | tr -s '[:space:]' ' ' | sed 's/^ //;s/ $//')
TMPL_NORM=$(cat "$TEMPLATE_FILE" 2>/dev/null | tr -s '[:space:]' ' ' | sed 's/^ //;s/ $//')

if [ "$BODY_NORM" = "$TMPL_NORM" ]; then
  echo "❌ PR body identique au template — remplir la description avant merge"
  exit 1
fi

WORD_COUNT=$(echo "$PR_BODY" | wc -w)
if [ "$WORD_COUNT" -lt 20 ]; then
  echo "⚠️  PR body trop court ($WORD_COUNT mots) — minimum recommandé : 20 mots"
  exit 1
fi

echo "✅ PR body OK ($WORD_COUNT mots)"
exit 0
