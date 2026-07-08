---
name: observability-triage
version: "1.0.0"
description: Méthode d'extraction d'évidence depuis les outils d'observabilité — Splunk, Datadog, AWS CloudWatch, Kubernetes/EKS (annexes reference/) — pour étayer un diagnostic ou un bilan. Golden signals, rétrécissement temps → service → classe d'erreur, règle de preuve re-exécutable (requête exacte + fenêtre + extrait anonymisé). À utiliser en phase Diagnostic d'un incident ou en phase Analyse d'un bilan, quand il faut transformer « ça a l'air cassé » en évidence citable.
---

# Observability Triage — de l'alerte à la preuve

Méthode **outil-agnostique** pour extraire de l'évidence exploitable. La syntaxe
par outil vit dans les annexes : [`reference/splunk.md`](reference/splunk.md),
[`reference/datadog.md`](reference/datadog.md),
[`reference/aws-cloudwatch.md`](reference/aws-cloudwatch.md),
[`reference/kubernetes-eks.md`](reference/kubernetes-eks.md) (kubectl/k9s).
Ajouter un outil = ajouter une annexe, pas une skill.

Skill de **méthode** : elle guide ce que l'analyste exécute dans ses outils et
comment il en documente le résultat. Aucune connexion, aucun appel API — les
exports vont dans `docs/_scratch/inputs/` (git-ignoré), anonymisés.

## La méthode (dans l'ordre — ne pas sauter d'étape)

1. **Cadrer la fenêtre temporelle** depuis le symptôme : début du signal anormal
   − 30 min, jusqu'à maintenant. Élargir seulement si la fenêtre est vide.
   Chercher la cause avant d'avoir cadré la fenêtre = noyade garantie.
2. **Golden signals d'abord** — dans cet ordre : **erreurs** (taux, nouveaux
   codes), **latence** (p95/p99, pas la moyenne), **trafic** (volume anormal ?),
   **saturation** (CPU/mémoire/connexions/quotas).
3. **Rétrécir** : fenêtre temporelle → service/composant → classe d'erreur.
   À chaque étape, une requête, un constat noté.
4. **Borner l'anomalie** : premier événement anormal, dernier événement anormal.
   Le « premier » est la matière du diagnostic (qu'est-ce qui a changé juste avant ?).
5. **Corréler par identifiant** (request id, trace id, correlation id) : suivre
   UNE transaction défaillante de bout en bout vaut mieux que 1 000 lignes agrégées.
6. **Exporter la preuve** (voir règle ci-dessous) et s'arrêter : l'interprétation
   appartient à la phase d'analyse (bilan, RCA), pas au triage.

## Règle de preuve (binaire)

Une preuve est **re-exécutable** ou elle est non conforme. Chaque preuve citée
dans un bilan/post-mortem contient les 3 éléments :

```text
Requête  : <la requête exacte, copiable telle quelle>
Fenêtre  : <début — fin, en UTC>
Extrait  : <2-10 lignes de résultat, anonymisées>
```

Un screenshot de dashboard sans la requête sous-jacente n'est **pas** une preuve :
personne ne peut le reproduire dans 3 semaines pour vérifier le fix.

## Discipline d'export

- Destination : `docs/_scratch/inputs/` (git-ignoré, jamais committé).
- **Anonymiser avant de coller** : PII, tokens, ARN/comptes complets, IP internes
  → `<REDACTED>` (règles sécurité du workspace).
- Timestamps en **UTC** — les fuseaux mélangés ont ruiné plus d'un diagnostic.
- Préférer un tableau `stats` agrégé à un dump brut : plus petit, plus lisible,
  moins de risque de fuite.

## Articulation avec le reste du framework

- Nourrit les champs **Signal** et **Preuve** des findings de
  [`bilan-remediation`](../../workflows/bilan-remediation.md) et la phase
  Diagnostic d'[`incident-response`](../../workflows/incident-response.md).
- L'interprétation causale des preuves → skill
  [`root-cause-analysis`](../root-cause-analysis/SKILL.md).

## Anti-patterns

- ❌ Chercher la cause avant d'avoir cadré la fenêtre temporelle.
- ❌ Conclure depuis un dashboard sans citer la requête (preuve non re-exécutable).
- ❌ Moyennes de latence (la moyenne cache les p99 — regarder les percentiles).
- ❌ Coller des logs bruts avec PII/secrets dans un fichier versionné.
- ❌ Continuer à requêter une fois la preuve obtenue (le triage borne, l'analyse explique).
