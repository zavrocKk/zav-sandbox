---
type: analysis
date: 2026-05-30
topic: thinking-high-vs-low-eval
workflow: ad-hoc
personas: [Architect, Developer, QA, Scribe]
phase: 5.8
---

# Rapport d'auto-analyse TI — Thinking High vs Thinking Low

> **Avertissement méthodologique** : cet exercice est une **simulation introspective**.
> Les « tours de dégradation » et les « tokens consommés » sont des **estimations**
> non instrumentées (aucun compteur réel). Ils sont fournis comme ordres de grandeur,
> pas comme mesures. Les scénarios de bug sont fictifs mais réalistes.

## Demande initiale

Exécuter un protocole de test comparatif (« Thinking étendu » vs « Thinking désactivé »)
sur deux tâches de débogage TI de complexité identique, s'auto-analyser de façon
transparente, et produire un tableau de bord + une recommandation pour la Phase 5.8.

## Scénarios iso-complexité

| Axe | Scénario 1 (Session A) | Scénario 2 (Session B) |
|---|---|---|
| Nom | Race condition intermittente sur API de paiement | Fuite mémoire progressive sur microservice de stock |
| Symptôme | ~0,7 % de paiements double-débités sous pic | OOMKilled toutes les ~6 h sous charge |
| Reproductibilité | Non déterministe (timing) | Déterministe, cumulative |
| Difficulté root cause | Élevée (fenêtre de course ms) | Élevée (rétention d'objets invisible) |
| Criticité | Critique (argent) | Critique (rupture de service) |

## Synthèse des deux sessions

### Session A — Thinking High (Scénario 1)
- **Root cause** : `GET` puis `SETNX` non atomiques → fenêtre de course sur la clé d'idempotence.
- **Fix** : `SET key PENDING NX EX` atomique + `Idempotency-Key` transmise au PSP (double filet).
- **Observation** : raisonnement dense et juste T1→T5, puis **redondance dès ~T6** (réénumération d'hypothèses déjà écartées).

### Session B — Thinking Low (Scénario 2)
- **Root cause** : `static HashMap` non bornée, jamais évincée → fuite par accumulation de `StockEvent`.
- **Fix** : cache Caffeine borné (`maximumSize` + `expireAfterWrite`).
- **Bascule High forcée** : **OUI au Tour 2** pour la lecture du heap dump (corrélation dominator tree), afin d'éviter un faux diagnostic imputant l'ORM. Retour en Low ensuite.

## Tableau comparatif

| Critère d'évaluation | Session A (Thinking High) | Session B (Thinking Low) |
| :--- | :--- | :--- |
| **Scénario TI simulé** | Race condition API de paiement | Fuite mémoire microservice de stock |
| **Tour où la dégradation apparaît** | ~Tour 6 *(estimation, non instrumentée)* | ~Tour 9 *(estimation, non instrumentée)* |
| **Tokens consommés à ce moment** | ~8–10k *(estimation)* | ~4–5k *(estimation)* |
| **Qualité de la résolution (1-5)** | 5 | 4 |
| **Vitesse de traitement (1-5)** | 3 | 5 |
| **Bascule en High requise ?** | Non (par définition) | Oui — au Tour 2 (lecture heap dump) |

## Recommandation Phase 5.8

1. **Thinking = levier dominant ?** Partiellement. Il n'accélère pas la *détection* ;
   il fiabilise le *correctif* et sécurise les sous-tâches concurrentes/stateful.
   La Session B tient plus longtemps → le thinking est un levier **ciblé**, pas universel.
2. **Verbosité du protocole ?** Pèse modérément. Le coût du High se paie d'abord en
   *longueur redondante* (radotage post-T5) avant tout gain de justesse. Un mode `/light`
   est **utile mais pas indispensable** — il change le débit, pas la qualité technique.
3. **Usage hybride ?** **Oui — recommandation principale.** `Low` par défaut, bascule
   `High` à la demande sur déclencheurs explicites.

> **Règle proposée Phase 5.8** : `Thinking Low` = mode nominal de débogage.
> Déclencheurs de bascule `High` : *(a)* concurrence/atomicité, *(b)* analyse de dump/heap,
> *(c)* correctif sur flux financier ou intégrité transactionnelle. Le reste reste en Low.

## Points ouverts / Suite à donner
- Instrumenter réellement la consommation de tokens si une mesure objective est requise.
- Décider si le mode `/light` entre dans le protocole Orchestrator (ADR potentiel).
- Valider les déclencheurs de bascule High sur un cas réel.

## Notes Scribe
Métriques explicitement étiquetées « estimations non instrumentées » pour éviter
toute fabrication de précision. Exercice de simulation, non rejouable tel quel.
