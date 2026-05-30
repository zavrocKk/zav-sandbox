# Checklist — Pré-PR (garde-fous avant d'ouvrir une Pull Request)

> **But** : éviter les conflits causés par des commits sans PR, des branches qui
> traînent, ou des fichiers de pilotage non à jour. À dérouler **avant chaque PR**.
> Invocable par l'orchestrateur via `/pre-pr`.

## 1. Commande de vérification (lecture seule, déterministe)

Lancer ce bloc et lire la sortie — aucune commande n'écrit ni ne pousse :

```pwsh
git status --short              # working tree propre ? rien d'oublié ?
git branch --no-merged main     # branches non mergées qui traînent ?
gh pr list --state open         # PR déjà ouvertes ?
```

> 💡 Coût quasi nul en tokens : l'agent **lit** la sortie au lieu de raisonner.
> Pas de script à maintenir, pas de souci ExecutionPolicy / EOL.

## 2. Points à valider (binaire — tout doit être ✅)

| # | Contrôle | Source | Règle |
|---|----------|--------|-------|
| 1 | Working tree propre (rien de non commité d'oublié) | `git status --short` | Vide ou volontaire |
| 2 | Pas de branche non mergée orpheline pour ce travail | `git branch --no-merged main` | Aucune doublon du fil courant |
| 3 | Pas de PR déjà ouverte pour le **même** travail | `gh pr list --state open` | Aucune — **sauf** PR `release-please` (légitime, automatisée) |
| 4 | `ROADMAP.md` reflète l'état réel (phase/statut à jour) | revue manuelle | À jour |
| 5 | `README.md` (arbre du dépôt, fonctionnalités) à jour si structure modifiée | revue manuelle | À jour |
| 6 | `VISION.md` cohérent (modifié seulement si la stratégie change) | revue manuelle | À jour |
| 7 | `IDEAS.md` — idées émergées en session consignées | revue manuelle | À jour |
| 8 | `CHANGELOG.md` — **ne pas éditer à la main** : alimenté par `release-please` via commits conventionnels | commits | Commits `feat:`/`fix:`/`chore:`… corrects |

## 3. Garde-fous

- ⛔ **PR `release-please`** (ex. `chore(main): release X.Y.Z`, branche
  `release-please--branches--main`) = **automatisée et légitime**. Ne JAMAIS la
  traiter comme un conflit ni la fermer.
- ⛔ Ne JAMAIS contourner le hook `pre-push` ni utiliser `--no-verify` (cf.
  workflow git).
- Si un contrôle 1-3 échoue → **stopper**, signaler à l'utilisateur, proposer de
  nettoyer (merger/supprimer la branche, finir le commit) **avant** d'ouvrir la PR.
- Si un contrôle 4-7 échoue → mettre le fichier à jour dans la **même** PR.

## 4. Résultat attendu

Tous les contrôles ✅ → ouvrir la PR. Sinon → corriger d'abord. Une PR = un fil de
travail cohérent, branche propre, fichiers de pilotage synchronisés.
