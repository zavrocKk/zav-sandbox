---
type: module
referenced_by: .github/agents/orchestrator.agent.md
---

# Module — Party Mode : Panel & Débat

> Ce fichier est référencé par `orchestrator.agent.md`. Toute modification doit être
> répercutée dans les commandes spéciales et le PRE-FLIGHT de l'orchestrator.

---

## Panel (mode nominal multi-angles)

Le **Party Mode est le mode nominal** du framework. Dès qu'une demande est
**multi-angles** (problème fermé éclairé par plusieurs domaines), tu appliques le
**Panel** : chaque persona convoqué émet **UNE carte d'angle** (3 lignes :
Position / Risque clé / Reco), **une seule passe, aucune réaction inter-persona**,
puis le Scribe synthétise.

- **Sélection des agents** : tu convoques uniquement l'équipe pertinente. Question
  mono-domaine → **un seul persona, pas de Panel**.
- **Point d'ancrage** : les phases « persona variable » des workflows (ex. phase 4
  Cause racine d'[`incident-response.md`](../../agents/workflows/incident-response.md)).
- **Borné par construction** : une passe, pas de garde-fou. Si les personas doivent
  se répondre entre eux → c'est le **Débat** (`/debate`), pas le Panel.

Protocole complet et formats : [`agents/protocols/light-panel.md`](../../agents/protocols/light-panel.md).

---

## Débat — Brainstorming sur invocation (`/debate`)

Sur **invocation explicite `/debate`** uniquement, le Panel devient un **Débat** :
les personas **réagissent entre eux** sur **N rounds** (défaut 3, ajustable
`/debate max=N`), garde-fou max rounds, puis le Scribe **force la synthèse**.

- Réservé aux **problèmes ouverts** (brainstorming, arbitrage, idéation). Problème
  fermé → Panel.
- **Jamais auto-déclenché** : l'auto-détection « exploratoire vs exécutable » est
  hors scope.
- Le Débat se clôt **toujours** par une synthèse Scribe committée.

Protocole complet, formats et garde-fou : [`agents/protocols/debate.md`](../../agents/protocols/debate.md).
