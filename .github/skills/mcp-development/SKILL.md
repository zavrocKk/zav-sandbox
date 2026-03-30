# Skill: MCP Development in GSANE

## Overview
This skill defines how to create and maintain Model Context Protocol (MCP) tools within the GSANE V2 framework.

## Architecture
- **Serveur MCP** : Permet aux agents IA d'obtenir des capacités sur-mesure (comme la compression de contexte) sans polluer le prompt initial. Le framework utilise FastMCP.
- **Dossier Cible** : Tous les serveurs et outils MCP doivent être créés et maintenus dans _gsane/mcp-server/.
- **Environnement** : Un environnement virtuel Python .venv est requis à la racine pour isoler les dépendances (mcp, astmcp).

## Règles de Développement
1. **Zéro Prompt Bloat** : Les outils de lecture/recherche de fichiers DOIVENT retourner des données compressées et ciblées, pas des fichiers entiers.
2. Toujours spécifier le paramètre d'entrée avec précision via du typage strict Python (def my_tool(query: str) -> str:).
3. Utiliser le décorateur @mcp.tool() et l'instance FastMCP.

## Configuration Client
Pour dire à l'IA d'utiliser vos nouveaux outils locaux, il faut configurer un fichier .vscode/mcp.json pointant vers l'exécutable python absolu du .venv et le script absolu du mcp-server. Ne pas commiter ce fichier local.
