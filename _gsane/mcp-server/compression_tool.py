import os
import sys
from datetime import datetime
from pathlib import Path
from typing import cast

import yaml  # type: ignore[import-untyped]
from mcp.server.fastmcp import FastMCP

_GSANE_DIR = Path(__file__).resolve().parents[1]
MEMORY_DIR = _GSANE_DIR / "_memory"
CONFIG_DIR = _GSANE_DIR / "_config"
PROJECT_ROOT = _GSANE_DIR.parent
TOOLS_DIR = _GSANE_DIR / "tools"

if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from security_gate import (  # noqa: E402
    classify_security_request,
    ensure_path_within_roots as _ensure_path_within_roots,
    get_allowed_mcp_roots,
    is_allowed_mcp_agent_name,
    load_delegation_matrix,
    normalize_text,
)


def ensure_path_within_roots(candidate: Path, allowed_roots: "list[Path]") -> Path:
    """Typed wrapper around security_gate.ensure_path_within_roots."""
    return cast(Path, _ensure_path_within_roots(candidate, allowed_roots))

mcp = FastMCP("GSANE Memory Compressor")
ALLOWED_MCP_ROOTS = get_allowed_mcp_roots()
CANONICAL_VIEW_NAMES = (
    "gsane_read_canonical_brief",
    "gsane_read_active_delivery_contract",
    "gsane_read_project_snapshot",
)


def _escape_yaml_details(value: str) -> str:
    return value[:120].replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")


def _log_mcp_invocation(tool_name: str, details: str = "") -> None:
    """Write a trace entry and rotate if trace.log exceeds 500 KB."""
    try:
        trace_file = ensure_path_within_roots(MEMORY_DIR / "trace.log", ALLOWED_MCP_ROOTS)
        safe_details = _escape_yaml_details(details)
        entry = (
            f"- timestamp: {datetime.now().isoformat()}\n"
            f"  session_id: mcp\n"
            f"  event: tool_invoked\n"
            f"  agent: mcp\n"
            f"  task_id: {tool_name}\n"
            f"  duration_ms: 0\n"
            f"  trust_score: null\n"
            f'  details: "{safe_details}"\n'
        )
        with trace_file.open("a", encoding="utf-8") as handle:
            handle.write(entry)
        _rotate_trace_if_needed(trace_file)
    except OSError:
        return


def _rotate_trace_if_needed(trace_file: Path, max_bytes: int = 512_000) -> None:
    """Archive trace.log when it exceeds max_bytes (~500 KB)."""
    try:
        if not trace_file.exists() or trace_file.stat().st_size <= max_bytes:
            return
        archive_dir = ensure_path_within_roots(PROJECT_ROOT / "_gsane-output", ALLOWED_MCP_ROOTS)
        archive_name = f"trace-archive-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.log"
        archive_path = archive_dir / archive_name
        trace_file.rename(archive_path)
        trace_file.write_text(
            f"# trace.log — rotated {datetime.now().isoformat()}\n",
            encoding="utf-8",
        )
    except OSError:
        return


def _relative_project_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def _session_state_path() -> Path:
    return ensure_path_within_roots(
        MEMORY_DIR / "sessions" / "session-state.md",
        ALLOWED_MCP_ROOTS,
    )


def _session_analysis_log_path() -> Path:
    return ensure_path_within_roots(
        MEMORY_DIR / "sessions" / "session-analysis-log.md",
        ALLOWED_MCP_ROOTS,
    )


def _canonical_brief_path() -> Path:
    return ensure_path_within_roots(
        MEMORY_DIR / "project-context.md",
        ALLOWED_MCP_ROOTS,
    )


def _active_delivery_contract_path() -> Path:
    return ensure_path_within_roots(
        PROJECT_ROOT / "_gsane-output" / "current-delivery-contract.md",
        ALLOWED_MCP_ROOTS,
    )


def _framework_manifest_path() -> Path:
    return ensure_path_within_roots(CONFIG_DIR / "manifest.yaml", ALLOWED_MCP_ROOTS)


def _workflow_manifest_path() -> Path:
    return ensure_path_within_roots(
        CONFIG_DIR / "workflow-manifest.yaml",
        ALLOWED_MCP_ROOTS,
    )


def _agent_manifest_path() -> Path:
    return ensure_path_within_roots(CONFIG_DIR / "agent-manifest.yaml", ALLOWED_MCP_ROOTS)


def _iter_memory_markdown_files() -> list[Path]:
    files: list[Path] = []
    for root, _, filenames in os.walk(MEMORY_DIR, followlinks=False):
        for filename in filenames:
            if not filename.endswith(".md"):
                continue
            candidate = Path(root) / filename
            try:
                files.append(ensure_path_within_roots(candidate, ALLOWED_MCP_ROOTS))
            except ValueError:
                continue
    return files


def _read_text_or_none(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _read_yaml_or_default(path: Path, default):
    content = _read_text_or_none(path)
    if content is None:
        return default
    loaded = yaml.safe_load(content)
    return default if loaded is None else loaded


def _resolve_agent_memory_file(agent_name: str) -> Path:
    if not is_allowed_mcp_agent_name(agent_name):
        raise ValueError("Agent MCP invalide ou hors périmètre autorisé.")
    return ensure_path_within_roots(
        MEMORY_DIR / f"{agent_name}-sidecar" / "learned-lessons.md",
        ALLOWED_MCP_ROOTS,
    )


def _best_route_for_query(query: str, rules: list[dict]) -> dict | None:
    normalized_query = normalize_text(query)
    best_match = None
    max_score = 0
    best_priority = 50
    fallback_rule = None

    for rule in rules:
        triggers = rule.get("trigger", [])
        has_wildcard_trigger = any(str(keyword).strip() == "*" for keyword in triggers)
        if has_wildcard_trigger:
            if fallback_rule is None:
                fallback_rule = rule
            continue

        score = 0
        for keyword in triggers:
            normalized_keyword = normalize_text(str(keyword))
            if normalized_keyword and normalized_keyword in normalized_query:
                score += len(normalized_keyword)

        for keyword in rule.get("exclude_keywords", []):
            normalized_keyword = normalize_text(str(keyword))
            if normalized_keyword and normalized_keyword in normalized_query:
                score -= len(normalized_keyword)

        raw_priority = rule.get("priority", 50)
        try:
            priority = int(raw_priority)
        except (TypeError, ValueError):
            priority = 50

        if score > max_score or (score > 0 and score == max_score and (best_match is None or priority < best_priority)):
            max_score = score
            best_priority = priority
            best_match = rule

    if max_score <= 0:
        return fallback_rule

    return best_match


def _parse_contract_document(content: str) -> tuple[dict, str]:
    separator = "\n---\n"
    if separator not in content:
        return {}, content.strip()

    metadata_text, body = content.split(separator, 1)
    metadata = yaml.safe_load(metadata_text) or {}
    if not isinstance(metadata, dict):
        metadata = {}
    return metadata, body.strip()


def _dump_view(data: dict) -> str:
    result: str = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    return result


def _canonical_brief_view() -> dict:
    path = _canonical_brief_path()
    content = _read_text_or_none(path)
    if content is None:
        return {
            "view": "canonical_human_brief",
            "status": "missing",
            "source": _relative_project_path(path),
            "role": "human-brief",
            "content": "",
        }

    return {
        "view": "canonical_human_brief",
        "status": "available",
        "source": _relative_project_path(path),
        "role": "human-brief",
        "content": content.strip(),
    }


def _active_delivery_contract_view(include_content: bool = True) -> dict:
    path = _active_delivery_contract_path()
    content = _read_text_or_none(path)
    if content is None:
        view = {
            "view": "active_delivery_contract",
            "status": "missing",
            "source": _relative_project_path(path),
            "role": "mutable-work-contract",
            "metadata": {},
        }
        if include_content:
            view["content"] = ""
        return view

    metadata, body = _parse_contract_document(content)
    view = {
        "view": "active_delivery_contract",
        "status": "available",
        "source": _relative_project_path(path),
        "role": "mutable-work-contract",
        "metadata": metadata,
    }
    if include_content:
        view["content"] = body
    return view


def _project_snapshot_view() -> dict:
    config = _read_yaml_or_default(_GSANE_DIR / "config.yaml", {})
    manifest = _read_yaml_or_default(_framework_manifest_path(), {})
    agents = _read_yaml_or_default(_agent_manifest_path(), [])
    workflows = _read_yaml_or_default(_workflow_manifest_path(), [])
    contract_view = _active_delivery_contract_view(include_content=False)
    contract_metadata = contract_view.get("metadata")
    if not isinstance(contract_metadata, dict):
        contract_metadata = {}
    runtime_config = manifest.get("runtime") if isinstance(manifest, dict) else {}
    if not isinstance(runtime_config, dict):
        runtime_config = {}
    active_sources = runtime_config.get("active_sources") or {}
    if not isinstance(active_sources, dict):
        active_sources = {}

    active_delivery_contract = {"status": contract_view.get("status")}
    active_delivery_contract.update(contract_metadata)

    return {
        "view": "canonical_project_snapshot",
        "project": {
            "name": config.get("project_name"),
            "architecture": manifest.get("architecture") if isinstance(manifest, dict) else None,
            "communication_language": config.get("communication_language"),
        },
        "sources_of_truth": {
            "human_brief": active_sources.get(
                "human_brief",
                _relative_project_path(_canonical_brief_path()),
            ),
            "active_delivery_contract": active_sources.get(
                "active_delivery_contract",
                _relative_project_path(_active_delivery_contract_path()),
            ),
            "canonical_mcp_views": list(CANONICAL_VIEW_NAMES),
        },
        "runtime": {
            "active_agents": [entry.get("name") for entry in agents if isinstance(entry, dict) and entry.get("name")],
            "workflow_count": len(workflows) if isinstance(workflows, list) else 0,
            "active_delivery_contract": active_delivery_contract,
            "canonical_mcp_views": list(CANONICAL_VIEW_NAMES),
            "audit_continuity": [
                {
                    "path": _relative_project_path(_session_state_path()),
                    "role": "audit-only",
                    "present": _session_state_path().exists(),
                },
                {
                    "path": _relative_project_path(_session_analysis_log_path()),
                    "role": "audit-only",
                    "present": _session_analysis_log_path().exists(),
                },
            ],
        },
    }


@mcp.tool()
def gsane_read_canonical_brief() -> str:
    """Read the canonical human brief for the active runtime."""
    _log_mcp_invocation("gsane_read_canonical_brief", "canonical human brief")
    return _dump_view(_canonical_brief_view())


@mcp.tool()
def gsane_read_active_delivery_contract() -> str:
    """Read the active delivery contract without inventing mutable project state elsewhere."""
    _log_mcp_invocation(
        "gsane_read_active_delivery_contract",
        "active delivery contract",
    )
    return _dump_view(_active_delivery_contract_view())


@mcp.tool()
def gsane_read_project_snapshot() -> str:
    """Read a repo-derived project snapshot built from the canonical brief, manifests, and active contract."""
    _log_mcp_invocation("gsane_read_project_snapshot", "canonical project snapshot")
    return _dump_view(_project_snapshot_view())


@mcp.tool()
def gsane_fetch_compressed_memory(query: str) -> str:
    """Search markdown memory files and return a compact relevant summary."""
    _log_mcp_invocation("gsane_fetch_compressed_memory", f"query={query[:60]}")
    results: list[str] = []
    normalized_query = query.lower()

    for path in _iter_memory_markdown_files():
        content = _read_text_or_none(path)
        if content is None:
            continue

        if normalized_query not in content.lower():
            continue

        index = content.lower().find(normalized_query)
        start = max(0, index - 150)
        end = min(len(content), index + 150)
        results.append(f"[{path.name}] ...{content[start:end]}...")

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
    exchange_count: int,
) -> str:
    """Serialize a legacy audit/continuity checkpoint into session-state.md."""
    _log_mcp_invocation("gsane_write_session_checkpoint", f"exchange={exchange_count}")
    try:
        session_file = _session_state_path()
        if session_file.exists():
            content = session_file.read_text(encoding="utf-8")
        else:
            content = "last_agent_active: null\nfirst_run: true\n"

        lines = content.split("\n")
        filtered_lines: list[str] = []
        skip_block = False
        for line in lines:
            if line.startswith("checkpoint_compressed:"):
                skip_block = True
                continue
            if skip_block:
                if line == "" or (len(line) > 0 and line[0] in (" ", "\t")):
                    continue
                skip_block = False
            if (
                line.startswith("checkpoint_exchange:")
                or line.startswith("checkpoint_date:")
                or line.startswith("exchange_count:")
            ):
                continue
            filtered_lines.append(line)

        base_content = "\n".join(filtered_lines).rstrip("\n")
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
        indented_block = "\n".join(f"  {line}" if line else "" for line in checkpoint_block.split("\n"))

        new_content = (
            base_content
            + "\n"
            + f"exchange_count: {exchange_count}\n"
            + f"checkpoint_exchange: {exchange_count}\n"
            + f"checkpoint_date: {datetime.now().isoformat()}\n"
            + f"interrupted: false\n"
            + "checkpoint_compressed: |\n"
            + indented_block
            + "\n"
        )

        session_file.parent.mkdir(parents=True, exist_ok=True)
        session_file.write_text(new_content, encoding="utf-8")
        return f"✅ Checkpoint sauvegardé — exchange {exchange_count}"
    except Exception as error:
        return f"❌ Erreur: {error}"


@mcp.tool()
def gsane_read_checkpoint() -> str:
    """Read the legacy audit/continuity checkpoint block from session-state.md."""
    _log_mcp_invocation("gsane_read_checkpoint", "warm session read")
    try:
        session_file = _session_state_path()
        if not session_file.exists():
            return "No checkpoint found — cold session."

        content = session_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        in_block = False
        block_lines: list[str] = []
        for line in lines:
            if line.startswith("checkpoint_compressed:"):
                in_block = True
                continue
            if in_block:
                if line == "" or (len(line) > 0 and line[0] in (" ", "\t")):
                    block_lines.append(line)
                else:
                    break

        if not block_lines:
            return "No checkpoint found — cold session."

        checkpoint_content = "\n".join(line[2:] if line.startswith("  ") else line for line in block_lines).strip()
        if not checkpoint_content:
            return "No checkpoint found — cold session."

        # Check for interrupted session
        interrupted = False
        for line in lines:
            if line.strip() == "interrupted: true":
                interrupted = True
                break

        if interrupted:
            # Extract task and next_step from checkpoint
            task = ""
            next_step_val = ""
            last_agent = ""
            for bl in block_lines:
                stripped = bl.strip()
                if stripped.startswith("PLAN ACTIF :"):
                    task = stripped.replace("PLAN ACTIF :", "").strip()
                elif stripped.startswith("PROCHAINE ÉTAPE :"):
                    next_step_val = stripped.replace("PROCHAINE ÉTAPE :", "").strip()

            # Extract last_agent from session state
            for line in lines:
                if line.startswith("last_agent_active:"):
                    last_agent = line.split(":", 1)[1].strip()
                    break

            return (
                "⚠️ SESSION INTERROMPUE DÉTECTÉE\n"
                f"Dernière tâche : {task}\n"
                f"Dernier agent : {last_agent}\n"
                f"Prochaine étape : {next_step_val}\n"
                "Reprendre ? [oui/non]"
            )

        return f"=== CHECKPOINT TROUVÉ ===\n{checkpoint_content}"
    except Exception as error:
        return f"❌ Erreur: {error}"


@mcp.tool()
def _build_agent_display_name_map() -> dict[str, str]:
    """Build a mapping from canonical agent name to displayName from agent-manifest.yaml."""
    manifest_path = CONFIG_DIR / "agent-manifest.yaml"
    if not manifest_path.exists():
        return {}
    try:
        agents = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or []
        return {a["name"]: a.get("displayName", a["name"]) for a in agents if "name" in a}
    except Exception:
        return {}


def gsane_route(query: str) -> str:
    """Deterministic routing based on delegation-matrix.yaml and the security gate."""
    _log_mcp_invocation("gsane_route", f"query={query[:60]}")
    matrix_path = CONFIG_DIR / "delegation-matrix.yaml"
    if not matrix_path.exists():
        return "❌ ERROR: fichier delegation-matrix.yaml introuvable."

    try:
        security = classify_security_request(query, matrix_path=matrix_path)
        if security.is_security_request:
            bond_review = security.bond_review_agent or "non requise"
            bond_reasons = ", ".join(security.bond_review_reasons) or "aucune"
            topics = ", ".join(security.matched_topics)
            return (
                "⚠️ ESCALADE SÉCURITÉ REQUISE :\n"
                f"Escalade vers : {security.escalation_agent}\n"
                f"Owner sécurité : {security.owner}\n"
                f"Gate validation : {security.validation_agent}\n"
                f"Revue Bond : {bond_review}\n"
                f"Motifs Bond : {bond_reasons}\n"
                f"Sujets détectés : {topics}"
            )

        data = load_delegation_matrix(matrix_path)
        best_match = _best_route_for_query(query, data.get("rules", []))
        if best_match:
            agent_name = best_match.get("agent", "unknown")
            display_map = _build_agent_display_name_map()
            display_name = display_map.get(agent_name, agent_name)
            return (
                "✅ ROUTAGE CONFIRMÉ :\n"
                f"Agent cible : {display_name}\n"
                f"Description : {best_match.get('description', '')}"
            )

        return "⚠️ Aucun routage spécifique trouvé. Adressez-vous à Langis (Master)."
    except Exception as error:
        return f"❌ ERROR lors de la lecture de la matrice : {error}"


@mcp.tool()
def gsane_memory_fetch(agent_name: str, topic: str = "") -> str:
    """Read a constrained excerpt from an agent sidecar memory file."""
    _log_mcp_invocation("gsane_memory_fetch", f"agent={agent_name} topic={topic[:40]}")
    try:
        target_memory = _resolve_agent_memory_file(agent_name)
    except ValueError as error:
        return f"❌ Accès refusé : {error}"

    if not target_memory.exists():
        return f"ℹ️ Aucune mémoire persistante trouvée pour l'agent '{agent_name}'."

    try:
        lines = target_memory.read_text(encoding="utf-8").splitlines(keepends=True)
        if not topic:
            excerpt = "".join(lines[:15])
            if len(lines) > 15:
                excerpt += "\n... [Tronqué — précisez 'topic' pour chercher plus loin]"
            return excerpt

        normalized_topic = topic.lower()
        matches: list[str] = []
        for index, line in enumerate(lines):
            if normalized_topic in line.lower():
                start = max(0, index - 1)
                end = min(len(lines), index + 2)
                context = "".join(lines[start:end]).strip()
                if context and context not in matches:
                    matches.append(context)

        if matches:
            found = "\n---\n".join(matches[:5])
            if len(matches) > 5:
                found += "\n... [Plusieurs autres correspondances trouvées]"
            return f"🔍 Mémoires pour '{topic}' (Agent: {agent_name}):\n\n{found}"

        return f"ℹ️ Aucune mémoire trouvée concernant '{topic}' pour {agent_name}."
    except Exception as error:
        return f"❌ ERROR lors de l'accès à la mémoire : {error}"


@mcp.tool()
def gsane_search_memory(query: str, scope: str = "all") -> str:
    """Search markdown memory files filtered by scope (all, sessions, failures, decisions)."""
    _log_mcp_invocation("gsane_search_memory", f"query={query[:60]} scope={scope}")
    scope_map: dict[str, list[str]] = {
        "failures": ["failure-museum.md"],
        "decisions": ["decision-log.md"],
        "sessions": ["session-analysis-log.md"],
    }

    results: list[str] = []
    normalized_query = query.lower()

    for path in _iter_memory_markdown_files():
        if scope != "all" and scope in scope_map and path.name not in scope_map[scope]:
            continue

        content = _read_text_or_none(path)
        if content is None or normalized_query not in content.lower():
            continue

        lines = content.splitlines()
        for i, line in enumerate(lines):
            if normalized_query in line.lower():
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                snippet = "\n".join(lines[start:end])
                entry = f"[{_relative_project_path(path)}]\n{snippet}"
                if entry not in results:
                    results.append(entry)
                if len(results) >= 5:
                    break
        if len(results) >= 5:
            break

    if not results:
        return f"Aucun résultat pour '{query}' dans {scope}."
    return f"Résultats pour '{query}' dans {scope}:\n" + "\n---\n".join(results[:5])


@mcp.tool()
def gsane_list_agents(filter_capability: str = "") -> str:
    """List registered agents, optionally filtered by capability keyword."""
    _log_mcp_invocation("gsane_list_agents", f"filter={filter_capability[:40]}")
    agents = _read_yaml_or_default(_agent_manifest_path(), [])
    if not isinstance(agents, list):
        return "❌ agent-manifest.yaml invalide."

    results: list[str] = []
    normalized_filter = filter_capability.lower()

    for entry in agents:
        if not isinstance(entry, dict):
            continue
        if normalized_filter:
            capabilities = str(entry.get("capabilities", "")).lower()
            role = str(entry.get("role", "")).lower()
            if normalized_filter not in capabilities and normalized_filter not in role:
                continue
        name = entry.get("name", "unknown")
        display = entry.get("displayName", name)
        icon = entry.get("icon", "")
        role = entry.get("role", "")
        results.append(f"{icon} **{display}** ({name}) — {role}")

    if not results:
        return f"Aucun agent trouvé pour le filtre '{filter_capability}'."
    return "AGENTS ENREGISTRÉS :\n" + "\n".join(results)


STANDARD_EVENT_TYPES = (
    "delivery_contract_created",
    "delivery_contract_approved",
    "qa_gate_passed",
    "qa_gate_failed",
    "handoff_initiated",
    "session_milestone",
)


@mcp.tool()
def gsane_emit_event(event_type: str, agent: str, payload: dict | None = None, task_id: str = "") -> str:
    """Emit a structured event to the trace log for observability."""
    _log_mcp_invocation("gsane_emit_event", f"type={event_type} agent={agent}")
    warning = ""
    if event_type not in STANDARD_EVENT_TYPES:
        warning = f" ⚠️ event_type '{event_type}' non-standard."
    if payload is None:
        payload = {}
    try:
        import json as _json

        trace_file = ensure_path_within_roots(MEMORY_DIR / "trace.log", ALLOWED_MCP_ROOTS)
        safe_details = _escape_yaml_details(_json.dumps(payload, ensure_ascii=False))
        ts = datetime.now().isoformat()
        effective_task_id = task_id or "custom_event"
        entry = (
            f"- timestamp: {ts}\n"
            f"  session_id: mcp\n"
            f"  event: {event_type}\n"
            f"  agent: {agent}\n"
            f"  task_id: {effective_task_id}\n"
            f"  duration_ms: 0\n"
            f"  trust_score: null\n"
            f'  details: "{safe_details}"\n'
        )
        with trace_file.open("a", encoding="utf-8") as handle:
            handle.write(entry)
        return f"✅ Événement '{event_type}' émis par {agent} à {ts}.{warning}"
    except OSError as error:
        return f"❌ Erreur d'écriture trace : {error}"


@mcp.tool()
def gsane_trace_report() -> str:
    """Generate a structured Markdown report from trace.log."""
    _log_mcp_invocation("gsane_trace_report", "")
    trace_file = MEMORY_DIR / "trace.log"
    if not trace_file.exists():
        return "ℹ️ Aucun trace.log trouvé."

    try:
        content = trace_file.read_text(encoding="utf-8", errors="replace")
        entries = yaml.safe_load(content)
        if not isinstance(entries, list):
            raise ValueError("Not a list")
    except Exception:
        # Fallback regex
        import re

        agents = re.findall(r"  agent: (.+)", content)
        events = re.findall(r"  event: (.+)", content)
        scores = [int(x) for x in re.findall(r"  trust_score: (\d+)", content)]
        avg = round(sum(scores) / len(scores), 1) if scores else "N/A"
        agent_counts: dict[str, int] = {}
        for a in agents:
            a = a.strip()
            agent_counts[a] = agent_counts.get(a, 0) + 1
        lines = [
            "# 📊 GSANE Trace Report",
            "",
            "⚠️ Parsing YAML échoué — rapport partiel",
            "",
            f"- Events total : {len(events)}",
            f"- Trust score moyen : {avg}",
            f"- HUP rouge : {events.count('hup_rouge')}",
            f"- HUP jaune : {events.count('hup_jaune')}",
            f"- Circuit breakers : {events.count('circuit_breaker_triggered')}",
        ]
        return "\n".join(lines)

    agent_data: dict[str, dict] = {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        a = str(e.get("agent", "?")).strip()
        if a not in agent_data:
            agent_data[a] = {"count": 0, "scores": []}
        agent_data[a]["count"] += 1
        ts = e.get("trust_score")
        if ts is not None and str(ts).isdigit():
            agent_data[a]["scores"].append(int(ts))

    events_list = [str(e.get("event", "")) for e in entries if isinstance(e, dict)]
    timestamps = [e.get("timestamp", "") for e in entries if isinstance(e, dict)]
    first_ts = timestamps[0] if timestamps else "?"
    last_ts = timestamps[-1] if timestamps else "?"

    lines = [
        f"# 📊 GSANE Trace Report — {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Activité globale",
        f"- Events total : {len(entries)}",
        f"- Période : {first_ts} → {last_ts}",
        "",
        "## Top Agents",
        "| Agent | Events | Trust Score Moyen |",
        "|-------|--------|-------------------|",
    ]
    for a, d in sorted(agent_data.items(), key=lambda x: -x[1]["count"]):
        avg = round(sum(d["scores"]) / len(d["scores"]), 1) if d["scores"] else "N/A"
        lines.append(f"| {a} | {d['count']} | {avg} |")

    lines.extend(
        [
            "",
            "## Alertes",
            f"- HUP Rouge : {events_list.count('hup_rouge')}",
            f"- HUP Jaune : {events_list.count('hup_jaune')}",
            f"- Circuit Breakers : {events_list.count('circuit_breaker_triggered')}",
            f"- Huddles ouverts : {events_list.count('huddle_opened')}",
            "",
            "## Events P2P",
            f"- Messages P2P : {events_list.count('p2p_message_sent')}",
            "",
            "## Derniers 5 events",
        ]
    )
    for e in entries[-5:]:
        if isinstance(e, dict):
            ts = e.get("timestamp", "?")
            ag = e.get("agent", "?")
            ev = e.get("event", "?")
            det = str(e.get("details", ""))[:60]
            lines.append(f"- {ts} | {ag} | {ev} | {det}")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("--- RUNNING MANUAL TEST ---")
        print(gsane_fetch_compressed_memory("failure"))
        print("---")
        print(gsane_route("implement a new feature"))
    else:
        mcp.run()
