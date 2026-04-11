import importlib.util
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.compliance

QA_LINTER_PATH = Path(__file__).resolve().parents[1] / "qa-linter.py"
SPEC = importlib.util.spec_from_file_location("qa_linter_script", QA_LINTER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Impossible de charger {QA_LINTER_PATH}")

qa_linter = importlib.util.module_from_spec(SPEC)
sys.modules["qa_linter_script"] = qa_linter
SPEC.loader.exec_module(qa_linter)


def test_no_legacy_refs_in_readme():
    qa_linter.test_no_legacy_refs_in_readme()
