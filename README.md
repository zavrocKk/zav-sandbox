# zav-sandbox — GSANE Framework

[![CI](https://img.shields.io/badge/CI-passing-success)](#) [![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#) [![Tests](https://img.shields.io/badge/Tests-107%20passing-brightgreen)](#) [![MCP](https://img.shields.io/badge/MCP-5%20outils-purple)](#) [![License](https://img.shields.io/badge/License-Unspecified-lightgrey)](#)

## 💡 Qu'est-ce que GSANE ?

**GSANE** (Governance System for AI-Native Execution) est un framework multi-agents fonctionnant directement dans VS Code via GitHub Copilot Chat et la CLI `gsane.sh`. Il orchestre une équipe de 5 agents IA — la **Strike Team** — capables de concevoir, implémenter, tester et documenter du code de manière autonome grâce à une boucle d'amélioration continue : le **Zero-Touch Fix-Loop**.

GSANE est également **MCP-solid** : ses 5 outils MCP locaux sont intégrés au runtime du Master pour les opérations de mémoire compressée, de checkpoint de session, et de routage déterministe vers l'agent approprié.

---

## 🧩 Architecture Strike Team

Le projet repose sur une architecture plate (**Flat Design**) pilotée par 5 agents spécialisés. Pas d'intermédiaires, pas de hiérarchies profondes — chaque agent est autonome et collabore via des signaux P2P.

```mermaid
graph TD
    User((Hôte Humain)) -->|Demande| Master
    Master[🧙 Langis — Master\nOrchestration + DC] -->|Delivery Contract| Dev
    Dev[💻 Amelia — Dev\nTDD + Implémentation] -->|Code + Tests| QA
    QA[🧪 Quinn — QA\nQuality Gate] -->|bash gsane.sh validate| Gate{Exit 0?}
    Gate -- ❌ Échec --> Dev
    Gate -- ✅ Succès --> Arch[📝 ADR + CHANGELOG]
    Master -.->|Party Mode| Bond[🤖 Bond — Agent Builder]
    Master -.->|Design| Winston[🏗️ Winston — Architect]
```

| Agent | Persona | Spécialité |
|---|---|---|
| **Langis** | 🧙 Master | Orchestration, Delivery Contracts, analyse technique |
| **Amelia** | 💻 Dev | Implémentation TDD, code + tests concurrents |
| **Quinn** | 🧪 QA | Exécution Quality Gate, validation `gsane.sh validate` |
| **Winston** | 🏗️ Architect | Design système, ADR, outillage |
| **Bond** | 🤖 Agent Builder | Création/édition/validation des agents GSANE |

---

## 🔌 Intégration MCP

GSANE expose **5 outils MCP locaux** via `_gsane/mcp-server/compression_tool.py` — le point d'entrée unique branché dans VS Code/Copilot Chat.

| Outil | Description |
|---|---|
| `gsane_fetch_compressed_memory` | Recherche dans les fichiers mémoire agents, retourne un extrait compressé pertinent |
| `gsane_write_session_checkpoint` | Sérialise l'état de session dans `session-state.md` (plan actif, décisions, risques) |
| `gsane_read_checkpoint` | Lit le checkpoint pour reprendre une session warm sans relire tout le contexte |
| `gsane_route` | Routage déterministe vers l'agent cible via `delegation-matrix.yaml` (schéma `trigger`/`agent`) |
| `gsane_memory_fetch` | Extrait les learned-lessons d'un agent sidecar spécifique sans charger tout le fichier |

Les chemins sont dérivés de `Path(__file__)` — **indépendants du répertoire de travail du client MCP**.

Pour vérifier l'état de l'intégration MCP :
```bash
bash gsane.sh mcp --health      # Vérifie dépendances, imports et schéma
bash gsane.sh mcp --smoke-test  # Exécute les 5 outils en conditions réelles
```

---

## 👁️ Observabilité

Chaque invocation MCP et chaque événement système GSANE (handoff, circuit breaker, P2P) est journalisé dans `_gsane/_memory/trace.log` :

```bash
bash gsane.sh trace --tail 10    # Derniers 10 événements
bash gsane.sh trace --summary    # Résumé (agents actifs, trust scores, HUP)
bash gsane.sh trace --p2p        # Messages P2P entre agents
```

---

## ⚙️ Prérequis

- **Python 3.10+**
- **Git + Bash** (natif Linux/macOS, ou Git Bash/WSL sous Windows)
- **pytest** — moteur de la Quality Gate
- **GitHub Copilot Chat** — interface de communication avec la Strike Team
- **mcp[cli]** + **pyyaml** — dépendances du serveur MCP local

---

## 🚀 Installation & Setup

```bash
# 1. Cloner le repository
git clone https://github.com/zavrocKk/zav-sandbox.git
cd zav-sandbox

# 2. Créer l'environnement virtuel
python -m venv .venv

# 3. Activer l'environnement
# Windows (PowerShell) :
.venv\Scripts\activate
# Linux/macOS :
source .venv/bin/activate

# 4. Installer les dépendances
pip install pytest
pip install -r _gsane/mcp-server/requirements.txt

# 5. Initialiser le runtime GSANE (crée sidecars, trace.log, dossiers volatiles)
bash _gsane/tools/gsane-bootstrap.sh
```

---

## 🛠️ Commandes CLI

```bash
# Quality Gate — exécute tests + qa-linter + vérification CHANGELOG
bash gsane.sh validate

# Doctor — vérifie l'intégrité de l'environnement
bash gsane.sh doctor

# Observabilité — trace.log
bash gsane.sh trace --tail 10
bash gsane.sh trace --summary
bash gsane.sh trace --p2p

# MCP — santé et smoke test
bash gsane.sh mcp --health
bash gsane.sh mcp --smoke-test
```

---

## 📂 Structure du Workspace

```
_gsane/                    ← Réacteur GSANE
  agents/                  ← Les 5 agents Strike Team (master, dev, qa, architect, bond)
  _config/                 ← Manifestes YAML (agents, workflows, delegation-matrix)
  _memory/                 ← Mémoire persistante (sidecars, trace.log, sessions/)
  mcp-server/              ← Serveur MCP local (compression_tool.py — 5 outils)
  workflows/               ← Workflows (party-mode, delegation, cc-verify, flywheel...)
  tools/                   ← Outils infrastructure (gsane-bootstrap.sh)
_gsane-output/             ← Artefacts générés (delegation-audit, bond-creations, etc.)
tests/                     ← Suite de tests (107 tests : structurel + comportemental + MCP)
docs/architecture/decisions/  ← ADR (Architecture Decision Records)
.github/
  skills/                  ← Skills GSANE pour Copilot Chat
  prompts/                 ← Prompts slash commands (/gsane-*)
  hooks/                   ← Hooks session (session-start, session-stop, flywheel-trigger)
```

---

## 🔗 Liens Utiles

- [🤝 Comment Contribuer (CONTRIBUTING.md)](CONTRIBUTING.md)
- [🤖 Guide des Agents (AGENTS.md)](AGENTS.md)
- [📋 Historique des décisions (ADR-001)](docs/architecture/decisions/ADR-001-flat-design.md)
- [🔌 Documentation MCP Server](_gsane/mcp-server/README.md)
