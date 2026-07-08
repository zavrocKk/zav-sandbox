# Annexe AWS Batch — jobs en échec ou coincés

> Annexe de [`observability-triage`](../SKILL.md). Pré-requis : session vérifiée
> ([`aws-session.md`](aws-session.md)). Les logs des jobs vivent dans CloudWatch —
> l'analyse fine des logs se fait avec [`aws-cloudwatch.md`](aws-cloudwatch.md).

## Par symptôme — où regarder d'abord

| Symptôme | Cause dominante | Premier réflexe |
|---|---|---|
| Job coincé en `RUNNABLE` | Presque toujours le **compute environment** (capacité, quotas, subnets, ECS agent) — pas le job | État du compute env + ses événements |
| Job `FAILED` | Erreur applicative ou conteneur | `describe-jobs` → `statusReason` + exit code |
| File qui s'accumule | Débit du compute env < arrivées | Compter par statut (ci-dessous) |
| Jobs lents | Ressources sous-dimensionnées ou dépendance externe | `startedAt`→`stoppedAt` vs historique |

## Étapes 2-3 — état de la file et des jobs

```text
# Combien de jobs par statut (le « golden signal » Batch)
aws batch list-jobs --job-queue <queue> --job-status RUNNABLE --region <r> --profile <p>
aws batch list-jobs --job-queue <queue> --job-status FAILED   --region <r> --profile <p>

# Le pourquoi d'un échec : statusReason + raison conteneur + exit code
aws batch describe-jobs --jobs <job-id> --region <r> --profile <p>
#   → status, statusReason, container.reason, container.exitCode,
#     container.logStreamName, createdAt/startedAt/stoppedAt
```

Exit codes parlants : `137` = SIGKILL (souvent OOM — croiser avec la mémoire
demandée), `1` = erreur applicative → logs.

## Logs du job → CloudWatch

```text
# Log group standard : /aws/batch/job — stream = logStreamName du describe-jobs
aws logs get-log-events \
  --log-group-name /aws/batch/job \
  --log-stream-name <logStreamName> \
  --region <r> --profile <p>
```

Pour filtrer/agréger : Logs Insights sur `/aws/batch/job`
(patterns dans [`aws-cloudwatch.md`](aws-cloudwatch.md)).

## Étape 4 — borner

`describe-jobs` donne `createdAt` / `startedAt` / `stoppedAt` en **epoch
millisecondes** — convertir en UTC avant de citer. `createdAt → startedAt` long
= problème de placement (compute env) ; `startedAt → stoppedAt` court + FAILED
= crash au démarrage (image, droits, config).

## Pièges Batch

- **`RUNNABLE` éternel** : inspecter le compute environment (état `VALID` ?
  capacité max atteinte ? subnets avec IPs libres ?) — re-soumettre le job ne
  change rien.
- **`logStreamName` absent** du describe = le conteneur n'a **jamais démarré** :
  la cause est dans `statusReason`/compute env, pas dans les logs.
- **Jobs array** : le parent n'a pas de logs — décrire les **jobs enfants**
  (`<job-id>:<index>`).
- Un job retenté (`attempts`) a **plusieurs** log streams — citer celui de la
  tentative analysée.
