---
type: incident-input
source: datadog
service: notification-api
namespace: notif-prod
window: 2026-05-02T01:00:00Z to 2026-05-02T05:30:00Z
---

> **FIXTURE** — Données synthétiques créées pour les tests du MVP (Phase 4–5). Aucune donnée réelle de production.

# Datadog snapshot — notification-api (nuit 2026-05-01 / 2026-05-02)

> Export texte des graphiques Datadog clés sur la fenêtre d'incident. Fenêtre élargie à 01:00-05:30 pour comparer avant/pendant/après.

---

## 1. Erreurs HTTP par code (RED metrics)

Aggregation : 1-minute buckets. Source : `service:notification-api env:prod`.

```
Code  | 01:00-01:59 | 02:00-02:29 | 02:30-02:59 | 03:00-03:29 | 03:30-03:59 | 04:00-04:29 | 04:30-05:30
------|-------------|-------------|-------------|-------------|-------------|-------------|------------
200   |    8 412    |    6 230    |    3 105    |    2 880    |    3 442    |    5 820    |    8 105
4xx   |       42    |       58    |       91    |      120    |       96    |       54    |       38
500   |        0    |      183    |      642    |      724    |      511    |      247    |        4
502   |        0    |        0    |        4    |       12    |        7    |        2    |        0
504   |        0    |       11    |       38    |       45    |       29    |        9    |        0
```

**Lecture** : pic d'erreurs 500 entre 02:30 et 04:00, retour à la normale après 04:30. Erreurs 4xx également en hausse mais dans une moindre mesure. Trafic 200 nettement réduit pendant la fenêtre (effondrement du débit utile).

---

## 2. Latence p50 / p95 / p99 (millisecondes)

Aggregation : moyenne sur 5-minute buckets.

```
Window       |  p50  |  p95  |  p99  |  max
-------------|-------|-------|-------|------
01:00-01:59  |   42  |  180  |  340  |  812
02:00-02:29  |   95  |  640  | 1850  | 4 920
02:30-02:59  |  140  | 4 780 | 5 010 | 5 012  ← p95 plafond visible (timeout 5s)
03:00-03:29  |  155  | 4 920 | 5 011 | 5 012  ← p95 plafond visible
03:30-03:59  |  120  | 3 450 | 5 008 | 5 011
04:00-04:29  |   78  |  890  | 2 100 | 4 912
04:30-05:30  |   38  |  165  |  290  |  720
```

**Lecture** : p95 plafonne à ~5 000 ms entre 02:30 et 04:00. Le p50 reste relativement bas (~140 ms) → la majorité des requêtes passe normalement, mais une fraction significative timeout. Plafond suggère un timeout configuré côté client ou serveur.

---

## 3. Pod restarts (notif-prod namespace)

Aggregation : `kube_pod_container_status_restarts_total{namespace="notif-prod",pod=~"notification-api-.*"}`.

```
Pod                          | Restart at         | Reason (from kubectl)
-----------------------------|--------------------|----------------------
notification-api-7d8f-2xkl   | 03:42:18 UTC       | (Liveness probe failed)
notification-api-7d8f-9mpz   | 03:48:51 UTC       | (Liveness probe failed)
notification-api-7d8f-r4nq   | 04:31:02 UTC       | Manual rollout restart (operator)
notification-api-7d8f-x8tm   | 04:31:04 UTC       | Manual rollout restart (operator)
notification-api-7d8f-2xkl   | 04:31:07 UTC       | Manual rollout restart (operator)
notification-api-7d8f-9mpz   | 04:31:09 UTC       | Manual rollout restart (operator)
notification-api-7d8f-l5vx   | 04:31:11 UTC       | Manual rollout restart (operator)
```

**Lecture** : 2 restarts auto-déclenchés par Liveness probe entre 03:42 et 03:48. Puis rollout manuel par l'astreinte L2 à 04:31 (5 pods).

---

## 4. Memory usage des pods (RSS, %)

Aggregation : moyenne par pod sur 1-minute buckets.

```
Window       | avg pod memory |  peak pod memory |  HPA replicas
-------------|----------------|------------------|---------------
01:00-01:59  |     58 %       |       64 %       |       3
02:00-02:29  |     67 %       |       78 %       |       3
02:30-02:59  |     81 %       |       94 %       |       4   ← scale-out à 02:33
03:00-03:29  |     86 %       |       98 %       |       5   ← scale-out à 03:08
03:30-03:59  |     78 %       |       92 %       |       5
04:00-04:29  |     62 %       |       74 %       |       5
04:30-05:30  |     45 %       |       58 %       |       3   ← scale-in à 05:02
```

**Lecture** : HPA a effectivement réagi (3 → 5 pods) entre 02:33 et 03:08. Memory peak frôle la limite (98 %) mais ne déclenche pas d'OOMKill. Retour à la normale après 04:30.

---

## 5. CPU usage des pods (%)

```
Window       | avg pod CPU    |  peak pod CPU
-------------|----------------|----------------
01:00-01:59  |     38 %       |       52 %
02:00-02:29  |     54 %       |       68 %
02:30-02:59  |     61 %       |       73 %  ← scale-out déclenché ici (target 70 %)
03:00-03:29  |     58 %       |       69 %  ← après scale, en deçà du target
03:30-03:59  |     52 %       |       64 %
04:00-04:29  |     45 %       |       58 %
04:30-05:30  |     32 %       |       44 %
```

**Lecture** : CPU dépasse brièvement le target HPA (70 %) à 02:33 → scale-out légitime. Reste **modéré** pendant tout l'incident (jamais > 75 %).

---

## 6. Datadog alerts déclenchées sur la fenêtre

```
02:34:12  WARN   notification-api - 5xx error rate above 1% (threshold)
02:48:55  CRIT   notification-api - 5xx error rate above 5% (threshold)
03:11:02  CRIT   notification-api - p95 latency above 2000ms
03:42:18  CRIT   K8s liveness probe failures (notification-api pod)
04:38:40  WARN   notification-api - 5xx error rate cleared (below 1%)
05:01:15  INFO   K8s liveness probe failures cleared
```

---

## Notes de l'astreinte L2 (extrait Slack #incidents, traduit anonymisé)

```
03:45  Astreinte L2 : "Je vois des liveness fails et du 5xx, je redémarre les pods"
04:31  Astreinte L2 : "Rollout restart fait. Je surveille."
04:50  Astreinte L2 : "Ça se calme, latence revient normale"
05:05  Astreinte L2 : "OK clos pour ce soir, jour-J peut creuser demain matin si besoin"
```
