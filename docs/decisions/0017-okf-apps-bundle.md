---
type: adr
number: 0017
status: accepted
date: 2026-07-09
deciders: [Zav]
tags: [memoire, okf, apps, contrats-agents, experience-pre-enregistree]
---

# ADR-0017 — Mémoire d'entités : bundle OKF `docs/apps/` + contrats agents-mémoire (expérience pré-enregistrée)

> Format : Michael Nygard. Une décision = un fichier, immuable une fois `accepted`.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-09
**Décideurs** : Zav — décision explicite de construire **avant** le test terrain,
en assumant le statut d'expérience (sandbox, réversible), contre la recommandation
initiale d'attendre. Compromis retenu : **pré-enregistrement des hypothèses**
falsifiables dans le protocole de test (§3) avant toute session.

## Contexte

La mémoire du framework est indexée par *fil* (checkpoints) et par *décision*
(ADRs) ; le métier réel porte sur des **dizaines d'applications** — entités qui
traversent fils et décisions. Sans mémoire d'entités, chaque session repaie la
redécouverte de l'app. Le design retenu (session du 2026-07-08) s'appuie sur
l'**Open Knowledge Format** (Google Cloud, v0.1, juin 2026) : répertoire markdown
avec frontmatter, `index.md`/`log.md` réservés, chemin = identité, champs custom
tolérés. Trois implémentations indépendantes du même pattern (OKF, MemPalace,
mémoire Claude Code) convergent — évidence de structure. Le repo est déjà
proto-OKF (`type:` dans tous les templates).

## Décision

1. **Bundle `docs/apps/`** au format OKF v0.1 : `index.md` (registre + 1 ligne/app,
   seul fichier scanné au PLAN), `log.md` (journal des écritures), une fiche par
   app (template `agents/templates/app-card.md`, `type: application`, ≤ 100 lignes,
   pointeurs > recopie). Champs requis alignés sur le parseur strict connu
   (`type`, `title`, `description`, `timestamp`) + customs `aliases`, `verified`,
   `criticality`.
2. **Quatre contrats agents-mémoire binaires** (module `memory.md`) : résolution
   par l'orchestrateur seul (max 2 fiches, défaut = rien) ; fraîcheur déclarée au
   PLAN (`verified` > 90 j) ; **Δ-mémoire** (contradiction observée → 1 ligne dans
   le handoff, consolidée par le Scribe) ; **écrivain unique** (Scribe, à la
   SYNTHESIS, après approbation utilisateur, loggé dans `log.md`).
3. Le 5ᵉ contrat (preuve falsifiable par finding) est livré séparément (gate, PR #153).
4. **Zéro ligne ajoutée aux personas** — tout est ancré aux points de passage
   (index, context.md, module, gate).

## Hypothèses pré-enregistrées (falsifiables — mesurées par le protocole §3)

| # | Hypothèse | Ce qui la falsifie (observable) |
|---|---|---|
| H1 | Le rappel **par nom/alias** suffit (pas besoin de recherche sémantique) | ≥ 2 sessions où l'app est nommée mais la fiche n'est pas trouvée |
| H2 | ≤ 100 lignes par fiche suffisent | Une fiche doit dépasser 100 lignes pour être utile |
| H3 | Le budget 2 fiches/session est bien calibré | Dépassé ou insuffisant ≥ 2 fois |
| H4 | Le Δ-mémoire capture du savoir réel sans coût en tours | Aucun Δ utile après ~5 sessions touchant des apps fichées |

Ces critères sont écrits **avant** la première session — le résultat du test ne
pourra pas être réinterprété avec complaisance.

## Alternatives considérées

### Option B — Attendre les 2 évidences utilisateur (test des 10 tickets + fiches pilotes)

- Avantages : risque de conception nul avant données.
- Inconvénients : retarde le field test complet ; le test des 10 tickets ne mesure
  qu'H1 sur dossier, alors que les sessions réelles mesurent H1-H4 en usage.
- **Pourquoi rejetée** : dans un sandbox 100 % markdown réversible, construire
  l'appareil puis l'exposer au terrain EST l'expérience — à condition de
  pré-enregistrer ce qui donnerait tort (fait ci-dessus). Le test des 10 tickets
  reste un pré-check utile mais n'est plus bloquant.

### Option C — Mémoire sémantique (vector DB / MCP mémoire / knowledge graph)

- **Pourquoi rejetée** : infra contre la VISION (markdown pur, rien à installer) ;
  résout le rappel sémantique d'un corpus flou alors que le corpus est un
  annuaire d'entités nommées. Ré-ouvrable seulement si H1 est falsifiée.

## Conséquences

### Positives

- Le savoir par app cesse de s'évaporer à la clôture des sessions (Δ-mémoire).
- Portabilité : bundle consommable par tout agent (Copilot, Gemini, Claude) sans backend.

### Négatives

- 4 contrats jamais éprouvés entrent en test terrain en même temps que le reste —
  si les métriques se dégradent, une variable de plus à isoler.
- Bundle vide au départ : la valeur n'apparaît qu'après les premières fiches.

### Neutres / À surveiller

- Les critères H1-H4 au §3 du protocole ; l'entrée IDEAS « migration règles
  binaires → hooks » gagne un client de plus (validation du bundle par script).

## Implémentation

`docs/apps/{index.md,log.md}`, `agents/templates/app-card.md`, module
`memory.md` (4 contrats), `party-context.md` (§ Mémoire pertinente et consigne Δ),
protocole §3 (H1-H4), table de localisation, arborescence README.

## Références

- [ADR-0014](0014-workflow-bilan-remediation.md), [ADR-0015](0015-analyst-skills-family.md) — précédents d'amendement assumé.
- Spec OKF : GoogleCloudPlatform/knowledge-catalog (v0.1, 2026-06-12).
- [Protocole de test terrain](../_scratch/2026-07-01-plan-job-test-protocol.md) — §3.
