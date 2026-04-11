"""
Tests de routing dynamique GSANE.
Vérifie que gsane_route() délègue correctement
selon la delegation-matrix.yaml actuelle.
Ces tests ÉCHOUENT si le routing change sans mise à jour de la matrice.
"""

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, "_gsane/mcp-server")
from compression_tool import gsane_route  # noqa: E402


class TestDelegationRouting:
    """Routing nominal — cas standards."""

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "phrase,expected",
        [
            ("implement a new feature", "amelia"),
            ("code the function", "amelia"),
            ("code this story", "amelia"),
            ("design the architecture", "winston"),
            ("design a scalable API", "winston"),
            ("test the coverage", "quinn"),
            ("validate the coverage", "quinn"),
            ("create a new GSANE agent", "bond"),
            ("build the agent persona", "bond"),
        ],
    )
    def test_routing_oracle(self, phrase, expected):
        """Chaque phrase doit router vers l'agent attendu."""
        result = gsane_route(phrase)
        assert result is not None, f"gsane_route() retourne None pour '{phrase}'"
        assert expected in result.lower(), (
            f"Routing incorrect:\n"
            f"  Input    : '{phrase}'\n"
            f"  Attendu  : '{expected}'\n"
            f"  Obtenu   : '{result}'\n"
            f"  → Vérifier delegation-matrix.yaml"
        )

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "phrase",
        [
            "implement a new feature",
            "code the function",
            "code this story",
            "implement the fix",
            "develop code for the module",
        ],
    )
    def test_no_solo_creep_routing(self, phrase):
        """Langis ne doit JAMAIS être retourné pour une requête de code."""
        result = gsane_route(phrase)
        assert "langis" not in result.lower() and "master" not in result.lower(), (
            f"Solo-creep routing détecté:\n"
            f"  Input   : '{phrase}'\n"
            f"  Résultat: '{result}'\n"
            f"  → Langis ne doit pas coder directement"
        )

    @pytest.mark.integration
    def test_ambiguous_fallback_to_langis(self):
        """Requête ambiguë → fallback vers Langis."""
        ambiguous = ["help me", "what should I do", "bonjour", "je ne sais pas"]
        for phrase in ambiguous:
            result = gsane_route(phrase)
            assert result is not None, f"Pas de fallback pour '{phrase}'"
            assert "langis" in result.lower() or "master" in result.lower(), (
                f"Fallback cassé pour '{phrase}': {result}"
            )

    @pytest.mark.integration
    def test_routing_matrix_coherence(self):
        """Cohérence interne de la matrice : trigger, agent, fallback."""
        matrix = yaml.safe_load(
            Path("_gsane/_config/delegation-matrix.yaml").read_text(encoding="utf-8")
        )
        rules = matrix.get("rules", [])
        assert rules, "delegation-matrix.yaml vide"

        fallback_found = False
        for i, rule in enumerate(rules):
            assert "trigger" in rule, f"Règle {i} sans trigger: {rule}"
            assert "agent" in rule, f"Règle {i} sans agent: {rule}"
            triggers = rule.get("trigger", [])
            if "*" in triggers or triggers == ["*"]:
                fallback_found = True

        assert fallback_found, (
            "Aucun fallback (*) dans delegation-matrix — "
            "les requêtes ambiguës ne seront pas routées"
        )


class TestRoutingRegression:
    """Tests de régression — détectent si le routing a changé."""

    @pytest.mark.integration
    def test_routing_deterministic(self):
        """Même input → même output à chaque fois."""
        phrase = "implement a feature with TDD"
        results = [gsane_route(phrase) for _ in range(3)]
        assert len(set(results)) == 1, (
            f"Routing non-déterministe pour '{phrase}':\n  Résultats: {results}"
        )

    @pytest.mark.integration
    def test_all_5_agents_reachable(self):
        """Chaque agent doit être atteignable via routing."""
        agent_triggers = {
            "langis": "orchestrate this complex task",
            "amelia": "implement the function",
            "quinn": "validate test coverage",
            "winston": "design the architecture",
            "bond": "create a new agent persona",
        }
        unreachable = []
        for agent, phrase in agent_triggers.items():
            result = gsane_route(phrase)
            if agent not in (result or "").lower():
                unreachable.append(f"{agent} (phrase: '{phrase}' → {result})")
        assert not unreachable, "Agents non-atteignables via routing:\n" + "\n".join(
            f"  - {a}" for a in unreachable
        )
