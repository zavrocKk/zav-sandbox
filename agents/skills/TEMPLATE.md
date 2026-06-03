---
name: <skill-slug>          # lowercase, chiffres, tirets uniquement ; ≤ 64 car.
version: "1.0.0"            # SemVer — obligatoire (voir politique docs/architecture/2026-05-30-phase-8-skills.md §2)
description: >
  <Décrit ce que la skill fait ET quand l'utiliser, à la 3e personne.>
  <À utiliser quand… Ne pas utiliser pour…>
  # ≤ 1024 car. — c'est ce champ que le moteur lit pour décider du déclenchement.
---

# <Nom lisible de la skill>

<!-- Corps du SKILL.md :
  - < 500 lignes (règle de performance Anthropic). Au-delà → scinder en reference/*.md
  - Sections libres mais concises : savoir SPECIFIQUE seulement (conventions, patterns, pièges)
  - Pas d'info datée (« avant août 2025… ») → section « patterns hérités » si besoin
  - Chemins en slash avant (reference/guide.md), jamais antislash Windows
  - Pas d'appel réseau, pas de script exécuté : markdown statique uniquement
-->

## Quand utiliser quel outil / méthode

| Situation | Outil / approche | Pourquoi |
|---|---|---|
| <cas 1> | <outil 1> | <raison> |
| <cas 2> | <outil 2> | <raison> |

## Procédure / méthode

<!-- Décrire les étapes ou la méthode en détail. Utiliser des listes numérotées si l'ordre compte. -->

1. <Étape 1>
2. <Étape 2>
3. <Étape 3>

## Format de livrable attendu

<!-- Quel artefact cette skill aide à produire ? Table, Mermaid, section doc ? -->

```
<exemple minimal>
```

## Pièges courants

- ❌ <anti-pattern 1>
- ❌ <anti-pattern 2>

## Références internes

<!-- Optionnel — liens vers checklists, templates, workflows qui utilisent cette skill -->
- Workflow : [`agents/workflows/<nom>.md`](../workflows/<nom>.md)
- Checklist : [`agents/checklists/<nom>.md`](../checklists/<nom>.md)
