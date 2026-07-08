---
type: bilan
destinataire: <équipe ou développeur>
system: <application / service concerné>
status: draft            # draft | approved | handed-off | closed
date: <YYYY-MM-DD>
verified: —              # date de la vérification phase 6, sinon —
---

# Bilan — <titre court>

> Produit par le workflow [`bilan-remediation`](../workflows/bilan-remediation.md).
> Le statut du front-matter est la source de vérité du cycle de vie
> (`draft → approved → handed-off → closed`).

## Résumé exécutif

<5 lignes max : le problème, l'impact, l'action attendue du destinataire>

## Contexte

<système, période observée, symptôme rapporté, qui a signalé, référence ticket>

## Findings

### F1 — <titre du finding>

- **Signal** : <ce qui a été observé — métrique, log, ticket, comportement>
- **Hypothèse** : <l'explication candidate, formulée avant vérification>
- **Preuve** : <ce qui confirme ou infirme — fichier:ligne, timestamp de log, requête, mesure>
- **Conclusion** : <la cause établie, en une phrase>
- **Action recommandée** : <quoi faire, où — assez précis pour ouvrir un ticket>
- **Critère de vérification** : <observable binaire : comment on saura que c'est corrigé>

### F2 — <titre>

<même structure — les 6 champs sont obligatoires pour chaque finding>

## Hors périmètre / incertitudes

<ce qui n'a pas été analysé, hypothèses restantes, données manquantes>

## Annexes

- Inputs bruts : `docs/_scratch/inputs/<fichier>` (non committés)
- <liens : dashboard, ticket, PR, doc>

## Vérification (phase 6 — remplie en session ultérieure, ne pas pré-remplir)

| F# | Critère | Résultat (✓/✗) | Preuve | Date |
|----|---------|----------------|--------|------|
| F1 | <copié depuis le finding> | | | |
