---
name: gsane-session-bootstrap
description: "Affiche une carte de bootstrap canonique : brief humain, contrat actif, snapshot MCP derive du repo, puis git. A utiliser en debut de session sans relire les vieilles sessions comme verite du present."
applyTo: "**"
---

Exécute ce bootstrap de session silencieusement, puis affiche la carte de statut structurée ci-dessous. Pas de questions — juste lire et afficher.

## STEP 1 — Charger le brief canonique humain

Lire `{project-root}/_gsane/_memory/project-context.md` ou appeler `gsane_read_canonical_brief()` → extraire :
- `{project_name}` — nom du projet
- `{project_mission}` — mission durable en 1 phrase
- `{project_invariants}` — 2-3 invariants du runtime
- `{sources_of_truth}` — brief, contrat actif, vues MCP canoniques

## STEP 2 — Charger l'état courant canonique

Appeler `gsane_read_active_delivery_contract()` et `gsane_read_project_snapshot()` → extraire :
- `{active_task_id}`
- `{active_owner}`
- `{active_validation_agent}`
- `{active_risk_level}`
- `{architecture}`
- `{active_agents}`
- `{audit_continuity}` — statut des fichiers d'audit (`session-state.md`, `session-analysis-log.md`)

Si aucun contrat actif n'est disponible → afficher `Aucun Delivery Contract actif`.

## STEP 3 — Vérifier l'état git

Exécuter `git log --oneline -5` et `git status --short` pour obtenir :
- `{recent_commits}` — 5 derniers commits (hash + message)
- `{git_status}` — fichiers modifiés/non commités
- `{active_branch}` — branche git active

## STEP 4 — Afficher la carte de statut

Afficher en {communication_language} :

```
╔════════════════════════════════════════════════════════════╗
║  🧙 GSANE SESSION BOOTSTRAP                                ║
╚════════════════════════════════════════════════════════════╝

📦 BRIEF CANONIQUE
  Nom       : {project_name}
  Mission   : {project_mission}
  Invariants: {project_invariants}
  Vérités   : {sources_of_truth}

🧭 CONTRAT ACTIF
  Task ID    : {active_task_id}
  Owner      : {active_owner}
  Validation : {active_validation_agent}
  Risque     : {active_risk_level}

🛰️ SNAPSHOT MCP CANONIQUE
  Architecture : {architecture}
  Agents actifs: {active_agents}
  Audit        : {audit_continuity}

🌿 GIT
  Branche : {active_branch}
  Statut  : {git_status}

  Derniers commits :
  {recent_commits}

💡 SUGGESTION
  {si active_task_id disponible: "Lire les AC du contrat actif et executer le lot en cours" sinon "Tape [SR] pour demarrer intelligemment"}

📌 Actions : ▷ Lire le contrat actif · ▷ SR Smart Router · ▷ SS Session Solo · ▷ PM Party Mode
```

Si aucun contrat actif n'est disponible → afficher à la place :
```
🧙 Aucun contrat actif detecte. Lis le brief canonique, puis tape [SR] pour que GSANE detecte automatiquement le meilleur mode selon ton besoin, ou choisis directement : [SS] · [BS] · [PM].
```
