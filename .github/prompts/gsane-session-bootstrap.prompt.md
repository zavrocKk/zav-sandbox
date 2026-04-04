---
name: gsane-session-bootstrap
description: "Affiche une carte de statut de session complète : projet, dernier état, git, et prochaine action suggérée. À utiliser en début de session pour reprendre là où on s'était arrêté."
applyTo: "**"
---

Exécute ce bootstrap de session silencieusement, puis affiche la carte de statut structurée ci-dessous. Pas de questions — juste lire et afficher.

## STEP 1 — Charger le contexte projet

Lire `{project-root}/_gsane/_memory/project-context.md` → extraire :
- `{project_name}` — nom du projet
- `{project_objective}` — objectif en 1 phrase
- `{current_phase}` — phase ou sprint actuel
- `{active_branch}` — branche git active (du fichier ou de la commande git)
- `{stack_summary}` — technologies clés (2-3 items)

## STEP 2 — Charger l'état de la dernière session

Lire `{project-root}/_gsane/_memory/sessions/session-state.md` → extraire :
- `{last_session_date}`
- `{last_agent_active}`
- `{last_workflow_run}`
- `{plan_active}` + `{current_phase_plan}` + `{next_step}`
- `{open_items}` (HIGH findings non appliqués)

Si `session-state.md` absent ou `last_session_date = —` → session COLD (première fois).

## STEP 3 — Vérifier l'état git

Exécuter `git log --oneline -5` et `git status --short` pour obtenir :
- `{recent_commits}` — 5 derniers commits (hash + message)
- `{git_status}` — fichiers modifiés/non commités

## STEP 4 — Afficher la carte de statut

Afficher en {communication_language} :

```
╔════════════════════════════════════════════════════════════╗
║  🧙 GSANE SESSION BOOTSTRAP                                ║
╚════════════════════════════════════════════════════════════╝

📦 PROJET
  Nom       : {project_name}
  Objectif  : {project_objective}
  Phase     : {current_phase}
  Stack     : {stack_summary}

🔁 DERNIÈRE SESSION ({last_session_date})
  Agent actif    : {last_agent_active}
  Workflow lancé : {last_workflow_run}
  Plan actif     : {plan_active} — Phase {current_phase_plan}
  Prochaine étape: {next_step}
  Items ouverts  : {open_items}

🌿 GIT
  Branche : {active_branch}
  Statut  : {git_status}

  Derniers commits :
  {recent_commits}

💡 SUGGESTION
  {next_step si disponible, sinon "Tape [SR] pour démarrer intelligemment"}

📌 Actions : [Lancer {next_step}] · [SR] Smart Router · [SS] Session Solo · [PM] Party Mode
```

Si session COLD (première fois) → afficher à la place :
```
🧙 Première session détectée. Tape [SR] pour que GSANE détecte automatiquement le meilleur mode selon ton besoin, ou choisis directement : [SS] · [BS] · [PM].
```
