# GSANE MCP Server

Serveur MCP local exposant 5 outils pour l'intégration Copilot Chat ↔ GSANE.

**Point d'entrée unique** : `compression_tool.py`  
**Configuré dans** : `github-copilot.mcp.json`

---

## Outils Exposés

### 1. `gsane_fetch_compressed_memory(query: str) → str`
Recherche dans tous les fichiers `.md` de `_gsane/_memory/` les passages correspondant à `query`.
Retourne un résumé compressé (max 5 extraits de 300 chars) pour éviter le prompt bloat.

**Usage typique** : Le Master lit la mémoire projet au démarrage de session.

---

### 2. `gsane_write_session_checkpoint(plan_active, next_step, decisions, open_items, risks, exchange_count) → str`
Sérialise l'état de session dans `_gsane/_memory/sessions/session-state.md`.
Préserve les champs existants (`last_agent_active`, `first_run`) et met à jour le bloc `checkpoint_compressed`.

**Usage typique** : Le Master écrit un checkpoint toutes les N exchanges pour garantir la continuité.

---

### 3. `gsane_read_checkpoint() → str`
Lit le bloc `checkpoint_compressed` de `session-state.md` pour reprendre une session warm.
Retourne `"No checkpoint found — cold session."` si aucun fichier n'existe.

**Usage typique** : Détection WARM/COLD session au démarrage du Master.

---

### 4. `gsane_route(query: str) → str`
Routage déterministe vers l'agent GSANE cible via `_gsane/_config/delegation-matrix.yaml`.
Utilise un scoring par mots-clés sur la liste `trigger` de chaque règle.

**Schéma delegation-matrix.yaml requis** :
```yaml
rules:
  - trigger: [liste, de, mots-clés]
    agent: "Nom Agent (Persona)"
    description: "..."
```

**Usage typique** : Routage initial d'une requête ambiguë avant activation d'un agent.

---

### 5. `gsane_memory_fetch(agent_name: str, topic: str = "") → str`
Extrait les `learned-lessons.md` du sidecar d'un agent sans charger tout le fichier.
- Sans `topic` : retourne les 15 premières lignes
- Avec `topic` : recherche textuelle, retourne max 5 extraits avec contexte

**Agents valides** : `master`, `dev`, `qa`, `architect`, `bond`

**Usage typique** : Chargement JIT des leçons apprises d'un agent avant exécution.

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

## Chemins — Robustesse

Tous les accès fichiers utilisent des chemins dérivés de `__file__` :
```python
_GSANE_DIR = Path(__file__).parent.parent   # → _gsane/
MEMORY_DIR = _GSANE_DIR / "_memory"        # → _gsane/_memory/
CONFIG_DIR = _GSANE_DIR / "_config"        # → _gsane/_config/
```

Indépendants du répertoire de travail du client MCP.

---

## Installation

```bash
pip install -r _gsane/mcp-server/requirements.txt
# Packages: mcp[cli]>=1.2.0, pyyaml>=6.0.1
```

## Vérification

```bash
bash gsane.sh mcp --health      # Vérifie dépendances + imports + schéma
bash gsane.sh mcp --smoke-test  # Smoke test des 5 outils
python -m pytest tests/test_mcp.py -v  # Suite de tests complète
```
