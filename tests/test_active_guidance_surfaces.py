import json
import re
from pathlib import Path

import yaml  # type: ignore[import-untyped]

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE_GUIDANCE_FILES = [
    ".github/copilot-instructions.md",
    ".github/prompts/gsane-session-bootstrap.prompt.md",
    ".github/prompts/gsane-editorial-review-prose.prompt.md",
    ".github/prompts/gsane-editorial-review-structure.prompt.md",
    ".github/prompts/gsane-index-docs.prompt.md",
    ".github/prompts/gsane-review-adversarial-general.prompt.md",
    ".github/prompts/gsane-review-edge-case-hunter.prompt.md",
    ".github/prompts/gsane-shard-doc.prompt.md",
    ".github/prompts/gsane-smart-router.prompt.md",
    ".github/prompts/gsane-health-check.prompt.md",
    ".github/skills/agent-customization/SKILL.md",
    ".github/skills/agent-design-patterns/SKILL.md",
    ".github/skills/cognitive-flywheel/SKILL.md",
    ".github/skills/gsane-framework/SKILL.md",
    "_gsane/agents/master.md",
    "_gsane/agents/architect.md",
    "_gsane/_config/gsane-help.yaml",
    "_gsane/_config/ides/github-copilot.yaml",
    "_gsane/workflows/flywheel/workflow-aggregate.md",
]
FORBIDDEN_PATTERNS = [
    ("legacy core path", re.compile(r"_gsane/core/", re.IGNORECASE)),
    ("legacy workflow engine", re.compile(r"workflow\.xml", re.IGNORECASE)),
    ("legacy manifest CSV", re.compile(r"(?:agent|workflow)-manifest\.csv", re.IGNORECASE)),
    ("retired agent/persona name", re.compile(r"\b(?:Carson|Mary|John|Bob|Morgan|Wendy|Murat|Aria)\b", re.IGNORECASE)),
    ("retired optimizer alias", re.compile(r"\boptimizer\b", re.IGNORECASE)),
    ("retired strategy route", re.compile(r"\banalyst\+pm\+architect\b", re.IGNORECASE)),
    (
        "retired agent activation file",
        re.compile(
            r"_gsane/agents/(?:analyst|pm|sm|ux-designer|tech-writer|quick-flow-solo-dev|morgan|wendy|optimizer|aria|tea)\.md",
            re.IGNORECASE,
        ),
    ),
    ("invalid party-mode agent alias", re.compile(r"\bparty-mode facilitator\b", re.IGNORECASE)),
]


def read_text(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def load_yaml(rel_path: str):
    return yaml.safe_load(read_text(rel_path))


def load_json(rel_path: str):
    return json.loads(read_text(rel_path))


def test_active_guidance_surfaces_do_not_reference_legacy_runtime_or_agents():
    violations = []

    for rel_path in ACTIVE_GUIDANCE_FILES:
        content = read_text(rel_path)
        for line_number, line in enumerate(content.splitlines(), start=1):
            for label, pattern in FORBIDDEN_PATTERNS:
                if pattern.search(line):
                    violations.append(f"{rel_path}:{line_number} matches {label}")

    assert not violations, "Références legacy trouvées sur les surfaces actives:\n" + "\n".join(violations)


def test_github_copilot_agents_match_active_manifest_exactly():
    manifest = load_yaml("_gsane/_config/agent-manifest.yaml")
    ide_config = load_yaml("_gsane/_config/ides/github-copilot.yaml")

    expected_names = [entry["name"] for entry in manifest if entry.get("status") != "subagent"]
    expected_paths = {entry["name"]: entry["path"] for entry in manifest}

    configured_agents = ide_config["configuration"]["agents"]
    actual_names = [entry["name"] for entry in configured_agents]

    assert actual_names == expected_names

    for entry in configured_agents:
        assert entry["activation_file"] == expected_paths[entry["name"]]
        assert (REPO_ROOT / entry["activation_file"]).is_file()


def test_github_copilot_context_files_are_real_and_not_legacy_paths():
    ide_config = load_yaml("_gsane/_config/ides/github-copilot.yaml")
    context_files = ide_config["configuration"].get("context_files", [])

    for entry in context_files:
        path = entry["path"]
        assert "_gsane/core/" not in path
        assert "workflow.xml" not in path
        assert (REPO_ROOT / path).is_file(), f"Context file absent: {path}"


def test_gsane_help_references_only_active_agents_and_existing_workflows():
    manifest = load_yaml("_gsane/_config/agent-manifest.yaml")
    help_entries = load_yaml("_gsane/_config/gsane-help.yaml")
    valid_agents = {entry["name"] for entry in manifest}

    invalid_agents = []
    missing_workflows = []
    for index, entry in enumerate(help_entries):
        agent_name = entry.get("agent-name")
        workflow_file = entry.get("workflow-file")
        if agent_name and agent_name not in valid_agents:
            invalid_agents.append(f"entry[{index}] agent-name={agent_name}")
        if workflow_file and not (REPO_ROOT / workflow_file).is_file():
            missing_workflows.append(f"entry[{index}] workflow-file={workflow_file}")

    assert not invalid_agents, "Agents invalides dans gsane-help:\n" + "\n".join(invalid_agents)
    assert not missing_workflows, "Workflows manquants dans gsane-help:\n" + "\n".join(missing_workflows)


def test_hooks_json_deprecated_paths_are_specific_to_legacy_roots():
    hooks_config = load_yaml(".github/hooks/hooks.json")
    post_tool_use = next(hook for hook in hooks_config["hooks"] if hook["event"] == "PostToolUse")
    deprecated_paths = hooks_config["config"]["deprecatedPaths"]

    assert "Aria" not in post_tool_use["description"]
    assert "_gsane/" not in deprecated_paths
    assert "_gsane/core/" in deprecated_paths
    assert "_tmad/" in deprecated_paths


def test_flywheel_checklist_uses_negative_guard_for_legacy_core_path():
    content = read_text("_gsane/workflows/flywheel/flywheel-test-checklist.md")

    assert "Aucun chemin `_gsane/core/` ni ancien module `bmb` réintroduit dans les fichiers modifiés" in content
    assert "Chemins `_gsane/core/` (pas ancien `bmb`) dans tous les fichiers modifiés" not in content


def test_session_bootstrap_uses_canonical_brief_and_mcp_views():
    content = read_text(".github/prompts/gsane-session-bootstrap.prompt.md")

    assert "gsane_read_canonical_brief()" in content
    assert "gsane_read_active_delivery_contract()" in content
    assert "gsane_read_project_snapshot()" in content
    assert "Lire `{project-root}/_gsane/_memory/sessions/session-state.md`" not in content


def test_vscode_repo_policy_versions_only_extensions_json():
    gitignore = read_text(".gitignore")

    assert (REPO_ROOT / ".vscode" / "extensions.json").is_file()
    assert ".vscode/*" in gitignore
    assert "!.vscode/extensions.json" in gitignore


def test_precommit_and_cli_validate_nested_yaml_config_tree():
    pre_commit = read_text(".github/hooks/pre-commit.sh")
    cli = read_text("gsane.sh")
    expected = 'Path("_gsane/_config").rglob("*.yaml")'

    assert expected in pre_commit
    assert expected in cli


def test_bond_validation_workflow_exists_and_is_manifested():
    workflow_manifest = load_yaml("_gsane/_config/workflow-manifest.yaml")
    bond_content = read_text("_gsane/agents/bond.md")

    workflow_entry = next(
        (entry for entry in workflow_manifest if entry.get("path") == "_gsane/workflows/workflow-validate-agent.md"),
        None,
    )

    assert workflow_entry is not None
    assert workflow_entry["agent"] == "bond"
    assert (REPO_ROOT / workflow_entry["path"]).is_file()
    assert "_gsane/workflows/workflow-validate-agent.md" in bond_content
