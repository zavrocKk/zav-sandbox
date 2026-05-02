---
type: adr
number: "0001"
status: proposed
date: 2026-05-02
deciders: [Security, Architect, Developer]
tags: [auth, security, admin, jwt, api-gateway]
---

# ADR-0001 — Stratégie d'authentification pour les endpoints admin

> Format : Michael Nygard. Une décision = un fichier, immuable une fois `accepted`.

---

## Statut

**État actuel** : proposed
**Décidé le** : 2026-05-02
**Décideurs** : Security, Architect, Developer

---

## Contexte

L'endpoint `GET /admin/users` est accessible sans authentification, exposant toute la base utilisateurs (PII) à n'importe quel acteur externe. CVSS v3.1 : 9.8 (Critique). L'ensemble de la surface `/admin/**` est concernée.

Contraintes :
- Correction urgente requise (heures, pas semaines)
- Pas d'infrastructure API Gateway en place actuellement
- Secret management non formalisé (secrets potentiellement en dur ou en `.env`)
- Conformité RGPD Art. 32 à rétablir immédiatement

---

## Décision

Nous allons implémenter un middleware JWT stateless (`authenticate` + `requireRole('admin')`) sur tous les endpoints `/admin/**` comme mesure immédiate. Nous planifions la migration vers une API Gateway (Option B) en Q3 2026 pour centraliser auth, rate limiting et logging.

---

## Alternatives considérées

### Option A — JWT stateless dans l'application (retenu court terme)
- **Description** : middleware vérifiant le JWT sur chaque route admin, avec claim `role=admin`
- **Avantages** : déployable en heures, sans dépendance infra, standard industry
- **Inconvénients** : révocation de token manuelle (blacklist requise), `JWT_SECRET` à gérer en vault
- **Pourquoi retenu** : urgence de la situation — c'est la mesure la plus rapide à déployer

### Option B — API Gateway (Kong / AWS API GW / NGINX+)
- **Description** : gateway devant l'API qui centralise l'auth, le rate limiting et le logging
- **Avantages** : zero-trust par design, logs centralisés, découplage auth/app
- **Inconvénients** : coût opérationnel, latence additionnelle, migration non triviale
- **Pourquoi différé** : délai d'implémentation incompatible avec l'urgence immédiate

### Option C — Identity Provider (Keycloak / Auth0 / Cognito)
- **Description** : délégation complète de l'auth à un IdP OAuth2/OIDC
- **Avantages** : MFA natif, audit trail complet, standard enterprise
- **Inconvénients** : infrastructure lourde, courbe d'apprentissage, coût
- **Pourquoi rejetée** : over-engineering pour la taille actuelle du projet ; à réévaluer si l'équipe grandit

---

## Conséquences

### Positives
- Surface d'attaque admin fermée immédiatement
- Conformité RGPD Art. 32 rétablie
- Audit trail activé (user ID dans les logs une fois auth en place)

### Négatives
- `JWT_SECRET` est un nouveau secret à gérer (doit aller en vault — AWS SM, Azure KV, HashiCorp Vault)
- Révocation de tokens avant expiration nécessite une blacklist en cache (Redis)

### Neutres / À surveiller
- Durée d'expiration du token admin : recommandé 15 min avec refresh token
- Migration vers Option B à budgétiser pour Q3 2026
- Si exploitation passée avérée → notification CNIL obligatoire (72h, Art. 33 RGPD)

---

## Implémentation

1. **Imm\u00e9diat** : ajouter `authenticate` + `requireRole('admin')` sur `/admin/**`
2. **J+1** : déplacer `JWT_SECRET` vers un vault (ne jamais committer en dur)
3. **J+2** : activer logging des accès admin avec `req.user.id`
4. **J+3** : ajouter tests d'intégration 401/403 sur tous les endpoints admin
5. **Q3 2026** : évaluer et déployer API Gateway — superseder cet ADR

---

## Références

- [Rapport d'audit sécurité](../architecture/2026-05-02-security-audit-admin-users.md)
- [OWASP A01:2021 — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [RGPD Art. 32-33](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4)
