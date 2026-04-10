"""Garde-fous de sécurité/hygiène sur les fichiers textuels suivis par Git."""

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "_gsane" / "tools"))

from security_gate import (  # type: ignore[import-not-found]
    scan_repo_for_local_paths,
    scan_repo_for_secrets,
)


def test_tracked_text_files_do_not_expose_local_absolute_paths():
    matches = scan_repo_for_local_paths(REPO_ROOT)
    assert not matches, "Chemins absolus locaux détectés dans des fichiers suivis par Git:\n" + "\n".join(matches)


def test_tracked_text_files_do_not_expose_strong_secret_signatures():
    matches = scan_repo_for_secrets(REPO_ROOT)
    assert not matches, "Signatures fortes de secrets détectées dans des fichiers suivis par Git:\n" + "\n".join(matches)
