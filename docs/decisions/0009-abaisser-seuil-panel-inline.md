---
type: adr
number: "0009"
status: accepted
date: 2026-06-08
deciders: [Zav]
tags: [orchestration, party-mode, subagents, threshold]
supersedes_partial: 0008
---

# ADR-0009 — Abaisser le seuil Panel inline à ≤ 2 personas

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-06-08
**Décideurs** : Zav
**Relation à ADR-0008** : raffinement (révise la règle de bascule, l'infrastructure `/party-real` reste intacte)

---

## Contexte

[ADR-0008](0008-subagents-party-real.md) a introduit `/party-real` (sous-agents réels) pour les sessions **4+ personas**, en gardant Panel inline comme défaut pour **≤ 3 personas**. Ce seuil a été choisi de manière conservatrice : `runSubagent` était une nouveauté, on voulait limiter le blast radius.

Trois semaines d'usage plus tard, le constat est clair :

- **`runSubagent` est stable** — aucune régression observée, le fallback impersonation n'a quasi jamais été déclenché.
- **Le bénéfice « fenêtre fraîche » se manifeste dès 3 personas**, pas seulement à 4. Sur un workflow `data-engineer → devops → scribe` (3 personas), le Scribe reçoit déjà un contexte pollué par les outputs DevOps précédents.
- **Le seuil à 3 crée un faux palier** : trois workflows nommés à exactement 3 personas (pipeline Airflow en échec, stratégie de tests, cadrage feature) restent en Panel inline alors qu'ils gagneraient à profiter de Party Real.
- **L'esprit de l'architecture** est d'isoler le contexte par persona. Panel inline est l'**exception** (sessions très courtes, 1-2 personas), pas la règle.

---

## Décision

Abaisser le seuil de bascule : **≤ 2 personas → Panel inline**, **≥ 3 personas → `/party-real` automatique**. Aucune borne supérieure pour `/party-real` (workflow à 7 personas reste l'usage cible, mais 3, 4, 5… sont tous traités identiquement).

**Nouvelle règle de bascule** :

| Personas | Mode | Pourquoi |
|---|---|---|
| 1 | Persona unique inline | Surcoût `runSubagent` injustifié pour une seule perspective |
| 2 | Panel inline | Une seule passe d'impersonation, contexte borné par construction |
| **3+** | **`/party-real` automatique** | Fenêtre fraîche par persona, scaling linéaire, isolation des erreurs |
| Workflow complet | `/party-real` automatique | Indépendant du nombre |
| `/debate` demandé | Débat inline | Inline uniquement (incompatibilité technique avec sous-agents — voir [ADR-0008](0008-subagents-party-real.md)) |

L'utilisateur ne tape jamais `/party-real`. L'orchestrateur déclare le mode dans le PLAN.

**Qui / Quand / Pourquoi** — clarification du rôle de l'orchestrateur :

- **QUI invoquer** : la liste des personas est dérivée du mapping `demande → workflow → personas` (table dans `orchestrator.agent.md`). Si le PLAN liste N personas, l'orchestrateur appelle `runSubagent("<persona>")` pour chacun, dans l'ordre.
- **QUAND invoquer** : dès la fin de la phase CONFIRM, dans l'ordre du PLAN. Pas de saut, pas d'ajout silencieux.
- **POURQUOI** : chaque sous-agent reçoit une fenêtre fraîche → pas de croissance quadratique du contexte → le Scribe lit uniquement les handoffs condensés (≤ 500 tokens chacun) au lieu de l'historique brut de tous ses prédécesseurs.

---

## Alternatives considérées

### Option A — Statu quo (seuil à ≤ 3)

- Description : Conserver la règle ADR-0008 inchangée.
- Avantages : Aucun changement, ADR-0008 reste valide intégralement.
- Inconvénients : Les workflows à 3 personas continuent de subir la pollution contextuelle inutilement. Le seuil reste arbitraire.
- **Pourquoi rejetée** : trois semaines d'usage ont validé `runSubagent`. Le coût de l'inertie dépasse le risque d'abaisser le seuil.

### Option B — Supprimer Panel inline complètement (`/party-real` pour 2+ personas)

- Description : Tout multi-persona passe par sous-agents, Panel inline réservé au persona unique.
- Avantages : Règle ultra-simple ("1 = inline, 2+ = subagent"), aucune ambiguïté.
- Inconvénients : Surcoût `runSubagent` + `.party/` I/O pour les sessions à 2 personas où l'impersonation est largement suffisante (ex. `dev → scribe` après une question simple). Verbosité du protocole `.party/` non justifiée pour si peu.
- **Pourquoi rejetée** : 2 personas en impersonation est rapide, lisible, sans coût d'infra. Le gain de Party Real se manifeste à partir de 3.

### Option C — Seuil dynamique (basé sur la longueur estimée de l'output)

- Description : L'orchestrateur estime la verbosité attendue de chaque persona et bascule en sous-agents si le total prédit dépasse un budget.
- Avantages : Théoriquement optimal.
- Inconvénients : Heuristique impossible à appliquer fiablement par un LLM, surface de bug énorme, contredit le principe de règle binaire.
- **Pourquoi rejetée** : trop fragile, viole « règles binaires » du framework.

---

## Conséquences

**Positives** :

- Trois workflows ad-hoc (pipeline-airflow, stratégie-tests, cadrage-feature) basculent automatiquement en `/party-real` — gain de tokens estimé ~50 % sur ces sessions.
- Cohérence : Party Real devient le mode **par défaut** pour le multi-persona, conforme à l'esprit "isolation par défaut".
- Le rôle de l'orchestrateur se simplifie : la règle « 3+ → subagent » est plus mémorable que « 4+ → subagent ».
- Aucun upper-bound sur `/party-real` — un workflow à 10 personas fonctionne identiquement à un workflow à 3.

**Négatives / risques** :

- Overhead `runSubagent` + écriture/lecture `.party/handoff-*.md` pour les sessions à 3 personas qui prenaient une seule passe d'impersonation auparavant. Latence supplémentaire estimée : +1-2 s par persona.
- ADR-0008 contient désormais une affirmation périmée (« Panel inline inchangé pour ≤ 3 personas »). Note de référence ajoutée dans 0008 pour pointer vers 0009.
- Les exemples README existants à 4+ personas restent inchangés, mais tout nouvel exemple à exactement 3 doit montrer le mode Party Real.

**Mesures de mitigation** :

- Le fallback impersonation reste documenté (cf. ADR-0008 §Décision-5) si `runSubagent` échoue.
- La règle Mode/Personas est centralisée dans `orchestrator.agent.md` (§Règle de bascule) — une seule source de vérité à modifier.

---

## Références

- ADR-0008 (raffinée par celle-ci) : [`0008-subagents-party-real.md`](0008-subagents-party-real.md)
- Orchestrateur (source de vérité de la règle) : [`.github/agents/orchestrator.agent.md`](../../.github/agents/orchestrator.agent.md)
- Skill party-mode : [`agents/skills/party-mode/SKILL.md`](../../agents/skills/party-mode/SKILL.md)
- Protocole Panel (critères sémantiques, inchangés) : [`agents/protocols/light-panel.md`](../../agents/protocols/light-panel.md)
