# Roadmap — Agentic Team Framework

Document de référence sur l'avancement du projet et les prochaines étapes.
Mis à jour au fur et à mesure des sessions avec Claude.

## Vue d'ensemble

✅ Phase 0 — Setup
✅ Phase 1 — Fiabilité
✅ Phase 2 — Templates
✅ Phase 3 — Checklists
✅ Phase 4 — Test d'intégration
✅ Phase 4.5 — Clarification stratégique (vision, cible, différenciation)
✅ Phase 5 — MVP basé sur la vision (MVP validé 8/8 — clôturé Phase 5.5)
✅ Phase 5.7 — Hardening usage réel — discipline (5.7.A appliquée, 5.7.B recyclée vers 5.8)
🟡 Phase 5.8 — Hardening usage réel — performance & contexte ← PRIORITÉ ACTUELLE
⬜ Phase 6 — Party Mode (exécution parallèle) ← après Phase 5.8
⬜ Phase 7 — Mémoire persistante (artefacts de contexte)
⬜ Phase 8 — Skills techniques (Helm, K8s, Terraform, etc.)
⬜ Phase 9 — Brainstorming et comparaison avec le marché

#### Phase 5.7.B — Affinages & vigilance — CLÔTURÉE (recyclée vers 5.8)

**Statut au 2026-05-10** : ❌ non exécutée comme prévu, recyclée.

**Décision** : le déclenchement de 5.7.B était conditionné à un Field Report
intermédiaire post-5.7.A. Ce Field Report formel est abandonné (les données
empiriques d'usage sont suffisantes, voir diagnostic 2026-05-10). 5.7.B est donc
clôturée sans exécution dédiée, mais **deux de ses correctifs sont recyclés** vers
la Phase 5.8 car ils ciblent directement la performance/contexte :

| Correctif d'origine | Destination |
|---|---|
| 2.C — Auto-check saturation | → Phase 5.8 |
| 2.D — Anti-bavardage Orchestrator | → Phase 5.8 |
| 1.C — PRE-FLIGHT Q5 ressources externes | → parking lot (IDEAS.md), non prioritaire |
| 3.D — Auto-check Scribe avant création | → parking lot (IDEAS.md), non prioritaire |

**Justification de la clôture sans test** : le critère de succès initial de 5.7
(Field Report ≥ 4/5) ne mesurait pas la douleur réellement observée en usage —
la dégradation de performance au-delà de ~30K tokens. La Phase 5.8 redéfinit le
combat autour de cette douleur réelle.

### 🟡 Phase 5.8 — Hardening usage réel — performance & contexte

**Ouverte le 2026-05-10** suite au diagnostic empirique de performance.

**Objectif** : repousser le seuil de dégradation de performance en session, en
réduisant la consommation de contexte **par interaction** — sans sacrifier les
garde-fous de discipline acquis en 5.7.A.

**Cause racine identifiée** (diagnostic empirique 2026-05-10) : la dégradation
observée à ~30K tokens ne vient PAS de l'overhead de démarrage (~6 %, négligeable,
personas en lazy-loading natif confirmé). Elle vient de l'**accumulation par tour** :
thinking étendu (~9K/tour, levier dominant) + verbosité protocole (~1,5–3K/tour).

#### Leviers de la phase, par ordre d'impact

| # | Levier | Origine | Type | Impact |
|---|---|---|---|---|
| 1 | Réglage thinking (off/low pour tâches simples) | Diagnostic 2026-05-10 | Réglage utilisateur | 🔴 dominant |
| 2 | Mode `/light` — réduction verbosité protocole | IDEAS 2026-05-02 + 2026-05-10 | Correctif framework | 🟠 récurrent |
| 3 | 2.C — Auto-check saturation | Recyclé de 5.7.B | Correctif framework | 🟠 |
| 4 | 2.D — Anti-bavardage Orchestrator | Recyclé de 5.7.B | Correctif framework | 🟠 |

#### À explorer / trancher

- **Levier 1** est testable immédiatement, sans dev (réglage Copilot). À valider
  AVANT de construire le reste : si le thinking seul restaure la performance,
  les leviers 2-4 deviennent optionnels.
- **Mode `/light`** : distinguer de `/quick` existant. `/quick` saute la CONFIRM
  (réduit les tours) ; `/light` allège le format (réduit les tokens/tour). Cumulables.
  Ne doit PAS désactiver les règles binaires de 5.7.A, seulement leur habillage verbeux.
- **2.C auto-check saturation** : mécanisme où l'orchestrator signale lui-même
  l'approche du seuil et propose une action (clôture + nouvelle session).
- **2.D anti-bavardage** : réduction du méta-commentaire et de la verbosité des
  en-têtes/tables.

#### Critères de succès Phase 5.8

- ✅ Nombre d'interactions avant seuil 30K significativement augmenté (mesure
  avant/après sur sessions réelles comparables)
- ✅ Aucune régression des garde-fous 5.7.A (délégation, périmètre, discipline)
- ✅ Qualité perçue stable plus longtemps en session

#### Lien VISION

Cette phase sert directement la promesse VISION « Drift en session longue :
anti-drift par design ». La promesse « Mémoire entre sessions : persistante via
artefacts » reste, elle, du ressort de la Phase 7 (distincte).

Référence : entrée IDEAS.md 2026-05-10 « Diagnostic performance sessions ».

### ⬜ Phase 6 — Party Mode (délibération multi-agents) ← après Phase 5.8

**Reportée le 2026-05-09, recadrée le 2026-05-10.** Dépend de la Phase 5.8
(gestion de contexte) comme prérequis technique.

#### Définition (recadrée 2026-05-10)

Le Party Mode n'est PAS de l'exécution parallèle. C'est un **mode délibératif** :
plusieurs personas débattent en direct sur un problème, sous la conduite de
l'orchestrateur, pour l'explorer sous plusieurs angles AVANT de produire.

Distinction fondamentale avec le mode Orchestrator actuel :

| Aspect | Mode Orchestrator (actuel) | Party Mode (Phase 6) |
|---|---|---|
| Structure | Séquentielle (A finit → B commence) | Délibérative (les personas se répondent) |
| Objectif | **Produire** un livrable | **Explorer** un problème |
| Quand | On sait quoi faire | On ne sait pas encore quoi faire |
| Sortie | Artefact direct | Note de délibération + clarté pour décider |

**Cas d'usage** : brainstorming, exploration d'un problème mal défini, arbitrage
entre options, décision d'architecture où plusieurs angles s'opposent. Typiquement
en amont d'une session Orchestrator classique.

#### Mécanique cible

1. **Déclenchement automatique par l'orchestrateur** selon la nature de la demande.
   - Question simple/spécifique à un domaine → un seul persona invoqué (pas de party).
   - Demande complexe/multi-angles/exploratoire → l'orchestrateur convoque l'équipe
     pertinente et ouvre le débat.
   - L'orchestrateur décide QUELS personas sont pertinents (toutes les sessions
     n'ont pas besoin d'un QA ou d'un Architecte).

2. **Conduite du débat** : l'orchestrateur assigne les tours de parole, empêche
   les dérives, relance sur les angles morts. Pas de monologue parallèle — un
   échange ordonné.

3. **Synthèse + livrable** : le Scribe agrège les points de vue en fin de
   délibération et produit un artefact committable (voir format ci-dessous).

#### Notions empruntées au référentiel agentique (pioche chirurgicale)

Du référentiel `processus-developpement-agentique` (Guilhem-Bonnet), on retient
DEUX contrats markdown — et rien de la machinerie d'infra (Redis, vectoriel,
hooks, etc., explicitement écartés car contraires à VISION.md) :

- **Task envelope** — contrat court donné à chaque persona convoqué dans le débat :
  sa mission, l'angle qu'il défend, son budget de contexte, le format attendu de
  sa prise de parole. Empêche le débat de partir dans tous les sens.

- **Handoff packet** — paquet structuré que chaque persona rend en fin de prise
  de parole (résumé, hypothèses, risques, position). Permet au Scribe d'agréger
  proprement sans relire tout le fil, et limite la consommation de contexte.

> **Note transversale** : ces deux notions (+ les budgets de contexte tiny/small/
> medium/deep du même référentiel) ont un potentiel qui dépasse le Party Mode.
> Elles pourraient servir la Phase 5.8 (performance) et la Phase 7 (mémoire/recyclage
> de contexte). À réexaminer dans ces phases sans re-fouiller le référentiel.

#### Livrable du Party Mode

Format de la note de délibération (à affiner) : sujet exploré, personas convoqués
et pourquoi, positions/angles de chacun (issus des handoff packets), points de
convergence, points de désaccord, options dégagées, recommandation ou question
ouverte. Emplacement : à trancher (probablement `docs/decisions/` si ça débouche
sur un ADR, ou `docs/_scratch/` si exploratoire). À aligner sur la table de
localisation de `copilot-instructions.md`.

#### Dépendance critique à la Phase 5.8

Un débat génère beaucoup de tours (4 personas × 3 rounds = 12 prises de parole).
C'est le cas d'usage le plus exposé à la saturation de contexte à 30K. Le Party
Mode ne peut donc PAS être construit avant que la Phase 5.8 ait assaini la gestion
de contexte. Le handoff packet (paquets courts) est une mitigation native, mais
ne suffit pas à lever la dépendance.

#### Tension à surveiller avec VISION.md

Le Party Mode explore plutôt qu'il ne produit, ce qui frotte avec l'orientation
"livrables senior" de la VISION. Résolution retenue : le Party Mode se clôt
TOUJOURS par un livrable Scribe (note de délibération committée), pour rester
aligné avec le filtre 6 de la boussole ("produit du markdown structuré dans docs/").

#### À explorer / trancher (au moment de l'implémentation, pas avant)

- Comment l'orchestrateur détecte automatiquement "exploratoire vs exécutable" sans
  se tromper (risque : déclencher un party pour une question simple = gaspillage).
- Faut-il une commande manuelle de secours (`/party`, `/debate`) en plus de l'auto ?
- Format exact du task envelope et du handoff packet adaptés au format `.md` VSCode.
- Nombre max de rounds de débat avant synthèse forcée (garde-fou anti-saturation).

#### Inspiration

- Concept Party Mode : BMAD (débat multi-agents orchestré + synthèse).
- Système au bureau (sélection d'équipe intelligente, optimisation tokens ~70%).
- Contrats markdown : référentiel agentique Guilhem-Bonnet (envelope + handoff).

### ⬜ Phase 7 — Mémoire persistante

**Concept** : artefacts de contexte qui persistent entre sessions, permettant
au framework de "reprendre où il s'était arrêté".

**Inspiration** : système au bureau qui produit un artefact mémoire, reset
le contexte, et relit pour reprendre sans perte.

**À explorer** :

- Format des artefacts (markdown structuré ? YAML ?)
- Quand sauvegarder (fin de session ? checkpoint manuel ?)
- Comment le rendre invisible mais utile pour l'utilisateur

### ⬜ Phase 8 — Skills techniques

**Concept** : ajouter des skills spécialisées pour les technologies qu'utilisent
les équipes cibles.

**Candidates prioritaires** :

- Helm / Kubernetes
- Terraform / IaC
- GitHub Actions / GitLab CI
- AWS (EKS, ECS, IAM, etc.)
- Observabilité (Prometheus, Datadog, Splunk)
- Java / Python (analyse de stack traces)
- Méthodologies (5 Pourquoi Toyota, RCA, RACI)

### ⬜ Phase 9 — Ouverture

**Concept** : sortir le framework du contexte personnel pour le rendre
utilisable par d'autres.

**Étapes possibles** :

1. Test interne avec l'équipe
2. Documentation publique (README, guide démarrage, exemples)
3. Repo GitHub public
4. Site/blog de référence ("how-to construire un framework agentique")
5. Communication communautaire

## Principes directeurs (boussole)

À chaque décision future, on se réfère à ces principes :

1. **Pour qui ?** Analystes techniques + équipes DevOps/CI-CD avant tout.
2. **Configuration ?** En markdown, lisible et modifiable par non-devs.
3. **Outils ?** VSCode + Copilot natif, rien d'autre à installer.
4. **Complexité ?** Si un dev senior est nécessaire pour configurer, on a échoué.
5. **Drift ?** Anti-drift par design, fiabilité avant fonctionnalités.
6. **Livrables ?** Markdown structurés dans `docs/`, prêts à committer.

## Parking lot (idées en attente)

Voir `IDEAS.md` pour la liste complète des idées notées au fil des sessions.
