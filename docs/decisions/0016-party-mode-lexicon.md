---
type: adr
number: 0016
status: accepted
date: 2026-07-08
deciders: [Zav]
tags: [party-mode, lexique, orchestration, adr-0013]
---

# ADR-0016 — Achever ADR-0013 : lexique unifié « Party mode », retrait de « Party Real »

> Format : Michael Nygard. Une décision = un fichier, immuable une fois `accepted`.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-08
**Décideurs** : Zav
**Relation à ADR-0013** : complète son implémentation (le modèle format × mécanisme
était acté, le vocabulaire ne l'appliquait pas).

## Contexte

ADR-0013 a établi que « Party Real » n'est pas un 3ᵉ mode mais la case
*Panel × sous-agents*. Le terme a pourtant survécu dans ~49 occurrences des
fichiers vivants (18 fichiers), y compris un pseudo-token `/party-real` qui n'a
jamais été une commande. Constat d'usage : la friction de lecture est réelle et
récurrente pour l'utilisateur — la clarification par explication (ADR-0013) n'a
pas suffi, le nom lui-même entretenait la confusion.

L'entrée IDEAS prévoyait ce renommage « en une passe avec TOK-01 après le test
terrain ». Il est avancé (supprimée de IDEAS.md par la convention d'hygiène) ;
TOK-01 reste parqué et profitera d'un vocabulaire stabilisé.

## Décision

- **« Party mode »** est le terme unique du multi-personas. La case
  Panel × sous-agents s'écrit **« Party mode (sous-agents) »** ; le pseudo-token
  `/party-real` disparaît du vocabulaire vivant (il ne correspondait à aucune
  commande réelle).
- **Périmètre : fichiers vivants uniquement** (agents, modules, workflows, skills,
  templates, README, protocole de test). Les documents **historiques** (ADRs
  0008/0009/0013/0014/0015, CHANGELOG, ROADMAP) gardent leur formulation d'époque —
  un ADR est immuable, l'histoire ne se réécrit pas.
- **Deux mentions d'alias** conservées pour la traçabilité et la recherche :
  README (section Modes multi-personas) et module `party-mode.md`
  (« anciennement “Party Real” »).
- Déclaration dans le PLAN : `Mode : Party mode (sous-agents) — N personas — régime : …`.

## Alternatives considérées

### Option B — Attendre TOK-01 (plan initial de l'entrée IDEAS)

- Avantages : une seule passe sur les fichiers dupliqués.
- Inconvénients : la friction de lecture est quotidienne et le renommage seul est
  mécanique (49 substitutions + 5 retouches de style) ; TOK-01 exige, lui, des
  données terrain sur la conformité des handoffs.
- **Pourquoi rejetée** : les deux chantiers n'ont pas la même condition d'entrée ;
  les coupler faisait payer la friction en attendant une donnée qui n'a rien à
  voir avec le nom.

### Option C — Renommer aussi l'historique (ADRs, CHANGELOG, ROADMAP)

- **Pourquoi rejetée** : réécrire l'histoire casse la traçabilité des décisions ;
  les alias suffisent pour la recherche.

## Conséquences

### Positives

- Un seul concept, un seul nom — la lecture « 3ᵉ mode » ne peut plus renaître du lexique.
- Vocabulaire aligné sur les noms de fichiers déjà existants (`party-mode.md`, skill `party-mode`).

### Négatives

- Divergence de vocabulaire entre docs vivants et historiques (mitigée par les 2 alias).
- Le test terrain démarrera avec un vocabulaire renommé jamais éprouvé en session réelle
  — si l'orchestrateur montre une confusion de routage liée au nom, le signaler au journal.

### Neutres / À surveiller

- TOK-01 (dé-duplication) reste parqué — conditions d'entrée inchangées.

## Implémentation

49 substitutions dans 18 fichiers vivants + 5 retouches de style (README table,
orchestrator « pas une commande », module party-mode ×3) + 2 alias + suppression
de l'entrée IDEAS correspondante.

## Références

- [ADR-0013](0013-format-mechanism-model.md) — modèle format × mécanisme.
- [ADR-0008](0008-subagents-party-real.md) / [ADR-0009](0009-abaisser-seuil-panel-inline.md) — historique du terme.
