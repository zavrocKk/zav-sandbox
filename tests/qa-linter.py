
import glob
import os
import re
import sys
import yaml

def check_file(path):
    errors = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if '{{project_name}}' in content:
        print(f'[FAIL] {path}: Found forbidden macro {{project_name}}')
        errors += 1

    if '{project-root}' in content:
        print(f'[FAIL] {path}: Found forbidden pseudo-variable {{project-root}}')
        errors += 1
        
    if '<menu>' in content:
        print(f'[FAIL] {path}: Found forbidden legacy <menu> tag (Zero-Touch architecture violation)')
        errors += 1

    if re.search(r'\b(cis|tea|bmb)/', content, re.IGNORECASE):
        print(f'[FAIL] {path}: Found forbidden legacy module path (cis/, tea/, bmb/ are deprecated)')
        errors += 1

    return errors

# ──────────────────────────────────────────────────────────────
# 1b — Legacy terms scanner
# ──────────────────────────────────────────────────────────────

LEGACY_TERMS = [
    "léo", "leo (optimizer)", "aria (compliance)", "aria (aria)",
    "murat", "wendy", "morgan", "carson", "_gsane/core/",
    "agent-manifest.csv", "workflow-manifest.csv",
    "gsane-creative-intelligence-suite", "gsane-method-test-architecture",
    "gsane-builder-module-builder",
    "EXPECTED_AGENTS=25", "expected_agents=25",
]

LEGACY_SCAN_FILES = [
    ".github/hooks/session-start.sh",
    ".github/hooks/session-stop.sh",
    ".github/hooks/flywheel-trigger.sh",
    "_gsane/_config/manifest.yaml",
    "_gsane/_config/gsane-help.yaml",
    "_gsane/workflows/flywheel/workflow-aggregate.md",
    "_gsane/workflows/flywheel/workflow-apply.md",
    "_gsane/_memory/sessions/session-analysis-log.md",
    "gsane.sh",
]


def check_legacy_references(files_to_scan):
    """Scan files for forbidden legacy terms. Returns list of (file, line_no, term)."""
    hits = []
    for filepath in files_to_scan:
        try:
            with open(filepath, "r", encoding="utf-8") as fh:
                for line_no, line in enumerate(fh, start=1):
                    low = line.lower()
                    for term in LEGACY_TERMS:
                        if term.lower() in low:
                            hits.append((filepath, line_no, term))
        except (OSError, UnicodeDecodeError):
            pass
    return hits


# ──────────────────────────────────────────────────────────────
# 1b — Hooks check
# ──────────────────────────────────────────────────────────────

def check_hooks():
    """Vérifie que les hooks ne référencent pas _gsane/core/ et ont les bons chemins."""
    errors = 0
    hooks = {
        ".github/hooks/session-start.sh": {
            "must_contain": "_gsane/config.yaml",
            "must_not_contain": "_gsane/core/",
        },
        ".github/hooks/session-stop.sh": {
            "must_contain": "_gsane/workflows/",
            "must_not_contain": "_gsane/core/",
        },
        ".github/hooks/flywheel-trigger.sh": {
            "must_contain": "_gsane/workflows/",
            "must_not_contain": "_gsane/core/",
        },
    }
    for hook_path, rules in hooks.items():
        if not os.path.isfile(hook_path):
            print(f"[WARN] {hook_path}: fichier absent (skip)")
            continue
        with open(hook_path, "r", encoding="utf-8") as fh:
            content = fh.read()
        if rules["must_contain"] not in content:
            print(f"[FAIL] {hook_path}: manque '{rules['must_contain']}'")
            errors += 1
        if rules["must_not_contain"] in content:
            print(f"[FAIL] {hook_path}: référence legacy '{rules['must_not_contain']}'")
            errors += 1
    return errors


# ──────────────────────────────────────────────────────────────
# 1c — Manifests YAML check
# ──────────────────────────────────────────────────────────────

def check_all_manifests():
    """Charge tous les _gsane/_config/*.yaml et vérifie qu'ils parsent sans erreur."""
    errors = 0
    files = glob.glob("_gsane/_config/*.yaml")
    if not files:
        print("[FAIL] check_all_manifests: aucun fichier YAML trouvé dans _gsane/_config/")
        return 1
    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            yaml.safe_load(content)
        except yaml.YAMLError as exc:
            print(f"[FAIL] {filepath}: erreur de parsing YAML — {exc}")
            errors += 1
            continue
        if "manifest.yaml" in filepath:
            forbidden = ["creative-intelligence-suite", "test-architecture-enterprise"]
            for term in forbidden:
                if term in content:
                    print(f"[FAIL] {filepath}: contient terme déprécié '{term}'")
                    errors += 1
    return errors


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python qa-linter.py <file-to-test>')
        sys.exit(1)
        
    total_errors = 0
    for target in sys.argv[1:]:
        if os.path.isfile(target):
            total_errors += check_file(target)
    
    # ── Nouvelles vérifications ──────────────────────────────────
    legacy_hits = check_legacy_references(LEGACY_SCAN_FILES)
    for filepath, line_no, term in legacy_hits:
        print(f"[FAIL] {filepath}:{line_no}: référence legacy trouvée — '{term}'")
        total_errors += 1

    total_errors += check_hooks()
    total_errors += check_all_manifests()
    # ────────────────────────────────────────────────────────────

    if total_errors > 0:
        print(f'\nQA LINTER FAILED with {total_errors} errors.')
        sys.exit(1)
    else:
        print('\nQA LINTER PASSED. Output is strictly compliant.')
        sys.exit(0)

