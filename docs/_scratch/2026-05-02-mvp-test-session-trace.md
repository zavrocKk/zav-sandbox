
───────────────── 🛠️ DevOps — Triage et timeline ─────────────────

Reconstitution chronologique (sources : Datadog, Splunk, Helm/RDS config) :

Heure UTC	Événement	Source
02:00	État nominal (p95 ~180 ms, 0 erreurs 5xx, 3 pods, pool DB idle)	Datadog §1, §2
02:14	MonthlyDigestJob démarre, ~42 500 destinataires sur 17 batches via scheduler-pool-1	Splunk
02:32	Premier WARN HikariCP : total=20, active=20, idle=0, waiting=14, timeout 5001 ms	Splunk
02:33	GlobalErrorHandler mappe CannotGetJdbcConnectionException → HTTP 500	Splunk
02:33	HPA scale-out : 3 → 4 pods (CPU 73 % > target 70 %)	Datadog §4, §5
02:34	Datadog WARN « 5xx > 1 % »	Datadog §6
02:48	Datadog CRIT « 5xx > 5 % »	Datadog §6
03:08	HPA scale-out : 4 → 5 pods. Le nouveau pod sature sa propre pool en <1 min	Splunk, Datadog §4
03:11	Datadog CRIT « p95 > 2000 ms » (plafond 5 s = HikariCP timeout)	Datadog §2, §6
03:42	Liveness probe failure (DB indicator timeout) → restart auto pod 2xkl	Splunk, Datadog §3
03:48	Restart auto pod 9mpz	Datadog §3
04:18	MonthlyDigestJob termine : 40 850 dispatched, 1 650 échecs connection_timeout. Pool revient idle dès 04:19	Splunk
04:31	Rollout restart manuel L2 (5 pods) — incident déjà résolu depuis 13 min	Datadog §3, Splunk
04:38	Datadog WARN cleared (5xx < 1 %)	Datadog §6
Déclencheur exogène identifié : job batch programmé (MonthlyDigestJob) consommant la pool DB partagée à partir de 02:14. Pas de changement applicatif (dernier déploiement 4.7.2 le 2026-04-26).

Hypothèses pour Dev/Architect :

Saturation pool HikariCP confirmée par les stats (waiting=14→22).
Le scheduler partage la pool avec HTTP → contention directe.
Action L2 sans effet causal sur la résolution (post-hoc, ergo propter hoc inversé).
───────────────── 💻 Developer — Symptômes vs causes, fausses pistes ─────────────────

Cascade symptôme → cause :
HTTP 500 côté client (symptôme observé par métier)
   ↑ (mappé par GlobalErrorHandler.java, qui transforme TOUTE exception en 500)
CannotGetJdbcConnectionException (symptôme intermédiaire)
   ↑ (HikariCP timeout après 5 s)
Pool HikariCP saturée : active=20/20, waiting jusqu'à 22 threads
   ↑ (consommation > capacité)
MonthlyDigestJob accapare des connexions sur la pool partagée HikariPool-1 ← CAUSE TECHNIQUE

Conséquences en cascade (pas des causes) :

Liveness probe fails (03:42, 03:48) : MANAGEMENT_HEALTH_DB_ENABLED=true → le probe tente d'acquérir une connexion → timeout 5 s > probe timeout 5 s → pod tué. Conséquence du pool plein, pas une cause. Aggrave la situation (pods relancés démarrent avec leur propre pool de 20 vide à remplir, et entre-temps moins de capacité).
Latence p95 plafond à 5 010 ms : exactement SPRING_DATASOURCE_HIKARI_CONNECTION_TIMEOUT=5000. Plafond mathématique, pas un comportement applicatif.
HPA scale-out 3→5 : réaction CPU légitime, mais inutile car le bottleneck est la DB (chaque nouveau pod ajoute 20 connexions à demander à une DB déjà sous pression).
Fausses pistes documentées (à écarter explicitement) :

LazyInitializationException Hibernate : présentes 24/24 toutes les heures à :18 ±5 min, avant et après l'incident. Bug applicatif récurrent indépendant — à traiter en backlog, sans rapport avec l'incident.
StrictHttpFirewall warnings : scans automatiques continus, bruit de fond.
Le rollout restart L2 (04:31) a résolu l'incident : faux. La pool revient nominale à 04:19, soit 12 min avant le restart manuel. La résolution est due à la fin naturelle du job (04:18). Le restart a juste coïncidé avec la décrue.
Bug applicatif aggravant (à corriger en plus du root cause) :

GlobalErrorHandler transforme toute exception backend en HTTP 500 sans distinction. Une CannotGetJdbcConnectionException (transient, retryable) devrait remonter un 503 Service Unavailable avec Retry-After, pas un 500. Cela masque la nature transient et empêche les clients (et le métier) de comprendre qu'un retry aurait pu réussir.
Impact métier (notifications perdues) :

Job batch : 1 650 échecs connection_timeout sur 42 500 (~3,9 %) — ces notifications du digest mensuel ne sont pas parties.
Trafic HTTP synchrone : ~2 100 erreurs 500 cumulées entre 02:30 et 04:30 (Datadog §1) — notifications déclenchées par l'API (probablement les « critiques » du métier) en échec.
───────────────── 🏗️ Architect — Cause racine structurelle ─────────────────

Cause racine technique : partage non protégé d'une ressource saturée (pool DB) entre deux workloads concurrents (HTTP synchrone + batch scheduler), sur une infrastructure DB sous-dimensionnée par rapport au scale-out applicatif.

Démonstration arithmétique (capacity planning défaillant) :

Consommateur	Pool max	Pods max	Total connexions potentielles
notification-api HTTP + scheduler (pool partagée)	20	5 (HPA max 10)	100 (jusqu'à 200 si HPA max atteint)
reporting-api	15	n/a	15
notification-worker	10	n/a	10
Total demandeurs			125 minimum, 225 max théorique
DB max_connections			100
→ La configuration permet structurellement un dépassement de la capacité DB. Le HPA aggrave : chaque nouveau pod de notification-api ajoute 20 connexions demandées à une DB déjà saturée.

Causes systémiques (pourquoi cet incident a pu arriver et durer 1h45) :

Capacity planning DB absent : aucune vérification Σ(pool_max × replicas_max) ≤ max_connections × 0.8.
Couplage des workloads via pool DB partagée : MonthlyDigestJob et trafic HTTP partagent HikariPool-1. Un pic batch tue le synchrone.
Observabilité aveugle au bottleneck réel : alertes Datadog uniquement sur symptômes côté HTTP (5xx, p95). Aucune alerte sur :
hikaricp.connections.usage / hikaricp.connections.pending
hikaricp.connections.acquire (wait time)
RDS DatabaseConnections vs max_connections
Health check qui s'auto-DoS : MANAGEMENT_HEALTH_DB_ENABLED=true sur la liveness probe avec timeoutSeconds=5 = connectionTimeout HikariCP. La saturation pool tue les pods, aggravant la saturation au lieu de l'absorber. La liveness ne devrait pas dépendre de la DB ; la readiness oui, mais avec un pattern circuit-breaker.
Runbook scheduler inexistant : aucun signal/runbook ne dit à l'astreinte « si HikariCP sature pendant la fenêtre 02:00-05:00, vérifier MonthlyDigestJob avant tout ». L'astreinte L2 a fait un rollout restart inutile et risqué (aurait pu prolonger l'incident en vidant les pools warm).
Error handling masquant : GlobalErrorHandler qui mappe tout en 500 empêche la détection précoce et la classification correcte des erreurs DB transient.
Recommandations structurelles (à formaliser en ADR) :

Priorité	Action	Type
P0	Découpler le scheduler : pool HikariCP dédiée (scheduler-pool-ds) avec max=5, ou throttling explicite (semaphore N=5)	Préventif
P0	Désactiver le check DB sur liveness (MANAGEMENT_HEALTH_DB_ENABLED=false côté /health/liveness), garder sur readiness uniquement, augmenter timeoutSeconds readiness à 10 s	Préventif
P0	Alertes Datadog sur HikariCP : connections.pending > 5 pendant 2 min (WARN), > 15 pendant 1 min (CRIT) ; alerte RDS DatabaseConnections > 80	Détection
P1	Capacity planning DB : passer RDS à db.r6g.xlarge (200 connexions) ou plafonner HPA maxReplicas=4 tant que la DB n'est pas redimensionnée	Préventif
P1	GlobalErrorHandler : mapper CannotGetJdbcConnectionException et exceptions JDBC transient → HTTP 503 + Retry-After: 30	Préventif
P1	Retry / DLQ pour MonthlyDigestJob : les 1 650 destinataires en échec doivent être rejoués (à valider avec métier sur ce run précis)	Mitigation
P2	Runbook : « Saturation HikariCP pendant fenêtre batch nocturne »	Détection
P2	ADR sur stratégie de pooling et de séparation HTTP/batch	Structurel
Action immédiate métier : rejouer le batch sur les 1 650 destinataires en échec + identifier les 5xx HTTP de la fenêtre pour rejeu côté API appelants.

───────────────── 📝 Scribe — Bilan et livrable ─────────────────

Bilan synthétique : incident SEV2 sur notification-api causé par saturation de la pool HikariCP partagée entre trafic HTTP et MonthlyDigestJob, sur fond de sous-dimensionnement DB structurel (Σ pools potentielles > max_connections PostgreSQL). Symptômes (500, p95 plafond, liveness fails) tous explicables par cette cause unique. Le rollout restart L2 a coïncidé avec la fin naturelle du job (04:18) et n'a pas causé la résolution. Impact : ~1 650 notifications batch + ~2 100 erreurs HTTP synchrones non délivrées sur la fenêtre. 8 actions correctives proposées, dont 3 P0.

Création du livrable Type A maintenant.

Edited
2026-05-02-notification-api-5xx.md+148-1
CLOSE
Fichiers créés :

2026-05-02-notification-api-5xx.md — rapport d'incident complet (SEV2, 8 actions, 4 leçons)
Synthèse une ligne : cause racine = saturation pool HikariCP partagée entre HTTP et MonthlyDigestJob, sur fond de sous-dimensionnement DB structurel (Σ pools potentielles 125+ > max_connections=100). Résolution naturelle à 04:18 (fin du job), restart L2 à 04:31 = post-hoc.

Actions de suivi recommandées :

Immédiat (J+3) : action #6 — coordonner avec métier le rejeu des 1 650 destinataires en échec du digest mensuel.
Court terme (J+7) : actions #1 et #2 — désactiver DB check sur liveness + alertes HikariCP/RDS (changements de config low-risk, immense gain de signal).
Moyen terme : action #8 — ouvrir un ADR sur la stratégie de pooling. Je peux le démarrer dès que tu valides.