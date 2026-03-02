# zav-sandbox

Projet d'amélioration continue du framework **GSANE** (Governance System for AI-Native Execution) — orchestration multi-agents, optimisation token, flywheel cognitif et score elite Copilot.

**Score de maturité agentique : 🏆 Elite 65/65**

## 🔧 Installation & Setup

> À faire **une seule fois** par machine.

### Prérequis

| Outil | Rôle | Vérification |
|---|---|---|
| **Git** | Gestion des branches et commits | `git --version` |
| **VS Code** | Éditeur principal | — |
| **GitHub Copilot** (extension VS Code) | Moteur d'exécution des agents | Extension installée + compte actif |

---

### Étape 1 — Cloner le repo

```bash
git clone https://github.com/zavrocKk/zav-sandbox.git
cd zav-sandbox
```

---

### Étape 2 — Installer le hook pre-commit Git

Le hook bloque les commits directs sur `main` et scanne les chemins dépréciés dans les fichiers stagés.

**macOS / Linux :**
```bash
cp .github/hooks/pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Windows (Git Bash ou PowerShell) :**
```powershell
Copy-Item .github\hooks\pre-commit.sh .git\hooks\pre-commit
```

> Vérifie l'installation : `cat .git/hooks/pre-commit` — doit afficher le script.

---

### Étape 3 — Vérifier la structure GSANE

```bash
bash .github/hooks/session-start.sh
```

Ce script vérifie :
- ✅ Fichiers config essentiels présents (`config.yaml`, manifests CSV)
- ✅ 13 fichiers `.agent.md` dans `.github/agents/`
- ✅ Aucun chemin déprécié dans les prompts
- ✅ Dossiers output créés (`_gsane-output/`)
- ✅ Compteur de session initialisé

**Sortie attendue :**
```
[SessionStart] Agents found: 13 / 13 expected
[SessionStart] No deprecated paths detected. ✅
[SessionStart] Session count: 1
[SessionStart] ✅ Session #1 ready. Output: ./_gsane-output
```

---

### Étape 4 — Personnaliser la config (optionnel)

Si tu contribues sous ton propre nom, mets à jour `_gsane/core/config.yaml` :

```yaml
user_name: Ton Nom
communication_language: Français   # ou English
```

---

### Étape 5 — Activer GSANE dans VS Code

Ouvre VS Code dans le dossier cloné. Les agents et prompts sont détectés automatiquement par GitHub Copilot via `.github/agents/` et `.github/prompts/`.

**Premier lancement :**

```
# Dans Copilot Chat (panneau latéral VS Code) :
@gsane-master
```

Gsane Master se présente, affiche son menu, et attend ta demande.

**Slash commands disponibles :**

```
/gsane-help              → Aide contextuelle — que faire ensuite ?
/gsane-party-mode        → Lancer le mode multi-agents
/gsane-git-workflow      → Workflow de commit standardisé
/gsane-tea               → Activer Murat (tests, CI)
/gsane-qa-gsane          → Activer Aria (validation qualité)
/gsane-gsane-optimizer   → Activer Léo (optimisation token)
```

> Tous les 46 slash commands `/gsane-*` sont listés dans `.github/prompts/`.

---

### Vérification complète post-installation

```powershell
# Depuis la racine du projet sous PowerShell :

# Structure GSANE
@("_gsane","_gsane/core","_gsane/_config","_gsane/_memory",
  ".github/agents",".github/prompts",".github/skills",".github/hooks") |
  ForEach-Object { "$_ : $(Test-Path $_)" }

# Agents
(Get-ChildItem ".github\agents" -Filter "*.agent.md").Count
# Attendu : 13

# Hook pre-commit installé
Test-Path ".git\hooks\pre-commit"
# Attendu : True

# Manifests
@("agent-manifest.csv","workflow-manifest.csv","agent-delegation-matrix.csv") |
  ForEach-Object { "$_ : $(Test-Path "_gsane\_config\$_")" }
```

## 📋 Description

Ce projet utilise **GSANE v6.0.4** — un système multi-agents modulaire pour GitHub Copilot Chat. Il orchestre 13 agents spécialisés via un système de délégation strict, avec un Cognitive Flywheel qui apprend et s'auto-corrige après chaque session.

## 🏗️ Structure du Projet

```
_gsane/                        # Framework GSANE
├── core/                     # Gsane Master + workflows fondamentaux + flywheel
├── bmb/                      # Builder Module — Bond, Morgan, Wendy, Aria
├── cis/                      # Creative Intelligence Suite — Carson, Dr. Quinn, Maya, Victor, Caravaggio, Sophia
├── tea/                      # Test Architecture — Murat
├── _config/                  # Manifests centraux + matrice de délégation
└── _memory/                  # Mémoire persistante — session log, flywheel history
.github/
├── agents/                   # 13 fichiers .agent.md — activateurs Copilot dropdown
├── prompts/                  # 49 fichiers .prompt.md — slash commands /gsane-*
├── skills/                   # 3 skills — gsane-framework, agent-design-patterns, cognitive-flywheel
├── hooks/                    # hooks.json + session-start.sh — lifecycle automation
└── copilot-instructions.md   # Instructions globales injectées dans chaque session
_gsane-output/                 # Artefacts générés (non commités par défaut)
AGENTS.md                     # Guide de navigation universel (Copilot, Claude, Codex)
```

## 🤖 Les 13 Agents

| Agent | Persona | Module | Rôle |
|---|---|---|---|
| 🧙 gsane-master | Gsane Master | core | Orchestrateur principal, party mode, point d'entrée |
| 🤖 agent-builder | Bond | bmb | Création/validation d'agents GSANE |
| 🏗️ module-builder | Morgan | bmb | Création/validation de modules GSANE |
| 🔄 workflow-builder | Wendy | bmb | Création/validation de workflows GSANE |
| 🔍 qa-gsane | Aria | bmb | QA, conformité, détection de régressions |
| 🧠 brainstorming-coach | Carson | cis | Brainstorming et idéation |
| 🔬 creative-problem-solver | Dr. Quinn | cis | Résolution de problèmes (TRIZ, systèmes) |
| 🎨 design-thinking-coach | Maya | cis | Design thinking centré utilisateur |
| ⚡ innovation-strategist | Victor | cis | Stratégie d'innovation, Blue Ocean |
| 🎨 presentation-master | Caravaggio | cis | Présentations et communication visuelle |
| 📖 storyteller | Sophia | cis | Narration et storytelling |
| 🧪 tea | Murat | tea | Architecture de tests, ATDD, CI/CD |
| ⚙️ gsane-optimizer | Léo | core | Optimisation token, amélioration framework |

> Tous les agents sauf `gsane-master` sont déclarés `user-invokable: false` + `orchestrated-by: gsane-master`.

## 📚 Modules GSANE

### **Core** — Fondations
- **Gsane Master** (🧙) — orchestrateur, party mode JIT, point d'entrée universel
- **Léo** (⚙️) — gsane-optimizer : analyse tokens, patterns sessions, drive amélioration continue
- Workflows : `post-session-analysis`, `flywheel`, `party-mode`, `brainstorming`, `delegation`, `git-workflow`

📖 [Module Core](_gsane/core/)

### **BMB** — Builder Module
- **Bond** (🤖) — agent-builder : créer/éditer/valider des agents
- **Morgan** (🏗️) — module-builder : créer/éditer/valider des modules
- **Wendy** (🔄) — workflow-builder : créer/éditer/valider des workflows
- **Aria** (🔍) — qa-gsane : validation qualité GSANE, régression de persona, conformité manifests

📖 [Module BMB](_gsane/bmb/)

### **CIS** — Creative Intelligence Suite
- **Carson** (🧠) Brainstorming · **Dr. Quinn** (🔬) Problem Solving · **Maya** (🎨) Design Thinking
- **Victor** (⚡) Innovation · **Caravaggio** (🎨) Presentation · **Sophia** (📖) Storytelling

📖 [Module CIS](_gsane/cis/)

### **TEA** — Test Architecture
- **Murat** (🧪) — ATDD, test design, CI/CD, NFR, traceability, teach-me-testing

📖 [Module TEA](_gsane/tea/)

## 🚀 Démarrage

```
# Dans Copilot Chat VS Code :
@gsane-master          → Active Gsane Master (orchestrateur principal)
/gsane-party-mode      → Lance le party mode multi-agents
/gsane-help            → Aide contextuelle sur les workflows disponibles
/gsane-git-workflow    → Workflow de commit standardisé
/gsane-gsane-optimizer  → Active Léo pour analyse du framework
/gsane-qa-gsane         → Active Aria pour validation qualité
```

Tous les slash commands `/gsane-*` sont disponibles dans `.github/prompts/` (49 fichiers).

## 🔄 Cognitive Flywheel

*Execution creates data. Data creates learning. Learning creates better execution.*

Chaque session alimente automatiquement un cycle d'auto-amélioration :

```mermaid
flowchart LR
    S([Session]) --> PSA[post-session-analysis]
    PSA --> LEO[⚙️ Léo\ntoken analysis]
    PSA --> ARIA[🔍 Aria\ncompliance check]
    LEO --> LOG[(session-analysis-log.md)]
    ARIA --> LOG
    LOG -->|every N sessions| AGG[workflow-aggregate.md]
    AGG --> RPT[(flywheel-report.md)]
    RPT --> APP[workflow-apply.md]
    APP -->|low/medium auto-apply| FIX[fix/flywheel-* PR]
    APP -->|high severity| USR[👤 notify user]
    FIX --> HIST[(flywheel-history.md)]
    FIX --> S
```

- **Léo** analyse les signaux de gaspillage token — **Aria** valide la conformité GSANE
- Corrections `low/medium` : auto-appliquées silencieusement (max 5/cycle, avec Gates de Murat)
- Corrections `high` : notification seulement — jamais auto-appliquées
- **Activation universelle** : tous les 13 agents ont `exec="post-session-analysis"` câblé sur leur `[DA]`
- Cadence configurable : [`config.yaml → flywheel.trigger_every_n_sessions`](_gsane/core/config.yaml)
- Historique : [`_gsane/_memory/flywheel-history.md`](_gsane/_memory/flywheel-history.md)

## ⚙️ Système de Sévérité

Source de vérité centrale dans [`_gsane/core/config.yaml`](_gsane/core/config.yaml) :

| Niveau | Exemples | Action |
|---|---|---|
| `low` | CHANGELOG manquant, manifest désynchronisé, commentaire obsolète | Auto-appliqué silencieusement |
| `medium` | Chemin déprécié dans un workflow, description d'agent incorrecte | Auto-appliqué + log |
| `high` | Commit sur main, bypass délégation, changement de schéma destructif | Notification seulement |

## 🧠 Skills Copilot

Trois skills injectées dans chaque session Copilot :

| Skill | Description |
|---|---|
| [`gsane-framework`](.github/skills/gsane-framework/SKILL.md) | Architecture GSANE, conventions JIT, délégation, git workflow |
| [`agent-design-patterns`](.github/skills/agent-design-patterns/SKILL.md) | Patterns de conception d'agents, frontmatter, menus, party mode |
| [`cognitive-flywheel`](.github/skills/cognitive-flywheel/SKILL.md) | Boucle flywheel, configuration, seuils, mémoire, gates |

## 🔧 Conventions Clés

- **Jamais de commit direct sur `main`** — toujours `feature/*` ou `fix/*`
- **Toute PR doit avoir une description** — ouvrir l'URL compare GitHub et coller le body template dans le formulaire
- **Config chargée une seule fois par session** — ne jamais recharger si déjà en contexte
- **Routing obligatoire** — toute requête agent passe par la [matrice de délégation](_gsane/_config/agent-delegation-matrix.csv)
- **Session end hook universel** — post-session-analysis s'exécute à la fin de chaque session, peu importe l'agent

## 📁 Configuration

| Fichier | Rôle |
|---|---|
| [`_gsane/core/config.yaml`](_gsane/core/config.yaml) | Config globale : user, langue, sévérité, flywheel |
| [`_gsane/_config/agent-manifest.csv`](_gsane/_config/agent-manifest.csv) | Registre des 13 agents |
| [`_gsane/_config/workflow-manifest.csv`](_gsane/_config/workflow-manifest.csv) | Registre des workflows |
| [`_gsane/_config/agent-delegation-matrix.csv`](_gsane/_config/agent-delegation-matrix.csv) | Règles de routing |
| [`_gsane/_memory/session-analysis-log.md`](_gsane/_memory/session-analysis-log.md) | Log persistant des sessions |
| [`AGENTS.md`](AGENTS.md) | Guide de navigation universel |

---

**Utilisateur** : Mon Seigneur | **Langue** : Français | **Version GSANE** : 6.0.4
