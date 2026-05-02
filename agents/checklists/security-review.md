---
type: checklist
used_by: [security]
phase: code-review | infra-audit
---

# Checklist — Revue sécurité

À utiliser quand le 🔒 Security audite du code, une infra, ou une feature en design.

## 🔐 Secrets et credentials

- [ ] Aucun secret en clair dans le code (mots de passe, API keys, tokens)
- [ ] Aucun secret dans les logs ou messages d'erreur
- [ ] Aucun secret dans les URLs (paramètres, query strings)
- [ ] Secrets gérés via vault / secrets manager / variables d'env
- [ ] Rotation des secrets documentée
- [ ] `.env`, `*.key`, `*.pem` dans `.gitignore`

## 🛡️ AuthN / AuthZ

- [ ] Authentification requise sur tous les endpoints sensibles
- [ ] Autorisation vérifiée à chaque accès aux ressources (pas seulement à la connexion)
- [ ] Pas de privilèges par défaut excessifs
- [ ] Sessions : expiration, invalidation au logout, refresh sécurisé
- [ ] MFA disponible pour les comptes à privilège
- [ ] Politique de mot de passe (longueur, complexité, hash bcrypt/argon2)

## 💉 OWASP Top 10 — vérifications applicatives

- [ ] **Injection** (SQL, NoSQL, OS, LDAP) : requêtes paramétrées partout
- [ ] **Broken Access Control** : tests sur escalade horizontale et verticale
- [ ] **Cryptographic Failures** : TLS partout, pas de protocoles obsolètes
- [ ] **Insecure Design** : threat model fait pour les flux critiques
- [ ] **Security Misconfiguration** : headers sécurisés (CSP, HSTS, X-Frame-Options)
- [ ] **Vulnerable Components** : dépendances scannées (Snyk, Dependabot, npm audit)
- [ ] **Auth Failures** : pas d'enumeration des comptes, rate limiting auth
- [ ] **Software/Data Integrity** : signatures sur les artefacts critiques
- [ ] **Logging/Monitoring Failures** : événements sécurité loggés
- [ ] **SSRF** : whitelist des destinations sortantes, pas de fetch sur URL user

## 🌐 Données sensibles

- [ ] PII identifiée et inventoriée
- [ ] Chiffrement au repos (DB, backups, file storage)
- [ ] Chiffrement en transit (TLS 1.2+)
- [ ] Politique de rétention conforme RGPD / réglementations locales
- [ ] Logs : pas de PII en clair
- [ ] Backups : chiffrés, accès restreint, testés en restauration

## 🌩️ Infrastructure (si applicable)

- [ ] Network segmentation (VPC, security groups, firewalls)
- [ ] Principe du moindre privilège sur les rôles IAM
- [ ] Pas de buckets / DBs publics par défaut
- [ ] Containers : pas en root, image base à jour, image scan en CI
- [ ] Patching policy : OS, runtime, libs

## 📋 Output attendu

Pour chaque problème identifié :
- **Description** + **fichier:ligne** ou **ressource**
- **Sévérité** (Critical / High / Medium / Low — référence CVSS si applicable)
- **Mitigation recommandée** (concrète, pas "améliorer la sécurité")
- **Effort estimé** (S / M / L)
