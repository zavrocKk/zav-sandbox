from pathlib import Path

import yaml  # type: ignore[import-untyped]
from mcp.server.fastmcp import FastMCP

raise ImportError("Ce fichier est ARCHIVÉ. Utilisez compression_tool.py comme point d'entrée MCP.")

# Initialisation du serveur MCP pour GSANE
mcp = FastMCP("GSANE-Core-Server")

# Définition des chemins relatifs
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "_gsane" / "_config"
MEMORY_DIR = PROJECT_ROOT / "_gsane" / "_memory"


@mcp.tool()
def gsane_route(query: str) -> str:
    """
    Détermine l'agent GSANE approprié pour traiter une requête en se basant sur la delegation-matrix.yaml.
    Outil déterministe qui remplace la lecture LLM sujette aux hallucinations.

    Args:
        query: La demande brute de l'utilisateur ou la tâche à accomplir.
    """
    matrix_path = CONFIG_DIR / "delegation-matrix.yaml"

    if not matrix_path.exists():
        return "❌ ERROR: fichier delegation-matrix.yaml introuvable."

    try:
        with open(matrix_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        query_lower = query.lower()
        best_match = None
        max_score = 0

        # Logique de scoring par mots-clés
        for rule in data.get("rules", []):
            score = 0
            for kw in rule.get("trigger_keywords", []):
                if kw.lower() in query_lower:
                    score += len(kw)

            if score > max_score:
                max_score = score
                best_match = rule

        if best_match:
            return (
                f"✅ ROUTAGE CONFIRMÉ :\n"
                f"Agent cible : {best_match['target_agent']} ({best_match['target_module']})\n"
                f"Chemin du fichier : {best_match['target_path']}\n"
                f"Description de l'autorité : {best_match['description']}"
            )

        return "⚠️ Aucun routage spécifique trouvé. Adressez-vous à gsane-master."

    except Exception as e:
        return f"❌ ERROR lors de la lecture de la matrice : {str(e)}"


@mcp.tool()
def gsane_memory_fetch(agent_name: str, topic: str = "") -> str:
    """
    Recherche sémantique basique pour extraire les mémoires pertinentes d'un agent
    sans charger l'intégralité du fichier (prévention du memory bloat).

    Args:
        agent_name: Le nom de l'agent (ex: 'pm', 'architect', 'tea').
        topic: Le sujet recherché (mot-clé) pour filtrer les résultats. Vide = extrait général.
    """
    target_memory = MEMORY_DIR / f"{agent_name}-sidecar" / "learned-lessons.md"

    if not target_memory.exists():
        return f"ℹ️ Aucune mémoire persistante (learned-lessons) trouvée pour l'agent '{agent_name}'."

    try:
        with open(target_memory, encoding="utf-8") as f:
            lines = f.readlines()

        if not topic:
            # Si pas de recherche spécifique, renvoyer les 15 premières lignes pour économie de tokens
            excerpt_lines = lines[:15]
            summary = "".join(excerpt_lines)
            if len(lines) > 15:
                summary += "\n... [Tronqué : précisez le paramètre 'topic' pour chercher plus loin]"
            return summary

        # Recherche par mot-clé (Simulation sémantique/Grep)
        matches = []
        topic_lower = topic.lower()
        for count, line in enumerate(lines):
            if topic_lower in line.lower():
                # Ajouter un peu de contexte (la ligne au-dessus et en-dessous)
                start = max(0, count - 1)
                end = min(len(lines), count + 2)
                context = "".join(lines[start:end])
                if context not in matches:  # Éviter les dédoublements de contexte superposés
                    matches.append(context.strip())

        if matches:
            found = "\n---\n".join(matches[:5])  # Limiter aux 5 meilleurs matchs pour les tokens
            if len(matches) > 5:
                found += "\n... [Plusieurs autres correspondances trouvées]"
            return f"🔍 Mémoires trouvées pour '{topic}' (Agent: {agent_name}):\n\n{found}"

        return f"ℹ️ Aucune mémoire trouvée concernant '{topic}' pour {agent_name}."

    except Exception as e:
        return f"❌ ERROR lors de l'accès à la mémoire : {str(e)}"


if __name__ == "__main__":
    # Exposition via flux STDIO pour être consommable par les clients MCP
    mcp.run(transport="stdio")
