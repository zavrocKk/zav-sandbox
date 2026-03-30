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
    validate)
        echo "🔍 Validation statique des manifestes YAML..."
        python -c "
import yaml, glob
files = glob.glob('_gsane/_config/*.yaml')
for f in files:
    try:
        yaml.safe_load(open(f, encoding='utf-8'))
        print(f'✅ {f} : OK')
    except Exception as e:
        print(f'❌ {f} : ERREUR ({e})')
"
        ;;
    *)
        echo "❌ Commande '$ACTION' non reconnue."
        ;;
esac
