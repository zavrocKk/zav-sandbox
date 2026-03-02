---
name: session-branch
description: "Session Branch Setup — ensures every work session starts on a properly named branch, never on main. Validates existing branch context or creates a new one."
---

# Session Branch Workflow

**Commande**: `/gsane-session-branch`  
**Agent**: Gsane Master  
**Déclenchement**: Au début de toute session de travail impliquant des modifications GSANE

---

## Objectif

Garantir que chaque session de travail commence sur une branche propre et nommée correctement — jamais sur `main`, jamais en reprenant une branche d'une autre unité logique.

---

## Règles

- **Jamais sur `main`** — toute modification démarre sur une branche dédiée
- **1 session = 1 branche** si les changements sont d'une même unité logique
- **Branche existante** acceptable uniquement si la session continue une PR non-mergée
- **Nom de branche** : `feature/{description}-YYYY-MM-DD` ou `fix/{description}-YYYY-MM-DD`

---

## Étapes

### Step 1 — Vérifier la branche courante

```bash
git branch --show-current
git status --short
```

**Si sur `main`** → aller à Step 2  
**Si sur une branche `feature/*` ou `fix/*`** → vérifier Step 3 (branche en cours ou nouvelle ?)  
**Si sur autre chose** → warning + aller à Step 2

---

### Step 2 — Créer une nouvelle branche

Demander à l'utilisateur (ou inférer du contexte) :
- **Type** : `feature` (nouveau code, amélioration) ou `fix` (correction)
- **Description** : courte, kebab-case, représentative du travail (`tier1-improvements`, `gsane-manifest-sync`, `ci-workflow-integrity`)
- **Date** : aujourd'hui en `YYYY-MM-DD`

Construire : `{type}/{description}-{date}`  
Exécuter :
```bash
git checkout main
git pull origin main
git checkout -b {type}/{description}-{date}
```

Confirmer à l'utilisateur : `✅ Branche créée : {branch-name}`

---

### Step 3 — Valider la branche existante

Si une branche `feature/*` ou `fix/*` est active, vérifier :

1. **Est-elle pushée ?** `git log origin/{branch} 2>/dev/null` — si non, noter
2. **Y a-t-il des commits non-pushés ?** `git log origin/main..HEAD --oneline`
3. **La branche concerne-t-elle le même sujet que le travail actuel ?**
   - Si OUI → continuer sur cette branche
   - Si NON → recommander une nouvelle branche (Step 2)

---

### Step 4 — Résumé de session

Afficher à l'utilisateur :

```
🌿 SESSION BRANCH READY
  Branche : {branch-name}
  Statut  : {nouvelle | continuée}
  Commits : {count non-pushés}
  
  Rappels :
  • [CC] avant de déclarer terminé
  • Consulter FM avant d'implémenter
  • Party Mode si sévérité MEDIUM/HIGH
```

---

## Fin de session

À la fin du travail :
1. Exécuter `[CC]` — Completion Contract
2. `git push origin {branch-name}`
3. Fournir URL PR : `https://github.com/zavrocKk/zav-sandbox/pull/new/{branch-name}`
4. Post-session analysis s'exécute automatiquement via `[DA]`
