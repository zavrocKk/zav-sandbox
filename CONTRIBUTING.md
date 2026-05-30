# Contribuer à zav-sandbox

Bienvenue. Ce framework est 100 % Markdown, zéro dépendance runtime.
Contribuer = éditer des fichiers `.md` selon des conventions.

## Avant de commencer

1. Lis [`README.md`](README.md) — la philosophie et la structure.
2. Lis [`VISION.md`](VISION.md) — les 6 filtres de décision (toute contribution
   doit les passer).
3. Vérifie les [Issues ouvertes](https://github.com/zavrocKk/zav-sandbox/issues)
   pour éviter les doublons.

## Types de contributions

### Corriger un bug comportemental

Un persona ne répond pas comme attendu ? Un workflow produit le mauvais livrable ?

1. Ouvre une Issue avec le
   [template bug report](.github/ISSUE_TEMPLATE/bug_report.md).
2. Si tu as un fix : crée une branche `fix/<slug>`, propose une PR avec description
   du comportement avant/après.

### Ajouter une persona

1. Crée `agents/personas/<nom>.md` avec les sections : `Identité`, `Ton`,
   `Domaines`, `Quand intervenir`, `Output type`, `Handoffs`, `Anti-patterns`.
2. Ajoute la ligne dans le tableau personas de
   `.github/agents/orchestrator.agent.md`.
3. Mets à jour le mapping `demande → workflow → personas` si la persona ouvre de
   nouveaux types de demandes.
4. Mets à jour `README.md` (section structure) et `agents/personas/` dans l'arbre.

### Ajouter un workflow

1. Crée `agents/workflows/<nom>.md` avec : diagramme Mermaid des phases, table
   persona par étape, règles spécifiques, anti-patterns, livrable final.
2. Ajoute une ligne dans le mapping de l'orchestrator
   (`.github/agents/orchestrator.agent.md`).

### Ajouter une skill

Voir [`agents/skills/README.md`](agents/skills/README.md) pour la procédure
complète et les critères de qualité.

### Ajouter un template

1. Crée `agents/templates/<nom>.md` avec une structure prête à remplir
   (placeholders `<…>`).
2. Référence-le dans le persona Scribe (`agents/personas/scribe.md`) ou dans le
   workflow concerné.

### Améliorer la documentation

PRs bienvenues pour : coquilles, clarifications, exemples supplémentaires.

## Conventions

| Règle | Détail |
|---|---|
| Langue docs | Français |
| Langue code / identifiants | Anglais |
| Nommage `docs/incidents/` | `YYYY-MM-DD-slug.md` |
| Nommage `docs/decisions/` | `NNNN-slug.md` (numéro séquentiel 4 chiffres) |
| Nommage `docs/architecture/` | `YYYY-MM-DD-slug.md` |
| Diagrammes | Mermaid uniquement — pas d'images binaires |
| Secrets | Jamais en clair — `<REDACTED>` ou référence coffre |
| CHANGELOG | Généré par `release-please`, jamais édité à la main |

## Processus PR

1. Branche depuis `main` : `feat/<slug>`, `fix/<slug>`, `docs/<slug>`,
   `chore/<slug>`.
2. Commits en anglais, format conventionnel (`feat:`, `fix:`, `docs:`, `chore:`).
3. La CI vérifie les conventions de nommage des fichiers Markdown.
4. Ouvre la PR avec une description courte de ce qui change et pourquoi.
5. Merge par le mainteneur après review.

## Questions ?

Ouvre une [Discussion GitHub](https://github.com/zavrocKk/zav-sandbox/discussions)
ou une [Issue](https://github.com/zavrocKk/zav-sandbox/issues).
