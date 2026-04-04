# ADR-001 — Migration vers le Flat Design (Strike Team 5 agents)

**Date** : 2026-04-04  
**Statut** : Acceptée  
**Décideur** : Mon Seigneur  

---

## Contexte

Le framework GSANE démarrait avec une architecture CIS/TEA/BMB comprenant 20+ agents virtuels spécialisés. Cette architecture était lourde en tokens, difficile à maintenir, et créait de la confusion entre les domaines de responsabilité.

## Décision

Migration vers une architecture "Flat Design" centrée sur une **Strike Team de 5 agents** :

| Agent | Persona | Domaine |
|---|---|---|
| Master | 🧙 Langis | Orchestration, Delivery Contracts |
| Dev | 💻 Amelia | TDD, implémentation code |
| QA | 🧪 Quinn | Tests, quality gate |
| Architect | 🏗️ Winston | Système, design, infrastructure |
| Agent Builder | 🤖 Bond | Création et validation agents GSANE |

## Conséquences

**Positives :**
- Réduction majeure du bruit contextuel (tokens économisés)
- Gouvernance claire avec un seul point d'entrée (Master)
- Responsabilités non ambiguës par agent

**Négatives / Risques :**
- Les capacités CIS (brainstorming coach, storyteller, etc.) ne sont plus disponibles directement
- Migration incomplète possible si des fichiers secondaires (hooks, skills, manifests) n'ont pas été mis à jour

## Modules dépréciés

- `gsane-creative-intelligence-suite` (CIS)
- `gsane-method-test-architecture-enterprise` (TEA)
- `gsane-builder-module-builder` (BMB)

Ces modules sont retirés. Aucune référence à leurs agents (Léo, Aria, Murat, Wendy, Morgan, Carson, etc.) ne doit subsister.
