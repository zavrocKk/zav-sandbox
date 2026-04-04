# zav-sandbox — GSANE Framework Enhancement Project

**zav-sandbox** est un projet de démonstration et d'amélioration du framework GSANE (Governance System for AI-Native Execution), conçu pour explorer les capacités d'une architecture multi-agents d'élite ("Strike Team") dans un environnement autonome.

## 🚀 Architecture "Strike Team" (Ultra-Lean)

Le projet a évolué vers une architecture plate et ultra-optimisée, abandonnant les structures départementales lourdes au profit d'une équipe de 5 agents d'élite opérant dans une "War Room" centralisée.

### La Strike Team
1. **🧙 Langis (Master)** : L'Orchestrateur et Analyste Technique. Il reçoit les demandes, analyse le code, rédige les *Delivery Contracts* et coordonne la délibération.
2. **💻 Amelia (Dev)** : L'agent de développement. Elle implémente le code métier et les tests unitaires exigés par le contrat.
3. **🧪 Quinn (QA)** : L'Ingénieur Qualité. Elle exécute impitoyablement la *Quality Gate* et s'assure qu'aucun code défaillant ne passe.
4. **🏗️ Winston (Architect)** : L'Expert Système. Il valide les choix architecturaux (ex: gestion des packages Python, imports).
5. **🤖 Bond (Agent Builder)** : Le Bâtisseur d'Agents. Il maintient et valide la conformité des instructions des agents eux-mêmes.

## 📂 Structure du Workspace (Flat Design)

Pour minimiser la fragmentation du contexte (Token Overhead) et maximiser l'attention des LLMs, le projet adopte une structure O(1) :
- _gsane/ : Le réacteur de la Strike Team (configurations, agents, workflows, outils de maintenance).
- src/ : Le code métier fonctionnel (ex: math_utils.py, 	ext_analyzer.py).
- 	ests/ : Les tests unitaires (TDD).

## 🛡️ La Quality Gate

Le cœur de notre automatisation est la commande ash gsane.sh validate. 
Cette porte de qualité formelle exécute notre suite de tests (pytest). Si un test échoue, le processus est bloqué (xit 1) jusqu'à ce que la *"Zéro-Touch Fix-Loop"* des agents corrige l'erreur.
