"""Tests for DC validator."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "_gsane" / "tools" / "dc-validator.py"


def run_validator(dc_file):
    """Run dc-validator.py on a file and return (exit_code, stdout)."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(dc_file)],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
        encoding="utf-8", errors="replace", env=env,
    )
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def test_valid_dc_passes():
    """A well-formed DC should PASS validation."""
    dc_file = REPO_ROOT / "_gsane-output" / "dc-P6C-agent-versioning.contract.md"
    if not dc_file.exists():
        pytest.skip("DC file not found")
    code, output = run_validator(dc_file)
    assert code == 0, f"Expected PASS but got FAIL:\n{output}"
    assert "PASS" in output


def test_dc_without_acceptance_criteria_fails(tmp_path):
    """A DC missing acceptance_criteria should FAIL."""
    bad_dc = tmp_path / "bad.md"
    bad_dc.write_text(
        '---\ntask_id: "TEST"\nowner: "Amelia"\nvalidation_agent: "Quinn"\n---\n'
        "# Delivery Contract\n## Mission Goal\nDo something\n## Architectural Constraints\nNone\n",
        encoding="utf-8",
    )
    code, output = run_validator(bad_dc)
    assert code == 1, f"Expected FAIL but got PASS:\n{output}"
    assert "FAIL" in output
    assert "acceptance_criteria" in output.lower()


def test_dc_schema_exists():
    """The JSON schema file must exist."""
    schema_path = REPO_ROOT / "_gsane" / "_config" / "dc-schema.json"
    assert schema_path.exists(), "dc-schema.json not found"
