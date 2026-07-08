# Annexe Kubernetes / EKS — kubectl et k9s

> Annexe de [`observability-triage`](../SKILL.md). La méthode vit dans la skill ;
> ici, seulement la syntaxe. **k9s est l'outil de navigation, kubectl est la
> preuve** : une preuve re-exécutable cite la commande kubectl, pas la vue k9s.

## Pré-requis de session

```text
<cloudlogin / aws sso login>                     # session SSO active
aws eks update-kubeconfig --name <cluster> --region <region>
```

## Étape 2 — golden signals (état des pods)

```text
kubectl get pods -n <ns> -l app=<app> -o wide     # k9s : ':pods' puis '/<app>'
```

Colonnes qui parlent : **RESTARTS** (boucle ?) et **STATUS**. États à connaître :

| STATUS | Signification | Premier réflexe |
|---|---|---|
| `CrashLoopBackOff` | Le conteneur redémarre en boucle | Logs du conteneur **précédent** (`--previous`) |
| `OOMKilled` | Tué par manque mémoire | `describe` → Last State + limites mémoire |
| `ImagePullBackOff` | Image introuvable/refusée | `describe` → Events (registry, tag, droits) |
| `Pending` | Non schedulé | `describe` → Events (ressources, taints, PVC) |
| `Evicted` | Éjecté (pression node) | `kubectl get events` côté node |

## Étape 3 — rétrécir

```text
# Les événements récents du namespace, dans l'ordre (le tri par défaut est trompeur)
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -30      # k9s : ':events'

# Le pourquoi du dernier crash : Last State (raison + exit code) et Events
kubectl describe pod <pod> -n <ns>

# Les logs d'AVANT le crash (les logs courants = le nouveau conteneur)
kubectl logs <pod> -n <ns> --previous                # k9s : 'p' dans la vue logs
```

## Étape 4 — borner

```text
# Heure exacte du dernier crash
kubectl get pod <pod> -n <ns> \
  -o jsonpath='{.status.containerStatuses[0].lastState.terminated.finishedAt}'

# Qu'est-ce qui a changé juste avant ?
kubectl rollout history deployment/<app> -n <ns>
```

Croiser avec l'annexe [`aws-cloudwatch.md`](aws-cloudwatch.md) (Container Insights
si actif) pour les métriques node/pod dans la même fenêtre.

## Étape 5 — corréler / saturation

```text
kubectl logs -n <ns> -l app=<app> --since=30m | grep "<request_id>"
kubectl top pods -n <ns>                             # saturation CPU/mémoire ; k9s : ':pulses'
```

## Export de la preuve

- Citer la **commande kubectl exacte** + la fenêtre (`--since=…`) + l'extrait anonymisé.
- Un `describe` complet est du bruit : n'extraire que **Last State** et les
  **Events** pertinents (6 lignes utiles sur 150).
- Rédiger noms de cluster/comptes si sensibles (`<REDACTED>`).

## Pièges Kubernetes

- `OOMKilled` n'apparaît **pas** dans les logs — seulement dans Last State du `describe`.
- Oublier `--previous` après un CrashLoop = lire les logs du mauvais conteneur.
- `kubectl get events` sans `--sort-by=.lastTimestamp` mélange l'ordre.
- k9s affiche des âges **relatifs** (« 5m ») — convertir en timestamp UTC avant de
  citer dans une preuve.
- Une session SSO expirée produit des erreurs d'auth déguisées en erreurs cluster —
  vérifier le pré-requis avant de conclure.
