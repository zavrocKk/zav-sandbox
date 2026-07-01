---
type: adr
number: "0013"
status: accepted
date: 2026-07-01
deciders: [Zav]
tags: [orchestration, party-mode, panel, debate, subagents, format, mecanisme, mt2]
supersedes_partial: [0008, 0009]
---

# ADR-0013 — Modèle « format × mécanisme » d'orchestration multi-personas

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-01
**Décideurs** : Zav
**Relation à ADR-0008 / ADR-0009** : raffinement conceptuel (reformule le cadrage,
ne change **aucun comportement** ni commande).

---

## Contexte

Le vocabulaire hérité d'[ADR-0008](0008-subagents-party-real.md) et
[ADR-0009](0009-abaisser-seuil-panel-inline.md) mélange deux dimensions distinctes :

- **« Party Real »** désigne à la fois un *format* (Panel multi-angles) **et** un
  *mécanisme* (sous-agents réels via `.party/`). Lu comme un « 3ᵉ mode » parallèle à
  Panel et Débat, ce qui induit en erreur.
- Le **Débat** est verrouillé *inline*, présenté comme une « **incompatibilité
  technique** » avec les sous-agents — formulation qui suggère une limitation à lever.

MT2 (fil `orchestration-refacto-mt2-mt3`) réexamine ce cadrage et la faisabilité d'un
« Débat en sous-agents ».

---

## Décision

Adopter un **modèle explicite à 2 axes** :

- **Axe FORMAT** (comment les personas interagissent) : `persona-unique` | `Panel`
  (N personas, une passe, aucune réaction) | `Débat` (N personas, R rounds réactifs).
- **Axe MÉCANISME** (comment c'est exécuté) : `inline` (impersonation, une conversation)
  | `sous-agents` (`runSubagent` + relais `.party/`, fenêtres fraîches, handoffs ≤ 500 tokens).

### Matrice des combinaisons

| Format ↓ / Mécanisme → | Inline | Sous-agents |
|---|---|---|
| **Persona-unique** | ✅ défaut 1 persona | ⛔ inutile (1 sous-agent = aucun gain) |
| **Panel** | ✅ ≤ 2 personas | ✅ 3+ personas (**« Party Real »** = Panel × sous-agents) |
| **Débat** | ✅ toujours | ⛔ **vide par design** (voir ci-dessous) |

### Sélection du mécanisme — inchangée

Par **nombre de personas** du PLAN : 1 → inline ; 2 → Panel inline ; **3+ →
sous-agents** (automatique, l'utilisateur ne tape jamais `/party-real`). `/debate`
reste une invocation explicite.

### Le Débat reste inline — reformulé comme choix de design

Ce n'est **pas** une impossibilité technique à débloquer. Un Débat est **réactif** :
chaque persona doit voir l'**argumentation complète** des rounds précédents pour
rebondir. En sous-agents, il faudrait donc **ré-injecter tout l'historique du débat**
dans chaque sous-agent à chaque round :

- le bénéfice « handoffs condensés ≤ 500 tokens » **disparaît** (condenser ferait
  perdre la nuance argumentative nécessaire à la réaction) ;
- on **ajoute** latence (N × R allers-retours) et complexité de relais `.party/`.

→ La case `Débat × sous-agents` est **volontairement vide** : les sous-agents
n'apportent aucun gain pour un débat réactif. L'inline est le bon mécanisme.

---

## Alternatives considérées

### Option A' — Construire `Débat × sous-agents`
- Description : relayer chaque round via `.party/`, l'orchestrateur orchestrant les rounds.
- Avantages : fenêtres fraîches par persona sur débats très longs.
- Inconvénients : re-injection de l'historique complet à chaque round → **zéro gain
  tokens** + latence + complexité de relais.
- **Pourquoi rejetée** : coût/complexité sans bénéfice réel. Contredit VISION
  (« ne pas sur-construire »).

### Option B' — Statu quo (pas de modèle explicite)
- Description : garder le vocabulaire actuel (Panel / Débat / Party Real en parallèle).
- **Pourquoi rejetée** : la confusion « Party Real = 3ᵉ format » persiste, et le
  Débat-inline reste présenté comme une limitation subie plutôt qu'un choix.

---

## Conséquences

### Positives
- Vocabulaire sans ambiguïté : « Party Real » = *Panel × sous-agents*, pas un format à part.
- Le Débat-inline est justifié par un raisonnement de coût, pas par une « impossibilité ».
- Base conceptuelle claire pour toute évolution future.

### Négatives
- Aucune fonctionnalité nouvelle (c'est un refactor de clarté).

### Neutres / À surveiller
- **Aucun changement de comportement ni de commande** (`/debate`, bascule auto 3+).
- Si un usage réel révèle un besoin de débat sur fenêtres fraîches, rouvrir A' avec
  des données concrètes.

---

## Implémentation

Reformulation (framing) — pas de changement de logique :

1. `.github/agents/modules/party-mode.md` — introduire le modèle 2 axes ; reformuler
   « Incompatibilité `/debate` » en choix de design.
2. `agents/skills/party-mode/SKILL.md` — rappel express aligné sur les 2 axes.
3. `README.md` — note clarifiant « Party Real = Panel × sous-agents ».
4. `.github/agents/orchestrator.agent.md` — reformuler le rappel `/debate` inline.

## Références
- [ADR-0008](0008-subagents-party-real.md) — introduction de `/party-real`.
- [ADR-0009](0009-abaisser-seuil-panel-inline.md) — seuil ≤ 2 personas.
