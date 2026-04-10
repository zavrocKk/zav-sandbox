# GSANE MCP Server

Serveur MCP local exposant les vues canoniques de lecture du runtime GSANE, plus quelques outils historiques conserves pour compatibilite et continuite technique.

**Point d'entree unique** : `compression_tool.py`  
**Configure dans** : `github-copilot.mcp.json`

---

## Modele canonique

- `_gsane/_memory/project-context.md` est le brief canonique humain, court et durable.
- `_gsane-output/current-delivery-contract.md` porte le travail actif mutable.
- Les vues MCP canoniques exposent des lectures structurees derivees du repo.
- `session-state.md` et `session-analysis-log.md` restent des fichiers d'audit/continuite, pas des sources de verite du present.

---

## Outils exposes

### 1. `gsane_read_canonical_brief() -> str`
Retourne une vue YAML structuree du brief canonique humain.

**Usage typique** : Charger le cap durable du projet sans relire d'anciens resumes de session.

### 2. `gsane_read_active_delivery_contract() -> str`
Retourne une vue YAML structuree du Delivery Contract actif, avec ses metadonnees et son contenu.

**Usage typique** : Comprendre la tache courante et ses criteres d'acceptation.

### 3. `gsane_read_project_snapshot() -> str`
Retourne un snapshot YAML derive du repo : agents actifs, compte des workflows, contrat actif et statut des fichiers d'audit/continuite.

**Usage typique** : Obtenir l'etat courant sans inventer une nouvelle source de verite humaine.

### 4. `gsane_fetch_compressed_memory(query: str) -> str`
Recherche dans les fichiers `.md` de `_gsane/_memory/` les passages correspondant a `query`.
Retourne un resume compresse (max 5 extraits de 300 chars) pour eviter le prompt bloat.

### 5. `gsane_write_session_checkpoint(plan_active, next_step, decisions, open_items, risks, exchange_count) -> str`
Sérialise un checkpoint dans `_gsane/_memory/sessions/session-state.md`.

**Statut** : historique / audit / continuite technique. Ne pas utiliser comme source de verite du present.

### 6. `gsane_read_checkpoint() -> str`
Lit le bloc `checkpoint_compressed` de `session-state.md`.

**Statut** : historique / audit / continuite technique.

### 7. `gsane_route(query: str) -> str`
Routage déterministe vers l'agent GSANE cible via `_gsane/_config/delegation-matrix.yaml`.
Si la requête matche le bloc déclaratif `security_gate`, le MCP remonte vers le Master avec `owner=Winston`, `validation=Quinn` et `Bond` uniquement si la surface est GSANE/policy/guardrail/runtime critique.

### 8. `gsane_memory_fetch(agent_name: str, topic: str = "") -> str`
Extrait les `learned-lessons.md` du sidecar d'un agent sans charger tout le fichier.

**Agents valides** : `master`, `dev`, `qa`, `architect`, `bond`

---

## Traçabilité MCP

Chaque invocation outil est automatiquement journalisée dans `_gsane/_memory/trace.log` :
```yaml
- timestamp: 2026-04-04T10:00:00
  session_id: mcp
  event: tool_invoked
  agent: mcp
  task_id: gsane_route
  duration_ms: 0
  trust_score: null
  details: "query=implement a new feature"
```

---

## Chemins et confinement

Tous les accès fichiers utilisent des chemins dérivés de `__file__` et sont indépendants du répertoire de travail du client MCP.

Les accès exposés par le MCP sont confinés aux racines autorisées déclarées dans `delegation-matrix.yaml` :
- `_gsane/_memory/`
- `_gsane/_config/`
- `_gsane-output/`

`gsane_memory_fetch` refuse aussi tout nom d'agent hors allowlist (`master`, `dev`, `qa`, `architect`, `bond`).

---

## Installation

```bash
pip install -r _gsane/mcp-server/requirements.txt
# Packages: mcp[cli]>=1.2.0, pyyaml>=6.0.1
```

## Vérification

```bash
bash gsane.sh mcp --health      # Vérifie dépendances + imports + schéma
bash gsane.sh mcp --smoke-test  # Smoke test des vues canoniques + outils historiques
python -m pytest tests/test_mcp.py -v
```
