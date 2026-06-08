---
type: incident-report
status: draft  # draft | reviewed | finalized
created: YYYY-MM-DD
incident_date: YYYY-MM-DD
severity: # SEV1 (critique) | SEV2 (majeur) | SEV3 (mineur)
services_affected: []
duration_minutes:
---

# Incident — <titre court et descriptif>

<!-- Le titre doit décrire l'impact, pas la cause. Ex: "Latence 5xx sur /checkout" plutôt que "Bug dans le service paiement" -->

> **Style :** blameless. On critique des systèmes et des processus, jamais des personnes.

---

## Résumé exécutif

<!-- 3 lignes max. Quoi s'est passé, quand, quel impact utilisateur. -->

## Timeline

<!-- Heures en UTC. Format : HH:MM — événement. Inclure : détection, investigation, mitigation, résolution, communication. -->

| Heure (UTC) | Événement | Source |
|---|---|---|
| HH:MM | Détection initiale | Alerte Datadog / Rapport user / ... |
| HH:MM | Triage — DevOps prend l'appel | |
| HH:MM | Hypothèse retenue : `<…>` | `<log / métrique>` |
| HH:MM | Mitigation appliquée : `<…>` | `<commande / commit>` |
| HH:MM | Retour à la normale (SLI revert to green) | `<dashboard>` |

## Impact

<!-- Sois factuel et chiffré quand possible -->
- **Utilisateurs affectés** :
- **Requêtes échouées** :
- **Revenu impacté** :
- **SLA** :

## Cause racine

<!-- Distingue cause TECHNIQUE (le bug, la mauvaise config) et cause SYSTÉMIQUE (pourquoi le bug a pu atteindre la prod : test manquant, review insuffisante, monitoring aveugle, etc.). Les DEUX sont nécessaires. -->

### Cause technique

### Cause systémique

## Mitigation appliquée

<!-- Ce qui a été fait pour ramener le service. Inclure les commandes/actions précises. -->

## Ce qui a bien fonctionné

- `<…>`
- `<…>`

## Ce qui a moins bien fonctionné

- `<…>`
- `<…>`

## Action items

<!-- Chaque item = SMART (spécifique, mesurable, atteignable, réaliste, temporel). Owner et échéance OBLIGATOIRES. -->

| # | Action | Owner | Échéance | Type | Statut |
|---|---|---|---|---|---|
| 1 | ... | ... | YYYY-MM-DD | Préventif / Détection / Mitigation | À faire |

## Leçons apprises

<!-- 1-3 leçons qui dépassent cet incident spécifique. Quoi appliquer ailleurs ? -->

## Annexes

<!-- Liens vers : runs CI, dashboards, traces, code source des changements impliqués, autres incidents similaires. -->

---
*Post-mortem blameless : on parle systèmes et processus, pas personnes.*
