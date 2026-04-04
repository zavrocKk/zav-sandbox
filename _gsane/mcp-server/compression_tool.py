from mcp.server.fastmcp import FastMCP
from pathlib import Path
from datetime import datetime
import os
import yaml

mcp = FastMCP("GSANE Memory Compressor")

# Paths robustes dérivés de __file__ (indépendants du cwd)
_GSANE_DIR = Path(__file__).parent.parent          # _gsane/
MEMORY_DIR = _GSANE_DIR / "_memory"               # _gsane/_memory/
CONFIG_DIR = _GSANE_DIR / "_config"               # _gsane/_config/
PROJECT_ROOT = _GSANE_DIR.parent                   # project root


def _log_mcp_invocation(tool_name: str, details: str = "") -> None:
    """Writes a trace entry to _gsane/_memory/trace.log."""
    try:
        trace_file = MEMORY_DIR / "trace.log"
        entry = (
            f"- timestamp: {datetime.now().isoformat()}\n"
            f"  session_id: mcp\n"
            f"  event: tool_invoked\n"
            f"  agent: mcp\n"
            f"  task_id: {tool_name}\n"
            f"  duration_ms: 0\n"
            f"  trust_score: null\n"
            f"  details: \"{details[:120]}\"\n"
        )
        with open(trace_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception:
        pass  # Logging must never break the tool


@mcp.tool()
def gsane_fetch_compressed_memory(query: str) -> str:
    """
    Searches through GSANE memory files and returns a summarized, compressed string
    relevant ONLY to the query to avoid prompt bloat.
    """
    _log_mcp_invocation("gsane_fetch_compressed_memory", f"query={query[:60]}")
    results = []

    for root, dirs, files in os.walk(MEMORY_DIR):
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                try:
                    content = path.read_text(encoding="utf-8")
                    if query.lower() in content.lower():
                        idx = content.lower().find(query.lower())
                        start = max(0, idx - 150)
                        end = min(len(content), idx + 150)
                        results.append(f"[{file}] ...{content[start:end]}...")
                except Exception:
                    pass

    if not results:
        return "No memory found for this query."

    return "COMPRESSED SUMMARY: \n" + "\n---\n".join(results[:5])


@mcp.tool()
def gsane_write_session_checkpoint(
    plan_active: str,
    next_step: str,
    decisions: str,
    open_items: str,
    risks: str,
    exchange_count: int
) -> str:
    """
    Sérialise un checkpoint de session compressé dans _gsane/_memory/sessions/session-state.md.
    Préserve les champs existants (last_agent_active, first_run) et met à jour checkpoint_* et exchange_count.
    """
    _log_mcp_invocation("gsane_write_session_checkpoint", f"exchange={exchange_count}")
    try:
        session_file = MEMORY_DIR / "sessions" / "session-state.md"

        if session_file.exists():
            content = session_file.read_text(encoding="utf-8")
        else:
            content = "last_agent_active: null\nfirst_run: true\n"

        # Remove existing checkpoint_compressed block
        lines = content.split('\n')
        filtered_lines = []
        skip_block = False
        for line in lines:
            if line.startswith('checkpoint_compressed:'):
                skip_block = True
                continue
            if skip_block:
                if line == '' or (len(line) > 0 and line[0] in (' ', '\t')):
                    continue
                else:
                    skip_block = False
            if line.startswith('checkpoint_exchange:') or \
               line.startswith('checkpoint_date:') or \
               line.startswith('exchange_count:'):
                continue
            filtered_lines.append(line)

        base_content = '\n'.join(filtered_lines).rstrip('\n')

        checkpoint_block = (
            f"=== CHECKPOINT COMPRESSÉ — Exchange {exchange_count} ===\n"
            f"\n"
            f"PLAN ACTIF : {plan_active}\n"
            f"PROCHAINE ÉTAPE : {next_step}\n"
            f"\n"
            f"DÉCISIONS PRISES :\n"
            f"{decisions}\n"
            f"\n"
            f"RISQUES OUVERTS :\n"
            f"{risks}\n"
            f"\n"
            f"ITEMS EN ATTENTE :\n"
            f"{open_items}"
        )

        indented_lines = []
        for line in checkpoint_block.split('\n'):
            indented_lines.append('  ' + line if line else '')
        indented_block = '\n'.join(indented_lines)

        current_datetime = datetime.now().isoformat()

        new_content = (
            base_content + '\n'
            f'exchange_count: {exchange_count}\n'
            f'checkpoint_exchange: {exchange_count}\n'
            f'checkpoint_date: {current_datetime}\n'
            f'checkpoint_compressed: |\n'
            + indented_block + '\n'
        )

        session_file.parent.mkdir(parents=True, exist_ok=True)
        session_file.write_text(new_content, encoding="utf-8")

        return f"✅ Checkpoint sauvegardé — exchange {exchange_count}"
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


@mcp.tool()
def gsane_read_checkpoint() -> str:
    """
    Lit et retourne le bloc checkpoint_compressed de session-state.md pour une reprise warm.
    """
    _log_mcp_invocation("gsane_read_checkpoint", "warm session read")
    try:
        session_file = MEMORY_DIR / "sessions" / "session-state.md"

        if not session_file.exists():
            return "No checkpoint found — cold session."

        content = session_file.read_text(encoding="utf-8")
        lines = content.split('\n')
        in_block = False
        block_lines = []

        for line in lines:
            if line.startswith('checkpoint_compressed:'):
                in_block = True
                continue
            if in_block:
                if line == '' or (len(line) > 0 and line[0] in (' ', '\t')):
                    block_lines.append(line)
                else:
                    break

        if not block_lines:
            return "No checkpoint found — cold session."

        dedented_lines = []
        for line in block_lines:
            if line.startswith('  '):
                dedented_lines.append(line[2:])
            else:
                dedented_lines.append(line)

        checkpoint_content = '\n'.join(dedented_lines).strip()

        if not checkpoint_content:
            return "No checkpoint found — cold session."

        return f"=== CHECKPOINT TROUVÉ ===\n{checkpoint_content}"
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


@mcp.tool()
def gsane_route(query: str) -> str:
    """
    Détermine l'agent GSANE approprié pour traiter une requête en se basant sur
    la delegation-matrix.yaml. Outil déterministe qui remplace la lecture LLM.

    Args:
        query: La demande brute de l'utilisateur ou la tâche à accomplir.
    """
    _log_mcp_invocation("gsane_route", f"query={query[:60]}")
    matrix_path = CONFIG_DIR / "delegation-matrix.yaml"

    if not matrix_path.exists():
        return "❌ ERROR: fichier delegation-matrix.yaml introuvable."

    try:
        with open(matrix_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        query_lower = query.lower()
        best_match = None
        max_score = 0

        for rule in data.get("rules", []):
            score = 0
            # Clés actuelles du schéma delegation-matrix.yaml : "trigger" (liste) et "agent"
            for kw in rule.get("trigger", []):
                if str(kw).lower() in query_lower:
                    score += len(str(kw))

            if score > max_score:
                max_score = score
                best_match = rule

        if best_match:
            agent = best_match.get("agent", "unknown")
            description = best_match.get("description", "")
            return (
                f"✅ ROUTAGE CONFIRMÉ :\n"
                f"Agent cible : {agent}\n"
                f"Description : {description}"
            )

        return "⚠️ Aucun routage spécifique trouvé. Adressez-vous à Langis (Master)."

    except Exception as e:
        return f"❌ ERROR lors de la lecture de la matrice : {str(e)}"


@mcp.tool()
def gsane_memory_fetch(agent_name: str, topic: str = "") -> str:
    """
    Recherche dans la mémoire sidecar d'un agent GSANE sans charger l'intégralité du fichier.

    Args:
        agent_name: Nom de l'agent (ex: 'master', 'architect', 'dev', 'qa', 'bond').
        topic: Mot-clé pour filtrer les résultats. Vide = extrait général (15 premières lignes).
    """
    _log_mcp_invocation("gsane_memory_fetch", f"agent={agent_name} topic={topic[:40]}")
    target_memory = MEMORY_DIR / f"{agent_name}-sidecar" / "learned-lessons.md"

    if not target_memory.exists():
        return f"ℹ️ Aucune mémoire persistante trouvée pour l'agent '{agent_name}'."

    try:
        lines = target_memory.read_text(encoding="utf-8").splitlines(keepends=True)

        if not topic:
            excerpt = "".join(lines[:15])
            if len(lines) > 15:
                excerpt += "\n... [Tronqué — précisez 'topic' pour chercher plus loin]"
            return excerpt

        matches = []
        topic_lower = topic.lower()
        for i, line in enumerate(lines):
            if topic_lower in line.lower():
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                context = "".join(lines[start:end])
                if context not in matches:
                    matches.append(context.strip())

        if matches:
            found = "\n---\n".join(matches[:5])
            if len(matches) > 5:
                found += "\n... [Plusieurs autres correspondances trouvées]"
            return f"🔍 Mémoires pour '{topic}' (Agent: {agent_name}):\n\n{found}"

        return f"ℹ️ Aucune mémoire trouvée concernant '{topic}' pour {agent_name}."

    except Exception as e:
        return f"❌ ERROR lors de l'accès à la mémoire : {str(e)}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("--- RUNNING MANUAL TEST ---")
        result = gsane_fetch_compressed_memory("failure")
        print(result)
        print("---")
        result2 = gsane_route("implement a new feature")
        print(result2)
    else:
        mcp.run()

@mcp.tool()
def gsane_write_session_checkpoint(
    plan_active: str,
    next_step: str,
    decisions: str,
    open_items: str,
    risks: str,
    exchange_count: int
) -> str:
    """
    Sérialise un checkpoint de session compressé dans _gsane/_memory/sessions/session-state.md.
    Préserve les champs existants (last_agent_active, first_run) et met à jour checkpoint_* et exchange_count.
    """
    try:
        from datetime import datetime

        session_file = "_gsane/_memory/sessions/session-state.md"

        if os.path.exists(session_file):
            with open(session_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = "last_agent_active: null\nfirst_run: true\n"

        # Remove existing checkpoint_compressed block (key + all indented/empty continuation lines)
        lines = content.split('\n')
        filtered_lines = []
        skip_block = False
        for line in lines:
            if line.startswith('checkpoint_compressed:'):
                skip_block = True
                continue
            if skip_block:
                if line == '' or (len(line) > 0 and line[0] in (' ', '\t')):
                    continue
                else:
                    skip_block = False
            if line.startswith('checkpoint_exchange:') or \
               line.startswith('checkpoint_date:') or \
               line.startswith('exchange_count:'):
                continue
            filtered_lines.append(line)

        base_content = '\n'.join(filtered_lines).rstrip('\n')

        # Build checkpoint block content
        checkpoint_block = (
            f"=== CHECKPOINT COMPRESSÉ — Exchange {exchange_count} ===\n"
            f"\n"
            f"PLAN ACTIF : {plan_active}\n"
            f"PROCHAINE ÉTAPE : {next_step}\n"
            f"\n"
            f"DÉCISIONS PRISES :\n"
            f"{decisions}\n"
            f"\n"
            f"RISQUES OUVERTS :\n"
            f"{risks}\n"
            f"\n"
            f"ITEMS EN ATTENTE :\n"
            f"{open_items}"
        )

        # Indent block for YAML block scalar (2 spaces; empty lines stay empty)
        indented_lines = []
        for line in checkpoint_block.split('\n'):
            indented_lines.append('  ' + line if line else '')
        indented_block = '\n'.join(indented_lines)

        current_datetime = datetime.now().isoformat()

        new_content = (
            base_content + '\n'
            f'exchange_count: {exchange_count}\n'
            f'checkpoint_exchange: {exchange_count}\n'
            f'checkpoint_date: {current_datetime}\n'
            f'checkpoint_compressed: |\n'
            + indented_block + '\n'
        )

        os.makedirs(os.path.dirname(os.path.abspath(session_file)), exist_ok=True)

        with open(session_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        return f"✅ Checkpoint sauvegardé — exchange {exchange_count}"
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


@mcp.tool()
def gsane_read_checkpoint() -> str:
    """
    Lit et retourne le bloc checkpoint_compressed de session-state.md pour une reprise warm.
    """
    try:
        session_file = "_gsane/_memory/sessions/session-state.md"

        if not os.path.exists(session_file):
            return "No checkpoint found — cold session."

        with open(session_file, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split('\n')
        in_block = False
        block_lines = []

        for line in lines:
            if line.startswith('checkpoint_compressed:'):
                in_block = True
                continue
            if in_block:
                if line == '' or (len(line) > 0 and line[0] in (' ', '\t')):
                    block_lines.append(line)
                else:
                    break

        if not block_lines:
            return "No checkpoint found — cold session."

        # Dedent: remove leading 2-space indent (YAML block scalar indentation)
        dedented_lines = []
        for line in block_lines:
            if line.startswith('  '):
                dedented_lines.append(line[2:])
            else:
                dedented_lines.append(line)

        checkpoint_content = '\n'.join(dedented_lines).strip()

        if not checkpoint_content:
            return "No checkpoint found — cold session."

        return f"=== CHECKPOINT TROUVÉ ===\n{checkpoint_content}"
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("--- RUNNING MANUAL TEST ---")
        result = gsane_fetch_compressed_memory("failure")
        print(result)
    else:
        mcp.run()
