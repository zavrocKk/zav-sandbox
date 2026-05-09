---
type: decision
number: 0003
status: accepted
date: 2026-05-03
deciders: [zavrocKk]
tags: [test-mvp, phase-5, validation, frictions]
supersedes: none
---

# ADR-0003 — Test du MVP (Phase 5.4 + 5.4-bis) et clôture du chapitre 5

> Document de clôture de la Phase 5 du framework Agentic Team. Consolide les résultats du test MVP (cas synthétique notification-api) et du test complémentaire PRE-FLIGHT (prompt ambigu). Décide la suite : GO Phase 6 ou correctifs intermédiaires.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-05-03
**Décideurs** : utilisateur (zavrocKk)

## Contexte

À l'issue de la Phase 5.3 (refonte ciblée — 10 correctifs + 2 créations appliqués), il fallait valider que le framework livre **réellement** de la valeur sur un cas concret du quotidien d'analyste technique, conformément à la cible définie dans `VISION.md`.

Cette validation a été menée en deux temps :
- **Phase 5.4** — test sur un incident synthétique calibré (`docs/mvp-target-case.md`)
- **Phase 5.4-bis** — test complémentaire de la Friction A détectée en 5.4 (PRE-FLIGHT silencieux), via prompt volontairement ambigu

L'ADR-0003 consolide les résultats des deux tests et conclut formellement la Phase 5.

## Décision

**Le MVP du framework Agentic Team est validé.** Score final : **8/8 critères de réussite** sur les deux tests combinés.

Aucun correctif framework supplémentaire n'est requis avant la Phase 6 (Party Mode). Les frictions résiduelles identifiées sont notées dans `IDEAS.md` pour examen ultérieur.

## Méthode de test

### Phase 5.4 — Test principal

**Cas** : incident synthétique "Le 5xx fantôme du service notification-api"
**Setup** : Java Spring Boot sur EKS, fenêtre nuit 02:00-04:30 UTC, plainte métier le matin
**Inputs fournis** : Datadog snapshot, Splunk extract, runtime config (3 fichiers markdown synthétiques)
**Pièges intégrés** : 1 fausse piste (mapping 4xx→5xx) + 1 cause racine réelle (saturation pool HikariCP)
**Modèle** : Claude Sonnet 4.6, custom Orchestrator agent dans VSCode + Copilot Chat

### Phase 5.4-bis — Test complémentaire

**Cas** : prompt volontairement ambigu pour stresser le PRE-FLIGHT
**Prompt envoyé** : *« on a eu un truc bizarre cette nuit, je peux te montrer les logs si besoin. peux-tu m'aider à comprendre ? »*
**Ambiguïtés intégrées** : 5 (service, symptômes, fenêtre, impact, logs disponibles)
**Critère** : test réussi si l'orchestrator pose ≥ 2 questions ET ne démarre pas le PLAN sans clarification

## Résultats

### Score officiel — 8/8

| # | Critère | Phase 5.4 | Phase 5.4-bis | Statut |
|---|---|---|---|---|
| 1 | Détection cause racine | ✅ Cause technique + 5 causes systémiques identifiées | n/a | ✅ |
| 2 | Détection fausse piste 500/400 | ✅ Mapping middleware identifié, correction proposée (HTTP 503 + Retry-After) | n/a | ✅ |
| 3 | Distinction symptôme/cause | ✅ Cascade explicite + biais "post hoc ergo propter hoc" identifié | n/a | ✅ |
| 4 | PRE-FLIGHT respecté | 🟡 Probablement fait, non verbalisé | ✅ Verbalisé explicitement avec 5 questions ciblées | ✅ |
| 5 | PLAN avant exécution | ✅ Confirmé | ✅ "PLAN provisoire" présenté en attente de validation | ✅ |
| 6 | Workflow + checklist déclenchés | 🟡 Workflow implicite, checklist non visible | ✅ Workflow et checklist mentionnés explicitement | ✅ |
| 7 | Personas mobilisés | ✅ DevOps + Developer + Architect + Scribe (4 personas) | ✅ Mêmes 4 personas annoncés dans PLAN provisoire | ✅ |
| 8 | Synthèse Scribe (Type A) | ✅ "Création du livrable Type A maintenant" — fichier créé sans demander | n/a | ✅ |

### Métriques observées

**Durée d'exécution Phase 5.4** : **< 1 minute** (de prompt initial à création du fichier)
**Comparaison manuelle estimée** : 30 à 60 minutes pour produire un rapport équivalent
**Ratio gain de temps** : **30x à 60x** sur ce cas

### Qualité du livrable produit

Le rapport `2026-05-02-notification-api-5xx.md` produit par le Scribe contient :
- Timeline chronologique reconstituée (heure / événement / source)
- Cascade symptôme → cause documentée
- 3 fausses pistes documentées et écartées avec preuves
- Cause racine technique + 5 causes systémiques structurelles
- Démonstration arithmétique du capacity planning défaillant (Σ pools potentielles 125+ vs max_connections=100)
- 8 actions correctives priorisées (P0/P1/P2) avec ownership implicite
- 4 leçons apprises

**Niveau qualité** : senior. Au-delà de l'attendu (le test avait été calibré pour ≥ 6/8 critères, on a 8/8 + qualité ★★★).

### Validations spécifiques des correctifs Phase 5.3

Le test confirme l'efficacité des correctifs majeurs appliqués en Phase 5.3 :

| Correctif Phase 5.3 | Validation Phase 5.4 / 5.4-bis |
|---|---|
| Action 1 — Brancher checklists dans l'écosystème | ✅ Checklist `incident-triage.md` mentionnée explicitement en 5.4-bis |
| Action 2 — Centraliser contrat Scribe | ✅ Type A déclaré et fichier créé sans demander confirmation |
| Action 3 — Refactor PRE-FLIGHT | ✅ Mécanisme se déclenche correctement face à un prompt ambigu |
| Actions 9-10 — Templates runbook + architecture | (non testés ce test-ci, à valider sur cas futur) |

## Frictions résiduelles identifiées

### Friction A — PRE-FLIGHT silencieux quand le contexte est clair *(résolue par observation)*

**Description** : sur un prompt déjà bien structuré (Phase 5.4), le PRE-FLIGHT n'est pas verbalisé. L'utilisateur ne peut pas vérifier qu'il a été exécuté.

**Statut** : ⚪ **Acceptée comme comportement normal**.

**Justification** : le PRE-FLIGHT est par nature un mécanisme **conditionnel** — il s'active visiblement quand il y a quelque chose à challenger (ambiguïté, manque, présomption). Si le prompt initial ne présente aucune ambiguïté, le PRE-FLIGHT n'a rien à verbaliser. Le test 5.4-bis a confirmé qu'il s'active **correctement** quand nécessaire.

**Décision** : pas de correctif. La verbalisation systématique (incluant un PRE-FLIGHT "status: clear") serait du bruit pour les cas non-ambigus.

### Friction B — Test PRE-FLIGHT impossible avec un prompt trop bien structuré *(résolue par méthode)*

**Description** : le protocole de test Phase 5.4 utilisait un prompt initial trop propre pour stresser le PRE-FLIGHT.

**Statut** : ⚪ **Résolue par l'ajout de la Phase 5.4-bis**.

**Justification** : on dispose désormais d'un **double test** complémentaire (cas structuré + cas ambigu) qui couvre les deux modes de fonctionnement du PRE-FLIGHT.

**Décision** : conserver ce double-test comme méthode standard pour les futurs tests d'intégration (Phase 6+).

### Friction C — Format des questions PRE-FLIGHT *(notée dans IDEAS.md)*

**Description** : les 5 questions de cadrage sont posées en format markdown numéroté. L'utilisateur peut oublier de répondre à 1 ou 2 questions, ce qui peut engendrer des re-prompts.

**Statut** : 🟡 **Ouverte — notée dans IDEAS.md (entrée du 2026-05-03)**.

**Investigation à mener** : utilisation potentielle du tool natif `askQuestions` de VSCode pour les questions fermées (single/multi-select), conservation du format markdown pour les questions ouvertes.

**Décision** : **non urgent**. Le format actuel marche. À examiner en Phase 6 ou plus tôt si l'usage réel le révèle bloquant.

### Friction D — Observabilité du raisonnement de l'orchestrator *(notée dans IDEAS.md)*

**Description** : l'utilisateur ne voit que la sortie écrite, pas le raisonnement interne de l'orchestrator (combien d'hésitations, quel chemin de pensée, etc.). Difficile d'auditer en temps réel.

**Statut** : 🟡 **Ouverte — à noter dans IDEAS.md**.

**Investigation à mener** : ajouter des marqueurs explicites (« je consulte la checklist X », « je passe la main à Y parce que Z ») pour rendre le flux interne visible.

**Décision** : pas avant Phase 7 (mémoire persistante) — sujet lié à l'instrumentation globale.

## Conséquences

### Positives

- ✅ **Le MVP est officiellement validé.** Le framework fait ce que promet `VISION.md` : produire des livrables de qualité senior à partir de markdown pur, dans VSCode + Copilot natif.
- ✅ **ROI démontré** : gain de 30x à 60x sur le temps d'analyse pour ce type de cas, à qualité équivalente ou supérieure.
- ✅ **Anti-drift validé** : le PRE-FLIGHT s'active correctement face à un prompt ambigu, refuse de démarrer sans clarification.
- ✅ **Anti-clone validé** : aucun nom BMAD n'apparaît dans le framework ni dans les sorties. Identité propre tenue.
- ✅ **Différenciation tenue** : 100% markdown, natif VSCode + Copilot, lisible par non-dev, anti-drift par design — toutes les promesses VISION.md sont opérationnelles.
- ✅ **Innovations propres confirmées** : Type A vs Type B, contrat Scribe, PRE-FLIGHT en 4 questions — fonctionnent en pratique.

### Négatives

- 🟡 **Test sur un seul profil de cas** : on a validé sur un incident technique post-mortem. Pas encore validé sur les autres workflows (`code-analysis`, `feature-development`, `architecture-design`, `data-pipeline`).
- 🟡 **Test sur un seul utilisateur** : seul l'auteur du framework l'a utilisé. Pas encore validé sur un collègue moins senior, qui est pourtant la cible primaire de VISION.md.
- 🟡 **Templates `runbook.md` et `architecture.md` non testés** : créés en Phase 5.3 mais pas mis sous tension par ce test-ci.

### Neutres / À surveiller

- 4 frictions identifiées (A-D), dont 2 résolues et 2 ouvertes en parking lot. Aucune n'est bloquante pour la Phase 6.
- L'innovation `Type A vs Type B` est validée mais sa **lisibilité par un nouveau venu** reste à confirmer.

## Décision sur la suite

### GO Phase 6 — Party Mode contextuel

Conditions de GO satisfaites :
- ✅ MVP validé (8/8 critères)
- ✅ Aucune friction bloquante
- ✅ Socle Phase 5.3 confirmé en pratique
- ✅ Vision tenue

**Périmètre Phase 6 (rappel)** : permettre à l'orchestrator de mobiliser **plusieurs personas en parallèle** sur un même problème, avec **sélection contextuelle** (pas tous les personas, ceux qui apportent une perspective unique). Différence vs BMAD bureau : sélection ciblée pour éviter la saturation contexte et la perte de signal.

### Tests complémentaires recommandés (Phase 5.6 optionnelle)

Avant ou pendant la Phase 6, deux tests valideraient des angles non couverts :

| Test | Périmètre | Bénéfice |
|---|---|---|
| Phase 5.6.A | Cas autre workflow (ex: `code-analysis` sur un module legacy) | Validation que le framework marche au-delà d'incident-response |
| Phase 5.6.B | Test par un collègue (anonymisé, debrief structuré) | Validation que la cible primaire VISION.md (analystes moins seniors) en tire valeur |

**Décision** : ces tests sont **optionnels avant Phase 6**. Recommandation : les faire si l'occasion réelle se présente, sans bloquer la suite du projet.

## Implémentation

Aucune action de modification framework requise.

**Actions de suivi** :
1. Mettre à jour `ROADMAP.md` : Phase 5 marquée terminée, Phase 6 ouverte
2. Ajouter l'entrée `2026-05-03 — Format de questionnement structuré pour PRE-FLIGHT` dans `IDEAS.md`
3. Conserver les artefacts de test dans le repo comme baseline :
   - `docs/mvp-target-case.md`
   - `docs/_scratch/mvp-inputs/` (datadog, splunk, runtime-config)
   - `docs/incidents/2026-05-02-notification-api-5xx.md` (rapport produit)
4. Conserver le prompt de test 5.4-bis comme méthode standard pour futurs tests :
   ```
   on a eu un truc bizarre cette nuit, je peux te montrer les logs si besoin. peux-tu m'aider à comprendre ?
   ```

## Références

- `VISION.md` — boussole stratégique (Phase 4.5)
- `ROADMAP.md` — feuille de route
- `docs/decisions/0002-audit-existant.md` — audit Phase 5.1 (base de la refonte 5.3)
- `docs/mvp-target-case.md` — cas du test MVP (Phase 5.2)
- `docs/incidents/2026-05-02-notification-api-5xx.md` — livrable produit par le test
- `IDEAS.md` — parking lot (entrée 2026-05-03 sur le format de questionnement)

---

## Conclusion — Clôture du chapitre 5

La Phase 5 du framework Agentic Team est **terminée avec succès**. Le MVP fait ce qu'il promet, dans le temps qu'il promet, pour la cible qu'il vise.

Le projet entre maintenant dans son **chapitre 6** : extension de l'orchestration vers le travail en parallèle via Party Mode contextuel.
