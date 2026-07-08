# Annexe AWS CloudWatch — logs, métriques, alarmes

> Annexe de [`observability-triage`](../SKILL.md). La méthode vit dans la skill ;
> ici, seulement la syntaxe. Pré-requis : session vérifiée
> ([`aws-session.md`](aws-session.md)). Comptes/régions/ARN = à rédiger
> (`<REDACTED>`) dans les preuves versionnées.

## Par symptôme — où regarder d'abord

| Symptôme | Métriques CloudWatch | Puis |
|---|---|---|
| 5xx sur ALB/API | `HTTPCode_Target_5XX_Count`, `TargetResponseTime`, `UnHealthyHostCount` | Logs des targets |
| Lambda en erreur | `Errors`, `Throttles`, `Duration` (p99), `ConcurrentExecutions` | Logs Insights sur le log group |
| ECS dégradé | `CPUUtilization`, `MemoryUtilization` + **Service events** (console ECS) | Logs conteneur |
| File qui gonfle | SQS `ApproximateAgeOfOldestMessage`, `ApproximateNumberOfMessagesVisible` | Consommateur (Lambda/ECS) |

## Étapes 2-3 — Logs Insights (rétrécir)

```text
# Erreurs dans la fenêtre, chronologique
fields @timestamp, @message
| filter @message like /ERROR|Exception|FATAL/
| sort @timestamp asc
| limit 50

# Regrouper par classe d'erreur
fields @message
| filter @message like /ERROR/
| parse @message /(?<error_class>[A-Za-z]+(Exception|Error))/
| stats count(*) as n by error_class
| sort n desc
```

## Étape 4 — borner

```text
# Premier/dernier événement anormal
fields @timestamp, @message
| filter @message like /ERROR/
| stats min(@timestamp) as first_seen, max(@timestamp) as last_seen, count(*) as n
```

Croiser `first_seen` avec : historique de l'**alarme** (Alarms → History, heure de
bascule OK → In alarm), et les déploiements récents (CodeDeploy/pipeline).

## Étape 5 — corréler une transaction

```text
# Si les logs portent un request id (API GW : @requestId)
fields @timestamp, @message
| filter @requestId = "<id>"
| sort @timestamp asc
```

X-Ray (si activé) : la trace map par `trace_id` suit la requête à travers les
services.

## Export de la preuve

- Logs Insights affiche la fenêtre interrogée : la recopier **en UTC** avec la
  requête et l'extrait.
- `Export results` → coller l'extrait (anonymisé) dans `docs/_scratch/inputs/`.
- Toujours noter **région + log group** (rédiger le numéro de compte).

## Pièges CloudWatch

- La console affiche l'heure **locale** par défaut — basculer l'affichage en UTC
  avant de noter des timestamps.
- Logs Insights ne couvre que la rétention du log group : une fenêtre vide peut
  signifier « logs expirés », pas « pas d'erreur ».
- Les métriques < 1 min (haute résolution) expirent vite ; les agrégats 5 min
  restent — préciser la granularité dans la preuve.
