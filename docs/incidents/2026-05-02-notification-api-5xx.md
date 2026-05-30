---
type: incident-report
status: draft
created: 2026-05-03
incident_date: 2026-05-02
severity: SEV2
services_affected: [notification-api, notification-worker (indirect), reporting-api (indirect)]
duration_minutes: 105
---

# Incident — Pic d'erreurs 5xx et latence dégradée sur `notification-api` (nuit 02:00-04:30 UTC)

> **Style :** blameless. On critique des systèmes et des processus, jamais des personnes.

---

## Résumé exécutif

Entre **02:32 et 04:18 UTC** le 2026-05-02, `notification-api` a subi une saturation de sa pool de connexions DB (HikariCP) provoquée par le `MonthlyDigestJob` qui partage la même pool que le trafic HTTP. Conséquences : ~2 100 erreurs HTTP 500, p95 plafonné à 5 s (timeout pool), 2 redémarrages auto par liveness probe, et ~1 650 notifications du digest mensuel non délivrées (échecs `connection_timeout`). L'incident s'est résolu naturellement à la fin du job (04:18), avant le rollout restart manuel de l'astreinte (04:31).

## Timeline

| Heure (UTC) | Événement | Source |
|---|---|---|
| 02:00 | État nominal — p95 ~180 ms, 0 erreurs 5xx, 3 pods, pool DB idle | [datadog-snapshot.md](../_scratch/mvp-inputs/datadog-snapshot.md) §1, §2 |
| 02:14 | Démarrage `MonthlyDigestJob` — ~42 500 destinataires, 17 batches de 2 500, sur `scheduler-pool-1` | [splunk-extract.md](../_scratch/mvp-inputs/splunk-extract.md) |
| 02:32 | **Premier WARN HikariCP** : `total=20, active=20, idle=0, waiting=14`, timeout 5001 ms | splunk-extract |
| 02:33 | `GlobalErrorHandler` mappe `CannotGetJdbcConnectionException` → HTTP 500 (toutes exceptions confondues) | splunk-extract |
| 02:33 | HPA scale-out 3 → 4 pods (CPU 73 % > target 70 %) | datadog §4, §5 |
| 02:34 | Datadog WARN « 5xx > 1 % » | datadog §6 |
| 02:48 | Datadog CRIT « 5xx > 5 % » | datadog §6 |
| 03:08 | HPA scale-out 4 → 5 pods. Le nouveau pod sature sa propre pool en < 1 min | splunk-extract, datadog §4 |
| 03:11 | Datadog CRIT « p95 > 2000 ms » (plafond observé : 5 010 ms = `connectionTimeout` HikariCP) | datadog §2, §6 |
| 03:42 | Liveness probe failure (DB indicator timeout 5 s) → restart auto pod `2xkl` | splunk-extract, datadog §3 |
| 03:48 | Restart auto pod `9mpz` (même cause) | datadog §3 |
| 04:18 | **Fin `MonthlyDigestJob`** : 40 850 dispatched, **1 650 échecs `connection_timeout`** | splunk-extract |
| 04:19 | Pool HikariCP revient nominale (`active=12, idle=8, waiting=0`) — incident résolu | splunk-extract |
| 04:31 | Rollout restart manuel L2 (5 pods) — **incident déjà résolu depuis 13 min** | datadog §3, splunk-extract |
| 04:38 | Datadog WARN « 5xx cleared » | datadog §6 |
| 05:01 | Datadog INFO « liveness probe failures cleared » | datadog §6 |

## Impact

- **Utilisateurs affectés** : ~1 650 destinataires du digest mensuel (notifications non délivrées) + appelants synchrones de l'API entre 02:32 et 04:18 (taux d'erreur jusqu'à ~18 % aux pics).
- **Requêtes échouées** :
  - HTTP 5xx synchrones : **~2 100** sur la fenêtre (cumul Datadog §1 : 183 + 642 + 724 + 511 + 247).
  - Notifications batch perdues : **1 650** (`failed_reason: connection_timeout` dans le job).
- **Revenu impacté** : non chiffré — dépend de la criticité des notifications du digest mensuel et des notifications synchrones (à valider avec métier).
- **SLA** : taux d'erreur > seuil contractuel (à confirmer selon SLO interne ; le SLI 5xx a dépassé 5 % pendant ~1h30).

## Cause racine

### Cause technique

**Saturation de la pool de connexions HikariCP `HikariPool-1` partagée entre le trafic HTTP synchrone et le `MonthlyDigestJob`.**

Cascade observée :

```
HTTP 500 (côté client métier)
   ↑ GlobalErrorHandler mappe TOUTE exception en 500 (sans distinction transient/fatal)
CannotGetJdbcConnectionException
   ↑ HikariCP timeout après 5 s (SPRING_DATASOURCE_HIKARI_CONNECTION_TIMEOUT=5000)
Pool saturée : active=20/20, waiting jusqu'à 22 threads
   ↑ Concurrence HTTP + scheduler sur la MÊME pool DB
MonthlyDigestJob accapare des connexions sur HikariPool-1 ← DÉCLENCHEUR
```

Le job utilise une pool de **threads** dédiée (`scheduler-pool-1`) mais partage la pool de **connexions DB** (`HikariPool-1`) avec le trafic HTTP. La séparation est donc illusoire.

### Cause systémique

1. **Capacity planning DB absent** : `Σ(pool_max × replicas_max)` = 5 pods × 20 + reporting-api 15 + notification-worker 10 = **125** ≥ `max_connections` PostgreSQL = **100**. Avec HPA `maxReplicas=10`, le théorique monte à 225. La configuration permet structurellement le dépassement.
2. **Couplage workloads via pool DB partagée** : tout pic batch tue le synchrone.
3. **Observabilité aveugle au bottleneck réel** : alertes Datadog uniquement sur **symptômes côté HTTP** (5xx, p95 latency). Aucune alerte sur `hikaricp.connections.usage`, `hikaricp.connections.pending`, `hikaricp.connections.acquire`, ni sur `RDS.DatabaseConnections`.
4. **Health check qui s'auto-DoS** : `MANAGEMENT_HEALTH_DB_ENABLED=true` sur la liveness probe + `timeoutSeconds=5` (= `connectionTimeout` HikariCP). Saturation pool → liveness fail → pod tué → nouveau pod démarre avec sa propre pool vide → aggrave la pression DB.
5. **Pas de runbook scheduler** : l'astreinte n'avait pas de signal indiquant « si HikariCP sature pendant la fenêtre 02:00-05:00, vérifier `MonthlyDigestJob` avant tout ». Action choisie (rollout restart) inutile et potentiellement aggravante.
6. **Error handling masquant** : `GlobalErrorHandler` mappe toute exception en HTTP 500 sans distinguer les exceptions transient (DB pool exhausted) qui devraient être HTTP 503 + `Retry-After`.

## Mitigation appliquée

- **04:31** : `kubectl rollout restart deployment/notification-api -n notif-prod` (5 pods).
- **Effet réel** : marginal. La pool était déjà revenue nominale à 04:19 (fin naturelle du job à 04:18). Le restart a coïncidé avec la décrue mais ne l'a **pas** causée.
- **Aucune autre mitigation** appliquée (pas de scaling DB, pas de coupure du job, pas de circuit-breaker activé).

## Symptômes vs causes — clarification

| Observation | Nature | Vraie cause |
|---|---|---|
| HTTP 500 côté client | Symptôme (mappé) | Pool HikariCP saturée, masqué par `GlobalErrorHandler` |
| p95 plafonné à 5 010 ms | Symptôme (mathématique) | `connectionTimeout=5000` ms — plafond, pas un vrai temps de réponse |
| Liveness probe failures (03:42, 03:48) | **Conséquence aggravante**, pas cause | Pool saturée + DB check actif sur liveness |
| HPA scale-out 3 → 5 pods | Réaction CPU légitime mais **inutile** | Bottleneck est la DB, pas le CPU |
| Pool nominale après 04:19 | Résolution | Fin naturelle du `MonthlyDigestJob` à 04:18 |

## Fausses pistes écartées

1. **`LazyInitializationException` Hibernate** dans les logs : récurrentes toutes les heures à `:18 ±5 min`, **avant et après** l'incident. Bug applicatif indépendant à traiter en backlog, sans rapport.
2. **`StrictHttpFirewall` warnings** : scans automatiques continus, bruit de fond.
3. **« Le rollout restart L2 a résolu l'incident »** : faux. Décrue à 04:19, restart à 04:31. Corrélation ≠ causalité.
4. **Déploiement applicatif récent** : aucun depuis le 2026-04-26 (4.7.2). Cause structurelle, pas régression de release.

## Ce qui a bien fonctionné

- Détection Datadog rapide sur les symptômes HTTP (WARN à 02:34, soit 2 min après le premier timeout).
- HPA a réagi correctement à son signal (CPU), même si non pertinent ici.
- Logs structurés JSON (Logback + Logstash encoder) ont permis une reconstitution précise post-mortem.
- Le scheduler a continué à dispatcher partiellement (40 850 / 42 500 = 96 %) plutôt que de s'effondrer entièrement.

## Ce qui a moins bien fonctionné

- Aucune alerte sur la **vraie cause** (pool DB) — diagnostic en aveugle pour l'astreinte.
- Liveness probe couplée à la DB : a tué des pods qui auraient pu absorber la décrue.
- Pas de runbook scheduler → action L2 choisie au feeling, sans effet.
- `GlobalErrorHandler` masque la nature transient des erreurs DB (pas de 503, pas de `Retry-After`).
- Capacity planning DB structurellement défaillant (Σ pools > `max_connections`).
- Plainte métier (« notifications critiques non envoyées ») non corrélée immédiatement aux 1 650 échecs du job.

## Action items

| # | Action | Owner | Échéance | Type | Priorité | Statut |
|---|---|---|---|---|---|---|
| 1 | Désactiver le check DB sur **liveness** (`MANAGEMENT_HEALTH_DB_ENABLED=false`), conserver sur readiness avec `timeoutSeconds=10` | DevOps | 2026-05-09 | Préventif | P0 | À faire |
| 2 | Créer alertes Datadog : `hikaricp.connections.pending > 5 pendant 2 min` (WARN), `> 15 pendant 1 min` (CRIT) ; `RDS.DatabaseConnections > 80` (WARN) | DevOps | 2026-05-09 | Détection | P0 | À faire |
| 3 | Découpler le scheduler : pool HikariCP **dédiée** `scheduler-pool-ds` (`max=5`) ou throttling explicite (semaphore N=5) | Developer | 2026-05-16 | Préventif | P0 | À faire |
| 4 | Capacity planning DB : passer RDS à `db.r6g.xlarge` (200 connexions) **OU** plafonner HPA `maxReplicas=4` tant que non redimensionné | Architect + DevOps | 2026-05-16 | Préventif | P1 | À faire |
| 5 | `GlobalErrorHandler` : mapper `CannotGetJdbcConnectionException` et exceptions JDBC transient → HTTP 503 + `Retry-After: 30` | Developer | 2026-05-16 | Préventif | P1 | À faire |
| 6 | Identifier les 1 650 destinataires en échec du `MonthlyDigestJob` et coordonner rejeu avec métier (DLQ ou requête dédiée) | Developer + Product | 2026-05-06 | Mitigation | P1 | À faire |
| 7 | Runbook : « Saturation HikariCP pendant fenêtre batch nocturne » (signaux, premières actions, qui escalader) | DevOps | 2026-05-23 | Détection | P2 | À faire |
| 8 | ADR : stratégie de pooling DB et séparation workloads HTTP / batch | Architect | 2026-05-30 | Structurel | P2 | À faire |

## Leçons apprises

1. **Alerter sur les causes, pas seulement sur les symptômes.** Les SLI HTTP (5xx, latence) détectent l'impact, pas l'origine. Les ressources contraintes (pools, threads, connexions DB, file descriptors) doivent avoir leurs propres alertes prédictives.
2. **Une liveness probe ne doit jamais dépendre d'une ressource externe partagée.** Sinon la saturation de la ressource crée une boucle de rétroaction destructrice. Garder les checks de dépendances sur la **readiness** uniquement.
3. **Le partage de pool DB entre workloads concurrents est un anti-pattern.** Un job batch et un trafic synchrone ont des SLO différents et doivent avoir des budgets de connexions séparés.
4. **Capacity planning DB ≠ capacity planning app.** Quand le HPA monte, la pression DB monte multiplicativement. Toujours vérifier `Σ(pool_max × replicas_max) ≤ max_connections × 0.8`.

## Annexes

- Inputs sources : [datadog-snapshot.md](../_scratch/mvp-inputs/datadog-snapshot.md), [splunk-extract.md](../_scratch/mvp-inputs/splunk-extract.md), [runtime-config.md](../_scratch/mvp-inputs/runtime-config.md)
- Workflow appliqué : [agents/workflows/incident-response.md](../../agents/workflows/incident-response.md)
- Checklist appliquée : [agents/checklists/incident-triage.md](../../agents/checklists/incident-triage.md)
- Incident antérieur de référence : [2026-05-02-postgres-disk-full.md](2026-05-02-postgres-disk-full.md)

---
*Post-mortem blameless : on parle systèmes et processus, pas personnes.*
