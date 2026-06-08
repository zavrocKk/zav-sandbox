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
  Cause racine d'[`incident-response.md`](../../../agents/workflows/incident-response.md)).
- **Borné par construction** : une passe, pas de garde-fou. Si les personas doivent
  se répondre entre eux → c'est le **Débat** (`/debate`), pas le Panel.

Protocole complet et formats : [`agents/protocols/light-panel.md`](../../../agents/protocols/light-panel.md).

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

Protocole complet, formats et garde-fou : [`agents/protocols/debate.md`](../../../agents/protocols/debate.md).

---

## Party Real — sous-agents réels (3+ personas, défaut multi-persona)

Dès que le PLAN liste **3+ personas** ou un **workflow complet**, l'orchestrateur
bascule **automatiquement** en `/party-real` (l'utilisateur ne tape rien).
Aucune borne supérieure.

**Déclaration dans le PLAN** :

```
Mode : Party Real (sous-agents) — N personas détectés
```

**Qui / Quand / Pourquoi** :

- **QUI** : les personas du PLAN (dérivés du mapping `demande → workflow → personas`).
  Chaque persona = un appel `runSubagent("<persona>")`.
- **QUAND** : après validation du PLAN (phase CONFIRM), dans l'ordre exact du PLAN.
  Ni saut, ni ajout silencieux, ni réordonnancement.
- **POURQUOI** : chaque sous-agent reçoit une **fenêtre fraîche** (pas de croissance
  quadratique du contexte). Le Scribe lit uniquement les handoffs condensés
  (≤ 500 tokens chacun) au lieu de l'historique brut de tous ses prédécesseurs.

**Flow opérationnel** :

1. Créer `.party/context.md` (template [`party-context.md`](../../../agents/templates/party-context.md))
   — objectif, scope, séquence agents.
2. Pour chaque agent : `runSubagent("<agent>")` → lit `.party/context.md` + handoffs
   précédents → produit → écrit `.party/handoff-<agent>.md` (≤ 500 tokens).
3. Lire `handoff-scribe.md` (quality gate).
4. **Supprimer `.party/`** (transitoire, `.gitignore`-d). Ne pas omettre.

**Fallback** : si `runSubagent` échoue → impersonne le persona + écrit le handoff
manuellement → continue la séquence.

**Agents disponibles** : `devops`, `developer`, `security`, `architect`, `qa`,
`product-analyst`, `scribe`. Fichiers : `.github/agents/<agent>.agent.md`.

**Incompatibilité `/debate`** : les sous-agents reçoivent chacun une fenêtre
fraîche → la dynamique de réaction inter-rounds est impossible. `/debate` reste
**inline uniquement**.

Détail opérationnel complet : [`agents/skills/party-mode/SKILL.md`](../../../agents/skills/party-mode/SKILL.md).
Décision : [`docs/decisions/0008-subagents-party-real.md`](../../../docs/decisions/0008-subagents-party-real.md)
et [`docs/decisions/0009-abaisser-seuil-panel-inline.md`](../../../docs/decisions/0009-abaisser-seuil-panel-inline.md).
