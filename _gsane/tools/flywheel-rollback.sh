#!/usr/bin/env bash
# Flywheel Rollback Tool — GSANE
# Usage:
#   bash _gsane/tools/flywheel-rollback.sh pre-tag        → Crée un tag avant auto-correction
#   bash _gsane/tools/flywheel-rollback.sh rollback <tag>  → Reviens à l'état du tag
#   bash _gsane/tools/flywheel-rollback.sh verify          → Exécute les tests, revert si échec

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

HISTORY_FILE="_gsane/_memory/flywheel-history.md"
FAILURE_MUSEUM="_gsane/_memory/failure-museum.md"

CMD="${1:-}"

case $CMD in
    pre-tag)
        TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
        TAG="gsane-flywheel-pre-${TIMESTAMP}"
        git tag "$TAG"
        echo "✅ Tag créé : $TAG"

        # Logge dans flywheel-history.md
        if [ ! -f "$HISTORY_FILE" ]; then
            mkdir -p "$(dirname "$HISTORY_FILE")"
            printf '# Flywheel History\n\n' > "$HISTORY_FILE"
        fi
        printf '\n- **Tag**: %s — Correction flywheel en cours\n' "$TAG" >> "$HISTORY_FILE"
        echo "📝 Tag loggé dans $HISTORY_FILE"
        ;;

    rollback)
        TAG="${2:-}"
        if [ -z "$TAG" ]; then
            echo "Usage: bash _gsane/tools/flywheel-rollback.sh rollback <tag>"
            echo "Tags disponibles:"
            git tag -l "gsane-flywheel-pre-*" 2>/dev/null || echo "  (aucun tag trouvé)"
            exit 1
        fi

        # Vérifie que le tag existe
        if ! git rev-parse "$TAG" >/dev/null 2>&1; then
            echo "❌ Tag '$TAG' introuvable."
            exit 1
        fi

        TAG_COMMIT="$(git rev-parse "$TAG")"
        HEAD_COMMIT="$(git rev-parse HEAD)"

        if [ "$TAG_COMMIT" = "$HEAD_COMMIT" ]; then
            echo "⚠️  HEAD est déjà au commit du tag $TAG — rien à revert."
            exit 0
        fi

        echo "🔄 Rollback vers le tag $TAG..."
        git revert --no-commit "$TAG_COMMIT..HEAD"
        echo "✅ Rollback appliqué (non committé). Vérifiez les changements avant de committer."
        ;;

    verify)
        echo "🧪 Exécution des tests de vérification..."
        if python -m pytest tests/ -m "not behavioral"; then
            echo "✅ Tests passés — aucune régression détectée."
            exit 0
        else
            echo "❌ Tests échoués — rollback automatique en cours..."

            # Trouver le dernier tag gsane-flywheel-pre-*
            LAST_TAG="$(git tag -l 'gsane-flywheel-pre-*' --sort=-creatordate 2>/dev/null | head -n 1)"
            if [ -z "$LAST_TAG" ]; then
                echo "❌ Aucun tag gsane-flywheel-pre-* trouvé pour rollback."
                echo "   Intervention manuelle requise."
                exit 1
            fi

            echo "🔄 Rollback vers $LAST_TAG..."
            TAG_COMMIT="$(git rev-parse "$LAST_TAG")"
            HEAD_COMMIT="$(git rev-parse HEAD)"

            if [ "$TAG_COMMIT" != "$HEAD_COMMIT" ]; then
                git revert --no-commit "$TAG_COMMIT..HEAD"
            fi

            # Log dans failure-museum.md
            if [ ! -f "$FAILURE_MUSEUM" ]; then
                mkdir -p "$(dirname "$FAILURE_MUSEUM")"
                printf '# Failure Museum — GSANE\n\n' > "$FAILURE_MUSEUM"
            fi
            FM_DATE="$(date +%Y-%m-%d)"
            cat >> "$FAILURE_MUSEUM" <<EOF

## FM-AUTO — Flywheel auto-correction rollback
- **Date**: ${FM_DATE}
- **Sévérité**: high
- **Agent(s) impliqué(s)**: Flywheel (Master)
- **Description**: Auto-correction flywheel a causé des régressions de tests
- **Cause racine**: Correction appliquée a introduit un breaking change
- **Correctif**: Rollback automatique vers tag ${LAST_TAG}
- **Règle ajoutée**: Verify gate dans flywheel-rollback.sh
EOF
            echo "📝 Échec loggé dans $FAILURE_MUSEUM"
            echo "❌ Rollback exécuté. Severity escaladée → HIGH."
            exit 1
        fi
        ;;

    *)
        echo "Usage: bash _gsane/tools/flywheel-rollback.sh <command>"
        echo "Commands:"
        echo "  pre-tag          Crée un tag git avant auto-correction"
        echo "  rollback <tag>   Revert au commit du tag spécifié"
        echo "  verify           Exécute les tests, rollback automatique si échec"
        exit 1
        ;;
esac
