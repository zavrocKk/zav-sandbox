# Annexe AWS Session — se connecter avant d'investiguer

> Annexe de [`observability-triage`](../SKILL.md). Pré-requis commun des annexes
> [`aws-cloudwatch.md`](aws-cloudwatch.md), [`kubernetes-eks.md`](kubernetes-eks.md)
> et [`aws-batch.md`](aws-batch.md) : **aucune investigation ne commence sans une
> session vérifiée** — une session expirée ou le mauvais profil produit des
> conclusions fausses avec assurance.

## Setup une fois — profil SSO

```text
aws configure sso
#  SSO start URL : <https://<org>.awsapps.com/start>
#  SSO region    : <région du SSO>
#  → choisir compte + rôle → nommer le profil (ex. <app>-prod-readonly)
```

Le profil atterrit dans `~/.aws/config`. Convention utile : **un profil par
compte × rôle**, nommé `<app>-<env>-<rôle>` — on sait toujours où on est.

```text
<!-- À remplir après fixtures (wrapper d'entreprise) :
Le wrapper interne (« cloudlogin ») génère-t-il les profils ~/.aws/config ?
Commande exacte, durée de session, comptes couverts : <…>
Note : « Skyhook cloud-login » est une GitHub Action CI (OIDC) — pas l'outil humain.
-->
```

## Chaque session d'investigation — la règle binaire

```text
aws sso login --profile <profil>
aws sts get-caller-identity --profile <profil>
```

**Toute investigation commence par un `get-caller-identity` réussi** dont le
compte et le rôle correspondent à l'environnement de l'incident. Pas de
vérification = pas d'investigation — c'est le « quel patient ? » du chirurgien.

Ensuite, selon la cible :

```text
export AWS_PROFILE=<profil>                     # ou --profile sur chaque commande
aws eks update-kubeconfig --name <cluster> --region <région> --profile <profil>   # si EKS
```

## Règles de preuve spécifiques AWS

- Chaque commande citée en preuve porte sa **région explicite** (`--region`) —
  la région implicite du profil est un piège de reproduction.
- La preuve mentionne le **profil/rôle utilisé** (compte rédigé `<REDACTED>`) :
  une preuve prise avec le mauvais rôle peut être incomplète (droits de lecture).

## Pièges de session

- **Session expirée** (durée typique 8-12 h) : les erreurs `ExpiredToken` /
  `Unable to locate credentials` se déguisent parfois en « ressource introuvable »
  — re-login avant de conclure qu'une ressource n'existe pas.
- **Mauvais profil par défaut** : `AWS_PROFILE` hérité d'un shell précédent →
  on investigue le mauvais compte. Le `get-caller-identity` d'ouverture attrape ça.
- **Multi-comptes** : prod et staging sont des comptes différents — un symptôme
  « introuvable » est souvent juste le mauvais compte.
- Le SSO ouvre un navigateur : sur un poste sans navigateur par défaut configuré,
  utiliser l'URL + code affichés dans le terminal.
