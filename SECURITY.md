# Security Policy  zav-sandbox

## Versions supportes

| Version | Supporte |
|---------|-----------|
| 2.x     |         |
| < 2.0   |         |

## Signaler une vulnrabilit

Si vous dcouvrez une vulnrabilit de scurit dans ce projet :

1. **NE PAS** ouvrir une issue publique
2. Contacter le mainteneur via les canaux privs GitHub (Security Advisories)
3. Inclure : description du problme, tapes de reproduction, impact potentiel

## Pratiques de scurit

- Aucun secret, token ou credential n'est hardcod dans le code source
- Les dpndances sont audites via `pip-audit` et Dependabot
- Le scan de scurit (`bandit`) est excut dans la CI sur chaque PR
- Les inputs utilisateur sont valids aux frontires CLI et MCP
- Le framework suit les principes OWASP Top 10
