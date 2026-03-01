# zav-sandbox

Terrain de jeu pour me développer avec le framework **BMAD** (Breakthrough Methodology for Adaptive Delivery).

## 📋 Description

Ce projet utilise **BMAD** — une méthodologie de framework multimodule conçue pour l'orchestration intelligente de workflows, agents et tâches. Il combine des capacités avancées de brainstorming, résolution de problèmes, design thinking et innovation stratégique en un système cohérent et extensible.

## 🏗️ Structure du Projet

```
_bmad/
├── core/                 # Module Core - Agents et workflows fondamentaux
├── bmb/                  # Module BMB - Builder (création d'agents, modules, workflows)
├── cis/                  # Module CIS - Creative Innovation Suite (brainstorming, design thinking)
├── tea/                  # Module TEA - Test Architecture (architecture et tests)
├── _config/              # Configuration centrale et manifests
└── _memory/              # Mémoire d'exécution et state management
_bmad-output/            # Artefacts générés par les workflows
```

## 📚 Modules BMAD

### **Core** - Fondations
- Agents de base et système de workflow central
- Tâches d'exécution (orchestration, indexation, review)
- Workflows avancés (brainstorming, party-mode, elicitation)

📖 [Documentation Core](_bmad/core/)

### **BMB** - Builder Module
Création d'agents, modules et workflows personnalisés
- Agent Builder - Créer des agents avec persona et capabilities
- Module Builder - Développer des modules BMAD complets
- Workflow Builder - Concevoir des workflows complexes

📖 [Documentation BMB](_bmad/bmb/)

### **CIS** - Creative Innovation Suite
Suite de créativité et innovation pour résolution de problèmes
- Brainstorming Coach
- Design Thinking Coach
- Creative Problem Solver
- Innovation Strategist
- Presentation Master
- Storyteller

📖 [Documentation CIS](_bmad/cis/)

### **TEA** - Test Architecture
Framework d'architecture et tests
- Test Architecture patterns
- Knowledge indexing
- Validation workflows

📖 [Documentation TEA](_bmad/tea/)

## 🚀 Démarrage

Pour accéder aux agents BMAD directement :
- Ouvrez **Copilot Chat** dans VS Code
- Tapez `/bmad-` pour voir tous les workflows et agents disponibles

## 📁 Artefacts Générés

Les outputs des workflows sont générés dans `_bmad-output/` :
- `bmb-creations/` - Agents et modules créés par BMB
- `test-artifacts/` - Artefacts de test générés par TEA

## 🔄 Fichiers de Configuration

- [`_bmad/_config/`](_bmad/_config/) - Manifests centraux et configurations
- [`_bmad/_memory/`](_bmad/_memory/) - État et mémoire d'exécution
- [`_tmad/core/config.yaml`](_bmad/core/config.yaml) - Configuration du mode BMAD

---
## 🔄 Cognitive Flywheel

*Execution creates data. Data creates learning. Learning creates better execution. The cycle never ends.*

Chaque session alimente automatiquement un cycle d'auto-amélioration :

```
SESSION  →  post-session-analysis  →  session-analysis-log.md
   ↑                                          ↓ (toutes les 5 sessions)
   └─ Skills enrichis ─ Prompts affinés ─ workflow-aggregate → flywheel-report.md
      Workflows patchs ─ Manifests syncés ─   workflow-apply → fix/flywheel-* PR
```

- **Léo** analyse les patterns de tokens — **Aria** valide la conformité
- Corrections `low/medium` appliquées automatiquement (max 5/cycle)
- Corrections `high` → notification seulement, décision manuelle
- Historique dans `_bmad/_memory/flywheel-history.md`
- Cadence configurable : `config.yaml → flywheel.trigger_every_n_sessions`

---
## 🧪 Testing & Validation

This project includes comprehensive systems for:
- **[Git Workflow](_bmad/core/workflows/git-workflow/workflow.md)** - Standardized commits with feature/fix branches
- **[CHANGELOG.md](CHANGELOG.md)** - Centralized change tracking integrated into Git Workflow
- **[Agent Delegation](_bmad/core/workflows/delegation/workflow.md)** - Intelligent request routing to appropriate agents

All changes follow the Git Workflow Steps 1-6, including mandatory Step 3.5 (CHANGELOG update).

---

**Utilisateur** : Mon Seigneur  
**Langue** : Français  
**Version BMAD** : 6.0.4
