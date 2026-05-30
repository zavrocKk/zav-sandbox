---
type: architecture
status: draft  # draft | reviewed | approved
scope: mémoire persistante inter-sessions (Phase 7)
owner: 🏗️ Architect / Orchestrator
last_reviewed: 2026-05-30
related:
  - ROADMAP.md (Phase 7)
  - IDEAS.md (cycle de vie artefacts, F4 mémoire fragile, docs/_scratch/)
  - docs/decisions/0004-field-report-analysis-phase-5-7.md (Friction F4)
  - docs/architecture/2026-05-30-party-mode-panel-vs-debate.md (envelope/handoff)
---

# Architecture — Phase 7 : Mémoire persistante (artefacts de contexte inter-sessions)

> **Usage :** note de **cadrage** qui fige le périmètre, le format et la mécanique
> de la mémoire persistante **avant** toute implémentation. Source de vérité pour
> les sous-phases d'implémentation à venir (7.x). Cette note **ne livre aucun
> template ni instruction orchestrateur** — elle cadre.

---

## Vue d'ensemble

**Système :** couche de mémoire inter-sessions du framework Agentic Team.
**Utilisateurs / consommateurs :** l'orchestrateur (custom agent) à la reprise
d'une session, et l'utilisateur (analyste technique, DevOps/SRE) qui enchaîne
plusieurs sessions courtes sur un même sujet.
**Problème résolu :** une session Copilot perd son contexte à la fermeture. La
friction **F4** (Field Report 2026-05-04→08) confirme qu'en usage réel les
sessions longues dérivent après ~40 min, et que l'orchestrateur **réexplique des
choses déjà établies** d'une session à l'autre. La mitigation actuelle (sessions
courtes 30-40 min) déplace le problème : on coupe avant la dérive, mais **on perd
le fil entre deux sessions**.

**Promesse VISION servie :** « Mémoire entre sessions : **persistante via
artefacts** » (tableau différenciateur) — le pendant de l'« anti-drift par
design » servi par la Phase 5.8.

---

## Contraintes de cadrage (filtres VISION — non négociables)

La Phase 7 doit passer les 6 filtres de la boussole. Trois sont structurants ici :

| Filtre | Conséquence directe sur la conception |
|---|---|
| 2 — Markdown lisible par non-dev | La mémoire est un **fichier markdown**, pas une base. |
| 3 — VSCode + Copilot natif, rien à installer | **Aucune DB vectorielle, aucun serveur, aucun MCP.** |
| 4 — Pas de dev senior pour configurer | Lecture/écriture pilotées par l'orchestrateur en langage naturel. |
| 6 — Markdown structuré dans `docs/` | L'artefact mémoire **vit dans `docs/`** et est committable. |

### Inspiration externe : conceptuelle uniquement

Les systèmes de référence de l'état de l'art — **MemPalace, In-Memoria, Mem0,
Letta (ex-MemGPT), LocalRecall** — reposent **tous** sur de l'infra lourde (base
vectorielle, embeddings, serveur de persistance, protocole MCP). Ils **échouent
aux filtres 2/3/4**. On en retient **le quoi/quand conceptuel** (quel contexte
mérite d'être persisté, quand le recharger, comment éviter la re-explication),
**jamais la machinerie**. C'est une décision de périmètre, pas un manque.

> **Position retenue :** Phase 7 = « checkpoint markdown discipliné », pas
> « moteur de mémoire ». L'intelligence est dans la **convention et la discipline
> de l'orchestrateur**, pas dans un index.

---

## 1. Que persiste-t-on ? (pérenne vs session)

La distinction **artefact pérenne vs artefact de session** (IDEAS 2025-05-02) est
le cœur de la Phase 7. Trois familles :

| Famille | Exemples | Durée de vie | Emplacement |
|---|---|---|---|
| **Pérenne** (déjà géré) | ADR, post-mortem, runbook, note d'archi | Permanent | `docs/decisions/`, `docs/incidents/`, `docs/runbooks/`, `docs/architecture/` |
| **Mémoire de session** (NOUVEAU Phase 7) | checkpoint de reprise : où on en est, décisions prises, prochaines étapes | Le temps du fil de travail (multi-sessions) | `docs/_scratch/` (checkpoints) |
| **Éphémère pur** (déjà géré) | logs, dumps, configs fournies en input | Jetable | `docs/_scratch/mvp-inputs/` |

**Ce que la mémoire de session capture** (et rien de plus — discipline tokens) :

1. **Objectif courant** : la tâche/phase en cours, en une ligne.
2. **État** : ce qui est fait / en cours / bloqué.
3. **Décisions arrêtées** : les choix déjà tranchés (pour ne PAS les rouvrir).
4. **Prochaines étapes** : la todo pour reprendre.
5. **Pointeurs** : liens vers les artefacts pérennes produits (ADR, PR, docs).
6. **Hypothèses / risques ouverts** : ce qui reste incertain.

**Ce qu'elle ne capture PAS** : le fil de conversation verbatim, le code complet,
les inputs bruts. La mémoire est un **résumé structuré de reprise**, pas un
transcript. C'est exactement le rôle d'un **handoff-packet** (cf. §5).

---

## 2. Où ? (emplacement et cycle de vie)

```
docs/_scratch/
  └── memory/
        └── <slug-du-fil>.md       # checkpoint de reprise, 1 par fil de travail
```

- **`docs/_scratch/memory/`** : zone des checkpoints de session. Le préfixe `_`
  marque déjà le caractère « zone de travail » (convention Phase 5.5-bis).
- **Un fichier par fil de travail** (pas un par session) : on **écrase/met à jour**
  le même checkpoint à chaque session sur le sujet → l'historique vit dans Git,
  pas dans une accumulation de fichiers.
- **Promotion vers le pérenne** : quand un checkpoint accouche d'une décision
  structurante, le contenu est **promu** en ADR / note d'archi dans `docs/` (le
  Scribe le propose). Le checkpoint reste un brouillon de travail, jamais la
  source de vérité finale.

> **Question ouverte (cleanup)** : politique de rétention des checkpoints clos
> (auto-archivage après N jours ? suppression manuelle proposée par le Scribe ?).
> Reliée à l'entrée IDEAS « cycle de vie des artefacts ». **Non tranchée ici** —
> proposée pour une sous-phase 7.x dédiée au cleanup.

> **Question ouverte (gitignore)** : `docs/_scratch/memory/` doit-il être versionné
> ou gitignored ? Arbitrage : **versionné** (la mémoire DOIT survivre et suivre le
> repo, c'est la promesse VISION), contrairement aux inputs bruts qui, eux,
> peuvent être gitignored. **Recommandation : versionner les checkpoints, gitignorer
> les inputs sensibles.**

---

## 3. Sous quel format ? (markdown structuré — recommandation argumentée)

> **Note utilisateur (2026-05-30)** : « je veux ton bilan et ta recommandation
> avant tout ». Ci-dessous l'analyse, puis la reco. Décision finale = utilisateur.

### Bilan comparatif

| Critère | Markdown structuré (sections) | YAML pur |
|---|---|---|
| Filtre 2 (lisible non-dev) | ✅ naturel, prose + listes | 🟡 lisible mais rigide |
| Filtre 6 (markdown dans `docs/`) | ✅ par construction | ❌ ce n'est pas du markdown |
| Lecture par l'orchestrateur | ✅ le LLM excelle sur du md | ✅ aussi |
| Champs stables (statut, phase, branche) | 🟡 prose à parser | ✅ clés/valeurs strictes |
| Cohérence avec l'existant | ✅ tous les artefacts sont md + front-matter YAML | ❌ rupture |
| Risque de dérive de format | 🟡 souplesse = variabilité | ✅ schéma contraint |

### Recommandation

**Markdown structuré avec un front-matter YAML léger** — exactement le pattern
déjà utilisé partout dans le repo (chaque `.md` a son bloc `---` de métadonnées).

- **Front-matter YAML** : les **métadonnées de reprise stables** et parsables —
  `phase`, `branch`, `status`, `last_session`, `next_action`.
- **Corps markdown** : les **6 rubriques** du §1 (objectif, état, décisions,
  étapes, pointeurs, risques), en sections fixes.

Cela donne le meilleur des deux : champs durs déterministes pour la reprise
mécanique, prose structurée pour le contexte riche. **Zéro nouveau format à
inventer** — on réutilise la convention front-matter du repo.

> Esquisse (illustrative, **non normative** — le template sera produit en
> implémentation 7.x) :
>
> ```markdown
> ---
> type: memory-checkpoint
> thread: phase-7-persistent-memory
> phase: "7"
> branch: feat/phase-7-memory-framing
> status: in-progress        # in-progress | blocked | closed
> last_session: 2026-05-30
> next_action: "Rédiger le template de checkpoint"
> ---
> ## Objectif courant
> ## État (fait / en cours / bloqué)
> ## Décisions arrêtées
> ## Prochaines étapes
> ## Pointeurs (ADR, PR, docs)
> ## Hypothèses / risques ouverts
> ```

---

## 4. Comment l'orchestrateur lit / écrit (la boucle)

Deux moments, symétriques :

### Écriture (checkpoint)

Déclenchement **hybride** (validé utilisateur) :
- **Manuel** : commande type `/checkpoint` (à figer en 7.x) → le Scribe écrit/MAJ
  le checkpoint du fil courant.
- **Proposition automatique** : réutilise l'**auto-check saturation** de la
  Phase 5.8 — quand l'orchestrateur détecte une session longue / saturée, **ou** en
  fin de session, le Scribe **propose** d'écrire un checkpoint (il ne l'impose
  pas → pas de charge cognitive imposée, filtre transparence).

### Lecture (reprise)

- **Au démarrage d'une session**, l'orchestrateur vérifie l'existence d'un
  checkpoint pour le fil annoncé et, le cas échéant, **le relit en premier** pour
  reconstituer l'état sans re-explication. C'est la réponse directe à **F4**.
- La relecture alimente le PRE-FLIGHT : l'ANALYSE part de l'état mémorisé, pas de
  zéro.

### Scoping — ne jamais recycler un fil sans rapport

> **Préoccupation utilisateur (2026-05-30)** : « je ne veux pas que l'agent garde
> en mémoire des sessions passées qui n'ont aucun lien avec ce qu'on fait. »

La mémoire est **scopée par fil**, jamais globale. Règle :

- **Un seul checkpoint chargé** : celui dont le `thread` (front-matter) correspond
  au fil explicitement repris (par `thread`, `branch` active, ou sujet annoncé).
- **Aucune correspondance → rien n'est chargé** : session neuve, zéro mémoire
  injectée. Pas de balayage de `docs/_scratch/memory/`.
- **Doute → demander** lequel reprendre, jamais supposer.
- Un checkpoint `status: closed` n'est **pas** rechargé automatiquement.

C'est ce qui garantit qu'un checkpoint d'un fil A (ex. un incident résolu) ne
vient **jamais** polluer une session sur un fil B sans rapport. La pertinence est
assurée par le **matching de `thread`**, pas par une recherche sémantique floue.

```mermaid
flowchart LR
    A[Session N<br/>travail] -->|saturation OU fin OU /checkpoint| B[📝 Scribe écrit/MAJ<br/>checkpoint markdown]
    B --> C[(docs/_scratch/memory/<br/>slug.md — versionné Git)]
    C -.fermeture session / reset.-> D[Contexte LLM perdu]
    D --> E[Session N+1<br/>démarrage]
    E -->|relit en 1er| C
    C --> F[PRE-FLIGHT reprend<br/>l'état sans re-explication]
    F --> G[Travail continue<br/>sans perte de fil]
    G -.->|nouvelle décision structurante.-> H[Promotion → ADR /<br/>note d'archi dans docs/]
```

---

## 5. Articulation avec les briques déjà flaggées

La ROADMAP (Phase 6) a explicitement flaggé **task-envelope**, **handoff-packet**
et les **budgets tiny/small/medium/deep** comme « à réexaminer en Phase 7 sans
re-fouiller le référentiel ». Voici leur rôle ici :

| Brique | Rôle en Phase 7 |
|---|---|
| **Handoff-packet** | C'est **exactement** le format de la mémoire de session : un paquet structuré (résumé, hypothèses, risques, prochaines étapes) qu'une session « rend » à la suivante. Le checkpoint EST un handoff-packet inter-sessions. |
| **Task-envelope** | À la **reprise**, l'orchestrateur reconstruit l'envelope de la tâche courante (mission, périmètre, budget) **à partir** du checkpoint. L'envelope est l'entrée, le handoff/checkpoint est la sortie. |
| **Budgets tiny/small/medium/deep** | Dimensionnent **combien** de mémoire on recharge : une tâche `tiny` relit juste `next_action` du front-matter ; une tâche `deep` relit tout le corps + les pointeurs vers les ADR. La mémoire est **lue à budget variable**, pas tout-ou-rien. |

> **Synergie clé** : le checkpoint n'est pas une nouvelle invention — c'est le
> **handoff-packet appliqué à l'axe temporel** (entre sessions au lieu d'entre
> personas). Cohérence conceptuelle totale avec la Phase 6.

---

## 5-bis. Hooks natifs VS Code — évaluation (couche optionnelle, hors socle)

> Les **agent hooks** VS Code (Preview, doc MAJ 2026-05-28) exécutent une commande
> shell à des points de cycle de vie. Évalués ici pour la mémoire ; **écartés du
> socle**, retenus comme accélérateur opt-in pour une sous-phase 7.x.

### Pourquoi les hooks ne fondent PAS le socle

1. **Filtres VISION 2 & 4** : un hook = un **script shell** (parse JSON stdin,
   lit le front-matter, décide) + `jq`. Un non-dev ne peut ni l'écrire ni le
   maintenir → échec du filtre 4 (« si un dev senior est nécessaire, on a échoué »).
2. **Filtre 5 (fiabilité)** : API **Preview** (« format and behavior might
   change »), et les **matchers sont ignorés** (un hook tourne sur *toutes* les
   invocations). Fonder le socle dessus contredit « anti-drift / fiabilité ».
3. **`SessionStart` rouvre le risque de pollution inter-fils** : au démarrage,
   `source = "new"` et **aucun prompt** → le hook ne sait pas quel fil est repris.
   Un auto-load à cet instant réinjecterait un contexte potentiellement sans
   rapport — exactement ce que la règle de scoping par `thread` empêche.

### Hooks à valeur réelle (sous-phase 7.x, opt-in uniquement)

| Hook | Valeur mémoire | Verdict |
|---|---|---|
| **PreCompact** | Sauve le checkpoint **avant compaction** du contexte → comble le seul vrai trou (« pas d'auto-save avant perte ») | 🟢 Retenu pour 7.x opt-in |
| **Stop** | Auto-save du checkpoint **en fin de session** | 🟢 Retenu pour 7.x opt-in |
| **SessionStart** | Auto-load au démarrage | 🔴 Écarté (pollution inter-fils) |
| **UserPromptSubmit / PostToolUse / SubagentStart-Stop** | Marginal pour la mémoire | ⚪ Écartés |
| **PreToolUse** | Bloquer `rm -rf` / `DROP TABLE` | 🔵 Pertinent mais **sécurité**, pas mémoire → autre phase |

**Décision** : le socle Phase 7 reste **markdown + instruction orchestrateur +
Git** (passe les 6 filtres, portable). Les hooks `PreCompact` et `Stop` sont
**flaggés en sous-phase 7.x optionnelle** (fournis clé-en-main, jamais requis).
`PreToolUse` sécurité = sujet distinct, hors Phase 7.

---

## 6. Tensions et points non tranchés

| Sujet | Tension | Statut |
|---|---|---|
| Rétention / cleanup des checkpoints | Auto-clean (risque de perte) vs accumulation (bruit) | ⏳ sous-phase 7.x dédiée |
| Granularité « 1 fichier par fil » | Simple mais suppose un découpage clair des fils | 🟡 à valider à l'usage |
| Commande `/checkpoint` | Nom + syntaxe à figer, orthogonalité avec `/quick` `/light` `/debate` | ⏳ implémentation 7.x |
| Restructuration `inputs/`/`outputs/` (IDEAS 2026-05-03) | Pourrait accompagner la Phase 7 | 🟡 décision séparée, hors cadrage |
| Front-matter vs prose pour les décisions | Risque de double source (front-matter ≠ corps) | 🟡 à cadrer dans le template 7.x |

---

## 7. Décision de cadrage (synthèse)

1. **Quoi** : un **résumé de reprise** (6 rubriques), pas un transcript. Distinction
   pérenne/session/éphémère explicite.
2. **Où** : `docs/_scratch/memory/<slug>.md`, **un fichier par fil**, versionné,
   promu vers `docs/` quand structurant.
3. **Format** : **markdown structuré + front-matter YAML léger** (réutilise la
   convention du repo, zéro nouveau format). *Recommandation soumise à validation.*
4. **Comment** : boucle **écrire (manuel `/checkpoint` + proposition auto Scribe à
   saturation/fin)** ↔ **relire en premier au démarrage** → PRE-FLIGHT sans
   re-explication.
5. **Articulation** : le checkpoint = **handoff-packet inter-sessions** ; relecture
   à **budget variable** (tiny→deep) ; **task-envelope** reconstruite à la reprise.

**Hors scope de cette note** : templates, instructions orchestrateur, commande
`/checkpoint`, politique de cleanup, restructuration inputs/outputs → sous-phases
d'implémentation 7.x.

---

## ─── 📝 Scribe — Synthèse ───

**Convergences** : la mémoire Phase 7 s'aligne sans friction sur l'existant
(front-matter YAML + corps md, `docs/_scratch/`, briques envelope/handoff de la
Phase 6). Pas de nouveau format ni d'infra → tous les filtres VISION passent.

**Divergences / décisions à valider** : (a) format md+front-matter vs YAML pur
— reco = md+front-matter ; (b) versionner vs gitignorer les checkpoints — reco =
versionner.

**Options dégagées** : checkpoint = handoff-packet inter-sessions, lu à budget
variable ; écriture hybride manuel + proposition auto à saturation.

**Reco / question ouverte** : valider la note de cadrage, puis ouvrir une
sous-phase **7.1 — template de checkpoint + commande `/checkpoint`** comme premier
incrément d'implémentation. Le cleanup (rétention) fait l'objet d'une sous-phase
distincte.
