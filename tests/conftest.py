"""Fixtures partagées pour les tests agentiques GSANE."""

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, "_gsane/mcp-server")


# ─── Fixtures trace.log ───────────────────────


@pytest.fixture(scope="session")
def trace_events():
    """Charge tous les events de trace.log."""
    trace = Path("_gsane/_memory/trace.log")
    if not trace.exists():
        return []
    try:
        content = trace.read_text(encoding="utf-8", errors="replace")
        return yaml.safe_load(content) or []
    except Exception:
        return []


@pytest.fixture(scope="session")
def trace_by_session(trace_events):
    """Groupe les events par session_id."""
    sessions: dict[str, list] = {}
    for e in trace_events:
        if not isinstance(e, dict):
            continue
        sid = e.get("session_id", "unknown")
        sessions.setdefault(sid, []).append(e)
    return sessions


@pytest.fixture(scope="session")
def challenge_events(trace_events):
    return [e for e in trace_events if isinstance(e, dict) and e.get("event") == "challenge_issued"]


@pytest.fixture(scope="session")
def qa_gate_events(trace_events):
    return [
        e
        for e in trace_events
        if isinstance(e, dict) and e.get("event") in ["qa_gate_passed", "qa_gate_failed"]
    ]


# ─── Fixtures routing ─────────────────────────


@pytest.fixture(scope="session")
def routing_oracle():
    """Source de vérité pour le routing attendu, basée sur delegation-matrix.yaml."""
    return {
        "implement a new feature": "amelia",
        "code the function": "amelia",
        "code this story": "amelia",
        "design the system architecture": "winston",
        "design a scalable API": "winston",
        "test the coverage": "quinn",
        "validate the coverage": "quinn",
        "create a new GSANE agent": "bond",
        "build the agent persona": "bond",
        "help me": "langis",
        "what should I do": "langis",
        "bonjour": "langis",
    }


# ─── Fixtures session state ───────────────────


@pytest.fixture(scope="session")
def session_log():
    """Charge session-analysis-log.md."""
    log = Path("_gsane/_memory/sessions/session-analysis-log.md")
    if not log.exists():
        return ""
    return log.read_text(encoding="utf-8", errors="replace")


@pytest.fixture(scope="session")
def flywheel_history():
    """Charge flywheel-history.md."""
    hist = Path("_gsane/_memory/flywheel-history.md")
    if not hist.exists():
        return ""
    return hist.read_text(encoding="utf-8", errors="replace")


@pytest.fixture(scope="session")
def gsane_config():
    """Charge config.yaml."""
    return yaml.safe_load(Path("_gsane/config.yaml").read_text(encoding="utf-8"))
