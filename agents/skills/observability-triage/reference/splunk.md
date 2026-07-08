# Annexe Splunk — patterns SPL d'investigation

> Annexe de [`observability-triage`](../SKILL.md). La méthode (fenêtre → golden
> signals → rétrécissement → preuve) vit dans la skill ; ici, seulement la syntaxe.
> Les noms d'index/sourcetype sont des placeholders — à adapter à ton instance
> (fixtures dans `docs/_scratch/mvp-inputs/`).

## Étape 2 — golden signals

```spl
# Erreurs : taux par code, la base du triage
index=<app> earliest=-1h status>=500
| stats count by status, uri
| sort -count

# Latence : percentiles, jamais la moyenne seule
index=<app> earliest=-1h
| stats p50(duration) p95(duration) p99(duration) by uri

# Trafic : le volume a-t-il changé ?
index=<app> earliest=-4h
| timechart span=5m count
```

## Étape 3 — rétrécir

```spl
# Spike visuel : quand ça a commencé, par statut
index=<app> earliest=-4h
| timechart span=5m count by status

# Quel composant : répartition des erreurs par host/service
index=<app> earliest=-1h status>=500
| stats count by host, source
```

## Étape 4 — borner (premier/dernier événement anormal)

```spl
index=<app> earliest=-24h status>=500
| stats earliest(_time) as first_seen, latest(_time) as last_seen, count by status, uri
| convert ctime(first_seen), ctime(last_seen)
```

`first_seen` est la donnée clé : qu'est-ce qui a changé juste avant (déploiement,
config, dépendance) ?

## Étape 5 — corréler une transaction

```spl
# Suivre UNE requête défaillante de bout en bout
index=<app> request_id="<id>"
| sort _time
| table _time, host, source, status, message
```

## Export de la preuve

```spl
# Préférer une table stats agrégée à un dump brut
… | stats … | outputcsv   # ou copier le tableau de résultats
```

Toujours noter avec l'extrait : la requête complète + la fenêtre (`earliest`/`latest`
effectifs) en UTC.

## Pièges Splunk

- `earliest=-1h` sans `latest` = « jusqu'à maintenant » — le préciser dans la preuve.
- Les résultats sont bornés par défaut (10k événements en verbose) : un `stats`
  n'est pas affecté, un export brut oui.
- Heure locale de l'UI ≠ `_time` — convertir en UTC avant de coller dans un bilan.
