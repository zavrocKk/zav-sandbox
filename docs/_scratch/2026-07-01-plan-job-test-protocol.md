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
| Sous-agents rarement déclenchés (télémétrie `SubagentStart` ≈ 0) | Party mode (sous-agents) reste tel quel — dé-prioriser son optimisation |
| Tours toujours élevés malgré le mode playbook | Chercher le goulot suivant (SYNTHESIS trop lourde ? relances ?) |
| Régime divergent utilisé et utile (angles réellement différents) | Conserver ; sinon simplifier (retour au convergent seul) |
| Besoin JIRA / ServiceNow / Confluence ressenti à chaque session | Skills de sortie livrées (ADR-0015) : les adapter à l'instance (fixtures `mvp-inputs/`), puis évaluer MCP (ADR) |
| Skills mal sélectionnées entre les 4 de la famille analyste (mauvais matching de description) | Affiner les `description` des SKILL.md concernées (ADR-0015) |
| Handoffs rejetés par le gate ≥ 2 fois | Les critères « Done quand » travaillent — les affiner par persona |
| Handoffs systématiquement proches du plafond (1000) malgré la cible ~500 | Soit la cible est irréaliste (l'acter par ADR), soit la règle « pointeur > recopie » n'est pas appliquée (renforcer le gate) |
| Routage `bilan-remediation` confondu avec incident-response / code-analysis ≥ 2 fois | Affiner la désambiguïsation du mapping (ADR-0014) |
| Routage `bilan-remediation` correct sur ≥ 3 sessions et gate d'approbation utile | Lever l'exclusion playbook du workflow (ADR-0014) |
| **H1** — app nommée mais fiche non trouvée (nom/alias) ≥ 2 fois | Enrichir les `aliases`, sinon invalider le rappel par nom (ADR-0017) |
| **H2** — une fiche app doit dépasser 100 lignes pour être utile | Revoir le plafond ou la structure de fiche (ADR-0017) |
| **H3** — budget 2 fiches/session dépassé ou insuffisant ≥ 2 fois | Recalibrer le budget mémoire (ADR-0017) |
| **H4** — aucun Δ-mémoire utile après ~5 sessions touchant des apps fichées | Le contrat Δ-mémoire ne paie pas — simplifier ou retirer (ADR-0017) |
| **H5** — l'orchestrateur ne retrouve pas un artefact produit précédemment (bilan, post-mortem) sans chemin exact fourni, ≥ 2 fois | La découvrabilité de `docs/` est insuffisante → étendre le pattern OKF (index des livrables) |

## 4. Journal des sessions

| Date | Type de tâche | Tours | Confirmations | Routage OK | Notes |
|---|---|---|---|---|---|
| | | | | | |

## Suivi

- Owner : Zav
- Révision : après ~5-10 sessions notées, ou fin 2026-07
- Ce plan est **temporaire** (`_scratch/`) — les décisions qui en sortiront iront
  dans `docs/decisions/` (ADR) si structurantes
