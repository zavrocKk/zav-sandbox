"""
Tests unitaires pour les outils MCP GSANE.
Ces tests importent directement les fonctions de compression_tool.py sans démarrer
un serveur MCP (smoke tests fonctionnels).
"""
# pyright: reportMissingImports=false, reportUnusedImport=false

import sys
from pathlib import Path

import pytest
import yaml  # type: ignore[import-untyped]

sys.path.insert(0, str(Path(__file__).parent.parent / "_gsane" / "mcp-server"))


class TestMcpImports:
    """Vérifie que le module MCP s'importe correctement avec ses vues canoniques et outils."""

    def test_module_importable(self):
        import compression_tool  # type: ignore[import-not-found]  # noqa: F401

    def test_all_tools_present(self):
        from compression_tool import (
            gsane_fetch_compressed_memory,
            gsane_memory_fetch,
            gsane_read_active_delivery_contract,
            gsane_read_canonical_brief,
            gsane_read_checkpoint,
            gsane_read_project_snapshot,
            gsane_route,
            gsane_write_session_checkpoint,
        )

        assert callable(gsane_read_canonical_brief)
        assert callable(gsane_read_active_delivery_contract)
        assert callable(gsane_read_project_snapshot)
        assert callable(gsane_fetch_compressed_memory)
        assert callable(gsane_write_session_checkpoint)
        assert callable(gsane_read_checkpoint)
        assert callable(gsane_route)
        assert callable(gsane_memory_fetch)


class TestMcpPaths:
    """Vérifie que les chemins dérivés de __file__ sont corrects (indépendants du cwd)."""

    def test_memory_dir_resolves(self):
        import compression_tool

        assert compression_tool.MEMORY_DIR.exists(), (
            f"MEMORY_DIR {compression_tool.MEMORY_DIR} introuvable — chemins relatifs cassés?"
        )

    def test_config_dir_resolves(self):
        import compression_tool

        assert compression_tool.CONFIG_DIR.exists(), (
            f"CONFIG_DIR {compression_tool.CONFIG_DIR} introuvable"
        )

    def test_paths_are_absolute(self):
        import compression_tool

        assert compression_tool.MEMORY_DIR.is_absolute()
        assert compression_tool.CONFIG_DIR.is_absolute()


class TestCanonicalViews:
    """Tests pour les vues MCP canoniques de lecture."""

    def test_canonical_brief_view_is_structured_and_points_to_project_context(self):
        from compression_tool import gsane_read_canonical_brief

        data = yaml.safe_load(gsane_read_canonical_brief())
        assert data["view"] == "canonical_human_brief"
        assert data["status"] == "available"
        assert data["source"] == "_gsane/_memory/project-context.md"
        assert "Cap du Projet" in data["content"]

    def test_active_delivery_contract_view_exposes_current_contract_metadata(self):
        from compression_tool import gsane_read_active_delivery_contract

        data = yaml.safe_load(gsane_read_active_delivery_contract())
        assert data["view"] == "active_delivery_contract"
        assert data["status"] in ("available", "missing")
        assert data["source"] == "_gsane-output/current-delivery-contract.md"
        if data["status"] == "available":
            metadata = data["metadata"]
            assert isinstance(metadata.get("task_id"), str)
            assert metadata["task_id"]
            assert isinstance(metadata.get("owner"), str)
            assert metadata["owner"]
            assert isinstance(metadata.get("validation_agent"), str)
            assert metadata["validation_agent"]
            assert isinstance(data.get("content"), str)
            assert data["content"]
        else:
            assert data["metadata"] == {}
            assert data.get("content") == ""

    def test_project_snapshot_view_reports_canonical_sources_and_audit_files(self):
        from compression_tool import gsane_read_project_snapshot

        data = yaml.safe_load(gsane_read_project_snapshot())
        assert data["view"] == "canonical_project_snapshot"
        assert data["sources_of_truth"]["human_brief"] == "_gsane/_memory/project-context.md"
        assert data["sources_of_truth"]["active_delivery_contract"] == "_gsane-output/current-delivery-contract.md"
        assert "gsane_read_project_snapshot" in data["runtime"]["canonical_mcp_views"]

        audit_paths = {entry["path"] for entry in data["runtime"]["audit_continuity"]}
        assert "_gsane/_memory/sessions/session-state.md" in audit_paths
        assert "_gsane/_memory/sessions/session-analysis-log.md" in audit_paths


class TestFetchCompressedMemory:
    """Tests pour gsane_fetch_compressed_memory."""

    def test_returns_string(self):
        from compression_tool import gsane_fetch_compressed_memory

        result = gsane_fetch_compressed_memory("master")
        assert isinstance(result, str)

    def test_no_result_message(self):
        from compression_tool import gsane_fetch_compressed_memory

        result = gsane_fetch_compressed_memory("xyzzy_query_that_does_not_exist_12345")
        assert "No memory found" in result

    def test_query_match_returns_data(self):
        from compression_tool import gsane_fetch_compressed_memory

        result = gsane_fetch_compressed_memory("agent")
        assert isinstance(result, str)
        assert len(result) > 0


class TestCheckpoint:
    """Tests pour gsane_write_session_checkpoint et gsane_read_checkpoint."""

    def test_write_checkpoint_success(self):
        from compression_tool import gsane_write_session_checkpoint

        result = gsane_write_session_checkpoint(
            plan_active="Test plan",
            next_step="Next step",
            decisions="Decision A",
            open_items="Item B",
            risks="Risk C",
            exchange_count=999,
        )
        assert "✅" in result
        assert "999" in result

    def test_read_checkpoint_after_write(self):
        from compression_tool import gsane_read_checkpoint, gsane_write_session_checkpoint

        gsane_write_session_checkpoint(
            plan_active="Read test plan",
            next_step="Step X",
            decisions="Dec X",
            open_items="Open X",
            risks="Risk X",
            exchange_count=998,
        )
        result = gsane_read_checkpoint()
        assert isinstance(result, str)
        assert len(result) > 0
        assert "CHECKPOINT" in result or "cold" in result.lower()

    def test_read_checkpoint_always_returns_string(self):
        from compression_tool import gsane_read_checkpoint

        result = gsane_read_checkpoint()
        assert isinstance(result, str)
        assert len(result) > 0
        assert "CHECKPOINT" in result or "cold" in result.lower() or "No checkpoint" in result


class TestGsaneRoute:
    """Tests pour gsane_route — schéma actuel de delegation-matrix.yaml."""

    def test_route_returns_string(self):
        from compression_tool import gsane_route

        result = gsane_route("implement a new feature")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_route_architecture_query(self):
        from compression_tool import gsane_route

        result = gsane_route("design a scalable architecture for the API")
        assert isinstance(result, str)
        assert "Winston" in result or "⚠️" in result or "✅" in result

    def test_route_code_query(self):
        from compression_tool import gsane_route

        result = gsane_route("implement this with test-driven development")
        assert isinstance(result, str)
        assert "Amelia" in result or "⚠️" in result or "✅" in result

    def test_route_security_query_escalates_to_master_with_owner_and_gate(self):
        from compression_tool import gsane_route

        result = gsane_route("security hardening for auth tokens and filesystem access")
        assert "ESCALADE SÉCURITÉ" in result
        assert "Langis" in result
        assert "Winston" in result
        assert "Quinn" in result

    def test_route_security_query_requests_bond_on_gsane_runtime_surface(self):
        from compression_tool import gsane_route

        result = gsane_route("security review for GSANE MCP sandbox guardrail policy")
        assert "ESCALADE SÉCURITÉ" in result
        assert "Bond" in result

    def test_route_missing_matrix_graceful(self, tmp_path, monkeypatch):
        import compression_tool

        original = compression_tool.CONFIG_DIR
        monkeypatch.setattr(compression_tool, "CONFIG_DIR", tmp_path)
        from compression_tool import gsane_route

        result = gsane_route("test query")
        assert "❌" in result or "introuvable" in result
        monkeypatch.setattr(compression_tool, "CONFIG_DIR", original)


class TestGsaneRouteEnhanced:
    """Tests renforcés pour le scoring de routing (priorité, exclusions, fallback)."""

    def test_route_architecture_with_test_keyword(self):
        from compression_tool import gsane_route

        result = gsane_route("test my architecture idea")
        assert "Winston" in result

    def test_route_code_architecture_broken(self):
        from compression_tool import gsane_route

        result = gsane_route("code architecture is broken")
        assert "Winston" in result

    def test_route_fallback_unknown(self):
        from compression_tool import gsane_route

        result = gsane_route("bonjour, help me")
        assert "Langis" in result

    def test_route_existing_behavior_preserved(self):
        from compression_tool import gsane_route

        result = gsane_route("implement a new feature")
        assert "Amelia" in result


class TestGsaneTraceReport:
    """Tests pour gsane_trace_report."""

    def test_trace_report_returns_string(self):
        from compression_tool import gsane_trace_report

        result = gsane_trace_report()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_trace_report_importable(self):
        from compression_tool import gsane_trace_report

        assert callable(gsane_trace_report)


class TestGsaneMemoryFetch:
    """Tests pour gsane_memory_fetch."""

    def test_fetch_master_sidecar(self):
        from compression_tool import gsane_memory_fetch

        result = gsane_memory_fetch("master", "")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_fetch_unknown_agent(self):
        from compression_tool import gsane_memory_fetch

        result = gsane_memory_fetch("agent_xyz_unknown_12345", "")
        assert isinstance(result, str)
        assert "Accès refusé" in result or "invalide" in result

    def test_fetch_with_topic(self):
        from compression_tool import gsane_memory_fetch

        result = gsane_memory_fetch("master", "leçon")
        assert isinstance(result, str)

    def test_fetch_rejects_path_traversal_agent_name(self):
        from compression_tool import gsane_memory_fetch

        result = gsane_memory_fetch("..\\master", "")
        assert "Accès refusé" in result or "invalide" in result
        trace_content = (
            Path(__file__).parent.parent / "_gsane" / "_memory" / "trace.log"
        ).read_text(encoding="utf-8")
        yaml.safe_load(trace_content)


class TestCompressionToolHygiene:
    """Empêche le retour des doublons signalés dans compression_tool.py."""

    def test_compression_tool_has_single_main_block_and_unique_core_functions(self):
        source = (
            Path(__file__).parent.parent / "_gsane" / "mcp-server" / "compression_tool.py"
        ).read_text(encoding="utf-8")
        assert source.count('if __name__ == "__main__":') == 1
        assert source.count("def gsane_write_session_checkpoint(") == 1
        assert source.count("def gsane_read_checkpoint(") == 1
        assert source.count("def gsane_read_canonical_brief(") == 1
        assert source.count("def gsane_read_active_delivery_contract(") == 1
        assert source.count("def gsane_read_project_snapshot(") == 1


class TestMcpConfigAlignment:
    """Vérifie que la config MCP active pointe vers le bon fichier."""

    def test_mcp_config_points_to_compression_tool(self):
        import json

        repo_root = Path(__file__).resolve().parents[1]
        config_candidates = [
            repo_root / "github-copilot.mcp.json",
            repo_root / ".vscode" / "mcp.json",
        ]
        existing_configs = [path for path in config_candidates if path.exists()]

        if not existing_configs:
            pytest.skip("Aucune config MCP locale présente dans ce workspace")

        for config_path in existing_configs:
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)

            servers = config.get("mcpServers") or config.get("servers") or {}
            assert len(servers) > 0, f"Aucun serveur MCP configuré dans {config_path.name}"

            all_args = " ".join(
                str(arg)
                for server in servers.values()
                for arg in server.get("args", [])
            )
            assert "compression_tool.py" in all_args, (
                f"La config MCP locale {config_path.name} ne pointe pas vers compression_tool.py"
            )

    def test_delegation_matrix_has_correct_schema(self):
        matrix_path = Path(__file__).parent.parent / "_gsane" / "_config" / "delegation-matrix.yaml"
        with open(matrix_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        rules = data.get("rules", [])
        assert len(rules) > 0, "delegation-matrix.yaml ne contient aucune règle"
        for rule in rules:
            assert "trigger" in rule, f"Clé 'trigger' manquante dans règle: {rule}"
            assert "agent" in rule, f"Clé 'agent' manquante dans règle: {rule}"
            assert "trigger_keywords" not in rule, (
                f"Clé obsolète 'trigger_keywords' trouvée dans règle: {rule}"
            )
            assert "target_agent" not in rule, (
                f"Clé obsolète 'target_agent' trouvée dans règle: {rule}"
            )
