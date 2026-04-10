import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "_gsane" / "tools"))

from security_gate import (  # type: ignore[import-not-found]  # noqa: E402
    classify_security_request,
    ensure_path_within_roots,
    get_allowed_mcp_roots,
    get_dependency_sources,
    get_reevaluation_thresholds,
    is_allowed_mcp_agent_name,
    load_security_gate_config,
)


def test_security_gate_has_expected_owner_gate_and_master_escalation():
    config = load_security_gate_config()
    assert config["owner"] == "Winston (Architect)"
    assert config["validation_agent"] == "Quinn (QA)"
    assert config["escalation_agent"] == "Langis (Master)"


def test_security_gate_classifies_security_requests_without_creating_new_agent_route():
    result = classify_security_request("hardening auth tokens and filesystem access")
    assert result.is_security_request is True
    assert result.owner == "Winston (Architect)"
    assert result.validation_agent == "Quinn (QA)"
    assert result.escalation_agent == "Langis (Master)"
    assert "auth" in result.matched_topics


def test_bond_review_is_conditional_only_on_critical_surface_keywords():
    normal_security = classify_security_request("improve auth token handling")
    critical_surface = classify_security_request(
        "GSANE MCP sandbox guardrail policy hardening"
    )

    assert normal_security.bond_review_required is False
    assert critical_surface.bond_review_required is True
    assert critical_surface.bond_review_agent == "bond"


def test_dependency_sources_point_to_real_repo_files():
    sources = get_dependency_sources()
    assert sources, "Aucune source de dépendances configurée"
    for source in sources:
        assert source.is_file(), f"Source de dépendances absente: {source}"


def test_security_gate_has_measurable_reevaluation_thresholds():
    thresholds = get_reevaluation_thresholds()
    required_keys = {
        "security_requests_30d",
        "bond_reviews_per_sprint",
        "blocking_escalation_sprints",
        "coordination_cost_points",
    }
    assert required_keys.issubset(thresholds.keys())
    for key in required_keys:
        assert isinstance(thresholds[key], int)
        assert thresholds[key] > 0


def test_allowed_mcp_roots_confine_paths():
    roots = get_allowed_mcp_roots()
    allowed = REPO_ROOT / "_gsane" / "_memory" / "sessions" / "session-state.md"
    outside = REPO_ROOT.parent / "escape.txt"

    assert ensure_path_within_roots(allowed, roots) == allowed.resolve()
    with pytest.raises(ValueError):
        ensure_path_within_roots(outside, roots)


def test_allowed_mcp_agent_names_are_explicit():
    assert is_allowed_mcp_agent_name("master") is True
    assert is_allowed_mcp_agent_name("../../master") is False
