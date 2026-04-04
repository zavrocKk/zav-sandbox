# zav-sandbox — GSANE Framework

[![CI](https://img.shields.io/badge/CI-passing-success)](#) [![Python](https://img.shields.io/badge/Python-3.14%2B-blue)](#) [![License](https://img.shields.io/badge/License-Unspecified-lightgrey)](#) [![Status](https://img.shields.io/badge/Status-Experimental-orange)](#)

## 💡 Qu'est-ce que GSANE ?
**GSANE** (Governance System for AI-Native Execution) est un framework multi-agents innovant fonctionnant directement à l'intérieur de VS Code (via Copilot Chat et CLI). 
Il orchestre une équipe d'agents IA ("Strike Team") capable de développer, tester et documenter du code de manière totalement autonome grâce à une boucle d'amélioration continue appelée **Zero-Touch Fix-Loop**.

## ⚙️ Prérequis
Pour interagir avec le framework et la Strike Team, vous aurez besoin de :
- **Python 3.14+** (pour l'exécution des outils internes et des tests)
- **Git** et **Bash** (natif sous Linux/macOS, ou via WSL/Git Bash sous Windows)
- **pytest** (le moteur de tests de notre Quality Gate)
- **GitHub Copilot Chat** (l'interface de communication avec les agents)

## 🚀 Installation & Setup Rapide
Clonez le dépôt et installez l'environnement virtuel pour activer les garde-fous de la Strike Team :

`ash
# 1. Cloner le repository
git clone https://github.com/zavrocKk/zav-sandbox.git
cd zav-sandbox

# 2. Créer l'environnement virtuel Python
python -m venv .venv

# 3. Activer l'environnement
# Sous Windows (PowerShell) :
.venv\Scripts\activate
# Sous Linux/macOS (Bash) :
source .venv/bin/activate

# 4. Installer les dépendances (dont pytest)
pip install pytest # ou pip install -r requirements.txt
`

## 🎯 Utilisation (Démo)
La commande fondamentale de GSANE est la **Quality Gate**. Elle vérifie si votre code source, vos tests et votre documentation sont 100% conformes aux lois du projet :

`ash
bash gsane.sh validate
`
*Exemple de sortie : Si un fichier src/ est modifié sans ajout dans CHANGELOG.md, ou si un test pytest échoue, la commande rejettera votre code (Exit 1).*

## 🧩 Architecture "Strike Team" (Ultra-Lean)

Le projet s'appuie sur une architecture plate (O(1)) inspirée de *Grimoire-kit*, éliminant les intermédiaires pour maximiser la vitesse et réduire les coûts en tokens.

`mermaid
graph TD;
    User((Hôte Humain)) -->|Demande de Feature| Langis
    Langis[🧙 Langis - Master] -->|Rédige Delivery Contract| Amelia
    Amelia[💻 Amelia - Dev] -->|Écrit Code + Tests| Quinn
    Quinn[🧪 Quinn - QA] -->|Exécute Quality Gate| Bash[bash gsane.sh validate]
    Bash -- Échec exit 1 --> Quinn
    Quinn -- Reboucle Zero-Touch --> Amelia
    Bash -- Succès exit 0 --> Arch[Archivage ADR & Changelog]
`

## 📂 Structure du Workspace
- _gsane/ : Le réacteur (manifestes, configurations, et les fichiers .md de nos 5 agents).
- src/ : Le code métier (ex: 	ext_analyzer.py).
- 	ests/ : Les tests unitaires propulsés par pytest.
- docs/ : L'historique des décisions d'architecture (ADR).

## 🔗 Liens Utiles
- [🤝 Comment Contribuer ? (CONTRIBUTING.md)](CONTRIBUTING.md)
- [🤖 Liste détaillée des Agents (AGENTS.md)](AGENTS.md)
- [📜 Historique des versions (CHANGELOG.md)](CHANGELOG.md)
