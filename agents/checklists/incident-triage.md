---
type: checklist
used_by: [devops]
phase: incident-triage
---

# Checklist — Triage d'incident (2 premières minutes)

À utiliser dès qu'un incident est signalé. L'objectif est de cadrer rapidement l'ampleur AVANT de plonger dans le diagnostic.

## 🚨 Cadrage initial

- [ ] **Service(s) affecté(s)** identifié(s) ?
- [ ] **Heure de début** précise (alerte / premier rapport user) ?
- [ ] **Incident en cours ou résolu** ?
- [ ] **Utilisateurs impactés** : tous, segment précis, métier critique ?
- [ ] **Workaround connu** ?

## 🔄 Changements récents (24h-7j)

- [ ] Déploiement applicatif récent ?
- [ ] Changement infra (config, scaling, IaC) ?
- [ ] Mise à jour de dépendance (package, image base) ?
- [ ] Changement DNS / certificat / réseau ?
- [ ] Migration de schéma DB ?

## 📊 Signaux observables

- [ ] **Métriques** : CPU / RAM / disque / réseau anormaux ?
- [ ] **Logs applicatifs** : pic d'erreurs, traces de stack inhabituelles ?
- [ ] **Logs infra** : OOM kills, restarts de pods, events K8s ?
- [ ] **Dépendances** : DB, cache, queues, services tiers — sains ?
- [ ] **Trafic** : volume normal, attaque potentielle ?

## 🎯 Décision après triage

- [ ] **Sévérité** estimée : SEV1 / SEV2 / SEV3
- [ ] **Communication** : qui prévenir et quand ?
- [ ] **Hypothèse principale** formulée (à valider en diagnostic)
- [ ] **Mitigation rapide possible** (rollback, feature flag, scale) à proposer ?

## 🚫 Anti-patterns à éviter

- ❌ Plonger dans le code avant d'avoir cadré l'ampleur
- ❌ Appliquer un fix en prod sans confirmation utilisateur
- ❌ Conclure sur une seule hypothèse non vérifiée
- ❌ Communiquer une cause racine pendant le triage (trop tôt)
