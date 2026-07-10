---
type: index
title: Registre des livrables — docs/
description: Une ligne par livrable produit (hors _scratch et decisions/, auto-indexés). Seul fichier à scanner pour retrouver un artefact — jamais de scan de dossiers.
timestamp: 2026-07-09
---

> **Règle binaire** ([copilot-instructions](../.github/copilot-instructions.md) §
> Table de localisation) : toute **création** ou **changement de statut** d'un
> livrable dans `docs/` ajoute/met à jour sa ligne ici — création sans ligne
> d'index = non conforme. Le Scribe tient ce registre à la SYNTHESIS.

## Racine `docs/` — bilans, analyses, features, data

| Date | Type | Sujet | Statut | Fichier |
|---|---|---|---|---|
| _(aucun livrable racine encore)_ | | | | |

## Incidents (post-mortems)

| Date | Sévérité | Sujet | Statut | Fichier |
|---|---|---|---|---|
| 2026-05-02 | SEV2 | API notifications 5xx | archived | [2026-05-02-notification-api-5xx.md](incidents/2026-05-02-notification-api-5xx.md) |
| 2026-05-02 | SEV2 | Postgres disque plein | archived | [2026-05-02-postgres-disk-full.md](incidents/2026-05-02-postgres-disk-full.md) |

## Architecture (notes évolutives, cadrages)

| Date | Sujet | Fichier |
|---|---|---|
| 2026-05-02 | Audit sécurité admin/users | [2026-05-02-security-audit-admin-users.md](architecture/2026-05-02-security-audit-admin-users.md) |
| 2026-05-04 | Field report (usage terrain) | [2026-05-04-field-report.md](architecture/2026-05-04-field-report.md) |
| 2026-05-10 | Stress test théorique | [2026-05-10-theoretical-stress-test-analysis.md](architecture/2026-05-10-theoretical-stress-test-analysis.md) |
| 2026-05-30 | Cadrage Phase 7 — mémoire persistante | [2026-05-30-phase-7-persistent-memory.md](architecture/2026-05-30-phase-7-persistent-memory.md) |
| 2026-05-30 | Cadrage Phase 8 — skills | [2026-05-30-phase-8-skills.md](architecture/2026-05-30-phase-8-skills.md) |

## Bundles auto-indexés (ne pas dupliquer ici)

- [`decisions/`](decisions/) — ADRs, auto-indexés par numéro séquentiel `NNNN`
- [`apps/`](apps/index.md) — fiches d'applications, index OKF propre
- `runbooks/` — à créer au premier runbook (une section sera ajoutée ici)
- `_scratch/` — temporaire par définition, jamais indexé
