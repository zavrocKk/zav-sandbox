---
name: party-mode
version: "2.1.0"
description: >
  Index des modes d'orchestration multi-personas (Panel, Débat, Party mode (sous-agents) sous-agents)
  et cheat-sheet des anti-patterns. À charger quand une session implique plusieurs personas
  ou qu'un rappel des règles Panel/Débat/Party mode (sous-agents) est nécessaire. Ne pas utiliser pour une
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
| Mécanique Party mode (sous-agents) (sous-agents, flow `.party/`, budgets, fallback) | [`.github/agents/modules/party-mode.md`](../../../.github/agents/modules/party-mode.md) |
| Reprise de session (checkpoint) | [`.github/agents/modules/memory.md`](../../../.github/agents/modules/memory.md) |

## Rappel express

**2 axes** : *format* (`Panel` / `Débat`) × *mécanisme* (`inline` / `sous-agents`).

- **Panel** (format) — 1 passe, chaque persona 1 carte d'angle (3 lignes), aucune réaction inter-persona → Scribe synthétise.
- **Débat** (`/debate`, format) — N rounds de réactions croisées, garde-fou max rounds, synthèse Scribe forcée. **Inline uniquement** (choix de design : aucun gain sous-agents pour un débat réactif).
- **Party mode (sous-agents)** (mécanisme) — **Panel × sous-agents** : 3+ personas → sous-agents réels via `.party/`, décidé automatiquement par l'orchestrateur (l'utilisateur ne tape jamais Party mode (sous-agents)). Deux **régimes** de lecture des handoffs : **convergent** (construction séquentielle, défaut) / **divergent** (diagnostic — chaque agent lit `context.md` seulement, anti-ancrage). Source : module party-mode.

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
| `context.md` > 500 tokens OU `handoff-*.md` > 1000 tokens (plafond) | Condenser avant de passer au suivant |
| Handoff gonflé sans signal (transcription, recopie d'un fichier du repo) | Cible ~500 tokens ; pointeur `voir path` plutôt que recopie |
| Sous-agent qui lit les handoffs en régime **divergent** | Angle contaminé : re-invoquer sans les handoffs |
| Handoff non conforme (sections manquantes, budget dépassé, « Done quand » non satisfait) | Gate orchestrateur : re-invoquer 1×, puis fallback |
