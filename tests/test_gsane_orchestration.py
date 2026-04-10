"""
test_gsane_orchestration.py — Tests structurels du système d'orchestration GSANE.
Ces tests vérifient la présence, la structure et la cohérence des fichiers GSANE.
"""
import os
import re
import yaml
import glob
from pathlib import Path
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def workflow_manifest():
    path = "_gsane/_config/workflow-manifest.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

@pytest.fixture
def agent_manifest():
    path = "_gsane/_config/agent-manifest.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

@pytest.fixture
def delegation_matrix():
    path = "_gsane/_config/delegation-matrix.yaml"
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("rules", [])

def read_agent(name):
    path = f"_gsane/agents/{name}.md"
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


# ============================================================
# 1. PROMPT ANALYSIS STRUCTURE
# ============================================================

class TestPromptAnalysis:
    def test_master_has_pae_analyse_step(self):
        content = read_agent("master")
        assert "PAE-ANALYSE" in content, "master.md doit avoir le step PAE-ANALYSE"

    def test_master_has_pae_map_step(self):
        content = read_agent("master")
        assert "PAE-MAP" in content

    def test_master_has_pae_parallel_step(self):
        content = read_agent("master")
        assert "PAE-PARALLEL" in content

    def test_master_has_pae_brainstorm_step(self):
        content = read_agent("master")
        assert "PAE-BRAINSTORM" in content

    def test_master_has_pae_aggregate_step(self):
        content = read_agent("master")
        assert "PAE-AGGREGATE" in content

    def test_master_references_shadow_zones_or_domains(self):
        content = read_agent("master")
        assert "shadow_zone" in content.lower() or "domains" in content.lower()


# ============================================================
# 2. DELEGATION MATRIX
# ============================================================

class TestDelegationMatrix:
    def test_has_code_agent(self, delegation_matrix):
        agents = [r.get("agent", "") for r in delegation_matrix]
        assert any("Amelia" in a or "dev" in a.lower() for a in agents), \
            "Deve avoir un agent pour le code (Amelia/Dev)"

    def test_has_arch_agent(self, delegation_matrix):
        agents = [r.get("agent", "") for r in delegation_matrix]
        assert any("Winston" in a or "architect" in a.lower() for a in agents)

    def test_has_test_agent(self, delegation_matrix):
        agents = [r.get("agent", "") for r in delegation_matrix]
        assert any("Quinn" in a or "qa" in a.lower() for a in agents)

    def test_delegation_workflow_exists(self):
        assert os.path.exists("_gsane/workflows/delegation/workflow.md")

    def test_delegation_workflow_has_audit(self):
        with open("_gsane/workflows/delegation/workflow.md", encoding="utf-8") as f:
            content = f.read()
        assert "delegation-audit" in content.lower()

    def test_delegation_workflow_has_trust_score(self):
        with open("_gsane/workflows/delegation/workflow.md", encoding="utf-8") as f:
            content = f.read()
        assert "trust_score" in content


# ============================================================
# 3. HUDDLE / PARTY-MODE
# ============================================================

class TestHuddle:
    def test_party_mode_workflow_exists(self):
        assert os.path.exists("_gsane/workflows/party-mode/workflow.md")

    def test_hudle_has_scoring_formula(self):
        with open("_gsane/workflows/party-mode/workflow.md", encoding="utf-8") as f:
            content = f.read()
        assert "keyword_score" in content or "domain_score" in content

    def test_huddle_has_consensus_protocol(self):
        with open("_gsane/workflows/party-mode/workflow.md", encoding="utf-8") as f:
            content = f.read()
        assert "APPROVE" in content and "BLOCK" in content

    def test_huddle_has_livrable(self):
        with open("_gsane/workflows/party-mode/workflow.md", encoding="utf-8") as f:
            content = f.read()
        assert "party-mode-audit" in content

    def test_brainstorm_has_devils_advocate(self):
        with open("_gsane/workflows/party-mode/workflow.md", encoding="utf-8") as f:
            content = f.read()
        assert "devil" in content.lower() or "Devil" in content

    def test_party_mode_has_phase3_planning_section(self):
        with open("_gsane/workflows/party-mode/workflow.md", encoding="utf-8") as f:
            content = f.read()
        assert "PHASE 3" in content and "Planning" in content, \
            "party-mode/workflow.md doit contenir 'PHASE 3 — Planning'"

    def test_execution_plan_template_exists(self):
        assert os.path.exists("_gsane/workflows/party-mode/templates/execution-plan.yaml"), \
            "Le template execution-plan.yaml doit exister"

    def test_execution_plan_template_has_required_fields(self):
        with open("_gsane/workflows/party-mode/templates/execution-plan.yaml", encoding="utf-8") as f:
            content = f.read()
        required = ["plan_id", "session_date", "objective", "scope", "tasks",
                    "owner", "depends_on", "parallel_group", "validation_agent",
                    "done_definition", "risk_level", "acceptance_criteria"]
        for field in required:
            assert field in content, \
                f"execution-plan.yaml template doit contenir le champ '{field}'"

    def test_delivery_contract_tpl_has_frontmatter_yaml(self):
        with open("_gsane/workflows/delivery-contract.tpl.md", encoding="utf-8") as f:
            content = f.read()
        assert content.startswith("---"), \
            "delivery-contract.tpl.md doit commencer par un frontmatter YAML '---'"
        assert "task_id" in content and "risk_level" in content, \
            "delivery-contract.tpl.md doit contenir task_id et risk_level dans le frontmatter"

    def test_master_post_brainstorm_action_present(self):
        content = read_agent("master")
        assert "POST-PARTY-MODE ACTION" in content, \
            "master.md doit contenir le bloc POST-PARTY-MODE ACTION dans PAE-BRAINSTORM"

    def test_master_brainstorm_cmd_has_planning_gateway(self):
        content = read_agent("master")
        assert "PHASE 3 GATEWAY" in content, \
            "master.md BRAINSTORM-CMD doit contenir la Phase 3 Gateway"


# ============================================================
# 4. CROSS-VALIDATION
# ============================================================

class TestCrossValidation:
    def test_standard_behavior_has_cross_validation(self):
        with open("_gsane/standard-agent-behavior.md", encoding="utf-8") as f:
            content = f.read()
        assert "cross" in content.lower() and "validation" in content.lower()

    def test_trust_score_formula_present(self):
        with open("_gsane/standard-agent-behavior.md", encoding="utf-8") as f:
            content = f.read()
        assert "factual_accuracy" in content

    def test_composite_threshold_present(self):
        with open("_gsane/standard-agent-behavior.md", encoding="utf-8") as f:
            content = f.read()
        assert "70" in content  # composite < 70 déclenche validation


# ============================================================
# 5. PRE/POST-FLIGHT
# ============================================================

class TestPrePostFlight:
    @pytest.mark.parametrize("agent", ["dev", "qa", "architect", "bond"])
    def test_agent_has_preflight(self, agent):
        content = read_agent(agent)
        assert "PRE-FLIGHT" in content, f"{agent}.md doit avoir PRE-FLIGHT"

    @pytest.mark.parametrize("agent", ["dev", "qa", "architect", "bond"])
    def test_agent_has_postflight(self, agent):
        content = read_agent(agent)
        assert "POST-FLIGHT" in content, f"{agent}.md doit avoir POST-FLIGHT"

    @pytest.mark.parametrize("agent", ["dev", "qa", "architect", "bond"])
    def test_agent_preflight_rouge_condition(self, agent):
        content = read_agent(agent)
        assert "ROUGE" in content


# ============================================================
# 6. CIRCUIT BREAKER
# ============================================================

class TestCircuitBreaker:
    def test_master_has_circuit_breaker(self):
        content = read_agent("master")
        assert "CIRCUIT" in content or "circuit" in content.lower()

    def test_circuit_breaker_references_failure_museum(self):
        content = read_agent("master")
        assert "failure-museum" in content.lower()

    def test_failure_museum_file_exists(self):
        assert os.path.exists("_gsane/_memory/failure-museum.md")


# ============================================================
# 7. WORKFLOW MANIFEST — AUCUN AGENT INEXISTANT
# ============================================================

class TestWorkflowManifest:
    def test_no_leo_in_manifest(self, workflow_manifest):
        text = str(workflow_manifest)
        assert "léo" not in text.lower() and "leo" not in text.lower()

    def test_no_aria_in_manifest(self, workflow_manifest):
        text = str(workflow_manifest)
        assert "aria" not in text.lower()

    def test_no_optimizer_in_manifest(self, workflow_manifest):
        text = str(workflow_manifest)
        assert "optimizer" not in text.lower()

    def test_all_workflow_paths_exist(self, workflow_manifest):
        missing = []
        for wf in workflow_manifest:
            path = wf.get("path", "")
            if path and not os.path.exists(path):
                missing.append(path)
        assert not missing, f"Workflow paths manquants: {missing}"

    def test_all_agents_are_valid(self, workflow_manifest, agent_manifest):
        valid_names = {a.get("name", "") for a in agent_manifest}
        for wf in workflow_manifest:
            agent = wf.get("agent", "")
            if agent:
                assert agent in valid_names, \
                    f"workflow '{wf.get('name')}' référence agent inconnu: '{agent}'"
        # co_agent also validated
        for wf in workflow_manifest:
            co = wf.get("co_agent", "")
            if co:
                assert co in valid_names, \
                    f"workflow '{wf.get('name')}' co_agent inconnu: '{co}'"


# ============================================================
# 8. TRACE LOG
# ============================================================

class TestTraceLog:
    def test_trace_log_exists(self):
        assert os.path.exists("_gsane/_memory/trace.log")

    def test_trace_log_has_initial_entry(self):
        with open("_gsane/_memory/trace.log", encoding="utf-8") as f:
            content = f.read()
        assert "timestamp" in content

    def test_trace_log_is_yaml_parseable(self):
        with open("_gsane/_memory/trace.log", encoding="utf-8") as f:
            content = f.read()
        data = yaml.safe_load(content)
        assert data is not None
        assert isinstance(data, list)

    def test_trace_log_entry_has_required_fields(self):
        with open("_gsane/_memory/trace.log", encoding="utf-8") as f:
            content = f.read()
        data = yaml.safe_load(content)
        entry = data[0]
        assert "timestamp" in entry
        assert "event" in entry
        assert "agent" in entry


# ============================================================
# 9. GSANE.SH TRACE COMMANDS
# ============================================================

class TestGsaneShTrace:
    def test_gsane_sh_has_trace_command(self):
        with open("gsane.sh", encoding="utf-8") as f:
            content = f.read()
        assert "trace)" in content or "trace )" in content

    def test_gsane_sh_has_tail_subcommand(self):
        with open("gsane.sh", encoding="utf-8") as f:
            content = f.read()
        assert "--tail" in content

    def test_gsane_sh_has_summary_subcommand(self):
        with open("gsane.sh", encoding="utf-8") as f:
            content = f.read()
        assert "--summary" in content

    def test_gsane_sh_has_p2p_subcommand(self):
        with open("gsane.sh", encoding="utf-8") as f:
            content = f.read()
        assert "--p2p" in content


# ============================================================
# 10. P2P INTER-AGENT COMMUNICATION
# ============================================================

class TestP2PCommunication:
    def test_standard_behavior_has_p2p(self):
        with open("_gsane/standard-agent-behavior.md", encoding="utf-8") as f:
            content = f.read()
        assert "P2P" in content or "p2p" in content.lower()

    def test_p2p_has_offer_type(self):
        with open("_gsane/standard-agent-behavior.md", encoding="utf-8") as f:
            content = f.read()
        assert "offer" in content.lower()

    def test_p2p_has_challenge_type(self):
        with open("_gsane/standard-agent-behavior.md", encoding="utf-8") as f:
            content = f.read()
        assert "challenge" in content.lower()

    def test_p2p_has_delegate_type(self):
        with open("_gsane/standard-agent-behavior.md", encoding="utf-8") as f:
            content = f.read()
        assert "delegate" in content.lower()

    @pytest.mark.parametrize("agent", ["dev", "qa", "architect", "bond"])
    def test_agent_has_p2p_behavior(self, agent):
        # P2P behaviors are defined in standard-agent-behavior.md for all agents
        # Verify each agent references standard behavior or has the relevant P2P refs
        content = read_agent(agent)
        agent_behavior_ref = (
            "standard-agent-behavior" in content or
            "STANDARD_BEHAVIOR" in content or
            "challenge" in content.lower() or
            "offer" in content.lower()
        )
        assert agent_behavior_ref, f"{agent}.md doit référencer les comportements P2P"


# ============================================================
# 11. BEHAVIORAL TESTS — exécutent réellement des commandes
# ============================================================

import subprocess


class TestBehavioral:
    """Tests comportementaux — exécutent réellement des commandes."""

    pytestmark = pytest.mark.behavioral

    def test_gsane_validate_exits_zero(self):
        """bash gsane.sh validate doit retourner 0."""
        bash = r"C:\Program Files\Git\bin\bash.exe"
        if not os.path.exists(bash):
            pytest.skip("Git Bash non disponible sur ce système")
        result = subprocess.run(
            [bash, "-c", "bash gsane.sh validate"],
            cwd=REPO_ROOT,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60
        )
        assert result.returncode == 0, f"gsane.sh validate FAIL:\n{result.stdout}\n{result.stderr}"

    def test_gsane_trace_tail_exits_zero(self):
        """bash gsane.sh trace --tail 5 doit retourner 0."""
        bash = r"C:\Program Files\Git\bin\bash.exe"
        if not os.path.exists(bash):
            pytest.skip("Git Bash non disponible")
        result = subprocess.run(
            [bash, "-c", "bash gsane.sh trace --tail 5"],
            cwd=REPO_ROOT,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30
        )
        assert result.returncode == 0, f"trace --tail FAIL:\n{result.stdout}\n{result.stderr}"

    def test_gsane_trace_summary_exits_zero(self):
        """bash gsane.sh trace --summary doit retourner 0."""
        bash = r"C:\Program Files\Git\bin\bash.exe"
        if not os.path.exists(bash):
            pytest.skip("Git Bash non disponible")
        result = subprocess.run(
            [bash, "-c", "bash gsane.sh trace --summary"],
            cwd=REPO_ROOT,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30
        )
        assert result.returncode == 0, f"trace --summary FAIL:\n{result.stdout}\n{result.stderr}"

    def test_yaml_manifests_all_valid(self):
        """Tous les _gsane/_config/*.yaml doivent parser sans erreur."""
        import yaml
        files = glob.glob("_gsane/_config/*.yaml")
        assert len(files) > 0, "Aucun manifest YAML trouvé"
        for f in files:
            with open(f, encoding="utf-8") as fh:
                yaml.safe_load(fh)
            # None is valid for empty files — ensure no parse error raised

    def test_no_legacy_in_hooks(self):
        """Les hooks ne doivent pas référencer _gsane/core/."""
        hooks = [
            ".github/hooks/session-start.sh",
            ".github/hooks/session-stop.sh",
            ".github/hooks/flywheel-trigger.sh",
        ]
        for hook in hooks:
            if os.path.exists(hook):
                content = open(hook, encoding="utf-8", errors="replace").read()
                assert "_gsane/core/" not in content, \
                    f"{hook} contient encore '_gsane/core/' (chemin legacy)"

    def test_no_legacy_agents_in_manifest(self):
        """manifest.yaml ne doit pas référencer les modules CIS/TEA/BMB."""
        with open("_gsane/_config/manifest.yaml", encoding="utf-8") as f:
            content = f.read()
        forbidden = ["creative-intelligence-suite", "test-architecture-enterprise", "builder-module-builder"]
        for term in forbidden:
            assert term not in content, f"manifest.yaml contient terme déprécié: {term}"
