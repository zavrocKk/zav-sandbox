# Annexe Datadog — logs, métriques, APM

> Annexe de [`observability-triage`](../SKILL.md). La méthode vit dans la skill ;
> ici, seulement la syntaxe. Noms de services/tags = placeholders à adapter.

## Étape 2 — golden signals

```text
# Logs Explorer — erreurs d'un service
service:<app> status:error
# affiner : service:<app> status:error @http.status_code:>=500

# Métriques — latence (Metrics Explorer ou notebook)
p95:trace.<framework>.request.duration{service:<app>}

# Trafic
sum:trace.<framework>.request.hits{service:<app>}.as_rate()

# Saturation (exemples usuels)
avg:system.cpu.user{service:<app>} / avg:jvm.heap_memory{service:<app>}
```

## Étape 3 — rétrécir (APM)

Service Catalog → service concerné → onglet **Traces** :

```text
# Erreurs par endpoint/resource
service:<app> status:error — group by resource_name

# Latence par endpoint : trier les resources par p99
```

## Étape 4 — borner

- Logs Explorer : requête d'erreur, trier par timestamp **ascendant** → premier
  événement anormal ; descendant → dernier.
- Monitors : historique d'état du monitor (`Status → History`) donne l'heure de
  bascule OK → ALERT — souvent le meilleur `first_seen`.

## Étape 5 — corréler une transaction

```text
# Une trace défaillante de bout en bout
trace_id:<id>            # dans Traces
@dd.trace_id:<id>        # retrouver les logs corrélés à la trace
```

La vue **Trace → Logs** connecte les deux si la corrélation logs/traces est
configurée.

## Export de la preuve

Trois éléments à noter systématiquement :

1. La **requête** (logs ou métrique) copiée telle quelle ;
2. Le **timeframe** effectif (les liens Datadog encodent la fenêtre — copier le
   permalien *et* écrire la fenêtre en UTC dans la preuve) ;
3. L'**extrait** (lignes de log anonymisées, ou valeurs de la métrique).

## Pièges Datadog

- Le timeframe de l'UI suit le fuseau du navigateur — convertir en UTC.
- Un permalien de dashboard sans la fenêtre figée (`Lock time`) montrera autre
  chose dans 3 semaines : figer la fenêtre avant de copier le lien.
- Les métriques sont agrégées après 15 jours (rollup) : exporter l'extrait tôt.
