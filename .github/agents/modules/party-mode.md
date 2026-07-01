---
type: module
referenced_by: .github/agents/orchestrator.agent.md
---

# Module — Party Mode : Panel & Débat

> Ce fichier est référencé par `orchestrator.agent.md`. Toute modification doit être
> répercutée dans les commandes spéciales et le PRE-FLIGHT de l'orchestrator.

---

## Modèle : format × mécanisme

Deux axes indépendants :

- **Format** (interaction des personas) : `persona-unique` | `Panel` (une passe, aucune réaction) | `Débat` (N rounds réactifs).
- **Mécanisme** (exécution) : `inline` (impersonation) | `sous-agents` (`runSubagent` + `.party/`).

« **Party Real** » n'est pas un format à part : c'est **Panel × sous-agents** (3+ personas).
Le mécanisme se choisit par nombre de personas (voir orchestrator § OUVERTURE).

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

1. **Purger `.party/` s'il contient des fichiers** (résidus d'une session Party Real
   interrompue = contexte périmé à ne jamais réutiliser), puis créer
   `.party/context.md` (template [`party-context.md`](../../../agents/templates/party-context.md))
   — objectif, scope, séquence agents.
2. Pour chaque agent : `runSubagent("<agent>")` → lit `.party/context.md` + handoffs
   précédents → produit → écrit `.party/handoff-<agent>.md` (≤ 500 tokens).
3. Lire `handoff-scribe.md` (quality gate).
4. **Supprimer `.party/`** (transitoire, `.gitignore`-d). Ne pas omettre.

**Fallback** : si `runSubagent` échoue → impersonne le persona + écrit le handoff
manuellement → continue la séquence.

**Agents disponibles** : `devops`, `developer`, `security`, `architect`, `qa`,
`product-analyst`, `scribe`. Fichiers : `.github/agents/<agent>.agent.md`.

**Débat = inline — choix de design, pas une limite technique.** Un débat est
*réactif* : chaque persona doit voir l'argumentation complète des rounds précédents.
En sous-agents, il faudrait ré-injecter tout l'historique à chaque round → le gain
« handoffs condensés » disparaît, et on ajoute latence + relais. Donc `/debate` reste
**inline uniquement** ; la case *Débat × sous-agents* est **volontairement vide**.
