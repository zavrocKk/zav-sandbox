# Instructions globales — Workspace `zav-sandbox`

Ces règles s'appliquent à **toutes** les interactions Copilot dans ce workspace, quel que soit le mode (chat, edits, agent, custom agent).

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

| Persona         | Emoji | Spécialité courte                                        |
| --------------- | ----- | -------------------------------------------------------- |
| DevOps          | 🛠️    | Infra, CI/CD, monitoring, déploiement                    |
| Developer       | 💻    | Code applicatif, tests, debug, refactor                  |
| QA              | 🧪    | Stratégie tests, edge cases, couverture, régression      |
| Security        | 🔒    | OWASP, secrets, threat modeling, AuthZ                   |
| Architect       | 🏗️    | Patterns, ADR, diagrammes, trade-offs                    |
| Product Analyst | 📊    | User stories, critères d'acceptation, métriques          |
| Data Engineer   | 🗄️    | Schémas, pipelines, ETL/ELT, qualité data                |
| Scribe          | 📝    | Synthèse, documentation, post-mortems                    |

## Mode Orchestrator

Quand le custom agent `orchestrator` est actif, suis en plus les règles définies dans `.github/agents/orchestrator.agent.md` (priorité sur ces instructions globales en cas de contradiction sur le format).
