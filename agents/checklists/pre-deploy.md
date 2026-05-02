---
type: checklist
used_by: [devops, developer]
phase: pre-deployment
---

# Checklist — Avant un déploiement en production

À parcourir AVANT tout déploiement en prod, surtout pour les changements à risque (migrations, refactor large, nouveau service).

## ✅ Validation du code

- [ ] Tous les tests CI passent (unit + integration + E2E)
- [ ] Code review approuvé par au moins 1 personne
- [ ] Linter et type checks verts
- [ ] Pas de TODO / FIXME critique non traité
- [ ] Changelog / release notes mis à jour

## 🗄️ Base de données

- [ ] Migrations testées sur env de staging avec données réalistes
- [ ] Migrations idempotentes (replay safe)
- [ ] Migrations destructives (DROP, ALTER) : plan en 2 phases (deploy code → deploy migration)
- [ ] Backup pris ou planifié avant migration
- [ ] Plan de rollback DB documenté
- [ ] Estimation de durée des migrations (lock long ?)

## 🔄 Stratégie de déploiement

- [ ] Type de déploiement choisi : rolling / blue-green / canary
- [ ] Plan de rollback précis (commande exacte, durée estimée)
- [ ] Feature flags activés pour le code à risque (peut être désactivé sans rollback)
- [ ] Capacité disponible : scaling pré-déployé si pic attendu
- [ ] Heure de déploiement : éviter pics de trafic et hors heures business si possible

## 📡 Observabilité prête

- [ ] Dashboards à monitorer pendant et après identifiés
- [ ] Alertes en place pour les nouveaux endpoints / services
- [ ] Logs structurés et accessibles
- [ ] Traces distribuées (si stack tracée) instrumentées sur les nouveaux chemins
- [ ] SLO/SLI définis si nouveau service

## 📢 Communication

- [ ] Stakeholders prévenus (Slack, email, statuspage)
- [ ] Support client briefé sur les changements visibles
- [ ] Doc utilisateur mise à jour si UX change
- [ ] Window de maintenance annoncée si nécessaire

## 🚨 Plan d'urgence

- [ ] Qui est on-call pendant et après ?
- [ ] Critères de rollback définis (ex: "si erreur >5% sur 5 min → rollback")
- [ ] Ligne de communication de crise prête (canal Slack dédié, war room virtuel)
- [ ] Post-déploiement : durée minimale d'observation avant validation

## 🚫 Anti-patterns

- ❌ Déployer un vendredi après-midi sans on-call
- ❌ Migrer un schéma sans tester sur staging
- ❌ Pas de plan de rollback ("on improvisera")
- ❌ Déployer plusieurs gros changements en même temps
