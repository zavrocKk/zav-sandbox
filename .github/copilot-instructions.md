# Instructions globales — Workspace `zav-sandbox`

Ces règles s'appliquent à **toutes** les interactions Copilot dans ce workspace, quel que soit le mode (chat, edits, agent, custom agent).

> **Boussole stratégique** : en cas de doute sur une décision de périmètre ou de priorisation, consulte [`VISION.md`](../VISION.md).

## Langue

- **Réponses en français** par défaut.
- **Code, identifiants, commentaires de code, noms de fichiers** : en anglais.
- Messages de commit : anglais, format conventionnel (`feat:`, `fix:`, `chore:`…).

## Livrables

- Tout document produit (analyse, post-mortem, ADR, PRD, synthèse) va dans `docs/` au format :
  ```
  docs/YYYY-MM-DD-slug.md
  docs/incidents/YYYY-MM-DD-slug.md
  docs/architecture/YYYY-MM-DD-slug.md
  docs/decisions/NNNN-slug.md   (ADR : numéro séquentiel sur 4 chiffres)
  ```
- Le `slug` est en `kebab-case` anglais, court et descriptif.

## Diagrammes

- **Mermaid uniquement** (flowchart, sequence, C4, gantt, state). Pas d'images binaires, pas d'ASCII art lourd.
- Un diagramme Mermaid doit être encadré par ` ```mermaid ` … ` ``` `.

## Sécurité

- **Jamais de secrets en clair** dans le code, les docs, les exemples ou les logs. Utilise `<REDACTED>`, `${ENV_VAR}` ou une référence à un coffre (Vault, Key Vault, AWS SM…).
- Toute commande **destructive ou difficilement réversible** (`rm -rf`, `DROP`, `force push`, `terraform destroy`, suppression de branche distante, modification d'IAM partagé) **exige une confirmation utilisateur explicite** avant exécution.
- Signaler toute vulnérabilité OWASP Top 10 détectée incidemment, même hors scope.

## Citation des fichiers

- Toujours sous la forme `chemin/relatif/au/repo.ext:ligne` (ou plage `:42-58`).
- Pour les références dans du markdown rendu : `[fichier.ext:ligne](fichier.ext#L42)`.

## Style

- Concret, factuel, pragmatique. Pas de blabla d'introduction (« Bien sûr ! », « Excellente question ! »).
- Listes et tables > paragraphes denses.
- Si une information manque, **demande** plutôt que d'inventer.

## Personas disponibles (mode Orchestrator)

Liste complète et mapping workflow → personas dans [`.github/agents/orchestrator.agent.md`](agents/orchestrator.agent.md).

## Mode Orchestrator

Quand le custom agent `orchestrator` est actif, suis en plus les règles définies dans `.github/agents/orchestrator.agent.md` (priorité sur ces instructions globales en cas de contradiction sur le format).

## Table de localisation des artefacts (référence unique)

| Type de livrable | Emplacement obligatoire | Format de nom |
|---|---|---|
| Rapport d'incident | `docs/incidents/` | `YYYY-MM-DD-slug.md` |
| ADR | `docs/decisions/` | `NNNN-slug.md` |
| Note d'architecture | `docs/architecture/` | `YYYY-MM-DD-slug.md` |
| Runbook | `docs/runbooks/` | `<system>-<topic>.md` |
| PRD | `docs/prd/` ou `docs/` | `<slug>.md` |
| Bilan de session | `docs/_scratch/` | `YYYY-MM-DD-session-<topic>.md` |
| Note de délibération (Débat) | `docs/decisions/` si ADR, sinon `docs/_scratch/` | `NNNN-slug.md` ou `YYYY-MM-DD-debate-<topic>.md` |
| Field Report (hors repo) | n/a | papier/OneNote/perso |

Le Scribe DOIT consulter cette table avant chaque création de fichier.
Cette table est l'unique référence — toute autre indication dans personas
ou workflows doit pointer vers elle.

Si un type de livrable n'est pas dans cette table, le Scribe DOIT
demander à l'utilisateur où le placer ET proposer d'ajouter une ligne
dans cette table.

## Ressources de référence

| Type | Chemin |
|---|---|
| Checklists | `agents/checklists/incident-triage.md`, `security-review.md`, `pre-deploy.md` |
| Templates | `agents/templates/incident-report.md`, `adr.md`, `prd.md` |
| Workflows | `agents/workflows/incident-response.md`, `code-analysis.md`, `feature-development.md`, `architecture-design.md`, `data-pipeline.md` |
| Protocoles | `agents/protocols/preflight.md` |
