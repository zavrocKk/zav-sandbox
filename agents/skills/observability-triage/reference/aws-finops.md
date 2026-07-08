# Annexe AWS FinOps — investiguer une anomalie de coût

> Annexe de [`observability-triage`](../SKILL.md). Pré-requis : session vérifiée
> ([`aws-session.md`](aws-session.md)) avec un rôle qui voit Cost Explorer.
> Même méthode que le triage d'incident — le « signal » est une facture, pas une
> alerte — et même règle de preuve : **paramètres exacts + période, sinon non
> re-exécutable**.

## La méthode (adaptation du rétrécissement)

1. **Cadrer la période et comparer** : le mois anormal vs le mois précédent
   (ou jour vs jour pour un spike récent). Sans comparaison, pas d'anomalie —
   juste un chiffre.
2. **Rétrécir par dimensions**, dans cet ordre : **service** → **région** →
   **usage type** → **compte lié / tag**. À chaque niveau, noter le delta.
3. **Identifier le driver** : usage qui monte (volume) ou configuration qui a
   changé (prix unitaire, type d'instance, classe de stockage) ?
4. **Croiser avec l'activité** : déploiement, nouvelle feature, backfill,
   oubli (ressource de test jamais éteinte) — le `first_seen` du coût rejoint
   souvent un événement Git/change.

## Requêtes

```text
# Coût par service, quotidien, sur la fenêtre
aws ce get-cost-and-usage \
  --time-period Start=2026-06-01,End=2026-07-01 \
  --granularity DAILY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --profile <profil>

# Puis rétrécir : Key=USAGE_TYPE (dans le service suspect), Key=LINKED_ACCOUNT,
# ou Type=TAG,Key=<tag-clé>
```

Console : Cost Explorer permet le même rétrécissement — la preuve cite alors
**période + granularité + group-by + filtres** (un screenshot seul n'est pas
re-exécutable).

## Coupables récurrents (à vérifier avant d'accuser l'app)

- **NAT Gateway data processing** — le classique silencieux des archis privées.
- **CloudWatch Logs ingestion** — un log level passé en DEBUG se paie.
- **EBS orphelins et snapshots** — volumes détachés jamais supprimés.
- **Instances/environnements de test** tournant la nuit et le week-end.
- **DynamoDB on-demand** sous un trafic nouveau, **transferts inter-AZ/région**,
  **S3 requests** (pas le stockage — les appels).

## Pièges FinOps

- Les données Cost Explorer ont **~24-48 h de retard** — un spike d'aujourd'hui
  n'y est pas encore.
- `UnblendedCost` vs `AmortizedCost` : avec RI/Savings Plans, l'unblended
  attribue mal — préciser la métrique utilisée dans la preuve.
- Un coût sans tag n'appartient pas à « personne » : le rétrécissement par
  usage type/région le localise quand même.
- Comparer un mois de 28 jours à un mois de 31 = fausse baisse — comparer en
  granularité DAILY ou normaliser.
