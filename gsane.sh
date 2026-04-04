#!/bin/bash
# -----------------------------------------------------------------------------
# GSANE Core CLI Router
# -----------------------------------------------------------------------------

ACTION=$1

if [ -z "$ACTION" ]; then
    echo "====================================="
    echo "🤖 GSANE CLI - Commandes disponibles :"
    echo "====================================="
    echo "  party-mode    : Copie le prompt Party Mode press-papier"
    echo "  brainstorming : Crée une nouvelle session de Brainstorming"
    echo "  health-check  : Vérifie l'intégrité de la CI et de l'environnement"
    echo "  validate      : (Beta) Parse strict des YAML d'architecture"
    exit 1
fi

case $ACTION in
    party-mode)
        echo "🎉 Préparation du Party Mode..."
        if [ -f "_gsane/core/prompts/party-mode.md" ]; then
            cat _gsane/core/prompts/party-mode.md | clip
            echo "✅ Le prompt Party Mode a été copié dans ton presse-papier !"
            echo "➡️ Ouvre le chat Copilot et fais Ctrl+V pour l'activer."
        else
            echo "❌ Fichier prompt introuvable."
        fi
        ;;
    brainstorming)
        SESSION_DIR="_gsane-output/brainstorming"
        timestamp="'%Y%m%d_%H%M%S'"
        stamp=""
        # avoiding powershell interpolation parsing errors
        stamp=date +%Y%m%d_%H%M%S
        SESSION_FILE="$SESSION_DIR/session-$stamp.md"
        
        echo "🧠 Création d'une nouvelle session de Brainstorming..."
        mkdir -p "$SESSION_DIR"
        
        echo "# 🧠 Cerveau Actif : Session Brainstorming" > "$SESSION_FILE"
        echo "**Date:** date" >> "$SESSION_FILE"
        echo "**Objectif principal :** [À définir]" >> "$SESSION_FILE"
        echo "" >> "$SESSION_FILE"
        echo "## 📌 Idées Brutes" >> "$SESSION_FILE"
        echo "- " >> "$SESSION_FILE"
        
        if command -v code &> /dev/null; then
            code "$SESSION_FILE"
        fi
        
        echo "✅ Session créée et ouverte : $SESSION_FILE"
        ;;
    health-check)
        echo "🩺 Lancement du Diagnostic GSANE..."
        bash .github/hooks/session-start.sh
        ;;
        doctor)
        echo "🩺 GSANE Doctor - Health Check global"
        echo "----------------------------------------"
        echo "1️⃣  Validation des liens morts (via session-start)..."
        bash .github/hooks/session-start.sh
        echo "----------------------------------------"
        echo "2️⃣  Validation hiérarchique des YAML..."
        python -c "
import yaml, glob
files = glob.glob('_gsane/_config/*.yaml')
errors = 0
for f in files:
    try:
        yaml.safe_load(open(f, encoding='utf-8'))
        print(f'  ✅ {f} : OK')
    except Exception as e:
        print(f'  ❌ {f} : ERREUR ({e})')
        errors += 1
if errors > 0: exit(1)
"
        echo "✅ GSANE est sain."
        ;;

    validate)
        echo "🔍 Quality Gate : Exécution de la suite de tests Python..."

        python -m pytest tests/
        EXIT_CODE=$?

        if [ $EXIT_CODE -ne 0 ]; then
            echo "❌ Quality Gate Failed : Des tests ont échoué ! (Code: $EXIT_CODE)"
            exit 1
        fi

        echo "✅ Quality Gate Passed : Tous les tests sont validés !"
        exit 0
        ;;
    *)
        echo "❌ Commande '$ACTION' non reconnue."
        ;;
esac

