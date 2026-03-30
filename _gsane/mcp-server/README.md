# GSANE Local MCP Server

Serveur Model Context Protocol (MCP) minimaliste pour l'architecture **GSANE V2**.
L'objectif de ce serveur est de déporter la logique statique (qui consomme beaucoup de tokens et provoque des hallucinations chez les LLMs) vers des scripts Python déterministes.

## Outils (Tools) Exposés

| Outil | Description | Remplace |
|---|---|---|
| `gsane_route(query)` | Interroge `delegation-matrix.yaml` et retourne l'agent expert à charger pour une tâche donnée. | La lecture brute par l'IA du CSV de routage |
| `gsane_memory_fetch(agent_name, topic)` | Extrait juste ce qu'il faut du sidecar de l'agent selon le contexte de la session. | Les balises `<load memory silently>` massives |

## Installation & Déploiement

### 1. Prérequis
Assurez-vous d'avoir Python 3.10+ installé.

### 2. Installation des dépendances
```bash
cd _gsane/mcp-server
pip install -r requirements.txt
```

### 3. Intégration Client MCP (ex: Claude Desktop / Cursor / Copilot)
Ajoutez ce serveur dans votre configuration de client AI supportant le standard MCP via la mécanique `stdio`.

**Exemple de config type (`mcp_config.json`) :**
```json
{
  "mcpServers": {
    "gsane-core": {
      "command": "python",
      "args": ["{CHEMIN_ABSOLU}/_gsane/mcp-server/server.py"]
    }
  }
}
```