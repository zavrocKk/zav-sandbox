---
type: memory-checkpoint
thread: orchestration-refacto-mt2-mt3
phase: "post-9.2 — refacto orchestration"
branch: feat/mt3-agent-source-unique (à créer)
status: in-progress
last_session: 2026-07-01
next_action: "MT3 implémenté (PR draft) — attendre revue/merge, puis attaquer MT2 (/debate 2 axes format×mécanisme, ADR-0013)"
---

# Checkpoint de mémoire — Refacto orchestration (MT2 / MT3)

> **Rôle :** résumé de **reprise**. À relire EN PREMIER au démarrage de la nouvelle
> session sur ce fil. Deux refontes structurelles restent à cadrer puis implémenter.

## Objectif courant

Cadrer puis exécuter deux refontes issues de l'audit du framework :
- **MT3** — tuer la double-définition `agents/personas/*.md` ↔ `.github/agents/*.agent.md`.
- **MT2** — découpler le *format* (persona-unique / Panel / Débat) du *mécanisme*
  (inline / sous-agents), pour débloquer notamment un **Débat en sous-agents**.

## État (fait / en cours / bloqué)

- ✅ **QW1** — bug staleness `.party/` corrigé : purge au **démarrage** d'un Party Real
  (pas seulement à la clôture). Cohérent sur 5 points (orchestrator, module party-mode,
  skill, template party-context, sous-agent scribe).
- ✅ **MT1** — source unique pour la sémantique party-mode : le skill
  `agents/skills/party-mode/SKILL.md` est devenu un **routeur** (v2.0.0) ; back-pointer
  circulaire retiré du module ; descripteurs alignés (skills.md, skills/README.md, README.md).
  ⚠️ **Correctif 2026-07-01** : ce travail était **complet mais jamais commité** (posé sur
  `main`). Désormais formalisé dans **PR #130** (`feat/mt1-party-mode-source-unique`), en
  attente de merge. Le « ✅ » d'origine était prématuré (fait, pas landé).
- ✅ **MT3 — spike faisabilité fait (2026-07-01)**. Faits VS Code [Confirmé] : (1) `.agent.md`
  doit vivre dans `.github/agents/` ; les `personas/*.md` ne sont pas des agents ; (2) le
  **corps** du `.agent.md` est le system prompt du sous-agent ; (3) un lien markdown vers la
  persona n'a **aucune garantie d'inlining** documentée. Reformulation : ce n'est pas une
  duplication mais un **split** qui peut laisser la persona non chargée côté sous-agent.
- 📝 **MT3 — ADR-0012 (brouillon)** créé : `docs/decisions/0012-agent-persona-single-source.md`,
  statut `proposed`. Recommande **Option C** (fusion : persona inlinée dans `.agent.md`,
  source unique) ; A (générateur) éliminé par filtre VISION #4, B (drift-check) = faux problème.
- ✅ **MT3 IMPLÉMENTÉ (2026-07-01)** — option C : les 8 personas inlinées dans leurs
  `.github/agents/*.agent.md` (source unique) ; `agents/personas/*.md` réduits en pointeurs
  inverses ; liens `../checklists/` recalculés ; références maj (orchestrator table + 3 ancres
  Contrat Scribe, README, CONTRIBUTING, onboarding). **Validation end-to-end** : re-test
  `runSubagent("developer")` → récite désormais règle clé + 4 anti-patterns **verbatim sans
  lire de fichier** (avant = INFO ABSENTE). Lint/liens/parité OK. Sur branche
  `feat/mt3-agent-source-unique` (ADR-0012 commit d57dd8f). PR draft à ouvrir.
  NB : le check CI `check-relative-links` est un **no-op** (bug subshell bash : `errors`
  incrémenté dans un pipe → jamais propagé). À corriger un jour (hors scope MT3).
- 🔄 **MT2** — cadrage à faire. Rien codé.
- ⛔ Rien de bloqué.

## Décisions arrêtées (NE PAS rouvrir)

- **QW3 abandonné** : la critique « Party Real coûte plus de tokens » était fausse.
  Les handoffs condensés (≤500 tokens) sont le vrai bénéfice. Ne pas « corriger » le
  framing tokens des ADR-0008 / 0009 — il est exact.
- **Séquencement : MT3 avant MT2.** MT2 réécrit les 9 `.agent.md` ; MT3 doit d'abord
  fixer *comment* ces fichiers sont produits, pour ne les toucher qu'une fois.
- **Chaque refonte = un ADR obligatoire** (changement de comportement, pas juste de la doc).
- **Références historiques intactes** : ADR-0008 et ROADMAP Phase 9.1 gardent `v1.1.0`
  (état à la livraison — ne pas réécrire l'historique).

## Prochaines étapes

1. ✅ **Hygiène Git (2026-07-01)** : MT1 landé en PR #130 ; branches stale fusionnées
   supprimées (locales + distantes) : `feat/hooks-security-scanner`,
   `docs/roadmap-readme-phase92`, `feat/lower-panel-threshold`,
   `docs/plan-correctifs-audit-2026-05-30`. **Reste à faire** : après merge #130, créer
   `feat/mt3-agent-source-unique`. **Branches distantes à contenu unique laissées
   intactes** (revue requise avant suppression) : `feat/phase-10-party-real-followup`,
   `feat/phase-10-subagents-party-real`, `feat/phase-9-correctifs-devx`,
   `fix/audit-coherence-2026-06-08`. Stash local `audit cleanup` conservé (non tranché).
2. ✅ **MT3 — spike fait** + **ADR-0012 brouillon** écrit (option C recommandée).
   **Reste** : lever l'inconnue empirique (Diagnostics), puis passer l'ADR à `accepted`.
3. **MT3 — implémentation (option C)** après merge #130 : sur `feat/mt3-agent-source-unique`,
   inliner chaque persona dans son `.agent.md`, réduire `personas/*.md` à un pointeur inverse,
   mettre à jour les références (orchestrator table, README, workflows). NB : l'ADR-0012
   brouillon est actuellement **non commité** (working tree) — le committer sur la branche MT3.
4. **MT2 — `/debate`** (problème de design ouvert) sur le modèle à 2 axes
   {format} × {mécanisme} : combinaisons valides, choix du mécanisme (compte / flag /
   budget), faisabilité Débat-en-sous-agents (relais de rounds via `.party/`).
5. **MT2 — ADR-0013** (révise ADR-0008 / ADR-0009) → implémentation → `/pre-pr`.

## Pointeurs (artefacts pérennes produits)

- `agents/skills/party-mode/SKILL.md` — réécrit en routeur (MT1, v2.0.0)
- `.github/agents/modules/party-mode.md` — source unique mécanique Party Real (QW1 + MT1)
- `docs/decisions/0008-subagents-party-real.md` — Party Real (référence, ne pas rouvrir)
- `docs/decisions/0009-abaisser-seuil-panel-inline.md` — seuil 3+ (référence)
- ADR-0012 (MT3) et ADR-0013 (MT2) — **à créer** dans `docs/decisions/`

## Hypothèses / risques ouverts

- **MT3 (valeurs)** : un générateur `.agent.md` réintroduirait un build « pour devs »
  → conflit avec VISION « 100% markdown ». Issue probable = drift-guard, pas générateur.
- **MT2 (faisabilité)** : Débat-en-sous-agents exige que l'orchestrateur relaie chaque
  round ; coût tokens et latence à valider avant de promettre la fonctionnalité.
- **MT2 (compat)** : ne pas casser les commandes existantes (`/debate`, Party Real auto).
  Mapper l'ancien comportement sur le nouveau modèle 2 axes sans surprise utilisateur.
