---
type: adr
number: "0012"
status: accepted
date: 2026-07-01
deciders: [Zav]
tags: [orchestration, agents, personas, single-source, subagents, mt3]
---

# ADR-0012 — Source unique par agent : fusionner la persona dans le `.agent.md`

> Format : Michael Nygard. Issu du spike de faisabilité MT3 (fil
> `orchestration-refacto-mt2-mt3`). Point pivot (inlining des liens) **levé empiriquement**
> le 2026-07-01 ; décision `accepted`.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-01
**Décideurs** : Zav
**Bloqueur avant `accepted`** : ~~lever le Point à confirmer~~ → **levé le 2026-07-01**
(test empirique, voir § « Point à confirmer »).

---

## Contexte

Chaque agent du framework est défini à **deux endroits** :

- `.github/agents/<agent>.agent.md` — le custom agent VS Code (frontmatter
  `name`/`description`/`tools` + comportement `/party-real`).
- `agents/personas/<agent>.md` — la persona riche (identité, ton, domaines,
  output type, handoffs, anti-patterns, périmètre).

Le `.agent.md` **ne copie pas** la persona : il la référence par un lien markdown
(`Persona complète : [agents/personas/<agent>.md](...)`). Ce n'est donc pas une
duplication littérale, mais un **split**.

### Constats du spike (2026-07-01)

Sur les 9 agents :

| Fichier | Taille | Rôle |
|---|---|---|
| 8 `*.agent.md` (hors orchestrateur) | ~30-40 lignes | Stub : frontmatter + lien persona + bloc `/party-real` |
| `personas/*.md` (hors orchestrateur) | 84-158 lignes | Contenu riche |
| `orchestrator.agent.md` | 202 lignes | **Inversé** : contenu réel ici… |
| `personas/orchestrator.md` | 13 lignes | …persona réduite à un pointeur (déjà fait, ADR-0006 C1) |

Le pattern est donc **incohérent** : l'orchestrateur a déjà `.agent.md` comme
source unique, les 8 autres ont l'inverse (persona = source, `.agent.md` = stub).

### Faits VS Code — **[Confirmé]** (doc officielle *Custom agents in VS Code*)

1. VS Code détecte comme custom agent **tout `.md` dans `.github/agents/`**. Les
   `agents/personas/*.md` **ne sont pas des agents** — juste des docs liées.
   → un `.agent.md` doit physiquement vivre dans `.github/agents/`.
2. « When you select the custom agent, the guidelines in the custom agent file
   **body are prepended to the prompt** » → le corps du `.agent.md` **est** le
   system prompt du (sous-)agent.
3. « You can **reference** other files by using Markdown links… to reuse
   instructions » — formulé comme un *renvoi*, **sans garantie documentée**
   d'expansion/inlining automatique dans le contexte.

### Le vrai problème (reformulé)

Ce n'est pas « tuer une duplication ». C'est : **le split peut laisser la moitié
de la définition non chargée**. Quand `runSubagent("developer")` s'exécute, le
sous-agent reçoit le stub (`name`/`tools`/`party-real`) ; rien ne garantit qu'il
reçoive les 88 lignes de persona (ton, domaines, anti-patterns, output). Le stub
dit « Persona complète : [lien] » — descriptif, pas impératif — et rien ne lui
ordonne de lire le fichier. L'orchestrateur échappe au problème parce qu'il est
déjà 100 % inline.

---

## Point à confirmer (pivot de la décision) — **RÉSOLU 2026-07-01**

**[Confirmé empiriquement]** VS Code **n'inline PAS** les liens markdown du corps d'un
`.agent.md` chargé comme sous-agent.

**Test** : `runSubagent("developer")` avec interdiction d'outils, demande de restituer
des éléments verbatim de la persona (règle de périmètre, 4 anti-patterns, format output).
**Résultat** : le sous-agent a répondu « INFO ABSENTE DE MON CONTEXTE » et a précisé que
son contexte contient « seulement le résumé du mode `developer` (comportement `/party-real`,
format de handoff) et un lien vers `agents/personas/developer.md`, mais pas le contenu ».

**Conséquence** : le split actuel laisse effectivement la persona **non chargée** côté
sous-agent. La fusion (Décision) corrige un **bug réel** — ce n'est pas cosmétique.

> Réserve de confiance : preuve = auto-rapport d'un sous-agent unique, cohérent avec la
> doc VS Code (§ Contexte, point 3). Suffisant pour trancher ; pas besoin de re-test.

---

## Décision

> Recommandée, **conditionnée** au Point à confirmer.

Adopter le `.agent.md` comme **source unique par agent** — généraliser aux 8
autres agents le modèle déjà retenu pour l'orchestrateur (ADR-0006 C1) :

- **Inliner** le contenu de `agents/personas/<agent>.md` dans
  `.github/agents/<agent>.agent.md`.
- Réduire `agents/personas/<agent>.md` à un **pointeur inverse** (identité + lien
  vers le `.agent.md`), ou le supprimer si aucune référence externe ne le justifie.
- Mettre à jour toutes les références (`orchestrator.agent.md` table personas,
  `README.md` arbre, workflows) vers `.github/agents/`.

**Pourquoi C plutôt que A/B** — passage aux 6 filtres VISION :

| Filtre VISION | Option C (fusion) |
|---|---|
| #1 Pour qui | ✅ Ne change pas l'audience |
| #2 Markdown lisible | ✅ Un seul `.md` par agent, éditable à la main |
| #3 VSCode + Copilot natif | ✅ Aucun outil hors VS Code |
| #4 Dev senior nécessaire ? | ✅ **Aucun build** — un non-dev édite un fichier |
| #5 Drift | ✅ Une seule source → plus de divergence possible |
| #6 Livrables markdown | ✅ Inchangé |

---

## Alternatives considérées

### Option A — Générateur (persona = source, `.agent.md` généré)
- Description : script de build qui inline la persona dans le `.agent.md`.
- Avantages : la persona reste le fichier « noble » ; génération déterministe.
- Inconvénients : introduit une étape de build/tooling.
- **Pourquoi rejetée** : **échoue au filtre VISION #4** — un générateur (script
  Node/Python/Make) exige un dev pour l'exécuter et le maintenir. Contredit
  frontalement « 100 % markdown, configurable par un non-dev ».

### Option B — Drift-check (garder les 2 fichiers, CI vérifie la cohérence)
- Description : CI qui alerte si `.agent.md` et persona divergent.
- Avantages : conserve la séparation actuelle.
- Inconvénients : il n'y a **rien à comparer** (le stub ne copie pas la persona),
  et ça ne corrige pas la persona potentiellement non chargée.
- **Pourquoi rejetée** : résout un faux problème (la duplication n'existe pas) et
  laisse le vrai (chargement) intact.

---

## Conséquences

### Positives
- Une seule source de vérité par agent ; cohérence totale avec l'orchestrateur.
- La persona est **garantie** dans le contexte du sous-agent (elle est dans le corps).
- Suppression du risque de drift silencieux `.agent.md` ↔ persona.

### Négatives
- Les 8 `.github/agents/*.agent.md` grossissent (~90 lignes chacun).
- `agents/personas/*.md` perd son rôle de doc « browsable » hors mécanique VS Code
  (mitigé par le pointeur inverse).
- Réécriture des 8 fichiers + mise à jour des références croisées (touche les mêmes
  fichiers que MT1 → **séquencer après merge PR #130**).

### Neutres / À surveiller
- Le comportement `/party-real` (déjà dans les `.agent.md`) reste inchangé.
- ~~Si le Point à confirmer révèle un inlining automatique, réévaluer l'urgence~~
  → **tranché** : pas d'inlining automatique, la fusion est un correctif, pas un choix
  cosmétique.

---

## Implémentation

> À exécuter **uniquement après** merge de la PR #130 (MT1) et création de la
> branche `feat/mt3-agent-source-unique`. ~~Prérequis : Point à confirmer levé.~~
> Prérequis levé (2026-07-01).

1. ~~Lever le Point à confirmer (Diagnostics / run sous-agent test).~~ ✅ fait.
2. Pour chaque agent (hors orchestrateur, déjà fait) : inliner la persona dans
   `.agent.md`, réduire/supprimer `agents/personas/<agent>.md`.
3. Mettre à jour les références : `orchestrator.agent.md`, `README.md`, workflows.
4. `/pre-pr` → PR.

## Références
- Spike : fil `orchestration-refacto-mt2-mt3`
  (`docs/_scratch/memory/orchestration-refacto-mt2-mt3.md`).
- Doc VS Code : [Custom agents in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents).
- [ADR-0006](0006-modulariser-orchestrator.md) — item C1 (déduplication
  orchestrateur : précédent du pattern retenu).
- VISION — 6 filtres de décision (`VISION.md`).
