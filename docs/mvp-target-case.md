---
type: mvp-target-case
phase: 5.2
status: accepted
date: 2026-05-02
---

# MVP Target Case — "Le 5xx fantôme du service notification-api"

> Cas concret servant à valider que le framework Agentic Team livre de la valeur réelle sur le quotidien d'un analyste technique. Ce fichier est la référence du test exécuté en Phase 5.4.

---

## Pourquoi ce cas (Phase 5.2)

Le framework a été construit en Phases 0-3, refactoré en Phase 5.3, et n'a été testé qu'une fois en Phase 4 (audit `/admin/users` — cas artificiel). Avant d'enchaîner sur Phase 6 (Party Mode) ou toute extension, il faut **prouver** que le framework livre de la valeur sur **un cas réel du quotidien d'analyste technique**.

Ce cas a été construit synthétiquement à partir de patterns réels rencontrés au bureau (cf. session du 2026-05-02), calibré pour un analyste seul (pas une équipe d'experts), sans fuite IP ni comparaison directe avec d'autres frameworks.

## Profil utilisateur simulé

L'analyste technique d'astreinte (toi) reçoit un signalement le matin et doit produire un rapport d'analyse exploitable **avec uniquement le framework Agentic Team comme support** (Copilot Chat + Sonnet 4.6 + custom Orchestrator).

## Contexte de l'incident

> Le service `notification-api` (Java Spring Boot, déployé sur EKS, namespace `notif-prod`) a remonté des alertes pendant la nuit dernière entre **02:00 et 04:30 UTC**. L'astreinte L2 a redémarré les pods (`kubectl rollout restart deployment/notification-api -n notif-prod`), ce qui a fait disparaître les symptômes. Aucun changement applicatif n'a été déployé dans les 7 derniers jours. Le métier remonte une plainte ce matin : *« certaines notifications critiques n'ont pas été envoyées entre 02h et 05h. »*
>
> **Mission de l'analyste** : comprendre ce qui s'est passé, identifier la cause racine probable, distinguer symptômes et causes, et produire un rapport d'analyse de logs exploitable.

## Inputs fournis au framework

Trois fichiers d'inputs synthétiques sont fournis au framework au démarrage de la session :

| Input | Fichier | Contenu |
|---|---|---|
| Métriques | `mvp-inputs/datadog-snapshot.md` | Graphiques résumés : erreurs HTTP, latence p50/p95/p99, pod restarts, memory usage |
| Logs applicatifs | `mvp-inputs/splunk-extract.md` | Échantillons de logs structurés (INFO/WARN/ERROR) sur la fenêtre 02:00-04:30 |
| Configuration | `mvp-inputs/runtime-config.md` | HPA, resources pods, connection pool DB |

L'analyste démarre la session en plaçant ces 3 fichiers dans son contexte VSCode et en formulant la mission au custom Orchestrator.

## Pièges intégrés (cachés au framework)

L'incident contient **1 fausse piste** + **1 cause racine réelle**.

🎭 **Fausse piste** : des erreurs HTTP **500** apparaissent dans Datadog. En réalité, ce sont des `400 Bad Request` qui ont été mal mappés par un middleware applicatif. Un analyste qui s'arrête au code 500 va chercher du côté serveur sans raison.

🎯 **Cause racine** : le **connection pool de la base de données est saturé** pendant un pic d'activité légitime (campagne mensuelle automatique de notifications, prévisible mais non documentée). Le HPA ne scale pas car il est configuré sur le CPU (resté à 60%), mais c'est la DB qui est en bottleneck. Les threads applicatifs en attente de connexion expirent au bout de 5s → erreurs 4xx vers le client → mappées en 500 par le middleware → faux signal.

Quand l'astreinte a fait `rollout restart`, le pic était **déjà en train de naturellement décroître** → fausse impression que le restart a corrigé.

**Note** : le framework ne doit PAS connaître ces réponses à l'avance. Il les découvre via l'analyse des inputs.

## Livrable attendu

Un fichier markdown créé par le Scribe à `docs/incidents/2026-05-02-notification-api-5xx.md` (ou nom équivalent), contenant **au minimum** :

1. **Timeline reconstituée** des événements (02:00 → 04:30 → 09:00 plainte métier)
2. **Hypothèses qualifiées** — au moins 3 hypothèses formulées, classées (validée / écartée / à investiguer)
3. **Cause racine probable** avec niveau de confiance et faisceau d'indices
4. **Distinction symptôme vs cause** explicitement formulée
5. **Bruit identifié** — la fausse piste 500/400 et pourquoi elle trompait
6. **Recommandations** prioritaires : capacity DB, HPA basé sur custom metric, amélioration logs, documentation des pics récurrents

Le format exact n'est pas imposé (volontairement — pas de template `log-analysis-report.md` créé en avance, conformément à la décision Phase 5.2).

## Critères de réussite

8 critères évalués pendant le test Phase 5.4. Test réussi si **6 critères sur 8** passent.

| # | Critère | OK si... | Lié à |
|---|---|---|---|
| 1 | **Détection cause racine** | Le framework identifie le connection pool DB comme cause probable, OU formule une hypothèse qualifiée correcte avec faisceau d'indices cohérent | Valeur métier |
| 2 | **Détection de la fausse piste** | Le framework écarte explicitement le code 500 comme cause primaire, identifie ou suspecte le mapping 4xx → 5xx | Valeur métier |
| 3 | **Distinction symptôme/cause** | Le rapport sépare clairement ce qui est conséquence de ce qui est cause | Qualité livrable |
| 4 | **PRE-FLIGHT respecté** | L'orchestrator pose les 4 questions PRE-FLIGHT avant de démarrer | Anti-drift (Phase 5.3 action 3) |
| 5 | **PLAN avant exécution** | Présente un PLAN avec personas mobilisés, attend confirmation utilisateur | Anti-drift |
| 6 | **Workflow et checklist déclenchés** | Identifie `incident-response.md` comme workflow approprié, mentionne `incident-triage.md` (au moins en référence) | Branchement Phase 5.3 action 1 |
| 7 | **Personas mobilisés** | DevOps + Developer (ou Architect) + Scribe au minimum, avec passage de relais explicite | Workflow respecté |
| 8 | **Synthèse Scribe (Type A)** | Création explicite d'un fichier `docs/incidents/...` (Type A — pas une consultation) sans demander à l'utilisateur si on doit créer le fichier | Contrat Scribe Phase 5.3 action 2 |

## Durée acceptable

**45 min à 1 heure** dans VSCode + Copilot Chat avec Claude Sonnet 4.6, en mode Agent Orchestrator custom.

Au-delà d'1h30, on considère que le framework a été en difficulté → critère implicite d'échec opérationnel.

## Observations à collecter pendant le test

À noter au fil de l'eau dans un fichier scratch (`docs/_scratch/2026-05-XX-test-mvp-observations.md`) qui sera consolidé dans `docs/decisions/0003-test-mvp-frictions.md` en Phase 5.5.

| Catégorie | À noter |
|---|---|
| **Frictions** | Où le framework hésite, drift, oublie quelque chose |
| **Manques** | Template absent, persona qui sature, output mal structuré |
| **Forces** | PRE-FLIGHT déclenché correctement, Scribe respecte le contrat, etc. |
| **Surprises** | Comportement inattendu (positif ou négatif) |
| **Temps** | Durée totale, durée par phase |

## Garde-fous d'exécution (Phase 5.4)

🚫 **Interdit pendant le test** :
- Modifier les fichiers du framework (personas, workflows, templates) en cours de test
- Aider le framework si il dérape — laisser le système échouer pour observer la friction
- Comparer en cours de test avec d'autres frameworks ou avec une exécution manuelle imaginée

✅ **Autorisé** :
- Reformuler la question si le framework demande une clarification légitime
- Confirmer un PLAN proposé (oui / ajuste)
- Annuler la session et redémarrer si le framework drift de manière irrécupérable (avec note dans le fichier observations)

## Décisions prises

- ✅ **Test sans template log-analysis-report.md** (option α de la Phase 5.2). Le template sera créé **après** le test, calibré sur ce que le Scribe aura produit naturellement.
- ✅ **Incident synthétique** (option C de la Phase 5.2), pas un incident réel ni le cas BMAD bureau.
- ✅ **1 fausse piste** (V2 simplifiée), pas 3 (V1 rejetée). Validation de la mécanique avant validation de la robustesse face au bruit.
- ✅ **Stack cloud-native** (Java Spring Boot + EKS + Datadog + Splunk), pas legacy onprem.

## Références

- `VISION.md` — boussole stratégique
- `ROADMAP.md` — feuille de route, Phase 5.2 → 5.4 → 5.5
- `docs/decisions/0002-audit-existant.md` — audit Phase 5.1
- `IDEAS.md` — parking lot (notamment "Templates manquants pour runbook et architecture", "Workflow problem-resolution", etc.)

---

## Prochaine étape

**Phase 5.4** — Exécution du test dans VSCode + Copilot Chat (Sonnet 4.6, Agent Orchestrator), avec collecte des observations en parallèle.

Quand le test est terminé, retour ici (Claude.ai) pour la **Phase 5.5** : consolidation des frictions dans un ADR-0003 et décision sur les prochains correctifs.
