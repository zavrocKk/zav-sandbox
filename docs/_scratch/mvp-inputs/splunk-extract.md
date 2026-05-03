---
type: incident-input
source: splunk
service: notification-api
namespace: notif-prod
window: 2026-05-02T02:00:00Z to 2026-05-02T04:30:00Z
log-format: JSON structured (Logback + Logstash encoder)
---

# Splunk extract — notification-api logs (fenêtre incident)

> 60 lignes représentatives sélectionnées sur les 18 000 lignes brutes de la fenêtre 02:00-04:30. Volumes retirés mais distribution préservée. Format JSON structuré (Logback + Logstash encoder).

---

## Distribution globale (résumé)

| Niveau | Volume sur fenêtre | % |
|---|---|---|
| INFO | 12 800 | 71 % |
| WARN | 4 200 | 23 % |
| ERROR | 980 | 5,5 % |
| DEBUG | 20 | 0,1 % |

---

## Échantillons représentatifs

### 02:01 — Activité normale (avant pic)

```json
{"@timestamp":"2026-05-02T02:01:14.512Z","level":"INFO","logger":"c.acme.notif.NotificationController","thread":"http-nio-8080-exec-12","message":"Processing notification request","correlation_id":"req-a1b2c3","user_id":"u-9821","channel":"email"}
{"@timestamp":"2026-05-02T02:01:14.687Z","level":"INFO","logger":"c.acme.notif.NotificationService","thread":"http-nio-8080-exec-12","message":"Notification queued for delivery","correlation_id":"req-a1b2c3","duration_ms":175,"status":"queued"}
{"@timestamp":"2026-05-02T02:01:15.044Z","level":"INFO","logger":"c.acme.notif.NotificationController","thread":"http-nio-8080-exec-7","message":"Processing notification request","correlation_id":"req-d4e5f6","user_id":"u-1432","channel":"sms"}
```

### 02:14 — Premier signal (montée du pic)

```json
{"@timestamp":"2026-05-02T02:14:08.221Z","level":"INFO","logger":"c.acme.notif.scheduler.MonthlyDigestJob","thread":"scheduler-pool-1","message":"Starting monthly digest dispatch","scheduled_at":"2026-05-02T02:00:00Z","estimated_recipients":42500}
{"@timestamp":"2026-05-02T02:14:09.115Z","level":"INFO","logger":"c.acme.notif.scheduler.MonthlyDigestJob","thread":"scheduler-pool-1","message":"Loaded recipients batch","batch_size":2500,"batch_index":1,"total_batches":17}
```

> 💡 **Indice** : un job programmé démarre à 02:14 avec ~42 500 destinataires. C'est probablement le **pic d'activité légitime** sous-jacent.

### 02:32 — Premiers WARN (saturation pool DB)

```json
{"@timestamp":"2026-05-02T02:32:01.891Z","level":"WARN","logger":"com.zaxxer.hikari.pool.HikariPool","thread":"http-nio-8080-exec-19","message":"HikariPool-1 - Connection is not available, request timed out after 5001ms"}
{"@timestamp":"2026-05-02T02:32:01.892Z","level":"WARN","logger":"com.zaxxer.hikari.pool.HikariPool","thread":"http-nio-8080-exec-19","message":"HikariPool-1 - Pool stats (total=20, active=20, idle=0, waiting=14)"}
{"@timestamp":"2026-05-02T02:32:02.114Z","level":"ERROR","logger":"c.acme.notif.repository.NotificationRepository","thread":"http-nio-8080-exec-19","message":"Failed to acquire JDBC connection","correlation_id":"req-x9y8z7","exception":"org.springframework.jdbc.CannotGetJdbcConnectionException: Failed to obtain JDBC Connection; nested exception is java.sql.SQLTransientConnectionException: HikariPool-1 - Connection is not available, request timed out after 5001ms"}
```

> 🎯 **Indice clé** : pool HikariCP saturé. `total=20, active=20, idle=0, waiting=14`. Timeout configuré à 5s.

### 02:33 — Comportement du middleware d'erreur (fausse piste)

```json
{"@timestamp":"2026-05-02T02:33:15.402Z","level":"ERROR","logger":"c.acme.notif.web.GlobalErrorHandler","thread":"http-nio-8080-exec-19","message":"Unhandled exception in request handler","correlation_id":"req-x9y8z7","mapped_status":500,"original_exception":"CannotGetJdbcConnectionException","handler_action":"return 500 to client"}
```

> 🎭 **Fausse piste** : le `GlobalErrorHandler` mappe **toutes** les exceptions backend en HTTP 500, peu importe la cause réelle. Une exception "connection timeout" devient un 500 côté client.

### 02:35 — Confirmation de la saturation (continue)

```json
{"@timestamp":"2026-05-02T02:35:42.667Z","level":"WARN","logger":"com.zaxxer.hikari.pool.HikariPool","thread":"http-nio-8080-exec-7","message":"HikariPool-1 - Pool stats (total=20, active=20, idle=0, waiting=22)"}
{"@timestamp":"2026-05-02T02:35:42.668Z","level":"WARN","logger":"com.zaxxer.hikari.pool.HikariPool","thread":"http-nio-8080-exec-3","message":"HikariPool-1 - Connection is not available, request timed out after 5002ms"}
{"@timestamp":"2026-05-02T02:35:43.012Z","level":"ERROR","logger":"c.acme.notif.repository.NotificationRepository","thread":"http-nio-8080-exec-3","message":"Failed to acquire JDBC connection","correlation_id":"req-m1n2o3","exception":"CannotGetJdbcConnectionException: Failed to obtain JDBC Connection..."}
```

### 03:08 — HPA scale-out (pas suffisant)

```json
{"@timestamp":"2026-05-02T03:08:19.444Z","level":"INFO","logger":"o.s.boot.web.embedded.tomcat.TomcatWebServer","thread":"main","message":"Tomcat started on port(s): 8080 (http)","pod_name":"notification-api-7d8f-l5vx"}
{"@timestamp":"2026-05-02T03:08:21.882Z","level":"INFO","logger":"com.zaxxer.hikari.HikariDataSource","thread":"main","message":"HikariPool-1 - Start completed.","pool_total":20}
{"@timestamp":"2026-05-02T03:09:55.117Z","level":"WARN","logger":"com.zaxxer.hikari.pool.HikariPool","thread":"http-nio-8080-exec-2","message":"HikariPool-1 - Pool stats (total=20, active=20, idle=0, waiting=18)"}
```

> 💡 **Indice** : un nouveau pod démarre à 03:08, mais sa propre pool de 20 connections sature **également** au bout d'1 minute. → Le scale-out app n'aide pas si la DB est le vrai bottleneck. Et 5 pods × 20 = 100 connections vers la DB, qui peut elle-même être limitée.

### 03:42 — Liveness probe failure (conséquence, pas cause)

```json
{"@timestamp":"2026-05-02T03:42:11.882Z","level":"WARN","logger":"o.s.b.actuate.health.HealthEndpoint","thread":"http-nio-8080-exec-actuator","message":"Health check timed out","duration_ms":5001,"timeout_threshold_ms":5000,"failed_indicator":"db"}
{"@timestamp":"2026-05-02T03:42:14.220Z","level":"WARN","logger":"o.s.b.actuate.health.HealthEndpoint","thread":"http-nio-8080-exec-actuator","message":"Health check timed out","duration_ms":5002,"timeout_threshold_ms":5000,"failed_indicator":"db"}
```

> 💡 **Indice** : le liveness probe checke la DB. Si la pool est saturée, le probe ne récupère pas de connection à temps → marqué failed → pod redémarré par Kubernetes. **C'est une conséquence du pool plein, pas une cause.**

### 03:43 — Job programmé continue normalement (intéressant)

```json
{"@timestamp":"2026-05-02T03:43:02.554Z","level":"INFO","logger":"c.acme.notif.scheduler.MonthlyDigestJob","thread":"scheduler-pool-1","message":"Loaded recipients batch","batch_size":2500,"batch_index":12,"total_batches":17}
{"@timestamp":"2026-05-02T03:43:14.992Z","level":"INFO","logger":"c.acme.notif.scheduler.MonthlyDigestJob","thread":"scheduler-pool-1","message":"Batch dispatched","batch_index":12,"successful":2412,"failed":88,"failed_reason":"connection_timeout"}
```

> 💡 **Indice** : le job programmé tourne sur sa propre pool (`scheduler-pool-1`) et continue à dispatcher. Mais ~3,5 % d'échecs `connection_timeout` → certaines notifications **ne partent pas**. Cohérent avec la plainte métier ("certaines notifications critiques n'ont pas été envoyées").

### 04:18 — Décrue naturelle du pic

```json
{"@timestamp":"2026-05-02T04:18:33.221Z","level":"INFO","logger":"c.acme.notif.scheduler.MonthlyDigestJob","thread":"scheduler-pool-1","message":"Monthly digest dispatch completed","total_dispatched":40850,"total_failed":1650,"duration_ms":7818214}
{"@timestamp":"2026-05-02T04:19:42.882Z","level":"INFO","logger":"com.zaxxer.hikari.pool.HikariPool","thread":"http-nio-8080-exec-5","message":"HikariPool-1 - Pool stats (total=20, active=12, idle=8, waiting=0)"}
```

> 💡 **Indice clé** : le job se termine à 04:18. La pool revient en mode normal **dès 04:19**. C'est le job qui se termine qui libère la DB, **pas le rollout restart manuel** (qui n'a lieu qu'à 04:31).

### 04:31 — Rollout manuel astreinte L2

```json
{"@timestamp":"2026-05-02T04:31:02.115Z","level":"INFO","logger":"o.s.b.actuate.shutdown.ShutdownEndpoint","thread":"http-nio-8080-exec-actuator","message":"Initiating graceful shutdown","pod_name":"notification-api-7d8f-r4nq","initiated_by":"kubectl-rollout-restart"}
{"@timestamp":"2026-05-02T04:31:48.667Z","level":"INFO","logger":"o.s.boot.web.embedded.tomcat.TomcatWebServer","thread":"main","message":"Tomcat started on port(s): 8080 (http)","pod_name":"notification-api-7d8f-r4nq"}
```

### 04:35 — Activité normale

```json
{"@timestamp":"2026-05-02T04:35:11.882Z","level":"INFO","logger":"com.zaxxer.hikari.pool.HikariPool","thread":"http-nio-8080-exec-3","message":"HikariPool-1 - Pool stats (total=20, active=4, idle=16, waiting=0)"}
{"@timestamp":"2026-05-02T04:35:42.114Z","level":"INFO","logger":"c.acme.notif.NotificationController","thread":"http-nio-8080-exec-3","message":"Notification queued for delivery","correlation_id":"req-q1w2e3","duration_ms":42,"status":"queued"}
```

> 💡 **Indice** : la pool a 16 connexions idle et 0 waiting. État normal. Mais l'incident était déjà résolu **avant** le rollout (à 04:18, cf. ci-dessus).

---

## Échantillons de bruit récurrent (présents même hors incident)

### Erreurs Hibernate récurrentes (présentes 24/24)

```json
{"@timestamp":"2026-05-02T02:18:42.115Z","level":"ERROR","logger":"o.h.engine.jdbc.spi.SqlExceptionHelper","thread":"http-nio-8080-exec-4","message":"Could not deserialize from session","exception":"org.hibernate.LazyInitializationException: could not initialize proxy [...] - no Session"}
{"@timestamp":"2026-05-02T01:18:42.115Z","level":"ERROR","logger":"o.h.engine.jdbc.spi.SqlExceptionHelper","thread":"http-nio-8080-exec-2","message":"Could not deserialize from session","exception":"org.hibernate.LazyInitializationException: could not initialize proxy [...] - no Session"}
```

> 🎭 **Bruit** : ces erreurs `LazyInitializationException` apparaissent **toutes les heures à :18 ±5 min**, même hors incident. Probable bug applicatif récurrent qui ne participe **pas** à l'incident actuel. Un analyste pressé pourrait s'arrêter dessus.

### Spring Security warnings récurrents

```json
{"@timestamp":"2026-05-02T02:45:33.117Z","level":"WARN","logger":"o.s.security.web.firewall.StrictHttpFirewall","thread":"http-nio-8080-exec-8","message":"Request rejected: untrusted hostname","host":"scanner-bot-xyz.com"}
```

> 🎭 **Bruit** : tentatives de scan automatique. Présent 24/24, pas lié à l'incident.
