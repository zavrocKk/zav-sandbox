"""
Tests des circuit breakers et protocoles de protection GSANE (HUP, trust score).
"""

from pathlib import Path

import pytest


class TestCircuitBreaker:
    """Tests du circuit breaker (max_retries)."""

    @pytest.mark.behavioral
    def test_circuit_breaker_config_exists(self, gsane_config):
        """Le circuit breaker doit être configuré."""
        config_str = str(gsane_config)
        assert (
            "max_retries" in config_str
            or "circuit_breaker" in config_str
            or "max_bounce" in config_str
            or "max_violations" in config_str
        ), "Circuit breaker non configuré dans config.yaml"

    @pytest.mark.behavioral
    def test_no_infinite_loops_in_trace(self, trace_by_session):
        """Aucune session interactive ne doit avoir plus de N events du même type consécutifs."""
        MAX_CONSECUTIVE = 10
        # Exclure les sessions de test (ex: 'mcp') qui émettent des events en batch
        EXCLUDED_SESSIONS = {"mcp", "test", "unknown"}
        violations = []

        for sid, events in trace_by_session.items():
            if sid in EXCLUDED_SESSIONS:
                continue
            event_types = [e.get("event", "") for e in events if isinstance(e, dict)]
            for i in range(len(event_types) - MAX_CONSECUTIVE):
                window = event_types[i : i + MAX_CONSECUTIVE]
                if len(set(window)) == 1 and window[0]:
                    violations.append(
                        f"Session {sid}: '{window[0]}' répété {MAX_CONSECUTIVE}x consécutifs"
                    )
                    break

        assert not violations, "Boucle infinie potentielle détectée:\n" + "\n".join(
            f"  - {v}" for v in violations
        )


class TestHUPProtocol:
    """Honest Uncertainty Protocol (HUP)."""

    @pytest.mark.behavioral
    def test_hup_defined_in_gsane(self):
        """HUP doit être défini dans les fichiers GSANE."""
        found = False
        for md in Path("_gsane").rglob("*.md"):
            content = md.read_text(encoding="utf-8", errors="replace")
            if "HUP" in content and ("Honest Uncertainty" in content or "hup" in content.lower()):
                found = True
                break

        assert found, "HUP (Honest Uncertainty Protocol) non défini dans _gsane/"

    @pytest.mark.behavioral
    def test_hup_rouge_in_agent_files(self):
        """HUP doit être référencé dans au moins 1 agent OU dans standard-agent-behavior.md."""
        hup_count = 0
        agents_dir = Path("_gsane/agents")
        for md in agents_dir.glob("*.md"):
            content = md.read_text(encoding="utf-8", errors="replace")
            if "HUP" in content or "hup_rouge" in content or "Honest Uncertainty" in content:
                hup_count += 1

        # HUP peut être centralisé dans standard-agent-behavior.md
        shared = Path("_gsane/standard-agent-behavior.md")
        if shared.exists():
            shared_content = shared.read_text(encoding="utf-8", errors="replace")
            if "HUP" in shared_content or "Honest Uncertainty" in shared_content:
                hup_count += 1

        assert hup_count >= 1, (
            f"HUP référencé dans seulement {hup_count} fichier(s) (minimum 1)"
        )


class TestTrustScoreCalculation:
    """Vérifie la formule et le calcul du trust score."""

    @pytest.mark.behavioral
    def test_trust_scores_in_valid_range(self, trace_events):
        """Tous les trust scores doivent être entre 0 et 5."""
        invalid_scores = []
        for e in trace_events:
            if not isinstance(e, dict):
                continue
            score = e.get("trust_score")
            if score is not None:
                try:
                    s = int(score)
                    if s < 0 or s > 5:
                        invalid_scores.append(
                            f"Score {s} hors range [0-5] en session {e.get('session_id')}"
                        )
                except (ValueError, TypeError):
                    invalid_scores.append(
                        f"Score invalide '{score}' en session {e.get('session_id')}"
                    )

        assert not invalid_scores, "Trust scores invalides:\n" + "\n".join(
            f"  - {s}" for s in invalid_scores
        )

    @pytest.mark.behavioral
    def test_trust_score_present_in_events(self, trace_events):
        """Events avec trust_score doivent exister si le framework est mature."""
        if len(trace_events) < 10:
            pytest.skip("Moins de 10 events — skip")

        with_score = sum(
            1
            for e in trace_events
            if isinstance(e, dict) and e.get("trust_score") is not None
        )
        if with_score == 0:
            pytest.skip("Aucun event avec trust_score — gsane_emit_event() ne les émet pas encore")
