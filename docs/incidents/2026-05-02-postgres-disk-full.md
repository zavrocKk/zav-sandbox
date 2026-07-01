---
type: incident-report
status: archived
created: 2026-05-02
incident_date: 2026-05-02
severity: SEV2
services_affected: [postgresql, api-backend]
duration_minutes: 30
---

# Incident — DB Postgres indisponible 30 min (disque plein)

> **Style :** blameless. On critique des systèmes et des processus, jamais des personnes.

---

## Résumé exécutif

Le 2026-05-02 entre 08:14 et 08:44 UTC, le volume disque hébergeant PostgreSQL a atteint 100% de capacité, rendant toute écriture impossible. L'ensemble des requêtes en écriture ont échoué pendant 30 minutes. La mitigation a consisté à libérer de l'espace manuellement (purge WAL + rotation logs) avant de redémarrer Postgres.

## Timeline

| Heure (UTC) | Événement | Source |
|---|---|---|
| 08:14 | Première alerte : erreurs `FATAL: No space left on device` dans les logs Postgres | Alerte monitoring / logs applicatifs |
| 08:17 | Triage — DevOps confirme : volume `/var/lib/postgresql` à 100% | `df -h` sur le serveur DB |
| 08:22 | Hypothèse retenue : accumulation de WAL non purgés + logs applicatifs non rotatés | `du -sh /var/lib/postgresql/*/pg_wal/` |
| 08:35 | Mitigation : suppression des WAL archivés obsolètes + rotation forcée des logs | `pg_archivecleanup`, `logrotate -f` |
| 08:41 | Espace libéré (~15 GB), redémarrage de Postgres | `systemctl restart postgresql` |
| 08:44 | Connexions rétablies, SLI reverts to green | Dashboard applicatif |

## Impact

- **Utilisateurs affectés** : tous les utilisateurs effectuant des opérations en écriture (créations, mises à jour, suppressions)
- **Requêtes échouées** : 100% des writes pendant 30 min — reads potentiellement dégradées selon saturation du pool de connexions
- **Revenu impacté** : <!-- TODO: à compléter avec les données de transactions échouées -->
- **SLA** : breach possible selon le SLA uptime contractuel (à vérifier)

## Cause racine

### Cause technique

Les fichiers WAL (Write-Ahead Logs) archivés n'ont pas été purgés depuis plusieurs semaines. Combinés à une rotation insuffisante des logs applicatifs, ils ont saturé le volume `/var/lib/postgresql` (capacité totale : <!-- TODO: à compléter avec la taille du volume -->).

### Cause systémique

- Aucune alerte de seuil sur l'occupation disque n'était configurée avant 100% (seuil d'alerte à 80% absent ou non fonctionnel).
- La politique de rétention des WAL archivés n'était pas documentée ni automatisée.
- Pas de test de capacité disque dans les checks de santé hebdomadaires.

## Mitigation appliquée

1. Identification de l'espace consommé :
   ```bash
   du -sh /var/lib/postgresql/*/pg_wal/
   du -sh /var/log/postgresql/
   ```
2. Purge des WAL archivés obsolètes :
   ```bash
   pg_archivecleanup /var/lib/postgresql/archive/ <dernier_WAL_valide>
   ```
3. Rotation forcée des logs :
   ```bash
   logrotate -f /etc/logrotate.d/postgresql
   ```
4. Redémarrage du service :
   ```bash
   systemctl restart postgresql
   systemctl status postgresql
   ```

## Ce qui a bien fonctionné

- Détection rapide grâce aux logs applicatifs qui exposaient clairement l'erreur `No space left on device`
- Triage efficace : cause identifiée en moins de 10 minutes
- Mitigation réversible et sans perte de données

## Ce qui a moins bien fonctionné

- Absence d'alerte proactive sur le taux d'occupation disque — détection réactive uniquement
- Politique de rétention WAL non documentée, ce qui a rallongé l'investigation
- Pas de runbook disponible : le diagnostic a reposé sur la mémoire de l'équipe

## Action items

| # | Action | Owner | Échéance | Type | Statut |
|---|---|---|---|---|---|
| 1 | Configurer une alerte monitoring sur occupation disque à 75% et 90% pour tous les volumes DB | DevOps | 2026-05-09 | Détection | À faire |
| 2 | Automatiser la purge des WAL archivés via `pg_archivecleanup` en cron quotidien | DevOps | 2026-05-09 | Préventif | À faire |
| 3 | Documenter la politique de rétention WAL et logs dans le wiki infra | DevOps | 2026-05-16 | Préventif | À faire |
| 4 | Créer un runbook dédié "Postgres disk full" dans `docs/runbooks/` | DevOps | 2026-05-16 | Mitigation | À faire |
| 5 | Ajouter un check de capacité disque dans les healthchecks hebdomadaires | DevOps | 2026-05-23 | Détection | À faire |

## Leçons apprises

- **Le monitoring réactif ne suffit pas** : une alerte à 80% d'occupation disque aurait donné 2-3 jours pour agir sans incident. Tout volume de base de données doit avoir un seuil d'alerte proactif.
- **Les politiques de rétention non automatisées sont une dette opérationnelle** : sans cron ou outil dédié (pgBackRest, Barman), l'accumulation WAL est inévitable sur le long terme.
- **Un runbook à portée de main réduit le MTTR** : ce post-mortem aurait duré 10 min de moins si un runbook "disk full" avait existé.

## Annexes

- <!-- TODO: à compléter avec le lien vers les logs Postgres de l'incident -->
- <!-- TODO: à compléter avec le lien vers le dashboard monitoring (période 08:00-09:00 UTC) -->
- <!-- TODO: à compléter avec le ticket de suivi des action items -->

---
*Post-mortem blameless : on parle systèmes et processus, pas personnes.*
