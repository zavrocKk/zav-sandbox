---
name: party-mode
version: "2.0.0"
description: >
  Index des modes d'orchestration multi-personas (Panel, Débat, Party Real sous-agents)
  et cheat-sheet des anti-patterns. À charger quand une session implique plusieurs personas
  ou qu'un rappel des règles Panel/Débat/Party-Real est nécessaire. Ne pas utiliser pour une
  tâche mono-persona ou une question simple.
---

# Party Mode — Index des modes multi-personas

Skill **routeur** : chaque règle vit dans **une seule** source canonique (ci-dessous).
Rien n'est redéfini ici — seul le cheat-sheet des anti-patterns est consolidé en bas.

## Où vit chaque règle (source unique)

| Sujet | Source canonique |
|---|---|
| Règle de bascule (1 / 2 / 3+ personas, `/debate`) | [`.github/agents/orchestrator.agent.md`](../../../.github/agents/orchestrator.agent.md) § OUVERTURE DE SESSION |
| Sémantique + format Panel (carte d'angle, critères, tiebreaker) | [`agents/protocols/light-panel.md`](../../../agents/protocols/light-panel.md) |
| Sémantique Débat (N rounds, garde-fou, formats) | [`agents/protocols/debate.md`](../../../agents/protocols/debate.md) |
| Mécanique Party Real (sous-agents, flow `.party/`, budgets, fallback) | [`.github/agents/modules/party-mode.md`](../../../.github/agents/modules/party-mode.md) |
| Reprise de session (checkpoint) | [`.github/agents/modules/memory.md`](../../../.github/agents/modules/memory.md) |

## Rappel express

- **Panel** — 1 passe, chaque persona 1 carte d'angle (3 lignes), aucune réaction inter-persona → Scribe synthétise.
- **Débat** (`/debate`) — N rounds de réactions croisées, garde-fou max rounds, synthèse Scribe forcée. **Inline uniquement.**
- **Party Real** — 3+ personas → sous-agents réels via `.party/`, décidé automatiquement par l'orchestrateur (l'utilisateur ne tape jamais `/party-real`).

---

## Anti-patterns (violations bloquantes)

| Violation | Correction |
|---|---|
| Débat déclenché sans `/debate` | Revenir au Panel |
| Carte d'angle > 3 lignes | Retailler |
| Persona réagit à un autre en mode Panel | Couper ou basculer `/debate` |
| Cycle clos sans synthèse Scribe | Ajouter avant de terminer |
| Dépassement N rounds sans synthèse | Couper, forcer le Scribe |
| `.party/` non purgé au démarrage OU non supprimé à la clôture | Purger avant, supprimer après |
| `context.md` ou `handoff-*.md` > 500 tokens | Condenser avant de passer au suivant |
