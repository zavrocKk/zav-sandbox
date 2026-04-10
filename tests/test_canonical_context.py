from pathlib import Path

import yaml  # type: ignore[import-untyped]

REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def test_project_context_is_a_short_canonical_human_brief():
    content = read_text("_gsane/_memory/project-context.md")

    required_headings = [
        "## 1. Cap du Projet",
        "## 2. Invariants de Fonctionnement",
        "## 3. Carte des Sources de Vérité (Ordre de Lecture)",
        "## 4. Règles d'Usage Humain",
        "## 5. Politique de Migration & Règles de Mise à Jour",
    ]
    for heading in required_headings:
        assert heading in content

    for forbidden_token in (
        "last_session_date",
        "last_agent_active",
        "last_workflow_run",
        "plan_active",
        "next_step",
        "active_branch",
    ):
        assert forbidden_token not in content


def test_master_and_bootstrap_use_canonical_brief_and_mcp_views():
    master = read_text("_gsane/agents/master.md")
    bootstrap = read_text(".github/prompts/gsane-session-bootstrap.prompt.md")

    for token in (
        "gsane_read_canonical_brief()",
        "gsane_read_active_delivery_contract()",
        "gsane_read_project_snapshot()",
    ):
        assert token in master
        assert token in bootstrap

    assert "Load _gsane/_memory/sessions/session-state.md — extract" not in master
    assert "Lire `{project-root}/_gsane/_memory/sessions/session-state.md`" not in bootstrap


def test_session_files_are_formally_marked_as_audit_continuity():
    manifest = yaml.safe_load(read_text("_gsane/_config/manifest.yaml"))
    runtime = manifest.get("runtime") or {}
    audit_continuity = ((runtime.get("audit_continuity") or {}).get("files") or [])

    assert "_gsane/_memory/sessions/session-state.md" in audit_continuity
    assert "_gsane/_memory/sessions/session-analysis-log.md" in audit_continuity

    workflow_manifest_text = read_text("_gsane/_config/workflow-manifest.yaml").lower()
    psa_text = read_text("_gsane/workflows/post-session-analysis/workflow.md").lower()

    assert "audit/continuity" in workflow_manifest_text or "audit/continuité" in workflow_manifest_text
    assert "audit/continuité" in psa_text
    assert "not a source of truth" in psa_text or "not a source of truth" in workflow_manifest_text or "not current project truth" in psa_text
