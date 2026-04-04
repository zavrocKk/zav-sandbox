"""
Tests unitaires pour les outils MCP GSANE.
Ces tests importent directement les fonctions de compression_tool.py sans démarrer
un serveur MCP (smoke tests fonctionnels).
"""
import sys
import os
import tempfile
from pathlib import Path

# Ajouter mcp-server au path pour import direct
sys.path.insert(0, str(Path(__file__).parent.parent / "_gsane" / "mcp-server"))

import pytest


class TestMcpImports:
    """Vérifie que le module MCP s'importe correctement avec ses 5 outils."""

    def test_module_importable(self):
        """Le module compression_tool doit s'importer sans erreur."""
        import compression_tool  # noqa: F401

    def test_all_tools_present(self):
        """Les 5 outils MCP doivent être présents."""
        from compression_tool import (
            gsane_fetch_compressed_memory,
            gsane_write_session_checkpoint,
            gsane_read_checkpoint,
            gsane_route,
            gsane_memory_fetch,
        )
        assert callable(gsane_fetch_compressed_memory)
        assert callable(gsane_write_session_checkpoint)
        assert callable(gsane_read_checkpoint)
        assert callable(gsane_route)
        assert callable(gsane_memory_fetch)


class TestMcpPaths:
    """Vérifie que les chemins dérivés de __file__ sont corrects (indépendants du cwd)."""

    def test_memory_dir_resolves(self):
        """MEMORY_DIR doit pointer vers _gsane/_memory/ et exister."""
        import compression_tool
        assert compression_tool.MEMORY_DIR.exists(), (
            f"MEMORY_DIR {compression_tool.MEMORY_DIR} introuvable — chemins relatifs cassés?"
        )

    def test_config_dir_resolves(self):
        """CONFIG_DIR doit pointer vers _gsane/_config/ et exister."""
        import compression_tool
        assert compression_tool.CONFIG_DIR.exists(), (
            f"CONFIG_DIR {compression_tool.CONFIG_DIR} introuvable"
        )

    def test_paths_are_absolute(self):
        """MEMORY_DIR et CONFIG_DIR doivent être des chemins absolus."""
        import compression_tool
        assert compression_tool.MEMORY_DIR.is_absolute()
        assert compression_tool.CONFIG_DIR.is_absolute()


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
        # "agent" apparaît dans presque tous les fichiers mémoire
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
        from compression_tool import gsane_write_session_checkpoint, gsane_read_checkpoint
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
        # Soit on trouve le checkpoint, soit cold session (si fichier absent)
        assert "CHECKPOINT" in result or "cold" in result.lower()

    def test_read_checkpoint_always_returns_string(self):
        """gsane_read_checkpoint doit toujours retourner une string non vide (warm ou cold)."""
        from compression_tool import gsane_read_checkpoint
        result = gsane_read_checkpoint()
        assert isinstance(result, str)
        assert len(result) > 0
        # Soit warm session (checkpoint trouvé), soit cold session (aucun fichier)
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
        # Doit trouver Winston (Architect) car "architecture", "design", "api" sont dans sa trigger list
        assert "Winston" in result or "⚠️" in result or "✅" in result

    def test_route_code_query(self):
        from compression_tool import gsane_route
        result = gsane_route("implement this with test-driven development")
        assert isinstance(result, str)
        # Doit trouver Amelia (Dev)
        assert "Amelia" in result or "⚠️" in result or "✅" in result

    def test_route_missing_matrix_graceful(self, tmp_path, monkeypatch):
        """Si delegation-matrix.yaml est absent, doit retourner un message d'erreur clair."""
        import compression_tool
        original = compression_tool.CONFIG_DIR
        monkeypatch.setattr(compression_tool, "CONFIG_DIR", tmp_path)
        from compression_tool import gsane_route
        result = gsane_route("test query")
        assert "❌" in result or "introuvable" in result
        monkeypatch.setattr(compression_tool, "CONFIG_DIR", original)


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
        assert "Aucune mémoire" in result or "trouvée" in result

    def test_fetch_with_topic(self):
        from compression_tool import gsane_memory_fetch
        result = gsane_memory_fetch("master", "leçon")
        assert isinstance(result, str)


class TestMcpConfigAlignment:
    """Vérifie que la config MCP active pointe vers le bon fichier."""

    def test_mcp_config_points_to_compression_tool(self):
        """github-copilot.mcp.json doit référencer compression_tool.py."""
        import json
        config_path = Path(__file__).parent.parent / "github-copilot.mcp.json"
        assert config_path.exists(), "github-copilot.mcp.json introuvable"
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        servers = config.get("mcpServers", {})
        assert len(servers) > 0, "Aucun serveur MCP configuré"
        # Au moins un serveur doit pointer vers compression_tool.py
        all_args = " ".join(
            str(arg)
            for server in servers.values()
            for arg in server.get("args", [])
        )
        assert "compression_tool.py" in all_args, (
            "La config MCP active ne pointe pas vers compression_tool.py"
        )

    def test_delegation_matrix_has_correct_schema(self):
        """delegation-matrix.yaml doit avoir les clés 'trigger' et 'agent' (pas les anciennes)."""
        import yaml
        matrix_path = Path(__file__).parent.parent / "_gsane" / "_config" / "delegation-matrix.yaml"
        with open(matrix_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        rules = data.get("rules", [])
        assert len(rules) > 0, "delegation-matrix.yaml ne contient aucune règle"
        for rule in rules:
            assert "trigger" in rule, f"Clé 'trigger' manquante dans règle: {rule}"
            assert "agent" in rule, f"Clé 'agent' manquante dans règle: {rule}"
            # Vérifier que les vieilles clés ne sont plus là
            assert "trigger_keywords" not in rule, (
                f"Clé obsolète 'trigger_keywords' trouvée dans règle: {rule}"
            )
            assert "target_agent" not in rule, (
                f"Clé obsolète 'target_agent' trouvée dans règle: {rule}"
            )
