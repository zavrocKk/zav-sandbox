import glob
import os
import re
import sys
import unicodedata
from pathlib import Path

import pytest
import yaml  # type: ignore[import-untyped]

REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
README_LEGACY_PATTERNS = {
    "CIS": re.compile(r"\bcis\b"),
    "TEA": re.compile(r"\btea\b"),
    "BMB": re.compile(r"\bbmb\b"),
    "Léo": re.compile(r"\bleo\b"),
    "Aria": re.compile(r"\baria\b"),
    "Morgan": re.compile(r"\bmorgan\b"),
    "Wendy": re.compile(r"\bwendy\b"),
    "gsane-master": re.compile(r"\bgsane-master\b"),
    "party-mode": re.compile(r"\bparty-mode\b"),
}

AGENT_REQUIRED_SECTIONS = [
    "## Identity",
    "## Activation",
    "## Voice",
    "## Workflow opérationnel",
    "## Handoff Protocol",
    "## Never Do",
    "## Golden Rule",
    "## Escalation",
]


def normalize_legacy_text(text):
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(
        character for character in normalized if not unicodedata.combining(character)
    ).casefold()


def collect_readme_legacy_hits():
    hits = []
    with README_PATH.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            normalized_line = normalize_legacy_text(line)
            for label, pattern in README_LEGACY_PATTERNS.items():
                if pattern.search(normalized_line):
                    hits.append((line_no, label, line.rstrip()))
    return hits


def check_readme_legacy_refs():
    hits = collect_readme_legacy_hits()
    for line_no, label, line in hits:
        print(
            f"[FAIL] README.md:{line_no}: référence legacy trouvée — '{label}' | {line}"
        )
    return len(hits)


def test_no_legacy_refs_in_readme():
    hits = collect_readme_legacy_hits()
    if hits:
        details = "\n".join(
            f"- README.md:{line_no}: '{label}' | {line}"
            for line_no, label, line in hits
        )
        pytest.fail("Références legacy trouvées dans README.md:\n" + details)

def check_file(path):
    errors = 0
    with open(path, encoding='utf-8') as f:
        content = f.read()

    if '{{project_name}}' in content:
        print(f'[FAIL] {path}: Found forbidden macro {{project_name}}')
        errors += 1

    if '{project-root}' in content:
        print(f'[FAIL] {path}: Found forbidden pseudo-variable {{project-root}}')
        errors += 1

    if '<menu>' in content:
        print(f'[FAIL] {path}: Found forbidden legacy <menu> tag (Zero-Touch architecture violation)')
        errors += 1

    if re.search(r'\b(cis|tea|bmb)/', content, re.IGNORECASE):
        print(f'[FAIL] {path}: Found forbidden legacy module path (cis/, tea/, bmb/ are deprecated)')
        errors += 1

    return errors

# ──────────────────────────────────────────────────────────────
# 1b — Legacy terms scanner
# ──────────────────────────────────────────────────────────────

LEGACY_TERMS = [
    "léo", "leo (optimizer)", "aria (compliance)", "aria (aria)",
    "murat", "wendy", "morgan", "carson", "_gsane/core/",
    "agent-manifest.csv", "workflow-manifest.csv",
    "gsane-creative-intelligence-suite", "gsane-method-test-architecture",
    "gsane-builder-module-builder",
    "EXPECTED_AGENTS=25", "expected_agents=25",
]

LEGACY_SCAN_FILES = [
    ".github/hooks/session-start.sh",
    ".github/hooks/session-stop.sh",
    ".github/hooks/flywheel-trigger.sh",
    "_gsane/_config/manifest.yaml",
    "_gsane/_config/gsane-help.yaml",
    "_gsane/workflows/flywheel/workflow-aggregate.md",
    "_gsane/workflows/flywheel/workflow-apply.md",
    "_gsane/_memory/sessions/session-analysis-log.md",
    "gsane.sh",
]

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

ACTIVE_GUIDANCE_FORBIDDEN_PATTERNS = [
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

CANONICAL_BRIEF_REQUIRED_HEADINGS = [
    "1. Cap du Projet",
    "2. Invariants de Fonctionnement",
    "3. Carte des Sources de Vérité (Ordre de Lecture)",
    "4. Règles d'Usage Humain",
    "5. Politique de Migration & Règles de Mise à Jour",
]

CANONICAL_BRIEF_FORBIDDEN_TOKENS = [
    "last_session_date",
    "last_agent_active",
    "last_workflow_run",
    "plan_active",
    "next_step",
    "active_branch",
]


def check_legacy_references(files_to_scan):
    """Scan files for forbidden legacy terms. Returns list of (file, line_no, term)."""
    hits = []
    for filepath in files_to_scan:
        try:
            with open(filepath, encoding="utf-8") as fh:
                for line_no, line in enumerate(fh, start=1):
                    low = line.lower()
                    for term in LEGACY_TERMS:
                        if term.lower() in low:
                            hits.append((filepath, line_no, term))
        except (OSError, UnicodeDecodeError):
            pass
    return hits


def load_yaml_file(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def check_active_guidance_surfaces():
    """Block legacy runtime references on prompts, skills, and active IDE/help config."""
    errors = 0

    for filepath in ACTIVE_GUIDANCE_FILES:
        if not os.path.isfile(filepath):
            print(f"[FAIL] {filepath}: surface active introuvable")
            errors += 1
            continue

        with open(filepath, encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, start=1):
                for label, pattern in ACTIVE_GUIDANCE_FORBIDDEN_PATTERNS:
                    if pattern.search(line):
                        print(f"[FAIL] {filepath}:{line_no}: {label}")
                        errors += 1

    return errors


def check_github_copilot_alignment():
    """Ensure the active IDE config exposes only the 5 current agents and real files."""
    errors = 0
    manifest_path = "_gsane/_config/agent-manifest.yaml"
    ide_path = "_gsane/_config/ides/github-copilot.yaml"

    if not os.path.isfile(manifest_path) or not os.path.isfile(ide_path):
        print("[FAIL] github-copilot alignment: fichiers manifest/config absents")
        return 1

    manifest = load_yaml_file(manifest_path) or []
    ide_config = load_yaml_file(ide_path) or {}

    expected_agents = [entry.get("name") for entry in manifest if entry.get("status") != "subagent"]
    expected_paths = {entry.get("name"): entry.get("path") for entry in manifest}

    configuration = ide_config.get("configuration", {})
    actual_agents = configuration.get("agents", [])
    actual_names = [entry.get("name") for entry in actual_agents]

    if actual_names != expected_agents:
        print(
            f"[FAIL] {ide_path}: agents exposes {actual_names} au lieu de {expected_agents}"
        )
        errors += 1

    for entry in actual_agents:
        name = entry.get("name")
        activation_file = entry.get("activation_file")
        if expected_paths.get(name) != activation_file:
            print(
                f"[FAIL] {ide_path}: activation_file pour '{name}' = '{activation_file}', attendu '{expected_paths.get(name)}'"
            )
            errors += 1
        if activation_file and not os.path.isfile(activation_file):
            print(f"[FAIL] {ide_path}: activation_file absent '{activation_file}'")
            errors += 1

    for entry in configuration.get("context_files", []):
        path = entry.get("path", "")
        if path and not os.path.isfile(path):
            print(f"[FAIL] {ide_path}: context file absent '{path}'")
            errors += 1
        if "_gsane/core/" in path or "workflow.xml" in path:
            print(f"[FAIL] {ide_path}: chemin legacy dans context_files '{path}'")
            errors += 1

    return errors


def check_gsane_help_agent_names():
    """Ensure active help entries only reference valid active agent names and real workflows."""
    errors = 0
    manifest_path = "_gsane/_config/agent-manifest.yaml"
    help_path = "_gsane/_config/gsane-help.yaml"

    if not os.path.isfile(manifest_path) or not os.path.isfile(help_path):
        print("[FAIL] gsane-help alignment: fichiers manifest/help absents")
        return 1

    valid_agents = {
        entry.get("name")
        for entry in (load_yaml_file(manifest_path) or [])
        if entry.get("name")
    }

    for index, entry in enumerate(load_yaml_file(help_path) or []):
        agent_name = entry.get("agent-name")
        workflow_file = entry.get("workflow-file")
        if agent_name and agent_name not in valid_agents:
            print(
                f"[FAIL] {help_path}: entree[{index}] agent-name='{agent_name}' n'est pas un agent actif"
            )
            errors += 1
        if workflow_file and not os.path.isfile(workflow_file):
            print(
                f"[FAIL] {help_path}: entree[{index}] workflow-file absent '{workflow_file}'"
            )
            errors += 1

    return errors


def check_hooks_json_config():
    """Ensure hooks.json uses generic PostToolUse wording and specific legacy roots only."""
    errors = 0
    hooks_path = ".github/hooks/hooks.json"

    if not os.path.isfile(hooks_path):
        print(f"[FAIL] {hooks_path}: fichier hooks absent")
        return 1

    hooks_config = load_yaml_file(hooks_path) or {}
    hooks = hooks_config.get("hooks") or []
    deprecated_paths = ((hooks_config.get("config") or {}).get("deprecatedPaths") or [])

    post_tool_use = next((hook for hook in hooks if hook.get("event") == "PostToolUse"), None)
    description = (post_tool_use or {}).get("description", "")

    if "Aria" in description:
        print(f"[FAIL] {hooks_path}: PostToolUse reference encore Aria")
        errors += 1

    if "_gsane/" in deprecated_paths:
        print(f"[FAIL] {hooks_path}: deprecatedPaths contient '_gsane/' trop large pour le flat-design")
        errors += 1

    for expected_path in ("_gsane/core/", "_tmad/"):
        if expected_path not in deprecated_paths:
            print(f"[FAIL] {hooks_path}: deprecatedPaths doit contenir '{expected_path}'")
            errors += 1

    return errors


def check_flywheel_checklist_guard():
    """Ensure the regression checklist explicitly bans the legacy core path in negative form."""
    errors = 0
    checklist_path = "_gsane/workflows/flywheel/flywheel-test-checklist.md"

    if not os.path.isfile(checklist_path):
        print(f"[FAIL] {checklist_path}: checklist introuvable")
        return 1

    with open(checklist_path, encoding="utf-8") as fh:
        content = fh.read()
    expected_guard = "Aucun chemin `_gsane/core/` ni ancien module `bmb` réintroduit dans les fichiers modifiés"
    legacy_guard = "Chemins `_gsane/core/` (pas ancien `bmb`) dans tous les fichiers modifiés"

    if expected_guard not in content:
        print(f"[FAIL] {checklist_path}: garde negative `_gsane/core/` absente ou incorrecte")
        errors += 1
    if legacy_guard in content:
        print(f"[FAIL] {checklist_path}: ancienne garde `_gsane/core/` encore presente")
        errors += 1

    return errors


def check_security_gate_alignment():
    """Ensure the declarative security gate exists and points to real repo surfaces."""
    errors = 0
    matrix_path = "_gsane/_config/delegation-matrix.yaml"

    if not os.path.isfile(matrix_path):
        print(f"[FAIL] {matrix_path}: delegation matrix absente")
        return 1

    matrix = load_yaml_file(matrix_path) or {}
    gate = matrix.get("security_gate") or {}

    expected_scalars = {
        "owner": "Winston (Architect)",
        "validation_agent": "Quinn (QA)",
        "escalation_agent": "Langis (Master)",
    }
    for key, expected in expected_scalars.items():
        if gate.get(key) != expected:
            print(f"[FAIL] {matrix_path}: security_gate.{key}='{gate.get(key)}' attendu '{expected}'")
            errors += 1

    dependency_sources = ((gate.get("dependency_sources") or {}).get("python") or [])
    if not dependency_sources:
        print(f"[FAIL] {matrix_path}: security_gate.dependency_sources.python vide")
        errors += 1
    for rel_path in dependency_sources:
        if not os.path.isfile(rel_path):
            print(f"[FAIL] {matrix_path}: source de dépendances absente '{rel_path}'")
            errors += 1

    bond_keywords = ((gate.get("bond_review") or {}).get("required_keywords") or [])
    for required_keyword in ("gsane", "policy", "guardrail", "mcp", "hook", "manifest"):
        if required_keyword not in bond_keywords:
            print(f"[FAIL] {matrix_path}: mot-clé Bond manquant '{required_keyword}'")
            errors += 1

    thresholds = gate.get("reevaluation_thresholds") or {}
    required_thresholds = (
        "security_requests_30d",
        "bond_reviews_per_sprint",
        "blocking_escalation_sprints",
        "coordination_cost_points",
    )
    for threshold in required_thresholds:
        value = thresholds.get(threshold)
        if not isinstance(value, int) or value <= 0:
            print(f"[FAIL] {matrix_path}: seuil de réévaluation invalide '{threshold}'={value}")
            errors += 1

    allowed_roots = ((gate.get("mcp") or {}).get("allowed_roots") or [])
    for rel_path in allowed_roots:
        if not os.path.isdir(rel_path):
            print(f"[FAIL] {matrix_path}: racine MCP absente '{rel_path}'")
            errors += 1

    return errors


def check_canonical_runtime_alignment():
    """Ensure the canonical brief and runtime surfaces follow the new source-of-truth model."""
    errors = 0

    brief_path = "_gsane/_memory/project-context.md"
    if not os.path.isfile(brief_path):
        print(f"[FAIL] {brief_path}: brief canonique introuvable")
        return 1

    with open(brief_path, encoding="utf-8") as fh:
        brief_content = fh.read()

    for heading in CANONICAL_BRIEF_REQUIRED_HEADINGS:
        if f"## {heading}" not in brief_content:
            print(f"[FAIL] {brief_path}: heading canonique manquant '{heading}'")
            errors += 1

    for token in CANONICAL_BRIEF_FORBIDDEN_TOKENS:
        if token in brief_content:
            print(f"[FAIL] {brief_path}: token mutable interdit trouve '{token}'")
            errors += 1

    runtime_files = {
        "_gsane/agents/master.md": [
            "gsane_read_canonical_brief()",
            "gsane_read_active_delivery_contract()",
            "gsane_read_project_snapshot()",
        ],
        ".github/prompts/gsane-session-bootstrap.prompt.md": [
            "gsane_read_canonical_brief()",
            "gsane_read_active_delivery_contract()",
            "gsane_read_project_snapshot()",
        ],
    }
    for filepath, required_tokens in runtime_files.items():
        if not os.path.isfile(filepath):
            print(f"[FAIL] {filepath}: surface runtime introuvable")
            errors += 1
            continue
        with open(filepath, encoding="utf-8") as fh:
            content = fh.read()
        for token in required_tokens:
            if token not in content:
                print(f"[FAIL] {filepath}: vue MCP canonique manquante '{token}'")
                errors += 1

    bootstrap_path = ".github/prompts/gsane-session-bootstrap.prompt.md"
    if os.path.isfile(bootstrap_path):
        with open(bootstrap_path, encoding="utf-8") as fh:
            bootstrap_content = fh.read()
        legacy_line = "Lire `{project-root}/_gsane/_memory/sessions/session-state.md`"
        if legacy_line in bootstrap_content:
            print(f"[FAIL] {bootstrap_path}: session-state.md encore lu comme etat actif")
            errors += 1

    manifest_path = "_gsane/_config/manifest.yaml"
    manifest = load_yaml_file(manifest_path) or {}
    runtime = manifest.get("runtime") or {}
    audit_continuity = (runtime.get("audit_continuity") or {}).get("files") or []
    for required_file in (
        "_gsane/_memory/sessions/session-state.md",
        "_gsane/_memory/sessions/session-analysis-log.md",
    ):
        if required_file not in audit_continuity:
            print(f"[FAIL] {manifest_path}: fichier d'audit non classe '{required_file}'")
            errors += 1

    return errors


# ──────────────────────────────────────────────────────────────
# 1b — Hooks check
# ──────────────────────────────────────────────────────────────

def check_hooks():
    """Vérifie que les hooks ne référencent pas _gsane/core/ et ont les bons chemins."""
    errors = 0
    hooks = {
        ".github/hooks/session-start.sh": {
            "must_contain": "_gsane/config.yaml",
            "must_not_contain": "_gsane/core/",
        },
        ".github/hooks/session-stop.sh": {
            "must_contain": "_gsane/workflows/",
            "must_not_contain": "_gsane/core/",
        },
        ".github/hooks/flywheel-trigger.sh": {
            "must_contain": "_gsane/workflows/",
            "must_not_contain": "_gsane/core/",
        },
    }
    for hook_path, rules in hooks.items():
        if not os.path.isfile(hook_path):
            print(f"[WARN] {hook_path}: fichier absent (skip)")
            continue
        with open(hook_path, encoding="utf-8") as fh:
            content = fh.read()
        if rules["must_contain"] not in content:
            print(f"[FAIL] {hook_path}: manque '{rules['must_contain']}'")
            errors += 1
        if rules["must_not_contain"] in content:
            print(f"[FAIL] {hook_path}: référence legacy '{rules['must_not_contain']}'")
            errors += 1
    return errors


# ──────────────────────────────────────────────────────────────
# 1c — Manifests YAML check
# ──────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────
# 1d — execution-plan.yaml schema validator
# ──────────────────────────────────────────────────────────────

EXECUTION_PLAN_REQUIRED_TOP = ["plan_id", "session_date", "objective", "scope", "tasks"]
EXECUTION_PLAN_REQUIRED_TASK = [
    "id", "description", "owner", "depends_on",
    "parallel_group", "validation_agent",
    "done_definition", "risk_level", "acceptance_criteria",
]
VALID_RISK_LEVELS = {"LOW", "MEDIUM", "HIGH"}


def validate_execution_plan_schema(path):
    """Valide un fichier execution-plan.yaml contre le schéma GSANE Phase 3."""
    errors = 0
    with open(path, encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(f"[FAIL] {path}: YAML parse error — {exc}")
            return 1
    if not isinstance(data, dict):
        print(f"[FAIL] {path}: contenu YAML invalide (doit être un mapping)")
        return 1
    for field in EXECUTION_PLAN_REQUIRED_TOP:
        if field not in data:
            print(f"[FAIL] {path}: champ requis manquant '{field}'")
            errors += 1
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list) or len(tasks) == 0:
        print(f"[FAIL] {path}: 'tasks' doit être une liste non vide")
        errors += 1
    if isinstance(tasks, list) and len(tasks) > 7:
        print(f"[FAIL] {path}: {len(tasks)} tâches — maximum autorisé est 7")
        errors += 1
    for i, task in enumerate(tasks if isinstance(tasks, list) else []):
        for field in EXECUTION_PLAN_REQUIRED_TASK:
            if field not in task:
                print(f"[FAIL] {path}: task[{i}] champ manquant '{field}'")
                errors += 1
        risk = task.get("risk_level", "")
        if risk not in VALID_RISK_LEVELS:
            print(f"[FAIL] {path}: task[{i}].risk_level='{risk}' invalide (LOW|MEDIUM|HIGH attendu)")
            errors += 1
    if errors == 0:
        print(f"[OK]   {path}: schéma execution-plan valide")
    return errors


def check_agent_versioning():
    """Validate semver version, ISO updated_at, and status for all agents in agent-manifest.yaml."""
    errors = 0
    manifest_path = "_gsane/_config/agent-manifest.yaml"

    if not os.path.isfile(manifest_path):
        print(f"[FAIL] {manifest_path}: agent manifest introuvable")
        return 1

    agents = load_yaml_file(manifest_path) or []
    semver_re = re.compile(r"^\d+\.\d+\.\d+$")
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    valid_statuses = {"active", "deprecated", "experimental", "subagent"}

    for agent in agents:
        name = agent.get("name", "<unknown>")

        version = agent.get("version")
        if not version or not semver_re.match(str(version)):
            print(f"[FAIL] {manifest_path}: agent '{name}' version invalide ou absente ('{version}', attendu X.Y.Z)")
            errors += 1

        updated_at = agent.get("updated_at")
        if not updated_at or not date_re.match(str(updated_at)):
            print(f"[FAIL] {manifest_path}: agent '{name}' updated_at invalide ou absent ('{updated_at}', attendu YYYY-MM-DD)")
            errors += 1

        status = agent.get("status")
        if not status or status not in valid_statuses:
            print(f"[FAIL] {manifest_path}: agent '{name}' status invalide ou absent ('{status}', attendu {valid_statuses})")
            errors += 1

    return errors


def check_agent_customize_files():
    """Ensure every agent in agent-manifest.yaml has a matching and minimally-populated .customize.yaml file."""
    errors = 0
    manifest_path = "_gsane/_config/agent-manifest.yaml"
    customize_dir = "_gsane/_config/agents"

    if not os.path.isfile(manifest_path):
        print(f"[FAIL] {manifest_path}: agent manifest introuvable")
        return 1

    agents = load_yaml_file(manifest_path) or []
    for agent in agents:
        name = agent.get("name", "<unknown>")
        status = agent.get("status")
        customize_path = os.path.join(customize_dir, f"{name}.customize.yaml")
        if not os.path.isfile(customize_path):
            print(f"[FAIL] {customize_path}: customize.yaml manquant pour l'agent '{name}'")
            errors += 1
            continue

        customize = load_yaml_file(customize_path)
        if not isinstance(customize, dict):
            print(f"[FAIL] {customize_path}: contenu YAML invalide ou vide")
            errors += 1
            continue

        for required_field in ("agent", "status", "scope", "constraints"):
            if required_field not in customize:
                print(f"[FAIL] {customize_path}: champ obligatoire manquant '{required_field}'")
                errors += 1

        customize_agent = customize.get("agent")
        if customize_agent != name:
            print(f"[FAIL] {customize_path}: champ 'agent'='{customize_agent}' attendu '{name}'")
            errors += 1

        customize_status = customize.get("status")
        if customize_status != status:
            print(f"[FAIL] {customize_path}: champ 'status'='{customize_status}' attendu '{status}'")
            errors += 1

        scope = customize.get("scope")
        if not isinstance(scope, list) or not scope or not all(str(item).strip() for item in scope):
            print(f"[FAIL] {customize_path}: champ 'scope' vide ou invalide")
            errors += 1

        constraints = customize.get("constraints")
        if not isinstance(constraints, dict):
            print(f"[FAIL] {customize_path}: champ 'constraints' vide ou invalide")
            errors += 1
            continue

        required_constraints = {
            "party_mode": bool,
            "delivery_contract_required": bool,
            "read_only": bool,
            "max_files_per_commit": int,
        }
        for constraint_name, expected_type in required_constraints.items():
            if constraint_name not in constraints:
                print(f"[FAIL] {customize_path}: contrainte obligatoire manquante '{constraint_name}'")
                errors += 1
                continue
            value = constraints.get(constraint_name)
            if expected_type is bool:
                if not isinstance(value, bool):
                    print(f"[FAIL] {customize_path}: contrainte '{constraint_name}' doit être booléenne")
                    errors += 1
            elif expected_type is int and (not isinstance(value, int) or value < 0):
                print(f"[FAIL] {customize_path}: contrainte '{constraint_name}' doit être un entier >= 0")
                errors += 1

    return errors


def check_agent_required_sections():
    """Ensure every agent declared in the manifest exposes the 8 required markdown sections."""
    errors = 0
    manifest_path = "_gsane/_config/agent-manifest.yaml"

    if not os.path.isfile(manifest_path):
        print(f"[FAIL] {manifest_path}: agent manifest introuvable")
        return 1

    agents = load_yaml_file(manifest_path) or []
    for agent in agents:
        agent_path = agent.get("path")
        if not agent_path:
            print(f"[FAIL] {manifest_path}: path manquant pour l'agent '{agent.get('name', '<unknown>')}'")
            errors += 1
            continue
        if not os.path.isfile(agent_path):
            print(f"[FAIL] {agent_path}: fichier agent introuvable")
            errors += 1
            continue

        with open(agent_path, encoding="utf-8") as fh:
            content = fh.read()

        for heading in AGENT_REQUIRED_SECTIONS:
            if not re.search(rf"^{re.escape(heading)}\s*$", content, re.MULTILINE):
                print(f"[FAIL] {agent_path}: section manquante '{heading}'")
                errors += 1

    return errors


def check_all_manifests():
    """Charge tous les _gsane/_config/*.yaml et vérifie qu'ils parsent sans erreur."""
    errors = 0
    files = glob.glob("_gsane/_config/*.yaml")
    if not files:
        print("[FAIL] check_all_manifests: aucun fichier YAML trouvé dans _gsane/_config/")
        return 1
    for filepath in files:
        try:
            with open(filepath, encoding="utf-8") as fh:
                content = fh.read()
            yaml.safe_load(content)
        except yaml.YAMLError as exc:
            print(f"[FAIL] {filepath}: erreur de parsing YAML — {exc}")
            errors += 1
            continue
        if "manifest.yaml" in filepath:
            forbidden = ["creative-intelligence-suite", "test-architecture-enterprise"]
            for term in forbidden:
                if term in content:
                    print(f"[FAIL] {filepath}: contient terme déprécié '{term}'")
                    errors += 1
    return errors


def test_master_never_do_delegation_rules():
    """Vérifie que master.md Never Do contient les 6 agents de délégation et les interdictions clés."""
    master_path = REPO_ROOT / "_gsane" / "agents" / "master.md"
    content = master_path.read_text(encoding="utf-8")

    required_agents = ["Amelia", "Quinn", "Winston", "Bond", "Vera", "Sage"]
    missing = [agent for agent in required_agents if agent not in content]
    assert not missing, f"master.md Never Do manque les agents : {missing}"

    assert "delegation-matrix" in content, "master.md doit mentionner la vérification delegation-matrix"
    assert "spécialiste" in content, "master.md doit interdire de produire un output de spécialiste"


def test_delegation_workflow_no_solo():
    """Vérifie que delegation/workflow.md contient la règle orchestrateur pur."""
    workflow_path = REPO_ROOT / "_gsane" / "workflows" / "delegation" / "workflow.md"
    content = workflow_path.read_text(encoding="utf-8")

    assert "orchestrateur pur" in content, "delegation/workflow.md doit contenir 'orchestrateur pur'"
    assert "Delivery Contracts" in content, "delegation/workflow.md doit mentionner les Delivery Contracts comme artefact Langis"
    assert "Exceptions autorisées" in content, "delegation/workflow.md doit lister les exceptions autorisées"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python qa-linter.py <file-to-test>')
        sys.exit(1)

    total_errors = 0
    for target in sys.argv[1:]:
        if os.path.isfile(target):
            total_errors += check_file(target)

    # ── Nouvelles vérifications ──────────────────────────────────
    legacy_hits = check_legacy_references(LEGACY_SCAN_FILES)
    for filepath, line_no, term in legacy_hits:
        print(f"[FAIL] {filepath}:{line_no}: référence legacy trouvée — '{term}'")
        total_errors += 1

    total_errors += check_active_guidance_surfaces()
    total_errors += check_github_copilot_alignment()
    total_errors += check_gsane_help_agent_names()
    total_errors += check_hooks_json_config()
    total_errors += check_flywheel_checklist_guard()
    total_errors += check_security_gate_alignment()
    total_errors += check_canonical_runtime_alignment()
    total_errors += check_readme_legacy_refs()
    total_errors += check_hooks()
    total_errors += check_all_manifests()
    total_errors += check_agent_versioning()
    total_errors += check_agent_customize_files()
    total_errors += check_agent_required_sections()

    # ── Validation schéma execution-plan.yaml ────────────────────
    import glob as _glob
    execution_plans = _glob.glob("_gsane-output/sessions/**/execution-plan.yaml", recursive=True)
    for ep_path in execution_plans:
        total_errors += validate_execution_plan_schema(ep_path)
    # ────────────────────────────────────────────────────────────

    if total_errors > 0:
        print(f'\nQA LINTER FAILED with {total_errors} errors.')
        sys.exit(1)
    else:
        print('\nQA LINTER PASSED. Output is strictly compliant.')
        sys.exit(0)

