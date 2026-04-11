# Security Policy — zav-sandbox

## Versions supportées

| Version | Supportée |
|---------|-----------|
| 2.x     | ✅        |
| < 2.0   | ❌        |

## Signaler une vulnérabilité

Si vous découvrez une vulnérabilité de sécurité dans ce projet :

1. **NE PAS** ouvrir une issue publique
2. Contacter le mainteneur via les canaux privés GitHub (Security Advisories)
3. Inclure : description du problème, étapes de reproduction, impact potentiel

## Pratiques de sécurité

- Aucun secret, token ou credential n'est hardcodé dans le code source
- Les dépendances sont auditées via `pip-audit` et Dependabot
- Le scan de sécurité (`bandit`) est exécuté dans la CI sur chaque PR
- Les inputs utilisateur sont validés aux frontières CLI et MCP
- Le framework suit les principes OWASP Top 10
