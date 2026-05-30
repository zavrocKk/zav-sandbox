# Politique de sécurité

## Versions supportées

Ce projet est actuellement en pré-release (v0.x). Les correctifs de sécurité
sont appliqués uniquement sur la branche `main`.

| Version | Supportée |
|---|---|
| 0.x (main) | ✅ |
| branches anciennes | ❌ |

## Signaler une vulnérabilité

**Ne pas signaler les vulnérabilités de sécurité via les Issues GitHub publiques.**

Pour signaler une vulnérabilité :

1. Ouvrir un [GitHub Security Advisory](https://github.com/zavrocKk/zav-sandbox/security/advisories/new)
   (canal privé — compte GitHub requis).
2. Décrire la vulnérabilité : nature, étapes de reproduction, impact potentiel.
3. Une réponse sera apportée dans les 5 jours ouvrés.

Nous suivons les principes de divulgation responsable : accusé de réception,
suivi de l'avancement, et crédit dans le correctif sauf si l'anonymat est souhaité.

## Périmètre

Ce projet est un **framework 100 % Markdown** sans serveur, sans dépendances
externes et sans traitement de données utilisateur. La surface d'attaque se
limite à :

- **Hooks d'agent** (`agents/hooks/`) — scripts shell qui s'exécutent avec les
  permissions VS Code. Ils sont **opt-in et désactivés par défaut**. À activer
  uniquement après révision des scripts.
- **Injection de prompt** — du contenu malveillant dans des fichiers lus par
  l'agent IA pourrait tenter de contourner les instructions du framework.

## Principes de conception sécurisée

- Aucun secret en clair — uniquement `<REDACTED>` ou références à un coffre.
- Les commandes destructives requièrent une confirmation explicite de l'utilisateur
  (appliqué via le hook `security-guard` quand il est activé).
- Tous les hooks d'agent sont des inspecteurs en lecture seule — ils n'exécutent
  jamais les commandes qu'ils analysent.
- Les skills/ressources externes nécessitent une autorisation explicite de
  l'utilisateur avant tout accès.
- Le framework lui-même ne contient aucun identifiant, clé API ou donnée de production.
