"""Tests compliance pour l'optimisation du contexte Copilot Pro+."""

from pathlib import Path

import pytest
import yaml


@pytest.mark.compliance
def test_all_skills_have_trigger_frontmatter():
    """14 SKILL.md doivent avoir trigger: dans frontmatter."""
    skills_dir = Path(".github/skills")
    missing = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            missing.append(f"{skill_dir.name}: SKILL.md absent")
            continue
        content = skill_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            missing.append(f"{skill_dir.name}: frontmatter absent")
            continue
        parts = content.split("---")
        frontmatter = parts[1] if len(parts) > 1 else ""
        if "trigger:" not in frontmatter:
            missing.append(f"{skill_dir.name}: trigger: absent")
    assert not missing, (
        "Skills sans trigger JIT:\n" + "\n".join(f"  - {m}" for m in missing)
    )


@pytest.mark.compliance
def test_skills_not_using_wildcard_applyto():
    """Aucune skill ne doit avoir applyTo: "**".

    C'est le pattern qui charge tout à chaque requête.
    Coût mesuré : ~3500 tokens gaspillés/requête.
    """
    skills_dir = Path(".github/skills")
    violations = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        content = skill_file.read_text(encoding="utf-8")
        if 'applyTo: "**"' in content or "applyTo: '**'" in content:
            violations.append(skill_dir.name)
    assert not violations, (
        "Skills avec applyTo: '**' détectées:\n"
        + "\n".join(f"  - {v}" for v in violations)
        + "\nChanger vers un pattern précis ou "
        "supprimer applyTo pour du vrai JIT."
    )


@pytest.mark.compliance
def test_skills_with_applyto_have_targeted_pattern():
    """Les skills avec applyTo doivent avoir un pattern ciblé (pas **)."""
    skills_dir = Path(".github/skills")
    allowed_patterns = [
        "_gsane/**",
        "_gsane/agents/**",
        "_gsane/mcp-server/**",
        "_gsane/_memory/**",
        ".github/**",
        "gsane.sh",
    ]
    violations = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        content = skill_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1])
        except Exception:
            continue
        if fm and "applyTo" in fm:
            pattern = fm["applyTo"]
            if pattern not in allowed_patterns:
                violations.append(
                    f"{skill_dir.name}: applyTo '{pattern}' non autorisé"
                )
    assert not violations, (
        "Patterns applyTo non autorisés:\n"
        + "\n".join(f"  - {v}" for v in violations)
    )


@pytest.mark.compliance
def test_config_has_context_optimization():
    """config.yaml doit avoir context_optimization."""
    config = yaml.safe_load(
        Path("_gsane/config.yaml").read_text(encoding="utf-8")
    )
    assert "context_optimization" in config, (
        "Section context_optimization manquante"
    )
    opt = config["context_optimization"]
    required = ["jit_loading", "recommend_compact_at", "new_session_at"]
    missing = [k for k in required if k not in opt]
    assert not missing, (
        f"Champs manquants dans context_optimization: {missing}"
    )


@pytest.mark.compliance
def test_session_start_mentions_compact():
    """session-start.sh doit mentionner /compact."""
    content = Path(".github/hooks/session-start.sh").read_text(encoding="utf-8")
    assert "/compact" in content, "session-start.sh ne mentionne pas /compact"


@pytest.mark.compliance
def test_copilot_instructions_intact():
    """copilot-instructions.md doit rester complet.

    PRE-ACTION-GATE et délégation sont intouchables.
    """
    content = Path(".github/copilot-instructions.md").read_text(encoding="utf-8")

    required_sections = [
        "PRE-EXECUTION GATE",
        "Agent Delegation",
        "delegation-matrix",
    ]
    missing = [s for s in required_sections if s not in content]
    assert not missing, (
        f"Sections critiques manquantes dans copilot-instructions.md: {missing}\n"
        f"Ces sections protègent contre le solo-creep — ne jamais les supprimer."
    )
