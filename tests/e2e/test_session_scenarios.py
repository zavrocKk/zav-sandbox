"""
Tests E2E GSANE — scénarios complets.
Vérifient la causalité entre les décisions des agents sur plusieurs sessions.
"""

import os
import re
import shutil
import subprocess

import pytest

_HAS_BASH = shutil.which("bash") is not None
_IN_PYTEST = "PYTEST_CURRENT_TEST" in os.environ


class TestSessionCausalityChain:
    """Vérifie la chaîne causale entre agents."""

    @pytest.mark.e2e
    def test_dc_exists_before_implementation(self, trace_events):
        """Tout event d'implémentation doit être précédé d'un DC approuvé."""
        if not trace_events:
            pytest.skip("trace.log vide")

        sessions: dict[str, list] = {}
        for e in trace_events:
            if not isinstance(e, dict):
                continue
            sid = e.get("session_id", "?")
            sessions.setdefault(sid, []).append(e)

        violations = []
        for sid, events in sessions.items():
            event_types = [e.get("event", "") for e in events]
            has_dc = "delivery_contract_created" in event_types
            has_code = any(
                "implement" in str(e.get("details", "")).lower()
                for e in events
                if isinstance(e, dict) and e.get("agent") in ["amelia", "dev"]
            )
            if has_code and not has_dc:
                violations.append(f"Session {sid}: code sans DC")

        assert not violations, (
            f"Code produit sans DC dans {len(violations)} session(s):\n"
            + "\n".join(f"  - {v}" for v in violations[:5])
        )

    @pytest.mark.e2e
    @pytest.mark.skipif(not _HAS_BASH, reason="bash non disponible")
    def test_session_resume_exits_zero(self):
        """gsane.sh session --resume doit retourner EXIT 0."""
        result = subprocess.run(  # noqa: S603 S607
            ["bash", "gsane.sh", "session", "--resume"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, f"session --resume échoue:\n{result.stderr}"

    @pytest.mark.e2e
    @pytest.mark.skipif(not _HAS_BASH, reason="bash non disponible")
    @pytest.mark.skipif(_IN_PYTEST, reason="Récursion pytest — gsane.sh validate relance pytest")
    def test_validate_pipeline_exits_zero(self):
        """bash gsane.sh validate doit EXIT 0."""
        result = subprocess.run(  # noqa: S603 S607
            ["bash", "gsane.sh", "validate"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0, (
            f"gsane.sh validate FAIL:\n{result.stdout[-500:]}\n{result.stderr[-200:]}"
        )

    @pytest.mark.e2e
    @pytest.mark.skipif(not _HAS_BASH, reason="bash non disponible")
    @pytest.mark.skipif(_IN_PYTEST, reason="Récursion pytest — gsane.sh vera relance pytest")
    def test_vera_security_scan_clean(self):
        """bash gsane.sh vera doit EXIT 0."""
        result = subprocess.run(  # noqa: S603 S607
            ["bash", "gsane.sh", "vera"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"Vera security scan FAIL:\n{result.stdout}\n{result.stderr}"
        )


class TestFrameworkEvolution:
    """Vérifie que le framework s'améliore lui-même."""

    @pytest.mark.e2e
    def test_session_count_increments(self, session_log):
        """Le compteur de sessions doit être > 1."""
        if not session_log:
            pytest.skip("session-analysis-log.md absent")

        numbers = re.findall(r"Session #(\d+)", session_log)
        if not numbers:
            pytest.skip("Aucun numéro de session trouvé")

        max_session = max(int(n) for n in numbers)
        assert max_session > 1, (
            f"Session count bloqué à {max_session} — session-start.sh ne s'incrémente pas"
        )

    @pytest.mark.e2e
    def test_no_legacy_in_recent_commits(self):
        """Aucune référence legacy dans les 20 derniers commits."""
        result = subprocess.run(  # noqa: S603 S607
            ["git", "log", "--oneline", "-20"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            pytest.skip("Git non disponible")

        legacy = ["CIS", "TEA", "BMB"]
        violations = []
        for line in result.stdout.splitlines():
            for term in legacy:
                if term in line:
                    violations.append(f"'{term}' dans commit: {line}")

        assert not violations, "Dérive legacy dans commits récents:\n" + "\n".join(
            f"  - {v}" for v in violations
        )

    @pytest.mark.e2e
    def test_mutation_score_above_threshold(self, gsane_config):
        """Si mutation testing a tourné, score doit être au-dessus du seuil."""
        mut = gsane_config.get("mutation_testing", {})
        last_score = mut.get("last_score")
        min_score = int(float(mut.get("min_score", 0.70)) * 100)

        if last_score is None:
            pytest.skip("Mutation jamais lancé — skip")

        assert last_score >= min_score, (
            f"Mutation score en régression:\n"
            f"  Score actuel : {last_score}%\n"
            f"  Seuil minimum: {min_score}%"
        )

    @pytest.mark.e2e
    def test_benchmark_baseline_documented(self, gsane_config):
        """Les baselines benchmark doivent être documentées dans config.yaml."""
        bench = gsane_config.get("benchmarks", {})
        baselines = bench.get("baselines", {})

        required_baselines = ["gsane_route_ms", "gsane_fetch_memory_ms", "yaml_parse_ms"]
        missing = [b for b in required_baselines if b not in baselines]
        assert not missing, "Baselines manquantes dans config.yaml:\n" + "\n".join(
            f"  - {m}" for m in missing
        )
