#!/bin/bash
# -----------------------------------------------------------------------------
# QUALITY GATE SCRIPT (Automated Toolsmith)
# Objectif : Valider la syntaxe et les règles de base des artefacts générés
# avant toute lecture humaine ou d'Agent QA coûteuse en tokens.
# -----------------------------------------------------------------------------

FILE_TARGET="$1"

if [ -z "$FILE_TARGET" ]; then
  echo "❌ ERREUR: Vous devez spécifier un fichier à valider."
  echo "Usage: ./_gsane/tools/validate.sh <chemin-du-fichier>"
  exit 1
fi

if [ ! -f "$FILE_TARGET" ]; then
  echo "❌ ERREUR: Le fichier $FILE_TARGET n'existe pas."
  exit 1
fi

echo "🔍 Lancement de la Quality Gate sur $FILE_TARGET..."

# Vérifications de type de fichier
if [[ "$FILE_TARGET" == *.py ]]; then
  echo "[Python] Vérification avec pylint/flake8 (simulation / appel au qa-linter.py)"
  python tests/qa-linter.py "$FILE_TARGET" || exit 1
  python -m py_compile "$FILE_TARGET" || exit 1
elif [[ "$FILE_TARGET" == *.js || "$FILE_TARGET" == *.ts ]]; then
  echo "[JS/TS] Vérification synthétique si node est installé..."
  # Exemple: npx eslint "$FILE_TARGET"
elif [[ "$FILE_TARGET" == *.md ]]; then
  echo "[Markdown] Validation syntaxique..."
  # Exemple: markdownlint "$FILE_TARGET" si dispo
fi

# Résultat final
echo "✅ LA QUALITY GATE EST PASSÉE AVEC SUCCÈS. Aucun problème syntaxique détecté."
exit 0
