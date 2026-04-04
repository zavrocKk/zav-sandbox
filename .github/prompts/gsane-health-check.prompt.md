---
name: gsane-health-check
description: "Vérifie la santé du framework GSANE : config, mémoire, manifests, git et cohérence des fichiers. Produit un rapport ✅/⚠️/❌ scoré sur 5."
applyTo: "**"
---

Exécute le health check GSANE complet et produit un rapport structuré. Pas de questions — analyse et affiche.

## CHECK 1 — Fichiers de configuration essentiels

Vérifier l'existence des fichiers suivants :

| Fichier | Statut | Sévérité si absent |
|---|---|---|
| `_gsane/core/config.yaml` | ✅/❌ | HIGH |
| `_gsane/_config/manifest.yaml` | ✅/❌ | HIGH |
| `_gsane/_config/agent-manifest.csv` | ✅/❌ | HIGH |
| `_gsane/_config/workflow-manifest.csv` | ✅/❌ | MEDIUM |
| `_gsane/_config/delegation-matrix.yaml` | ✅/❌ | HIGH |

Score : +1 si tous critiques présents, 0 sinon.

## CHECK 2 — Santé des fichiers mémoire

Vérifier l'existence ET le contenu non-vide des fichiers mémoire :

| Fichier | Statut | Note |
|---|---|---|
| `_gsane/_memory/project-context.md` | ✅/⚠️/❌ | ⚠️ si `{project_name}` non remplacé |
| `_gsane/_memory/session-state.md` | ✅/⚠️/❌ | ⚠️ si tous les champs = `—` |
| `_gsane/_memory/failure-museum.md` | ✅/⚠️/❌ | ⚠️ si vide ou absent |
| `_gsane/_memory/decision-log.md` | ✅/⚠️/❌ | info seulement |
| `_gsane/_memory/session-analysis-log.md` | ✅/⚠️/❌ | ⚠️ si absent |

Score : +1 si project-context.md ET session-state.md présents et non-vides, 0 sinon.

## CHECK 3 — Cohérence manifest vs fichiers réels

Spot-check : prendre les 5 premiers workflows listés dans `_gsane/_config/workflow-manifest.csv` (colonne `path`).

Pour chacun : vérifier que le fichier à ce `path` existe réellement dans le workspace.

- 5/5 présents → ✅ +1
- 3-4/5 présents → ⚠️ +0.5 (avertissement — désynchronisation partielle)
- <3/5 présents → ❌ 0 (manifest désynchronisé)

## CHECK 4 — État git

Exécuter `git status --short` et `git branch --show-current`.

Évaluer :
- Sur une branche `feature/*` ou `fix/*` → ✅ (bonne pratique)
- Sur `main` avec des fichiers modifiés → ❌ HIGH (commits directs sur main)
- Sur `main` sans modifications → ⚠️ (pas de travail en cours, vérifier si normal)
- Aucun fichier non commité → ✅

Score : +1 si branche feature/fix ET workdir propre, +0.5 si branche feature/fix mais fichiers non commités, 0 si sur main.

## CHECK 5 — Santé des agents principaux

Vérifier l'existence des fichiers agents core :

| Fichier | Statut |
|---|---|
| `_gsane/agents/master.md` | ✅/❌ |
| `_gsane/agents/bond.md` | ✅/❌ |
| `_gsane/agents/tea.md` | ✅/❌ |

Score : +1 si tous présents, 0 sinon.

---

## OUTPUT — Rapport de santé

Afficher en {communication_language} :

```
╔════════════════════════════════════════════════════════════╗
║  🏥 GSANE HEALTH CHECK — {date}                            ║
╚════════════════════════════════════════════════════════════╝

CHECK 1 — Configuration      : {✅/⚠️/❌} {détail si problème}
CHECK 2 — Mémoire persistante : {✅/⚠️/❌} {détail si problème}
CHECK 3 — Manifest vs fichiers: {✅/⚠️/❌} {détail si problème}
CHECK 4 — État git            : {✅/⚠️/❌} Branche: {branch} | {N} fichiers non commités
CHECK 5 — Agents core         : {✅/⚠️/❌} {détail si problème}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCORE GLOBAL : {score}/5

{score == 5}  → ✅ GSANE en bonne santé — prêt à travailler
{score >= 3}  → ⚠️ GSANE opérationnel — {N} points d'attention
{score < 3}   → ❌ GSANE dégradé — corrections requises avant de continuer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{si score < 5 : liste des actions recommandées pour corriger les ⚠️/❌}

📌 Actions : [CC] Completion Contract · [SR] Smart Router · [gsane-session-bootstrap] Reprendre la session
```

