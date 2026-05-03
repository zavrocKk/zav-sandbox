---
type: runbook
status: draft  # draft | reviewed | validated
target_system: # <nom du service ou composant>
owner: # <équipe ou persona responsable>
last_validated: YYYY-MM-DD
---

# Runbook — <nom du système / composant>

<!-- Le titre doit identifier le système sans ambiguïté. Ex: "Runbook — nginx API Gateway" -->

> **Usage :** ce document est opérationnel. Il doit pouvoir être utilisé par un DevOps sous pression en incident. Chaque procédure doit être testée et datée.

---

## Vue d'ensemble

<!-- Quoi : brève description du système. Pour qui : équipe(s) qui utilisent ce runbook. Périmètre : ce qui est couvert et ce qui ne l'est pas. -->

**Système :** <!-- description en 1-2 lignes -->
**Équipe principale :** <!-- DevOps / Platform / SRE -->
**Périmètre :** <!-- ex: démarrage, arrêt, scaling, monitoring de X -->

---

## Prérequis

<!-- Accès, outils, permissions nécessaires pour utiliser ce runbook. -->

- [ ] Accès : <!-- ex: accès kubectl prod, accès AWS Console, credentials Vault -->
- [ ] Outils : <!-- ex: kubectl, aws-cli, psql, curl -->
- [ ] Permissions : <!-- ex: rôle IAM ops-prod-readonly + ops-prod-write pour les actions déstructives -->

---

## Procédures opérationnelles

### Démarrage du service

<!-- Étapes séquentielles pour démarrer le service. Indiquer les commandes exactes et les vérifications attendues. -->

```bash
# Étape 1 — <description>
<commande>
# Vérification attendue : <résultat>

# Étape 2 — <description>
<commande>
```

### Arrêt du service

<!-- Étapes pour arrêter proprement le service (graceful shutdown). -->

```bash
# Étape 1 — <description>
<commande>
```

### Scaling

<!-- Comment scaler horizontalement / verticalement. Indiquer les limites. -->

| Action | Commande | Limite |
|---|---|---|
| Scale up | <!-- commande --> | <!-- max replicas --> |
| Scale down | <!-- commande --> | <!-- min replicas --> |

---

## Procédures d'incident

<!-- Pour chaque symptôme courant : diagnostic → mitigation → vérification. -->

### Symptôme : <description du symptôme observable>

**Diagnostic :**
```bash
# Vérifier <quoi>
<commande de diagnostic>
```

**Mitigation :**
```bash
# Action : <description>
<commande>
# ⚠️ DESTRUCTIVE — confirmation utilisateur requise avant exécution
```

**Vérification :**
```bash
# Confirmer que le problème est résolu
<commande de vérification>
# Résultat attendu : <valeur ou état>
```

---

## Métriques et alertes liées

<!-- Quelles métriques surveiller et quelles alertes sont configurées pour ce système. -->

| Métrique | Seuil normal | Seuil alerte | Dashboard / Source |
|---|---|---|---|
| <!-- ex: latence p95 --> | <!-- ex: < 200ms --> | <!-- ex: > 500ms --> | <!-- ex: Datadog → Service Map --> |
| <!-- ex: taux d'erreur --> | <!-- ex: < 1% --> | <!-- ex: > 5% --> | <!-- --> |

---

## Contacts d'escalade

| Niveau | Contact | Canal | Quand |
|---|---|---|---|
| L1 | <!-- équipe --> | <!-- Slack #oncall --> | <!-- ex: après 10 min sans résolution --> |
| L2 | <!-- tech lead --> | <!-- PagerDuty --> | <!-- ex: SEV1 ou impact > 1h --> |

---

## Historique de modifications

| Date | Auteur | Modification |
|---|---|---|
| YYYY-MM-DD | <!-- nom --> | Création initiale |
