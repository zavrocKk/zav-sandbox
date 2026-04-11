from __future__ import annotations

import argparse
import logging
import re
import subprocess  # nosec B404
import sys
import unicodedata
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from importlib.util import find_spec
from pathlib import Path

import yaml  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
GSANE_ROOT = REPO_ROOT / "_gsane"
DELEGATION_MATRIX_PATH = GSANE_ROOT / "_config" / "delegation-matrix.yaml"

LOCAL_PATH_PATTERNS = [
    (
        "Windows user path",
        re.compile(r"[A-Za-z]:[/\\](?:Users|Documents and Settings)[/\\][^\s\"'`]+"),
    ),
    (
        "Windows escaped user path",
        re.compile(r"[A-Za-z]:\\\\(?:Users|Documents and Settings)\\\\[^\s\"'`]+"),
    ),
    ("macOS home path", re.compile(r"/Users/[^/\s]+/[^\s\"'`]+")),
    ("Linux home path", re.compile(r"/home/[^/\s]+/[^\s\"'`]+")),
    ("macOS private temp path", re.compile(r"/private/var/[^\s\"'`]+")),
]

SECRET_PATTERNS = [
    ("GitHub personal access token", re.compile(r"\bghp_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    (
        "Private key header",
        re.compile(r"-----BEGIN (?:RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----"),
    ),
]


@dataclass(frozen=True)
class SecurityClassification:
    is_security_request: bool
    matched_topics: tuple[str, ...]
    matched_keywords: tuple[str, ...]
    escalation_agent: str
    owner: str
    validation_agent: str
    bond_review_required: bool
    bond_review_agent: str | None
    bond_review_reasons: tuple[str, ...]


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    without_accents = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )
    return re.sub(r"\s+", " ", without_accents.lower()).strip()


def load_delegation_matrix(matrix_path: Path = DELEGATION_MATRIX_PATH) -> dict:
    with matrix_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_security_gate_config(matrix_path: Path = DELEGATION_MATRIX_PATH) -> dict:
    matrix = load_delegation_matrix(matrix_path)
    security_gate = matrix.get("security_gate")
    if not isinstance(security_gate, dict):
        raise ValueError(
            "Le bloc 'security_gate' est absent de delegation-matrix.yaml."
        )
    return security_gate


def _dedupe(values: Iterable[str]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = normalize_text(value)
        if key and key not in seen:
            seen.add(key)
            ordered.append(value)
    return tuple(ordered)


def _keyword_hits(text: str, keywords: Sequence[str]) -> tuple[str, ...]:
    hits = [keyword for keyword in keywords if normalize_text(keyword) in text]
    return _dedupe(hits)


def classify_security_request(
    query: str, matrix_path: Path = DELEGATION_MATRIX_PATH
) -> SecurityClassification:
    config = load_security_gate_config(matrix_path)
    normalized_query = normalize_text(query)

    matched_topics: list[str] = []
    matched_keywords: list[str] = []
    for topic_name, topic_config in (config.get("topics") or {}).items():
        keywords = (topic_config or {}).get("keywords") or []
        hits = _keyword_hits(normalized_query, keywords)
        if hits:
            matched_topics.append(str(topic_name))
            matched_keywords.extend(hits)

    bond_config = config.get("bond_review") or {}
    bond_hits = _keyword_hits(
        normalized_query, bond_config.get("required_keywords") or []
    )

    return SecurityClassification(
        is_security_request=bool(matched_topics),
        matched_topics=_dedupe(matched_topics),
        matched_keywords=_dedupe(matched_keywords),
        escalation_agent=str(config.get("escalation_agent", "master")),
        owner=str(config.get("owner", "architect")),
        validation_agent=str(config.get("validation_agent", "qa")),
        bond_review_required=bool(bond_hits),
        bond_review_agent=(
            str(bond_config.get("agent", "bond")) if bond_hits else None
        ),
        bond_review_reasons=bond_hits,
    )


def get_dependency_sources(
    matrix_path: Path = DELEGATION_MATRIX_PATH,
) -> tuple[Path, ...]:
    config = load_security_gate_config(matrix_path)
    sources = (config.get("dependency_sources") or {}).get("python") or []
    return tuple((REPO_ROOT / source).resolve() for source in sources)


def get_reevaluation_thresholds(matrix_path: Path = DELEGATION_MATRIX_PATH) -> dict:
    config = load_security_gate_config(matrix_path)
    thresholds = config.get("reevaluation_thresholds") or {}
    if not isinstance(thresholds, dict):
        raise ValueError("Le bloc 'reevaluation_thresholds' doit être un mapping.")
    return thresholds


def get_bandit_targets(matrix_path: Path = DELEGATION_MATRIX_PATH) -> tuple[Path, ...]:
    config = load_security_gate_config(matrix_path)
    targets = ((config.get("validation") or {}).get("sast") or {}).get("targets") or []
    return tuple((REPO_ROOT / target).resolve() for target in targets)


def get_allowed_mcp_roots(
    matrix_path: Path = DELEGATION_MATRIX_PATH,
) -> tuple[Path, ...]:
    config = load_security_gate_config(matrix_path)
    roots = ((config.get("mcp") or {}).get("allowed_roots")) or []
    return tuple((REPO_ROOT / root).resolve() for root in roots)


def get_allowed_mcp_agents(
    matrix_path: Path = DELEGATION_MATRIX_PATH,
) -> tuple[str, ...]:
    config = load_security_gate_config(matrix_path)
    return tuple(((config.get("mcp") or {}).get("allowed_agents")) or [])


def is_allowed_mcp_agent_name(
    agent_name: str, matrix_path: Path = DELEGATION_MATRIX_PATH
) -> bool:
    allowed = {normalize_text(name) for name in get_allowed_mcp_agents(matrix_path)}
    return normalize_text(agent_name) in allowed


def is_path_within_root(candidate: Path, root: Path) -> bool:
    resolved_candidate = candidate.resolve()
    resolved_root = root.resolve()
    return (
        resolved_candidate == resolved_root
        or resolved_root in resolved_candidate.parents
    )


def ensure_path_within_roots(candidate: Path, allowed_roots: Sequence[Path]) -> Path:
    resolved_candidate = candidate.resolve()
    if any(is_path_within_root(resolved_candidate, root) for root in allowed_roots):
        return resolved_candidate
    raise ValueError(f"Path '{candidate}' is outside the allowed MCP roots.")


def list_repository_files(
    repo_root: Path = REPO_ROOT, staged_only: bool = False
) -> list[Path]:
    command = ["git", "ls-files", "-z"]
    if staged_only:
        command = ["git", "diff", "--cached", "--name-only", "-z", "--diff-filter=ACM"]

    result = subprocess.run(  # nosec B603
        command,
        cwd=repo_root,
        capture_output=True,
        check=True,
    )

    paths: list[Path] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        paths.append(repo_root / raw_path.decode("utf-8"))
    return paths


def _read_repository_text_file(
    path: Path,
    repo_root: Path = REPO_ROOT,
    staged_only: bool = False,
) -> tuple[str, str] | None:
    rel_path = path.relative_to(repo_root).as_posix()
    if staged_only:
        result = subprocess.run(  # nosec B603 B607
            ["git", "show", f":{rel_path}"],
            cwd=repo_root,
            capture_output=True,
        )
        if result.returncode != 0:
            return None
        data = result.stdout
    else:
        if not path.exists() or path.is_dir():
            return None
        data = path.read_bytes()

    if b"\0" in data:
        return None

    return rel_path, data.decode("utf-8", errors="replace")


_SELF_PATH = Path(__file__).resolve()


def collect_text_matches(
    repo_root: Path,
    patterns: Sequence[tuple[str, re.Pattern[str]]],
    staged_only: bool = False,
) -> list[str]:
    matches: list[str] = []
    for path in list_repository_files(repo_root, staged_only=staged_only):
        if path.resolve() == _SELF_PATH:
            continue
        text_blob = _read_repository_text_file(
            path,
            repo_root=repo_root,
            staged_only=staged_only,
        )
        if text_blob is None:
            continue

        rel_path, content = text_blob
        for line_number, line in enumerate(content.splitlines(), start=1):
            for label, pattern in patterns:
                if pattern.search(line):
                    matches.append(f"{rel_path}:{line_number} matches {label}")
                    break
    return matches


def scan_repo_for_secrets(
    repo_root: Path = REPO_ROOT, staged_only: bool = False
) -> list[str]:
    return collect_text_matches(repo_root, SECRET_PATTERNS, staged_only=staged_only)


def scan_repo_for_local_paths(
    repo_root: Path = REPO_ROOT, staged_only: bool = False
) -> list[str]:
    return collect_text_matches(repo_root, LOCAL_PATH_PATTERNS, staged_only=staged_only)


def _module_available(module_name: str) -> bool:
    return find_spec(module_name) is not None


def _relative_display(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def run_bandit(repo_root: Path = REPO_ROOT, staged_only: bool = False) -> int:
    if staged_only:
        configured_targets = [path for path in get_bandit_targets() if path.exists()]
        staged_python_files = [
            path
            for path in list_repository_files(repo_root, staged_only=True)
            if path.suffix == ".py"
            and any(is_path_within_root(path, target) for target in configured_targets)
        ]
        if not staged_python_files:
            print("ℹ️ Aucun fichier Python en staging pour Bandit.")
            return 0
        if not _module_available("bandit"):
            print(
                "❌ Bandit n'est pas installé. Installez-le avec: python -m pip install bandit"
            )
            return 1
        command = [sys.executable, "-m", "bandit", "-q"]
        command.extend(_relative_display(path) for path in staged_python_files)
        return subprocess.run(command, cwd=repo_root).returncode  # nosec B603

    if not _module_available("bandit"):
        print(
            "❌ Bandit n'est pas installé. Installez-le avec: python -m pip install bandit"
        )
        return 1

    configured_targets = [path for path in get_bandit_targets() if path.exists()]

    if not configured_targets:
        print("❌ Aucun target Bandit configuré pour la gate sécurité.")
        return 1

    command = [sys.executable, "-m", "bandit", "-q", "-r"]
    command.extend(_relative_display(path) for path in configured_targets)
    return subprocess.run(command, cwd=repo_root).returncode  # nosec B603


def run_pip_audit(repo_root: Path = REPO_ROOT) -> int:
    if not _module_available("pip_audit"):
        print(
            "❌ pip-audit n'est pas installé. Installez-le avec: python -m pip install pip-audit"
        )
        return 1

    dependency_sources = [path for path in get_dependency_sources() if path.exists()]
    if not dependency_sources:
        print("❌ Aucune source de dépendances Python exploitable n'est configurée.")
        return 1

    exit_code = 0
    for source in dependency_sources:
        print(f"🔎 pip-audit sur {_relative_display(source)}")
        result = subprocess.run(  # nosec B603
            [
                sys.executable,
                "-m",
                "pip_audit",
                "-r",
                _relative_display(source),
                "--progress-spinner",
                "off",
            ],
            cwd=repo_root,
        )
        exit_code = max(exit_code, result.returncode)
    return exit_code


def run_secret_scan(repo_root: Path = REPO_ROOT, staged_only: bool = False) -> int:
    matches = scan_repo_for_secrets(repo_root, staged_only=staged_only)
    if matches:
        scope = "staging" if staged_only else "repo"
        print(f"❌ Signatures fortes de secrets détectées ({scope}) :")
        print("\n".join(matches))
        return 1
    print("✅ Scan secrets: aucune signature forte détectée.")
    return 0


def check_prompt_injection(
    agents_dir: Path = GSANE_ROOT / "agents",
) -> list[dict[str, str]]:
    """Check agent .md files for prompt injection patterns."""
    findings: list[dict[str, str]] = []
    patterns = [
        "ignore previous instructions",
        "disregard your rules",
        "you are now a",
        "<script",
        "javascript:",
        "system prompt",
    ]
    if not agents_dir.is_dir():
        return findings
    for f in sorted(agents_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8").lower()
        for p in patterns:
            if p in content:
                findings.append(
                    {
                        "file": f.name,
                        "pattern": p,
                        "severity": "HIGH",
                        "type": "prompt_injection",
                    }
                )
    return findings


def check_ci_permissions(
    workflows_dir: Path = REPO_ROOT / ".github" / "workflows",
) -> list[dict[str, str]]:
    """Check GitHub Actions workflows for overly broad permissions."""
    findings: list[dict[str, str]] = []
    if not workflows_dir.is_dir():
        return findings
    for f in sorted(workflows_dir.glob("*.yml")):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            perms = data.get("permissions", {})
            if perms == "write-all":
                findings.append(
                    {
                        "file": f.name,
                        "permission": "write-all",
                        "severity": "HIGH",
                        "type": "ci_permission",
                    }
                )
            if isinstance(perms, dict):
                for k, v in perms.items():
                    if v == "write" and k not in ("contents", "pull-requests"):
                        findings.append(
                            {
                                "file": f.name,
                                "permission": f"{k}: write",
                                "severity": "MEDIUM",
                                "type": "ci_permission",
                            }
                        )
        except Exception:
            logger.debug("Failed to parse %s for permission check", f.name)
    return findings


def run_vera_checks() -> dict:
    """Run the 2 unique Vera security checks and return a structured report."""
    prompt_findings = check_prompt_injection()
    ci_findings = check_ci_permissions()
    all_findings = prompt_findings + ci_findings
    has_high = any(f["severity"] == "HIGH" for f in all_findings)
    return {
        "status": "FINDING" if has_high else "CLEAR",
        "findings": all_findings,
        "summary": f"{len(all_findings)} finding(s)",
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GSANE Security Gate helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    secrets_parser = subparsers.add_parser("scan-secrets")
    secrets_parser.add_argument("--staged", action="store_true")

    bandit_parser = subparsers.add_parser("run-bandit")
    bandit_parser.add_argument("--staged", action="store_true")

    subparsers.add_parser("run-pip-audit")
    subparsers.add_parser("vera-checks")
    subparsers.add_parser("print-dependency-sources")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    # Reconfigure stdout/stderr to UTF-8 on Windows (avoids cp1252 UnicodeEncodeError with emoji)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = _build_parser().parse_args(argv)

    if args.command == "scan-secrets":
        return run_secret_scan(staged_only=args.staged)
    if args.command == "run-bandit":
        return run_bandit(staged_only=args.staged)
    if args.command == "run-pip-audit":
        return run_pip_audit()
    if args.command == "vera-checks":
        result = run_vera_checks()
        for f in result["findings"]:
            print(f"  [{f['severity']}] {f['file']} — {f['type']}: {f.get('pattern', f.get('permission', ''))}")
        if result["status"] == "FINDING":
            print(f"❌ Vera checks: {result['summary']}")
            return 1
        print(f"✅ Vera checks CLEAR: {result['summary']}")
        return 0
    if args.command == "print-dependency-sources":
        for source in get_dependency_sources():
            print(_relative_display(source))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
