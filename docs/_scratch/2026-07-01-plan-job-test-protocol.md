# Plan — Protocole de test terrain (« à la job »)

> Objectif : valider les correctifs du 2026-07-01 (mode playbook, régimes party,
> contrats « Done quand », gate intermédiaire) sur des sessions de travail réelles
> **avant** toute décision structurante (roster, nouveaux workflows, intégrations
> JIRA/ServiceNow/Confluence/AWS — hors scope pour l'instant).

## 1. Setup (une fois, ~5 min)

1. Vérifier que le `.gitignore` de télémétrie est bien **versionné**
   (`docs/_scratch/telemetry/.gitignore` — commité, plus en `??` dans `git status`).
2. Activer les hooks dans les settings VS Code (workspace ou user) :

   ```jsonc
   "chat.hookFilesLocations": {
     "agents/hooks": true
   }
   ```

3. Recharger la fenêtre, vérifier **Output → GitHub Copilot Chat Hooks** (« Load Hooks »).
4. Procédure de test complète : `agents/hooks/README.md` § Procédure de test manuel.

## 2. Par session réelle (~1 min en fin de session)

Noter **3 métriques manuelles** (dans ce fichier, table § 4) :

| Métrique | Comment la compter |
|---|---|
| **Tours pour livrer** | Nombre de messages envoyés entre la demande initiale et le livrable final |
| **Confirmations subies** | Nombre de fois où l'orchestrateur a demandé une validation avant d'agir |
| **Routage correct** | Le(s) bon(s) persona(s) ont-ils été convoqués du premier coup ? (oui/non) |

Compléter si possible par un **mini field report** (modèle :
`docs/architecture/2026-05-04-field-report.md`) sur les sessions marquantes.

La télémétrie (si hooks actifs) compte automatiquement les événements et les
sous-agents : `docs/_scratch/telemetry/agent-telemetry.jsonl` (local, git-ignoré).

## 3. Critères de décision (après ~5-10 sessions)

| Observation | Décision à prendre |
|---|---|
| Routage erroné ≥ 2 fois | Ouvrir le chantier roster (personas dormants, table allégée) |
| Sous-agents rarement déclenchés (télémétrie `SubagentStart` ≈ 0) | Party Real reste tel quel — dé-prioriser son optimisation |
| Tours toujours élevés malgré le mode playbook | Chercher le goulot suivant (SYNTHESIS trop lourde ? relances ?) |
| Régime divergent utilisé et utile (angles réellement différents) | Conserver ; sinon simplifier (retour au convergent seul) |
| Besoin JIRA / ServiceNow / Confluence ressenti à chaque session | Ouvrir le chantier templates de sortie, puis évaluer MCP (ADR) |
| Handoffs rejetés par le gate ≥ 2 fois | Les critères « Done quand » travaillent — les affiner par persona |
| Handoffs systématiquement proches du plafond (1000) malgré la cible ~500 | Soit la cible est irréaliste (l'acter par ADR), soit la règle « pointeur > recopie » n'est pas appliquée (renforcer le gate) |

## 4. Journal des sessions

| Date | Type de tâche | Tours | Confirmations | Routage OK | Notes |
|---|---|---|---|---|---|
| | | | | | |

## Suivi

- Owner : Zav
- Révision : après ~5-10 sessions notées, ou fin 2026-07
- Ce plan est **temporaire** (`_scratch/`) — les décisions qui en sortiront iront
  dans `docs/decisions/` (ADR) si structurantes
