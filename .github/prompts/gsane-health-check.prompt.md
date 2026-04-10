---
name: gsane-health-check
description: "Vérifie la santé du framework GSANE : sources canoniques actives, audit de continuité, manifests, git et cohérence des fichiers. Produit un rapport ✅/⚠️/❌ scoré sur 5."
applyTo: "**"
---

Exécute le health check GSANE complet et produit un rapport structuré. Pas de questions — analyse et affiche.

## CHECK 1 — Fichiers de configuration essentiels

Vérifier l'existence des fichiers suivants :

| Fichier | Statut | Sévérité si absent |
|---|---|---|
| `_gsane/config.yaml` | ✅/❌ | HIGH |
| `_gsane/_config/manifest.yaml` | ✅/❌ | HIGH |
| `_gsane/_config/agent-manifest.yaml` | ✅/❌ | HIGH |
| `_gsane/_config/workflow-manifest.yaml` | ✅/❌ | MEDIUM |
| `_gsane/_config/delegation-matrix.yaml` | ✅/❌ | HIGH |

Score : +1 si tous critiques présents, 0 sinon.

## CHECK 2 — Sources canoniques et audit de continuité

Vérifier l'existence ET le contenu non-vide des surfaces suivantes :

| Fichier | Statut | Note |
|---|---|---|
| `_gsane/_memory/project-context.md` | ✅/⚠️/❌ | brief canonique humain durable |
| `_gsane-output/current-delivery-contract.md` | ✅/⚠️/❌ | contrat actif du runtime |
| `_gsane/_memory/failure-museum.md` | ✅/⚠️/❌ | ⚠️ si vide ou absent |
| `_gsane/_memory/decision-log.md` | ✅/⚠️/❌ | info seulement |
| `_gsane/_memory/sessions/session-state.md` | ✅/⚠️/❌ | audit/continuité seulement |
| `_gsane/_memory/sessions/session-analysis-log.md` | ✅/⚠️/❌ | audit/continuité pour PSA/flywheel |

Score : +1 si `project-context.md` ET `current-delivery-contract.md` sont présents et non-vides, 0 sinon.

## CHECK 3 — Cohérence manifest vs fichiers réels

Spot-check : prendre les 5 premiers workflows listés dans `_gsane/_config/workflow-manifest.yaml` (champ `path`).

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
| `_gsane/agents/architect.md` | ✅/❌ |
| `_gsane/agents/dev.md` | ✅/❌ |
| `_gsane/agents/qa.md` | ✅/❌ |
| `_gsane/agents/bond.md` | ✅/❌ |

Score : +1 si tous présents, 0 sinon.

---

## OUTPUT — Rapport de santé

Afficher en {communication_language} :

```
╔════════════════════════════════════════════════════════════╗
║  🏥 GSANE HEALTH CHECK — {date}                            ║
╚════════════════════════════════════════════════════════════╝

CHECK 1 — Configuration      : {✅/⚠️/❌} {détail si problème}
CHECK 2 — Sources canoniques  : {✅/⚠️/❌} {détail si problème}
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

