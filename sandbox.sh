#!/bin/bash
# -----------------------------------------------------------------------------
# GSANE Sandbox Entry Point
# -----------------------------------------------------------------------------
# This script mimics the grimoire-init.sh approach inside VS Code Task runners.
# It acts as a universal router for high-level operations without typing 
# complex commands.
# -----------------------------------------------------------------------------

ACTION=$1

if [ -z "$ACTION" ]; then
    echo "Usage: bash sandbox.sh [action]"
    echo "Actions: party-mode, brainstorming, health-check, list-agents"
    exit 1
fi

case $ACTION in
    party-mode)
        echo "🚀 Initialisation du Party Mode [PM]..."
        # Lancement simulé de Party Mode via l'arborescence
        cat _gsane/core/workflows/party-mode/workflow.md | grep -A 5 "name: party-mode"
        echo -e "\n➡️ Tapez '/gsane-master' et demandez le [PM] Party Mode à l'agent."
        ;;
    brainstorming)
        echo "🧠 Initialisation de la Session de Brainstorming [BS]..."
        cat _gsane/core/workflows/brainstorming/workflow.md | grep -A 5 "name: brainstorming"
        echo -e "\n➡️ Tapez '/gsane-master' et demandez '[BS]' ou 'Brainstorming' à l'agent."
        ;;
    health-check)
        echo "🩺 Lancement du Diagnostic GSANE..."
        bash .github/hooks/session-start.sh
        ;;
    list-agents)
        echo "📋 Liste des activateurs d'Agents disponibles (Top 5) :"
        ls -l .github/agents/*.md | head -n 5
        echo "..."
        ;;
    *)
        echo "❌ Action inconnue : $ACTION"
        echo "Actions supportées : party-mode, brainstorming, health-check, list-agents"
        exit 1
        ;;
esac
