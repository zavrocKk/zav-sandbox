"""
Tests comportementaux GSANE.
Vérifient les décisions réelles des agents depuis trace.log et les checkpoints MCP.
Skip si données insuffisantes.
"""

import re
import sys

import pytest

sys.path.insert(0, "_gsane/mcp-server")
from compression_tool import gsane_read_checkpoint  # noqa: E402

MIN_SESSIONS_REQUIRED = 3


class TestSoloCreepDetection:
    """Détecte les patterns de solo-creep."""

    @pytest.mark.behavioral
    def test_no_code_produced_by_langis(self, trace_events):
        """Langis ne doit pas produire de code directement."""
        if len(trace_events) < 5:
            pytest.skip("Moins de 5 events — données insuffisantes")

        solo_creep_detected = []
        for event in trace_events:
            if not isinstance(event, dict):
                continue
            if event.get("agent") in ["master", "langis"]:
                details = str(event.get("details", "")).lower()
                code_signals = ["def ", "class ", "import ", "```python", "return ", "async def"]
                if any(s in details for s in code_signals):
                    solo_creep_detected.append(
                        {
                            "session": event.get("session_id"),
                            "event": event.get("event"),
                            "details": details[:100],
                        }
                    )

        assert not solo_creep_detected, (
            f"Solo-creep détecté dans {len(solo_creep_detected)} events:\n"
            + "\n".join(f"  Session {s['session']}: {s['details']}" for s in solo_creep_detected[:3])
        )

    @pytest.mark.behavioral
    def test_checkpoint_agent_is_specialist(self):
        """Le dernier checkpoint MCP doit être produit par un spécialiste, pas Langis."""
        checkpoint = gsane_read_checkpoint()
        if not checkpoint:
            pytest.skip("Aucun checkpoint MCP")

        checkpoint_str = str(checkpoint).lower()
        if any(w in checkpoint_str for w in ["implement", "code", "function"]):
            assert "amelia" in checkpoint_str or "dev" in checkpoint_str, (
                f"Checkpoint de code par non-Amelia:\n{str(checkpoint)[:200]}"
            )


class TestChallengeProtocol:
    """Vérifie l'intégrité du protocole CHALLENGE."""

    @pytest.mark.behavioral
    def test_all_challenges_resolved(self, challenge_events, trace_events):
        """Tout CHALLENGE émis doit avoir une résolution."""
        if not challenge_events:
            pytest.skip("Aucun CHALLENGE dans trace.log")

        resolution_types = ["challenge_resolved", "challenge_accepted", "challenge_overruled"]
        unresolved = []
        for ch in challenge_events:
            sid = ch.get("session_id")
            resolved = any(
                isinstance(e, dict)
                and e.get("event") in resolution_types
                and e.get("session_id") == sid
                for e in trace_events
            )
            if not resolved:
                unresolved.append(f"Session {sid}: {ch.get('details', '')[:80]}")

        assert not unresolved, f"{len(unresolved)} CHALLENGE(s) non résolus:\n" + "\n".join(
            f"  - {u}" for u in unresolved
        )

    @pytest.mark.behavioral
    def test_challenge_has_source_and_target(self, challenge_events):
        """Chaque CHALLENGE doit avoir source et cible différentes."""
        if not challenge_events:
            pytest.skip("Aucun CHALLENGE")

        invalid = []
        for ch in challenge_events:
            details = str(ch.get("details", ""))
            match = re.search(r"\[?(\w+)\]?\s*→\s*\[?(\w+)\]?", details)
            if match:
                source, target = match.group(1), match.group(2)
                if source.lower() == target.lower():
                    invalid.append(f"Auto-challenge: {source} → {target}")

        assert not invalid, "CHALLENGEs invalides (source = cible):\n" + "\n".join(
            f"  - {i}" for i in invalid
        )


class TestQualityGateBehavior:
    """Vérifie que Quinn ne laisse pas passer les bugs."""

    @pytest.mark.behavioral
    def test_qa_gate_fail_before_pass(self, trace_events):
        """Dans une session avec FAIL puis PASS, le FAIL doit précéder le PASS."""
        # Exclure les sessions de test qui émettent des events en batch
        EXCLUDED_SESSIONS = {"mcp", "test", "unknown"}
        sessions_with_both: dict[str, list] = {}
        for e in trace_events:
            if not isinstance(e, dict):
                continue
            sid = e.get("session_id")
            if sid in EXCLUDED_SESSIONS:
                continue
            event = e.get("event")
            if event in ["qa_gate_passed", "qa_gate_failed"]:
                sessions_with_both.setdefault(sid, []).append(event)

        violations = []
        for sid, events in sessions_with_both.items():
            if "qa_gate_passed" in events and "qa_gate_failed" in events:
                first_pass = next(
                    (i for i, e in enumerate(events) if e == "qa_gate_passed"), None
                )
                first_fail = next(
                    (i for i, e in enumerate(events) if e == "qa_gate_failed"), None
                )
                if (
                    first_pass is not None
                    and first_fail is not None
                    and first_pass < first_fail
                ):
                    violations.append(f"Session {sid}: PASS avant FAIL")

        assert not violations, "Quinn permissive détectée:\n" + "\n".join(
            f"  - {v}" for v in violations
        )


class TestTrustScoreEvolution:
    """Vérifie l'évolution du trust score."""

    @pytest.mark.behavioral
    def test_trust_score_not_regressing(self, trace_events):
        """Le trust score moyen récent ne doit pas régresser de plus de 15%."""
        scores = [
            int(e.get("trust_score", 0))
            for e in trace_events
            if isinstance(e, dict) and e.get("trust_score") is not None
        ]
        if len(scores) < MIN_SESSIONS_REQUIRED * 2:
            pytest.skip(f"Moins de {MIN_SESSIONS_REQUIRED * 2} scores — skip")

        recent = scores[-5:]
        older = scores[:-5]
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)

        assert recent_avg >= older_avg * 0.85, (
            f"Trust score en régression:\n"
            f"  Récent  : {recent_avg:.2f} ({recent})\n"
            f"  Ancien  : {older_avg:.2f}\n"
            f"  Seuil   : {older_avg * 0.85:.2f}"
        )
