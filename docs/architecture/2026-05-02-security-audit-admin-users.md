---
type: security-audit
status: open
created: 2026-05-02
audit_scope: /admin/users endpoint
severity: critique
reporter: orchestrator / Security persona
---

# Audit Sécurité — Endpoint `/admin/users` non authentifié

---

## Résumé exécutif

L'endpoint `GET /admin/users` de l'API e-commerce est accessible sans aucune authentification ni autorisation. N'importe quel acteur externe peut exfiltrer l'intégralité de la base utilisateurs (PII, rôles, potentiellement hashes de mots de passe). CVSS v3.1 : **9.8 (Critique)**. Déclaration CNIL potentiellement requise si des données ont été consultées. Correction requise en urgence.

---

## Périmètre de l'audit

- **Endpoint audité** : `GET /admin/users`
- **Surface concernée** : toute la route `/admin/**` (par extension probable)
- **Données exposées** : PII utilisateurs (emails, noms, adresses), rôles, données de compte
- **Conformité** : RGPD Art. 32 (sécurité du traitement), Art. 33 (notification de violation)

---

## Vulnérabilités identifiées

| # | Catégorie OWASP / CWE | Description | CVSS v3.1 | Priorité |
|---|---|---|---|---|
| V1 | **A01:2021 — Broken Access Control** / CWE-862 | Endpoint admin sans authentification | **9.8** | 🔴 Critique |
| V2 | **A02:2021 — Cryptographic Failures** / CWE-200 | PII retournées en clair sans vérification de canal | 8.5 | 🔴 Haute |
| V3 | **A04:2021 — Insecure Design** / CWE-284 | Absence de couche RBAC sur toute la surface admin | 7.5 | 🟠 Haute |
| V4 | **A09:2021 — Security Logging Failures** / CWE-778 | Impossibilité de tracer les accès (non-répudiation) | 5.3 | 🟡 Moyen |

### Détail V1 — Broken Access Control (Critique)

**Vecteur d'attaque** : réseau, aucune interaction utilisateur requise.

**Exploit minimal** :
```bash
curl https://api.monshop.com/admin/users
# → HTTP 200, liste complète des utilisateurs
```

**Impact** :
- Exfiltration de toute la base clients (credential stuffing, phishing ciblé, revente)
- Identification des comptes administrateurs pour attaques ciblées
- Violation RGPD Art. 32 — notification CNIL obligatoire si exploitation avérée (72h)

---

## Scénarios d'attaque

### Scénario 1 — Mass enumeration automatisée
```
Attaquant → GET /admin/users?page=1 → 200 OK
Attaquant → GET /admin/users?page=2 → 200 OK
... boucle jusqu'à page N
→ Exfiltration complète en < 5 min
```

### Scénario 2 — Privilege escalation assistée
La réponse contenant les rôles, l'attaquant identifie les comptes `role=admin` pour des attaques de credential stuffing ou de réinitialisation de mot de passe ciblées.

### Scénario 3 — Surveillance passive (insider / log leak)
Sans authentification, les logs de l'API ne peuvent pas attribuer les accès à un utilisateur identifié — l'audit trail est inexploitable.

---

## Corrections requises

### Correction immédiate (Priorité 1 — appliquer dans les heures)

Ajouter un middleware d'authentification JWT + contrôle de rôle sur tous les endpoints `/admin/**`.

**Node.js / Express :**
```js
// Middleware authenticate — vérifie la présence et validité du JWT
function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Authentication required' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}

// Middleware requireRole — contrôle RBAC
function requireRole(...roles) {
  return (req, res, next) => {
    if (!roles.includes(req.user?.role))
      return res.status(403).json({ error: 'Insufficient privileges' });
    next();
  };
}

// Application sur la route
router.get('/admin/users', authenticate, requireRole('admin'), async (req, res) => {
  const users = await UserService.findAll();
  res.json(users.map(sanitizeUser)); // filtrer champs sensibles
});
```

**Python / FastAPI :**
```python
@router.get("/admin/users")
async def list_users(current_user=Depends(get_current_admin_user)):
    return await user_service.get_all_sanitized()
```

**Spring Boot :**
```java
.requestMatchers("/admin/**").hasRole("ADMIN")
```

### Sanitisation de la réponse (Priorité 1)

Ne jamais retourner : `password_hash`, `reset_token`, `payment_method_raw`, secrets internes.

```js
function sanitizeUser({ password_hash, reset_token, payment_method_raw, ...safe }) {
  return safe;
}
```

### Tests de non-régression à ajouter (Priorité 1)

| Cas de test | Expected |
|---|---|
| Requête sans token | HTTP 401 |
| Token utilisateur (role=user) | HTTP 403 |
| Token expiré | HTTP 401 |
| Token admin valide | HTTP 200, champs sensibles absents |

### Correction structurelle — API Gateway (Priorité 2 — Q3)

Centraliser l'authentification, le rate limiting et le logging sur une API Gateway (Kong, AWS API Gateway, NGINX+) devant toute la surface admin. Voir ADR [docs/decisions/0001-auth-strategy-admin-api.md](../decisions/0001-auth-strategy-admin-api.md).

---

## Automatisation CI/CD

| Outil | Règle | Quand |
|---|---|---|
| `semgrep --config=p/owasp-top-ten` | Détection routes sans middleware auth | PR gate |
| `OWASP ZAP` (`zap-cli active-scan`) | Fuzz endpoints non protégés | Pipeline nightly |
| Tests d'intégration 401/403 | Assert sur chaque endpoint admin | Chaque PR |

---

## Actions de remédiation

| # | Action | Owner | Échéance | Statut |
|---|---|---|---|---|
| 1 | Ajouter middleware `authenticate` + `requireRole('admin')` sur `/admin/**` | Developer | **Immédiat** | À faire |
| 2 | Ajouter sanitisation de la réponse (exclure PII sensibles) | Developer | Immédiat | À faire |
| 3 | Ajouter tests 401/403/token-expiré sur tous les endpoints admin | QA / Developer | J+1 | À faire |
| 4 | Activer logging des accès admin avec user ID dans les logs | DevOps | J+2 | À faire |
| 5 | Stocker `JWT_SECRET` dans un vault (Vault, AWS SM, Azure KV) | DevOps | J+3 | À faire |
| 6 | Évaluer et planifier migration vers API Gateway | Architect | Q3 2026 | À planifier |
| 7 | Vérifier si exploitation passée (logs, SIEM) — décision CNIL | Security / DPO | Immédiat | À faire |

---

## Analyse RGPD

- **Art. 32** : mesures techniques insuffisantes → violation caractérisée
- **Art. 33** : si des données ont été consultées sans autorisation → notification CNIL sous 72h obligatoire
- **Recommandation** : auditer les logs d'accès immédiatement pour détecter toute consultation suspecte de cet endpoint

---

## Annexes

- [ADR-0001 — Stratégie d'auth admin](../decisions/0001-auth-strategy-admin-api.md)
- [OWASP — A01:2021 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [CWE-862 — Missing Authorization](https://cwe.mitre.org/data/definitions/862.html)
- [RGPD Art. 32-33](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4)
