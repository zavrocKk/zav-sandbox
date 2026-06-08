---
type: adr
number: "0008"
status: accepted
date: 2026-06-08
deciders: [Zav]
tags: [orchestration, party-mode, subagents, tokens]
---

# ADR-0008 — Introduire `/party-real` : sous-agents réels pour les workflows 4+ personas

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-06-08
**Décideurs** : Zav

---

## Contexte

Le framework Agentic Team (zav-sandbox) utilise un mode **Panel inline** : l'orchestrateur impersonne séquentiellement chaque persona dans une seule fenêtre de contexte. Cette approche fonctionne bien pour les sessions courtes (≤ 3 personas).

Sur les workflows complets (ex : `feature-development` = 7 personas), le problème est structurel : **chaque persona hérite du contexte de tous ses prédécesseurs**. La fenêtre croît de manière quadratique. Sur un workflow 7 personas, le Scribe reçoit ~42 000 tokens d'input là où 5 000 suffiraient.

Conséquences observées :
- Saturation de contexte sur les sessions longues
- Risque de perte de protocole après compaction
- Coût token élevé sans gain de qualité sur les personas tardifs

VS Code Copilot expose `runSubagent` (déjà déclaré dans les tools de l'orchestrateur) qui permet d'invoquer un agent nommé dans une fenêtre fraîche. Ce mécanisme résout le problème structurel de pollution de contexte.

---

## Décision

Introduire **`/party-real`** comme nouveau mode du Party Mode pour les sessions 4+ personas.

**Règle de bascule** :
- ≤ 3 personas → Panel inline (impersonation, aucun changement)
- 4+ personas OU workflow complet bout-en-bout → `/party-real`

**Mécanisme** :
1. L'orchestrateur crée `.party/context.md` (≤ 500 tokens) — objectif, scope, séquence.
2. Pour chaque agent : `runSubagent("<agent>")` → fenêtre fraîche → lit `context.md` + handoffs précédents → produit son travail → écrit `.party/handoff-<agent>.md` (≤ 500 tokens).
3. Le Scribe consolide depuis tous les handoffs → produit le livrable `docs/`.
4. L'orchestrateur supprime `.party/` (transitoire, `.gitignore`-d).
5. Fallback si `runSubagent` échoue : impersonation + écriture manuelle du handoff.

**Infrastructure** :
- 7 fichiers `.github/agents/<persona>.agent.md` avec tools restreints au périmètre du persona.
- `.party/` gitignore-d à la racine.
- Templates `agents/templates/party-context.md` et `agents/templates/party-handoff.md`.

---

## Alternatives considérées

### Option A — Statu quo (Panel inline uniquement)

- Description : Continuer avec l'impersonation séquentielle dans une seule fenêtre.
- Avantages : Zéro infrastructure, zéro maintenance.
- Inconvénients : Saturation quadratique sur sessions longues, coût token non maîtrisé.
- **Pourquoi rejetée** : Le problème est structurel et s'aggrave avec la complexité des sessions.

### Option B — Hooks Python (style gmad)

- Description : Utiliser des scripts Python (`session_start.py`, `subagent_start.py`) pour injecter automatiquement le contexte dans chaque sous-agent.
- Avantages : Injection automatique sans intervention de l'orchestrateur.
- Inconvénients : Dépendance Python, surface de maintenance supplémentaire, hors paradigme VS Code Copilot natif.
- **Pourquoi rejetée** : `runSubagent` natif VS Code est suffisant et élimine la dépendance infrastructure. La discipline des budgets tokens (≤ 500) remplace l'injection automatique.

### Option C — Compaction manuelle entre chaque persona (Panel inline amélioré)

- Description : L'orchestrateur résume le contexte avant chaque persona pour limiter la croissance.
- Avantages : Pas de nouvelle infrastructure.
- Inconvénients : Résumé manuel = travail de l'orchestrateur, risque de perte d'information, ne résout pas le problème fondamental.
- **Pourquoi rejetée** : Solution palliative, pas structurelle.

---

## Conséquences

**Positives** :
- Réduction estimée ~80 % des tokens input sur les workflows 4+ personas.
- Isolation des erreurs inter-agents.
- Chaque agent ne voit que ce dont il a besoin (principe de moindre privilège appliqué aux outils via `tools` restreints).
- Compatibilité ascendante totale : Panel inline inchangé pour ≤ 3 personas.

**Négatives / risques** :
- 7 `.agent.md` à maintenir en cohérence avec les personas `.md` (source de dérive potentielle).
- `runSubagent` peut échouer (erreur 400) — fallback impersonation documenté et testé.
- Débogage légèrement plus complexe (handoffs à lire dans `.party/`).

---

## Références

- Protocole Panel : [`agents/protocols/light-panel.md`](../../agents/protocols/light-panel.md)
- Skill party-mode (v1.1.0) : [`agents/skills/party-mode/SKILL.md`](../../agents/skills/party-mode/SKILL.md)
- Templates : [`agents/templates/party-context.md`](../../agents/templates/party-context.md), [`agents/templates/party-handoff.md`](../../agents/templates/party-handoff.md)
- Agents personas : `.github/agents/devops.agent.md`, `developer.agent.md`, `security.agent.md`, `architect.agent.md`, `qa.agent.md`, `product-analyst.agent.md`, `scribe.agent.md`
- Analyse comparative gmad vs zav-sandbox : session du 2026-06-08
