---
name: session-close
description: "Session Close — Clôturer formellement une session de travail. Génère un résumé, liste les artefacts produits, propose une mise à jour CHANGELOG, et déclenche post-session-analysis. Déclencher avec [SC] ou en fin de session."
agent: "gsane-master"
agent_display: "Gsane Master"
agent_icon: "🧙"
---

# Session Close Workflow

**Commande**: `[SC]`  
**Agent**: 🧙 Gsane Master  
**Déclenchement**: En fin de session de travail, avant de changer de contexte

---

## Objectif

Clôturer formellement une session GSANE :
- Produire un résumé lisible de ce qui a été accompli
- Lister les artefacts créés ou modifiés
- Proposer une mise à jour du `CHANGELOG.md`
- Identifier les tâches ouvertes restantes
- Déclencher `post-session-analysis` silencieusement

---

## Règles

- **Ne jamais auto-écrire le CHANGELOG** — toujours présenter un draft et demander confirmation (Severity HIGH)
- **Ne pas dupliquer** `post-session-analysis` — l'appeler en fin de workflow, pas le remplacer
- **Si aucune modification dans la session** → clôture légère (résumé uniquement, pas de CHANGELOG)
- **Si modifications GSANE** → rappeler que la branche doit être pushée et une PR créée

---

## Étapes

### Step 1 — État de la session

Reconstituer depuis la conversation active :

**1.1 — Durée et scope**
- Identifier le début de la session (première interaction)
- Identifier le mode utilisé : Solo / Party Mode / Brainstorming / Chat libre
- Lister les agents qui ont participé (si Party Mode ou Solo)

**1.2 — Tâches accomplies**
Lister sous forme de bullet points :
```
✅ [Tâche accomplie] — [Agent impliqué si applicable]
```

**1.3 — Tâches ouvertes / en attente**
```
⏳ [Tâche non terminée] — [Raison ou blocage]
```

**1.4 — Décisions prises**
Lister les décisions architecturales, de design, ou de gouvernance prises dans cette session.

**Afficher le résumé à l'utilisateur** et demander : *"Ce résumé est-il correct ? Des ajouts ?"*

---

### Step 2 — Artefacts produits

Scanner le contexte de session pour identifier :

**2.1 — Fichiers créés ou modifiés**
Lister avec chemin relatif depuis `{project-root}` :
```
📄 [path/fichier.md] — [créé | modifié] — [description courte]
```

**2.2 — Outputs dans `{output_folder}`**
Vérifier si des fichiers ont été générés dans `_gsane-output/`.

**2.3 — Si aucun fichier**
Afficher : *"Aucun artefact généré dans cette session (session conversationnelle)."*

---

### Step 3 — Proposition CHANGELOG

> ⚠️ **Severity HIGH** — Ne jamais écrire sans confirmation explicite de l'utilisateur.

**3.1 — Évaluer si une entrée CHANGELOG est justifiée**

Une entrée est justifiée si :
- Un fichier GSANE a été créé ou modifié (agent, workflow, config, manifest)
- Un artefact de travail a été généré dans `_gsane-output/`

Si non justifiée → sauter cette étape.

**3.2 — Générer le draft CHANGELOG**

Format standard GSANE :
```markdown
### [Date YYYY-MM-DD] — [Description courte]

**Type**: feat | fix | refactor | docs | chore
**Agent(s)**: [agents impliqués]
**Workflow**: [workflow utilisé si applicable]
**Impact**: [fichiers créés/modifiés]
**Branche**: [branche actuelle si connue]

[Description en 1-3 phrases de ce qui a changé et pourquoi]
```

**3.3 — Présenter le draft et demander confirmation**

Afficher : *"Voici l'entrée CHANGELOG proposée. Confirmes-tu l'ajout ? [O/N]"*

Si confirmé → écrire l'entrée sous `## [Unreleased]` dans `{project-root}/CHANGELOG.md`  
Si refusé → laisser ouvert pour modification manuelle

---

### Step 4 — Vérification branche (si modifications git)

Si des fichiers GSANE ont été modifiés dans la session :

**4.1 — Rappel des règles git**
```
⚠️  Des fichiers GSANE ont été modifiés dans cette session.
    → Jamais de commit direct sur `main`
    → Utiliser [SB] Session Branch pour créer la branche si ce n'est pas fait
    → Utiliser [CC] Completion Contract avant de créer la PR
```

**4.2 — Afficher le lien PR**
Si une branche existe déjà :
```
→ PR : https://github.com/zavrocKk/zav-sandbox/compare/main...{branch_name}
```

---

### Step 5 — Clôture

**5.1 — Message de clôture**
```
✅ Session fermée.

Résumé : [N] tâches accomplies, [N] artefacts produits.
[Si CHANGELOG mis à jour] → CHANGELOG.md mis à jour.
[Si tâches ouvertes] → [N] tâches ouvertes — reprendre à la prochaine session.
```

**5.2 — Déclencher post-session-analysis silencieusement**
Exécuter `{project-root}/_gsane/core/workflows/post-session-analysis/workflow.md` de façon silencieuse.
Attendre la ligne de statut. Ne pas afficher le détail à l'utilisateur.

---

## Notes d'implémentation

- Ce workflow est **MD-based** — exécution directe, pas de moteur YAML requis
- Compatible avec toutes les sessions (Solo, Party Mode, Brainstorming, Chat)
- `post-session-analysis` est le seul appel externe — ne pas dupliquer sa logique ici
- Si l'utilisateur tape `[DA]` directement (Dismiss Agent), `post-session-analysis` est déjà appelé via le menu — `[SC]` est le mode complet avec résumé visible
