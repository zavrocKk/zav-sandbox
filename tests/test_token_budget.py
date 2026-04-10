"""Tests de régression sur le budget tokens des fichiers GSANE."""
import os
import glob
import warnings
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def estimate_tokens(text: str) -> int:
    """Approximation tokens ≈ words × 1.3 (sans dépendance tiktoken)."""
    return int(len(text.split()) * 1.3)


def read_file(rel_path: str) -> str:
    with open(os.path.join(PROJECT_ROOT, rel_path), encoding="utf-8") as f:
        return f.read()


# --- Seuils calibrés par Winston (état actuel + 30% headroom) ---
AGENT_MANIFEST_THRESHOLD = 3000
AGENT_THRESHOLDS = {
    "master.md": 7500,
    "architect.md": 3000,
    "bond.md": 3000,
    "dev.md": 3000,
    "qa.md": 3000,
}
SKILL_THRESHOLD = 1000
CONFIG_THRESHOLD = 400
SESSION_BUDGET_THRESHOLD = 10500  # état actuel (~8046) + 30% headroom

WARNING_RATIO = 0.80


@pytest.mark.token_budget
def test_agent_manifest_token_budget():
    rel_path = os.path.join("_gsane", "_config", "agent-manifest.yaml")
    content = read_file(rel_path)
    tokens = estimate_tokens(content)
    threshold = AGENT_MANIFEST_THRESHOLD
    if tokens > threshold * WARNING_RATIO:
        warnings.warn(
            f"⚠️ {rel_path} à {tokens}/{threshold} tokens "
            f"({tokens / threshold * 100:.0f}%) — proche du seuil"
        )
    assert tokens <= threshold, (
        f"❌ {rel_path} dépasse le seuil : {tokens} > {threshold} tokens"
    )


@pytest.mark.token_budget
def test_agent_files_token_budget():
    pattern = os.path.join(PROJECT_ROOT, "_gsane", "agents", "*.md")
    agent_files = glob.glob(pattern)
    assert agent_files, "Aucun fichier agent trouvé dans _gsane/agents/"
    for filepath in sorted(agent_files):
        filename = os.path.basename(filepath)
        rel_path = os.path.join("_gsane", "agents", filename)
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        tokens = estimate_tokens(content)
        threshold = AGENT_THRESHOLDS.get(filename, 3000)
        if tokens > threshold * WARNING_RATIO:
            warnings.warn(
                f"⚠️ {rel_path} à {tokens}/{threshold} tokens "
                f"({tokens / threshold * 100:.0f}%) — proche du seuil"
            )
        assert tokens <= threshold, (
            f"❌ {rel_path} dépasse le seuil : {tokens} > {threshold} tokens"
        )


@pytest.mark.token_budget
def test_skill_files_token_budget():
    pattern = os.path.join(PROJECT_ROOT, ".github", "skills", "*", "SKILL.md")
    skill_files = glob.glob(pattern)
    assert skill_files, "Aucun fichier skill trouvé dans .github/skills/"
    for filepath in sorted(skill_files):
        parts = filepath.replace("\\", "/").split("/")
        skill_idx = parts.index("skills")
        skill_name = parts[skill_idx + 1]
        rel_path = os.path.join(".github", "skills", skill_name, "SKILL.md")
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        tokens = estimate_tokens(content)
        threshold = SKILL_THRESHOLD
        if tokens > threshold * WARNING_RATIO:
            warnings.warn(
                f"⚠️ {rel_path} à {tokens}/{threshold} tokens "
                f"({tokens / threshold * 100:.0f}%) — proche du seuil"
            )
        assert tokens <= threshold, (
            f"❌ {rel_path} dépasse le seuil : {tokens} > {threshold} tokens"
        )


@pytest.mark.token_budget
def test_config_token_budget():
    rel_path = os.path.join("_gsane", "config.yaml")
    content = read_file(rel_path)
    tokens = estimate_tokens(content)
    threshold = CONFIG_THRESHOLD
    if tokens > threshold * WARNING_RATIO:
        warnings.warn(
            f"⚠️ {rel_path} à {tokens}/{threshold} tokens "
            f"({tokens / threshold * 100:.0f}%) — proche du seuil"
        )
    assert tokens <= threshold, (
        f"❌ {rel_path} dépasse le seuil : {tokens} > {threshold} tokens"
    )


@pytest.mark.token_budget
def test_session_budget_total():
    # agent-manifest
    manifest_content = read_file(
        os.path.join("_gsane", "_config", "agent-manifest.yaml")
    )
    manifest_tokens = estimate_tokens(manifest_content)

    # config
    config_content = read_file(os.path.join("_gsane", "config.yaml"))
    config_tokens = estimate_tokens(config_content)

    # le plus gros agent
    agent_pattern = os.path.join(PROJECT_ROOT, "_gsane", "agents", "*.md")
    agent_files = glob.glob(agent_pattern)
    agent_token_counts = []
    for filepath in agent_files:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        agent_token_counts.append(estimate_tokens(content))
    max_agent_tokens = max(agent_token_counts) if agent_token_counts else 0

    # les 2 plus gros skills
    skill_pattern = os.path.join(PROJECT_ROOT, ".github", "skills", "*", "SKILL.md")
    skill_files = glob.glob(skill_pattern)
    skill_token_counts = []
    for filepath in skill_files:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        skill_token_counts.append(estimate_tokens(content))
    skill_token_counts.sort(reverse=True)
    top_2_skills = sum(skill_token_counts[:2])

    total = manifest_tokens + config_tokens + max_agent_tokens + top_2_skills
    threshold = SESSION_BUDGET_THRESHOLD
    if total > threshold * WARNING_RATIO:
        warnings.warn(
            f"⚠️ Session budget total à {total}/{threshold} tokens "
            f"({total / threshold * 100:.0f}%) — proche du seuil"
        )
    assert total <= threshold, (
        f"❌ Session budget total dépasse le seuil : {total} > {threshold} tokens "
        f"(manifest={manifest_tokens}, config={config_tokens}, "
        f"max_agent={max_agent_tokens}, top2_skills={top_2_skills})"
    )
