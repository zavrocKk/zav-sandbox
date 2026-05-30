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
✅ Phase 5.8 — Hardening usage réel — performance & contexte (correctifs framework livrés ; levier thinking côté utilisateur)
✅ Phase 6 — Party Mode : Panel (défaut) + Débat (sur invocation)
🟦 Phase 7 — Mémoire persistante (cadrage + 7.1 mécanisme livrés ; cleanup à venir)
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

#### Clôture (2026-05-30)

**Statut : ✅ close.** Correctifs framework livrés :

| Levier | Livré | Emplacement |
|---|---|---|
| 2 — Mode `/light` | ✅ commande + règle PRE-FLIGHT Q2-bis (allège le format, pas les règles binaires, cumulable `/quick`) | `.github/agents/orchestrator.agent.md`, `agents/protocols/preflight.md` |
| 3 — Auto-check saturation (2.C) | ✅ section « Auto-check saturation » + proposition de checkpoint | `.github/agents/orchestrator.agent.md` |
| 4 — Anti-bavardage (2.D) | ✅ fusion des 3 sections anti-pattern en une seule (déduplication ~300-400 tk) + `/light` | `.github/agents/orchestrator.agent.md` |
| Allègement orchestrator | ✅ ancre « Règles critiques » en tête (contre le lost-in-the-middle en session longue) | `.github/agents/orchestrator.agent.md` |

**Action restante côté utilisateur (hors code)** : Levier 1 — réglage du thinking
(off/low pour tâches simples) dans Copilot. Non committable, à appliquer en usage.

**Report assumé** : externalisation du mapping workflow (~600 tk) — écartée car
flaggée risquée (chargement au bon moment) dans IDEAS 2026-05-09 ; gain marginal
face au risque. À reconsidérer seulement si la lourdeur persiste.

#### Lien VISION

Cette phase sert directement la promesse VISION « Drift en session longue :
anti-drift par design ». La promesse « Mémoire entre sessions : persistante via
artefacts » reste, elle, du ressort de la Phase 7 (distincte).

Référence : entrée IDEAS.md 2026-05-10 « Diagnostic performance sessions ».

### ✅ Phase 6 — Party Mode : Panel (défaut) + Débat (sur invocation)

> **Statut : CLOSE le 2026-05-30.** Livré : protocoles
> [`agents/protocols/light-panel.md`](agents/protocols/light-panel.md) (Panel) et
> [`agents/protocols/debate.md`](agents/protocols/debate.md) (Débat) ; branchement
> Panel par défaut + commande `/debate` dans
> [`.github/agents/orchestrator.agent.md`](.github/agents/orchestrator.agent.md) ;
> ancrage Panel sur la phase 4 (Cause racine) d'`incident-response.md` ; ligne
> « note de délibération » ajoutée à la table de localisation de
> `copilot-instructions.md` (Débat exploratoire → `docs/_scratch/`, ADR →
> `docs/decisions/`). Garde-fou Débat : N=3 rounds par défaut (ajustable).

#### Définition (recadrée 2026-05-30 — voir [ADR de cadrage](docs/architecture/2026-05-30-party-mode-panel-vs-debate.md))

> ⚠️ **Cette définition remplace celle de 2026-05-10** (« Party Mode = mode
> délibératif »). Voir la note de décision
> [`docs/architecture/2026-05-30-party-mode-panel-vs-debate.md`](docs/architecture/2026-05-30-party-mode-panel-vs-debate.md)
> pour le détail du renommage et la justification.

Le **Party Mode est le mode nominal du framework**, toujours actif. Il se décline
en **deux réglages de la même mécanique** — la sélection intelligente des agents
par l'orchestrateur — qui ne diffèrent que par le nombre de passes :

| | **Panel** — Party Mode (défaut) | **Débat** — Brainstorming (sur invocation) |
|---|---|---|
| Statut | Mode nominal, **toujours actif** | Activé explicitement (`/debate`) |
| Nature du problème | **Fermé** : une réponse à trouver | **Ouvert** : on bloque ou on explore |
| Travail type | Incident, analyse, doc, design | Brainstorming, arbitrage, idéation |
| Friction | Coûteuse → on l'évite | Productive → on la cherche |
| Mécanique | Chaque expert → son angle **une fois** → synthèse | Les experts se répondent sur **N rounds** → synthèse |
| Coût tokens | Borné par construction | Volontairement plus élevé (assumé) |
| Garde-fou | Aucun nécessaire | Max rounds avant synthèse forcée |

**Brique centrale commune** : la sélection intelligente des agents par
l'orchestrateur. Panel et Débat ne sont que deux réglages — *une passe* vs
*N rounds* — de cette même brique.

**Changement clé vs définition précédente** : l'**auto-détection**
« exploratoire vs exécutable » sort du scope. Elle est remplacée par l'invocation
manuelle `/debate` — ce qui supprime le seul morceau réellement risqué (piège
classique du sur-déclenchement multi-agents) et rend le Panel quasi-immédiatement
constructible.

#### Règle binaire de séparation

> **Panel** : aucun persona ne réagit à un autre. Une passe, puis Scribe synthétise.
> **Débat** : les personas réagissent entre eux, max N rounds, puis Scribe force la synthèse.

Le garde-fou anti-saturation (max rounds) ne s'applique **qu'au Débat** — le Panel
est borné par construction.

#### Mécanique cible

1. **Sélection des agents par l'orchestrateur** selon la nature de la demande
   (déjà le cœur du mode Orchestrator actuel). Question simple/mono-domaine → un
   seul persona. Demande multi-angles → l'orchestrateur convoque l'équipe
   pertinente (toutes les sessions n'ont pas besoin d'un QA ou d'un Architecte).

2. **Panel (défaut)** : chaque persona convoqué émet **une carte d'angle** au
   format contraint (3 lignes : Position / Risque clé / Reco), puis le Scribe
   synthétise. Point d'ancrage naturel : les phases « persona variable » des
   workflows existants (ex. phase 4 Cause racine d'`incident-response.md`).

3. **Débat (`/debate`)** : surcouche au-dessus du Panel — les personas se
   répondent sur N rounds sous la conduite de l'orchestrateur (tours de parole,
   anti-dérive, relance sur les angles morts), garde-fou max rounds, puis
   synthèse Scribe.

4. **Synthèse + livrable** : le Scribe agrège les points de vue et produit un
   artefact committable (voir format ci-dessous). Vrai pour les deux réglages.

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

#### Livrable

**Panel** : la synthèse Scribe alimente le livrable normal du workflow en cours
(post-mortem, ADR, note d'archi…). Pas de nouveau type d'artefact à inventer.

**Débat** : note de délibération (à affiner) : sujet exploré, personas convoqués
et pourquoi, positions/angles de chacun, convergences, désaccords, options
dégagées, recommandation ou question ouverte. Emplacement : `docs/decisions/`
si ça débouche sur un ADR, ou `docs/_scratch/` / `docs/brainstorming/` si
exploratoire. À aligner sur la table de localisation de `copilot-instructions.md`.

#### Tension avec VISION.md (résolue par design)

Le Débat explore plutôt qu'il ne produit, ce qui frotte avec l'orientation
"livrables senior" de la VISION. Résolution retenue : **Panel ET Débat se closent
TOUJOURS par une synthèse Scribe committée**, pour rester alignés avec le filtre 6
de la boussole ("produit du markdown structuré dans docs/").

#### À explorer / trancher (au moment de l'implémentation, pas avant)

- Format exact de la carte d'angle (Panel) adapté aux phases « persona variable »
  des workflows existants.
- Nombre max de rounds de débat avant synthèse forcée (garde-fou anti-saturation).
- Orthogonalité des commandes : `/quick`, `/light` (Phase 5.8) et `/debate`
  doivent rester cumulables.
- Emplacement définitif du livrable du Débat (decisions vs scratch vs brainstorming).

> **Note** : l'auto-détection « exploratoire vs exécutable » est **retirée du scope**
> (remplacée par l'invocation manuelle `/debate`). C'était le seul morceau
> réellement risqué ; sa suppression dé-risque toute la phase.

#### Inspiration

- Concept Party Mode : BMAD (débat multi-agents orchestré + synthèse).
- Système au bureau (sélection d'équipe intelligente, optimisation tokens ~70%).
- Contrats markdown : référentiel agentique Guilhem-Bonnet (envelope + handoff).

### 🟦 Phase 7 — Mémoire persistante

**Concept** : artefacts de contexte qui persistent entre sessions, permettant
au framework de "reprendre où il s'était arrêté".

**Inspiration** : système au bureau qui produit un artefact mémoire, reset
le contexte, et relit pour reprendre sans perte.

> **Cadrage fait le 2026-05-30** — voir la note d'architecture
> [`docs/architecture/2026-05-30-phase-7-persistent-memory.md`](docs/architecture/2026-05-30-phase-7-persistent-memory.md).
> Décisions de cadrage : (1) **quoi** = résumé de reprise en 6 rubriques (pas un
> transcript), distinction pérenne/session/éphémère ; (2) **où** =
> `docs/_scratch/memory/<slug>.md`, 1 fichier par fil, versionné, promu vers
> `docs/` si structurant ; (3) **format** = markdown structuré + front-matter YAML
> léger ; (4) **comment** = écrire (manuel `/checkpoint` + proposition auto Scribe
> à saturation/fin) ↔ relire en premier au démarrage ; (5) **articulation** =
> checkpoint = handoff-packet inter-sessions, lu à budget variable tiny→deep.
> Répond à la friction **F4**. Inspiration externe (MemPalace, In-Memoria, Mem0,
> Letta, LocalRecall) retenue **conceptuellement seulement** — infra lourde écartée
> (filtres VISION 2/3/4).

**✅ Sous-phase 7.1 — mécanisme minimal (2026-05-30)** : template
[`agents/templates/memory-checkpoint.md`](agents/templates/memory-checkpoint.md) ;
zone versionnée [`docs/_scratch/memory/`](docs/_scratch/memory/) ; câblage
orchestrateur (commande `/checkpoint`, section « Mémoire persistante »
lecture-au-démarrage/écriture, branchement de l'auto-check saturation) ; ligne
« Checkpoint de mémoire » dans la table de localisation de `copilot-instructions.md`.

**⏳ Reste à explorer (sous-phases 7.x)** :

- Politique de rétention / cleanup des checkpoints clos (auto-archivage ? proposition Scribe ?)
- **Hooks natifs VS Code (opt-in)** : `PreCompact` + `Stop` (nudge `/checkpoint` non bloquant) + `PreToolUse` (garde-fou `ask` sur commandes destructives). **Livrés OFF par défaut** dans [`agents/hooks/`](agents/hooks/) (non auto-chargés, activation manuelle). `SessionStart` et `Stop`-block écartés (pollution inter-fils / premium requests). Voir note de cadrage §5-bis.
- Restructuration `inputs/`/`outputs/` (IDEAS 2026-05-03) — décision séparée
- Validation à l'usage de la granularité « 1 fichier par fil »

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
