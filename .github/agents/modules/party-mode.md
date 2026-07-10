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

« **Party mode (sous-agents)** » — anciennement « Party Real » (ADR-0013) — n'est pas un format à part : c'est **Panel × sous-agents** (3+ personas).
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

## Party mode (sous-agents) — sous-agents réels (3+ personas, défaut multi-persona)

Dès que le PLAN liste **3+ personas** ou un **workflow complet**, l'orchestrateur
bascule **automatiquement** en Party mode sous-agents (l'utilisateur ne tape rien).
Aucune borne supérieure.

**Déclaration dans le PLAN** :

```
Mode : Party mode (sous-agents) — N personas détectés — régime : <convergent|divergent>
```

## Régime de lecture des handoffs — convergent vs divergent

Le bénéfice cognitif du multi-personas est l'**indépendance des angles** (anti-ancrage).
Or un sous-agent qui lit les handoffs de ses prédécesseurs avant de former son angle
est **contaminé** par leurs conclusions. D'où deux régimes, choisis au PLAN :

| Régime | Quand | Lecture des handoffs par les sous-agents |
|---|---|---|
| **Convergent** (défaut) | Chaque persona **construit sur** le travail du précédent : feature, pipeline, refonte, implémentation | `context.md` + tous les handoffs précédents (comportement historique) |
| **Divergent** | Diagnostic multi-hypothèses, RCA, audit — l'indépendance des angles prime | `context.md` **UNIQUEMENT**. Seul le **Scribe** lit tous les handoffs et confronte les angles |

Règle de choix : les personas doivent-ils se **compléter** (convergent) ou pouvoir se
**contredire** (divergent) ? Cause inconnue à diagnostiquer → divergent. Solution connue
à construire → convergent. Le régime est déclaré dans `.party/context.md` (champ `Régime`).

**Qui / Quand / Pourquoi** :

- **QUI** : les personas du PLAN (dérivés du mapping `demande → workflow → personas`).
  Chaque persona = un appel `runSubagent("<persona>")`.
- **QUAND** : après validation du PLAN (phase CONFIRM), dans l'ordre exact du PLAN.
  Ni saut, ni ajout silencieux, ni réordonnancement.
- **POURQUOI** : chaque sous-agent reçoit une **fenêtre fraîche** (pas de croissance
  quadratique du contexte). Le Scribe lit uniquement les handoffs condensés
  (cible ≤ 500 tokens, plafond 1000) au lieu de l'historique brut de tous ses prédécesseurs.

**Flow opérationnel** :

1. **Purger `.party/` s'il contient des fichiers** (résidus d'une session Party mode
   interrompue = contexte périmé à ne jamais réutiliser), puis créer
   `.party/context.md` (template [`party-context.md`](../../../agents/templates/party-context.md))
   — objectif, scope, séquence agents, **régime** (convergent / divergent).
2. Pour chaque agent : `runSubagent("<agent>")` → lit `.party/context.md` (+ handoffs
   précédents **en régime convergent uniquement**) → produit → écrit
   `.party/handoff-<agent>.md` (budget : voir règle ci-dessous).
3. **Gate intermédiaire (orchestrateur)** — avant d'invoquer l'agent suivant, vérifier le
   handoff produit : 4 sections présentes, budget respecté (plafond 1000 tokens ; un
   handoff gonflé sans signal est non conforme même sous le plafond), critères
   « Done quand » du persona satisfaits (section dédiée de son `.agent.md`),
   et **chaque finding porte un pointeur de preuve falsifiable** (fichier:ligne,
   requête + fenêtre UTC, lien doc) — une affirmation qui ne pourrait pas être
   contredite par une observation n'est pas un finding, c'est une opinion.
   Handoff non conforme → re-invoquer l'agent (**1 seule fois**), puis fallback
   impersonation si l'échec persiste. La qualité ne repose jamais sur le seul Scribe.
4. Lire `handoff-scribe.md` (quality gate final).
5. **Supprimer `.party/`** (transitoire, `.gitignore`-d). Ne pas omettre.

**Budget handoff — le nécessaire, pas le maximum** :

- **Cible ≤ 500 tokens** ; **plafond absolu 1000 tokens / 4000 chars**. Le plafond est
  un filet de sécurité, jamais un objectif de remplissage.
- **Règle binaire pointeur > recopie** : une info qui existe dans un fichier du repo
  (diff, table, analyse) est **référencée** (`voir path/to/file`), jamais recopiée dans
  le handoff. Le suivant lit le fichier s'il en a besoin.
- Au-delà de la cible, chaque ligne doit être du **signal** (findings conclusifs,
  contexte critique, risques) — la transcription du raisonnement est une violation.
- `context.md` reste à **≤ 500 tokens** (écrit par l'orchestrateur : objectif/scope,
  pas de matière longue).

**Fallback** : si `runSubagent` échoue → impersonne le persona + écrit le handoff
manuellement → continue la séquence.

**Agents disponibles** : `devops`, `developer`, `security`, `architect`, `qa`,
`product-analyst`, `data-engineer`, `scribe`. Fichiers : `.github/agents/<agent>.agent.md`.

**Débat = inline — choix de design, pas une limite technique.** Un débat est
*réactif* : chaque persona doit voir l'argumentation complète des rounds précédents.
En sous-agents, il faudrait ré-injecter tout l'historique à chaque round → le gain
« handoffs condensés » disparaît, et on ajoute latence + relais. Donc `/debate` reste
**inline uniquement** ; la case *Débat × sous-agents* est **volontairement vide**.
