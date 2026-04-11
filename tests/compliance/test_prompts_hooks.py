"""Tests compliance — prompts GSANE et hooks PRBodyCheck (DC-PROMPTS-HOOKS-001)."""

from pathlib import Path

import pytest
import yaml as _yaml


@pytest.mark.compliance
def test_new_prompts_exist():
    """Les 7 nouveaux prompts doivent exister."""
    prompts_dir = Path(".github/prompts")
    required = [
        "gsane-challenge.prompt.md",
        "gsane-party-mode.prompt.md",
        "gsane-session-resume.prompt.md",
        "gsane-hypothesis.prompt.md",
        "gsane-mutation.prompt.md",
        "gsane-benchmark.prompt.md",
        "gsane-delegation-audit.prompt.md",
    ]
    missing = [p for p in required if not (prompts_dir / p).exists()]
    assert not missing, "Prompts manquants:\n" + "\n".join(
        f"  - {p}" for p in missing
    )


@pytest.mark.compliance
def test_prompts_have_valid_frontmatter():
    """Tous les prompts doivent avoir description dans le frontmatter."""
    prompts_dir = Path(".github/prompts")
    violations = []
    for f in sorted(prompts_dir.glob("*.prompt.md")):
        content = f.read_text(encoding="utf-8")
        if not content.startswith("---"):
            violations.append(f"{f.name}: pas de frontmatter")
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            violations.append(f"{f.name}: frontmatter incomplet")
            continue
        try:
            fm = _yaml.safe_load(parts[1])
        except Exception as e:
            violations.append(f"{f.name}: YAML invalide ({e})")
            continue
        if not fm or "description" not in fm:
            violations.append(f"{f.name}: description: manquant")
    assert not violations, "Prompts avec frontmatter invalide:\n" + "\n".join(
        f"  - {v}" for v in violations
    )


@pytest.mark.compliance
def test_pr_body_check_hook_exists():
    """Le hook PRBodyCheck doit avoir un script."""
    assert Path(".github/hooks/pr-body-check.sh").exists(), (
        "pr-body-check.sh manquant — PRBodyCheck déclaré dans hooks.json sans script"
    )


@pytest.mark.compliance
def test_new_prompts_in_workflow_manifest():
    """Les 7 nouveaux prompts dans workflow-manifest."""
    manifest = _yaml.safe_load(
        Path("_gsane/_config/workflow-manifest.yaml").read_text(encoding="utf-8")
    )
    names = [w.get("name", "") for w in manifest]
    required = [
        "gsane-challenge",
        "gsane-party-mode",
        "gsane-session-resume",
        "gsane-hypothesis",
        "gsane-mutation",
        "gsane-benchmark",
        "gsane-delegation-audit",
    ]
    missing = [r for r in required if r not in names]
    assert not missing, "Prompts absents du workflow-manifest:\n" + "\n".join(
        f"  - {m}" for m in missing
    )
