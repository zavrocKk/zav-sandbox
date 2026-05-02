# Runbook — Debug routing nginx pour routes API

**Date** : 2026-05-02
**Contexte** : Routes API mal redirigées derrière un reverse proxy nginx.

---

## 1. Vérification syntaxe et config résolue

```bash
nginx -t          # test syntaxe uniquement
nginx -T          # dump config complète (tous les includes résolus)
```

En cas d'erreur de syntaxe, nginx affiche le fichier et la ligne. Corriger avant de continuer.

---

## 2. Localiser le bloc `location` responsable

```bash
grep -rn "location\|proxy_pass\|rewrite\|return" /etc/nginx/conf.d/ /etc/nginx/sites-enabled/
```

> **Règle nginx** : le bloc `location` **le plus spécifique** (préfixe le plus long, ou regex) est appliqué. Un bloc générique (`location /`) peut masquer un bloc API si mal ordonné.

---

## 3. Tester la route en live

```bash
# Voir le code HTTP et les headers de réponse
curl -v http://localhost/api/ta-route

# Suivre les redirections
curl -Lv http://localhost/api/ta-route
```

Codes HTTP à interpréter :

| Code | Cause fréquente |
|---|---|
| 301 / 302 en boucle | `return` ou `rewrite` mal scopé |
| 404 | Mauvais préfixe transmis à l'upstream (voir §5) |
| 502 Bad Gateway | Upstream non joignable ou crash |
| 400 Bad Request | Header `Host` manquant ou incorrect |

---

## 4. Lire les logs

```bash
tail -f /var/log/nginx/error.log /var/log/nginx/access.log | grep "/api/"
```

### Activer le debug logging temporairement

```nginx
# Dans nginx.conf ou le vhost, section http ou server
error_log /var/log/nginx/debug.log debug;
```

```bash
nginx -s reload
# ... reproduire le problème ...
tail -f /var/log/nginx/debug.log
```

> ⚠️ Remettre `error_log ... warn;` après le diagnostic. Le mode debug est très verbeux.

---

## 5. Piège principal : `proxy_pass` avec ou sans `/` final

| Config | Comportement | Exemple |
|---|---|---|
| `proxy_pass http://backend/;` | **Strip le préfixe** du `location` | `/api/foo` → `/foo` |
| `proxy_pass http://backend;` | **Conserve le préfixe** | `/api/foo` → `/api/foo` |

Ces deux configs sont **sémantiquement différentes**. C'est la cause n°1 de mauvais routing.

---

## 6. Template correct pour une API

```nginx
location /api/ {
    proxy_pass         http://127.0.0.1:3000/;
    proxy_set_header   Host              $host;
    proxy_set_header   X-Real-IP         $remote_addr;
    proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header   Connection        "";
}
```

---

## 7. Bypass nginx pour valider l'upstream

```bash
# Appeler l'app directement (sans passer par nginx)
curl -v http://127.0.0.1:<PORT_APP>/ta-route
```

- Si ça répond correctement ici **mais pas via nginx** → problème dans le bloc `location` / `proxy_pass`
- Si ça ne répond pas non plus → problème côté application

---

## 8. Checklist de résolution rapide

- [ ] `nginx -t` passe sans erreur
- [ ] Le bon bloc `location` matche (vérifier avec `nginx -T | grep -A5 "location /api"`)
- [ ] `proxy_pass` avec ou sans `/` selon le comportement voulu
- [ ] `proxy_set_header Host $host;` présent
- [ ] Pas de `return` ou `rewrite` qui intercepte avant le bon bloc
- [ ] `error_log` remis en `warn` après debug
