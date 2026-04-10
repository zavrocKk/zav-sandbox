---
name: git-workflow
description: "Cheat-sheet du workflow Git GSANE — branches, commits, PRs."
applyTo: "**"
---

# Git Workflow — Cheat Sheet

## Règle absolue

Jamais de commit direct sur `main`. Toujours : branche → commit → push → PR → merge.

## Nommage des branches

| Type | Format | Exemple |
|------|--------|---------|
| Fonctionnalité | `feature/{desc}-{YYYYMMDD}` | `feature/add-mcp-tool-20260410` |
| Correction | `fix/{desc}-{YYYYMMDD}` | `fix/changelog-encoding-20260410` |

## Conventional Commits

```
feat(agents): ajout menu contextuel dans master.md
fix(mcp): correction chemin relatif dans compression_tool
chore(deps): mise à jour mcp[cli] vers 1.2.0
docs(skills): création skill prompt-engineering
test(qa): ajout test validation AC format
```

Scopes courants : `agents`, `mcp`, `deps`, `skills`, `workflows`, `ci`, `qa`, `core`.

## Checklist PR

- [ ] Description remplie (titre + corps — jamais de PR vide)
- [ ] Tests ajoutés/mis à jour (`pytest tests/ -v`)
- [ ] Linting OK (`ruff check _gsane/ tests/`)
- [ ] CHANGELOG.md mis à jour (section `[Unreleased]`)
- [ ] Pas de secrets hardcodés
- [ ] Delivery Contract référencé (si applicable)

## Vérification pre-push

```bash
bash gsane.sh validate
```

Exécute : pytest + qa-linter + vérification CHANGELOG. EXIT 0 requis avant push.
