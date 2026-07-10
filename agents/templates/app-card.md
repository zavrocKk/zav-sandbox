---
type: application
title: <Nom officiel de l'application>
description: <Une ligne — ce que fait l'app, pour qui>
tags: [<stack>, <domaine>]
timestamp: <YYYY-MM-DD>       # dernière mise à jour de la fiche
aliases: [<surnom d'équipe>, <code projet JIRA>, <nom de service/endpoint>]
verified: <YYYY-MM-DD>        # dernière vérification humaine du contenu
criticality: <P1 | P2 | P3>
---

> **≤ 100 lignes** (hors front-matter). Règle « pointeur > recopie » : les détails
> vivent dans les documents liés, la fiche donne la carte, pas le territoire.
> `verified` > 90 jours → l'orchestrateur le déclare au PLAN avant d'utiliser la fiche.

## Résumé & architecture

<2-5 lignes : rôle, consommateurs, criticité réelle>

```mermaid
flowchart LR
  <diagramme minimal : composants principaux et flux>
```

## Dépendances

- <service/API amont ou aval> — <nature du lien>

## Environnements & comptes

| Env | Compte/cluster (rédigé si sensible) | Région | Observabilité |
|---|---|---|---|
| prod | `<REDACTED>` | | <lien dashboard / index Splunk> |

## Quirks connus

- <comportement piégeux, faux positifs d'alertes, redémarrages rituels…>

## Liens (pointeurs, pas de recopie)

- Incidents : <`docs/incidents/…`>
- ADRs : <`docs/decisions/…`>
- Runbook : <`docs/runbooks/…` ou Confluence>
