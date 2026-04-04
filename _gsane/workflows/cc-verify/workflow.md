---
name: cc-verify
description: "Quality Gate exécutable pour la clôture d'un Delivery Contract. Définit les prérequis, checks, conditions PASS/FAIL et format de sortie standard."
version: 2.0
---

# Workflow : CC-Verify (Completion Contract)

> Gate exécutable obligatoire avant toute déclaration de tâche terminée.  
> Exécuté par Quinn (QA). Résultat : [CC] PASS ou [CC] FAIL.

---

## Prérequis

Avant d'executer cc-verify, les éléments suivants doivent être disponibles :
- `task_id` : identifiant de la tâche à clôturer
- `delivery_contract` : fichier .contract.md ou brief structuré de la tâche
- Accès au système de fichiers pour lecture/écriture

---

## ÉTAPE 1 — Vérification des critères d'acceptation

```
POUR CHAQUE critère d'acceptation dans delivery_contract :
  CHECK_1 : Le critère est-il vérifiable objectivement ? (fichier existe, commande retourne 0, test passe)
  CHECK_2 : Le critère est-il satisfait dans l'état actuel du dépôt ?
  
  SI CHECK_1 = non → marquer comme UNTESTABLE (non bloquant, log uniquement)
  SI CHECK_1 = oui ET CHECK_2 = non → marquer comme FAILED (bloquant)
  SI CHECK_1 = oui ET CHECK_2 = oui → marquer comme PASSED
```

---

## ÉTAPE 2 — Quality Gate automatique

```
EXÉCUTER : bash gsane.sh validate
  SI exit_code = 0 → GATE_AUTO = PASS
  SI exit_code != 0 → GATE_AUTO = FAIL
    → Logger l'output complet dans _gsane-output/cc-verify-{task_id}-{date}.log
    → Envoyer les logs à Amelia via P2P CHALLENGE (voir standard-agent-behavior.md)
    → NE PAS alerter l'utilisateur — attendre re-soumission après correction
```

---

## ÉTAPE 3 — Vérification des artefacts obligatoires

```
CHECK_CHANGELOG : CHANGELOG.md a-t-il une entrée pour cette tâche/feature ?
  SI non et que des fichiers src/ ont été modifiés → ARTEFACT_FAIL

CHECK_CONTRACT : Si la tâche avait un .contract.md → est-il archivé dans _gsane-output/ ?
  SI non → log avertissement (non bloquant)

CHECK_TRACE : _gsane/_memory/trace.log a-t-il un event session_started pour cette session ?
  SI non → log avertissement (non bloquant)
```

---

## ÉTAPE 4 — Décision finale

```
CONDITIONS POUR [CC] PASS :
  GATE_AUTO = PASS
  AND aucun critère FAILED à l'étape 1
  AND CHECK_CHANGELOG = true (si code modifié)

CONDITIONS POUR [CC] FAIL :
  GATE_AUTO = FAIL
  OR au moins 1 critère FAILED
  OR CHECK_CHANGELOG = false et code modifié

[CC] INCOMPLETE :
  Au moins 1 critère UNTESTABLE ET aucun FAILED ET GATE_AUTO = PASS
  → Déclarer PASS avec liste des éléments non testés en avertissement
```

---

## Format de sortie standard

```
[CC] {PASS|FAIL|INCOMPLETE} — {task_id} — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Critères satisfaits : N
❌ Critères échoués   : N  ← si FAIL
⚠️  Non testables      : N  ← si INCOMPLETE
─
Quality Gate       : {PASS|FAIL}
CHANGELOG          : {✅|❌}
─
{Si FAIL : "Items bloquants :"}
  - {critère} : {raison de l'échec}
{Si PASS : "Prochaine étape recommandée :"}
  - Archiver le contract et merger
```

---

## Comportement Zero-Touch Fix-Loop

```
SI [CC] FAIL et GATE_AUTO = FAIL :
  1. Quinn envoie P2P CHALLENGE → Amelia avec les logs complets
  2. Amelia corrige et re-soumet gsane.sh validate
  3. Quinn ré-exécute cc-verify automatiquement (pas d'intervention humaine)
  4. Maximum 3 itérations (CIRCUIT-BREAKER au bout de 3 échecs consécutifs)
  5. L'humain n'est notifié QUE en cas de [CC] PASS final OU circuit-breaker déclenché
```
