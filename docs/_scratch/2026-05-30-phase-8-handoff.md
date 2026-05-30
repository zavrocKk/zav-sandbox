---
type: handoff-prompt
date: 2026-05-30
target-phase: "8"
topic: skills techniques
---

# Prompt de passation — Phase 8 (Skills techniques)

> Copier-coller le bloc ci-dessous pour démarrer la Phase 8 dans une session neuve.
> Auto-suffisant : un agent sans historique peut reprendre.

```text
/light

Contexte : framework "Agentic Team" — orchestration multi-personas 100% markdown,
mono-session, natif VS Code + GitHub Copilot, ZÉRO dépendance/install. Boussole =
VISION.md (6 filtres : pour-qui DevOps/SRE • markdown lisible non-dev • VSCode+Copilot
natif • pas de dev senior requis • anti-drift • livrables markdown dans docs/).

ÉTAT DU PROJET (phases closes) :
- Phases 0 → 6 closes. Phase 6 = Party Mode (Panel défaut + Débat /debate).
- Phase 7 (Mémoire persistante) livrée et mergée (PR #108) :
  • Note de cadrage : docs/architecture/2026-05-30-phase-7-persistent-memory.md
  • Mécanisme : checkpoints markdown dans docs/_scratch/memory/<thread-slug>.md
    (1 fichier par fil, versionné, front-matter YAML + 6 rubriques).
    Template : agents/templates/memory-checkpoint.md
  • Orchestrateur câblé : commande /checkpoint + section "Mémoire persistante"
    (lecture-au-démarrage scopée par `thread`, écriture hybride manuel + auto à
    saturation). Règle binaire de scoping : ne JAMAIS recharger un fil sans rapport.
  • Hooks VS Code OPT-IN (OFF par défaut) dans agents/hooks/ : security-guard
    (PreToolUse → ask sur commandes destructives), memory-nudge (PreCompact/Stop
    → rappel /checkpoint). SessionStart et Stop-block écartés (risque).

OBJECTIF PHASE 8 — Skills techniques :
Ajouter des "skills" = modules markdown de connaissance/méthodologie qu'un persona
peut invoquer dans n'importe quel workflow, SANS dupliquer les workflows existants.

AVANT TOUT CODE (obligatoire, comme Phases 6 et 7) :
Produire d'abord une NOTE DE CADRAGE d'architecture
(docs/architecture/YYYY-MM-DD-phase-8-skills.md) qui tranche :
1. Qu'est-ce qu'une "skill" vs un workflow vs un persona ? (frontière nette)
2. Format/structure d'un fichier skill (front-matter ? sections imposées ?
   emplacement : agents/skills/ ?).
3. Mécanique d'invocation : comment l'orchestrateur/persona charge une skill au
   bon moment sans surcharger le contexte (lien avec budgets tiny/small/medium/deep).
4. Liste priorisée des skills candidates et critère de sélection de la 1ère.

SKILLS CANDIDATES (ROADMAP Phase 8) :
- Helm / Kubernetes • Terraform / IaC • GitHub Actions / GitLab CI • AWS (EKS, ECS,
  IAM…) • Observabilité (Prometheus, Datadog, Splunk) • Java/Python (analyse stack
  traces) • Méthodologies (5 Pourquoi Toyota, RCA, RACI).

⛔ RÈGLE DE CRÉATION (binaire) : ne créer AUCUNE skill par anticipation. Avant chaque
skill, DEMANDER à l'utilisateur quel outil il utilise réellement dans son contexte,
et ne créer que celles confirmées. Pas de skill « au cas où » (anti-bloat).

PRÉ-REQUIS LIVRÉ (Phase 8.1 — garde-fous pré-PR) :
- Checklist agents/checklists/pre-pr.md + commande /pre-pr : à dérouler AVANT toute
  PR (working tree propre, pas de branche orpheline, pas de PR ouverte en double,
  ROADMAP/README/VISION/IDEAS à jour ; CHANGELOG généré par release-please, jamais
  édité à la main).

ENTRÉES IDEAS.md À RELIRE (déjà flaggées Phase 8) :
- "Personas découvrables → promus en skills ?" (2025-05-02)
- "pentest-remediation : skill plutôt que workflow" (2026-05-02)
- "workflow problem-resolution (5 Pourquoi/Ishikawa) : workflow OU skill ?" (2026-05-02)
- F5 "Connexion native aux outils (MCP/APIs)" (2026-05-09) — vérifier si une skill
  doit cadrer l'usage d'outils externes SANS casser le filtre "rien à installer".

CONTRAINTES DE PÉRIMÈTRE :
- Une skill DOIT passer les 6 filtres VISION. Pas d'infra, pas de runtime.
- Réutiliser les conventions existantes : front-matter YAML + corps markdown (comme
  personas/workflows/templates). Pas de nouveau format.
- Mettre à jour : ROADMAP.md (Phase 8), table de localisation de
  .github/copilot-instructions.md si un nouveau type d'artefact apparaît, README.md
  (arbre du dépôt), et le bloc <skills> du système si pertinent.
- Git : brancher feat/phase-8-skills, PR, JAMAIS de push direct sur main (hook
  pre-push bloque). Commits conventionnels en anglais. Respecter la checklist
  pré-PR (agents/checklists/pre-pr.md, commande /pre-pr) AVANT d'ouvrir la PR.

RÉFÉRENCES UTILES :
- Fichiers clés : .github/agents/orchestrator.agent.md (mapping demande→workflow,
  commandes spéciales), agents/personas/*.md, agents/workflows/*.md, VISION.md, IDEAS.md.
- Format skill existant dans l'écosystème : SKILL.md (description + instructions +
  file pointer) — pattern à évaluer pour cohérence avec les skills natives VS Code.

Démarre par PRE-FLIGHT (ANALYSE → PLAN → CONFIRM). Pose des questions si la frontière
skill/workflow/persona ou le format d'invocation est ambigu AVANT de coder.
```
