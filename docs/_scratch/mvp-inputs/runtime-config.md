---
type: incident-input
source: kubernetes-helm-config
service: notification-api
namespace: notif-prod
captured-at: 2026-05-02T09:30:00Z
---

> **FIXTURE** — Données synthétiques créées pour les tests du MVP (Phase 4–5). Aucune donnée réelle de production.

# Runtime configuration — notification-api

> Configuration en vigueur au moment de l'incident, captée lors du diagnostic le matin (09:30 UTC). Aucun changement appliqué depuis 7 jours.

---

## Helm values (extraits pertinents)

```yaml
# values-prod.yaml — notification-api

replicaCount: 3  # min HPA

image:
  repository: registry.acme/notification-api
  tag: 4.7.2
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 250m
    memory: 512Mi
  limits:
    cpu: 500m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  # Note: pas de custom metric configurée

livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 60
  periodSeconds: 30
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

env:
  SPRING_DATASOURCE_HIKARI_MAXIMUM_POOL_SIZE: "20"
  SPRING_DATASOURCE_HIKARI_CONNECTION_TIMEOUT: "5000"
  SPRING_DATASOURCE_HIKARI_LEAK_DETECTION_THRESHOLD: "60000"
  MANAGEMENT_HEALTH_DB_ENABLED: "true"   # ← liveness check inclut DB
  SCHEDULER_MONTHLY_DIGEST_CRON: "0 0 2 1-31 * ?"  # 02:00 UTC chaque jour (mais conditionnel sur date)
```

---

## Database connection (RDS PostgreSQL)

```
Engine             : PostgreSQL 14.10
Instance class     : db.r6g.large
Max connections    : 100  (PostgreSQL `max_connections`)
Connections used   : ~1 par pod app × pool size + autres consommateurs
Other consumers    : reporting-api (pool max 15), notification-worker (pool max 10)
Network            : same VPC, ~1 ms RTT
```

> 💡 **Calcul** : si notification-api scale à 5 pods × 20 = 100 connexions potentielles. Plus reporting-api (15) + notification-worker (10) = **125 demandeurs potentiels** pour 100 connexions max DB. Pas garanti que tous demandent en même temps, mais le risque est structurellement présent.

---

## Job programmé (Spring scheduler)

```
Nom              : MonthlyDigestJob
Cron             : 0 0 2 1-31 * ?  (02:00 UTC tous les jours, conditionnel sur logique métier interne)
Logique métier   : déclenche le digest mensuel le jour J du mois (variable selon segment client)
Volume           : ~30k à 60k destinataires selon le segment
Pool dédiée      : scheduler-pool-1 (séparée du pool HTTP)
Pool DB utilisée : MAIN (HikariPool-1) — partagée avec le trafic HTTP ⚠️
```

> 💡 **Indice** : le job utilise une pool de threads dédiée (`scheduler-pool-1`) pour ne pas bloquer le trafic HTTP, **mais il partage la même pool de connexions DB** (`HikariPool-1`). Donc le job consomme des connexions DB au détriment du trafic HTTP.

---

## Datadog alert thresholds (extraits)

```
notification-api - 5xx error rate above 1%      (WARN)
notification-api - 5xx error rate above 5%      (CRIT)
notification-api - p95 latency above 2000ms     (CRIT)
notification-api - p99 latency above 5000ms     (WARN)
K8s liveness probe failures (notif-prod)        (CRIT)

Aucune alerte sur :
- Connection pool saturation (HikariCP gauge `hikaricp.connections.usage`)
- Connection wait time (HikariCP gauge `hikaricp.connections.acquire`)
- DB connection count (RDS metric)
```

> 💡 **Observation** : les alertes sont basées sur **les symptômes côté HTTP** (5xx, latence). Aucune alerte sur les **causes structurelles** (saturation pool DB, wait time, max connections atteint).

---

## Historique de déploiement (7 derniers jours)

```
2026-04-25 14:30  notification-api 4.7.0 → 4.7.1  (bugfix mineur)
2026-04-26 11:15  notification-api 4.7.1 → 4.7.2  (release courante)
... (rien depuis)
```

→ **Aucun changement applicatif** dans les 5 jours précédant l'incident.
