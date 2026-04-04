#!/usr/bin/env python3
"""
_gsane/tools/harmony_audit.py — Outil d'audit architectural HarmonyCheck.
Inspiré du HarmonyCheck de Grimoire-kit.

Analyses :
  1. Agents Orphelins   — agents sans aucune référence dans le projet
  2. Budget de Contexte — agents chargeant trop de tokens au démarrage
  3. Fichiers Morts     — fichiers _gsane/ non référencés nulle part

Usage : python _gsane/tools/harmony_audit.py
"""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────

ROOT          = Path(__file__).resolve().parents[2]
AGENT_DIRS    = [ROOT / ".github/agents", ROOT / "_gsane/core/agents"]
REF_DIRS      = [
    ROOT / ".github/prompts",
    ROOT / "_gsane/_config",
    ROOT / "_gsane/core/workflows",
    ROOT / "_gsane/bmb/workflows",
    ROOT / "_gsane/tea/workflows",
    ROOT / "_gsane/cis/workflows",
]
DEAD_FILE_ROOT  = ROOT / "_gsane"
OUTPUT_PATH     = ROOT / "_gsane-output" / "harmony-audit-report.json"
BUDGET_THRESHOLD = 20_000   # tokens
CHARS_PER_TOKEN  = 4         # estimation standard

AGENT_EXTS   = {".md"}
SEARCH_EXTS  = {".md", ".yaml", ".yml", ".csv", ".json", ".sh", ".py"}
DEAD_EXTS    = {".md", ".yaml", ".yml", ".csv"}

# Dossiers à exclure de la détection de fichiers morts
DEAD_EXCLUDE_DIRS = {"_memory/sessions", "archive", "_gsane-output"}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _all_files(root: Path, exts: set) -> list[Path]:
    results = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in exts:
            results.append(p)
    return results


def _extract_frontmatter_name(content: str) -> str | None:
    # Accepte optionnellement un code fence (```chatagent) avant ---
    m = re.match(r"^(?:```\w+\n)?---\n(.*?)---\n", content, re.DOTALL)
    if not m:
        return None
    fm = m.group(1)
    nm = re.search(r'^name:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
    return nm.group(1).strip() if nm else None


def _agent_identifiers(p: Path, content: str) -> set[str]:
    """Retourne tous les identifiants possibles d'un agent pour la recherche de références."""
    ids = set()

    # Logical stem : retire tous les suffixes composés (.agent.md, .prompt.md, etc.)
    name_no_ext = p.name
    for ext in (".agent.md", ".prompt.md", ".md", ".yaml"):
        if name_no_ext.endswith(ext):
            name_no_ext = name_no_ext[: -len(ext)]
            break
    stem = name_no_ext  # ex: "gsane-agent-bmb-bond" (sans .agent)

    # 1. Stem logique complet
    ids.add(stem)

    # 2. Nom friendly (champ name: du frontmatter)
    fm_name = _extract_frontmatter_name(content)
    if fm_name:
        ids.add(fm_name)

    # 3. Variantes courtes dérivées du stem
    # gsane-agent-bmb-bond → short = "bond"
    m = re.match(r"^gsane-agent-(?:[a-z]+-)?(.+)$", stem)
    if m:
        short = m.group(1)   # ex: "bond", "cis-dev", etc.
        ids.add(short)
        parts = short.split("-", 1)
        ids.add(parts[0])    # premier segment
        ids.add(parts[-1])   # dernier segment (si slug composé comme cis-dev → dev)

    # 4. ID explicite dans le frontmatter
    aid = re.search(r'^(?:id|agent.?id):\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if aid:
        ids.add(aid.group(1).strip())

    # Filtrer les tokens trop courts (< 3 chars)
    ids = {i for i in ids if i and len(i) >= 3}
    return ids


def _collect_reference_corpus() -> str:
    """Concatène TOUT le projet (hors .git/.venv) en une seule chaîne.
    Utilisé pour la détection d'orphelins : si un identifiant n'est nulle part,
    l'agent est réellement orphelin."""
    corpus_parts = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p)
        if any(excl in rel for excl in [".git\\", ".git/", ".venv", "__pycache__", ".mypy_cache"]):
            continue
        if p.suffix in SEARCH_EXTS:
            corpus_parts.append(_read(p))
    return "\n".join(corpus_parts)


# ── Analyse 1 — Agents Orphelins ─────────────────────────────────────────────

def analyse_orphan_agents(corpus: str) -> list[dict]:
    orphans = []
    for agent_dir in AGENT_DIRS:
        if not agent_dir.exists():
            continue
        for p in agent_dir.iterdir():
            if not p.is_file() or p.suffix not in AGENT_EXTS:
                continue
            content = _read(p)
            identifiers = _agent_identifiers(p, content)

            referenced = any(ident in corpus for ident in identifiers)
            if not referenced:
                orphans.append({
                    "file": str(p.relative_to(ROOT)),
                    "name": _extract_frontmatter_name(content) or p.stem,
                    "identifiers_checked": sorted(identifiers),
                })
    return orphans


# ── Analyse 2 — Budget de Contexte ───────────────────────────────────────────

def _estimate_load_tokens(agent_content: str) -> int:
    """Cherche les patterns LOAD / read_file / exec dans le contenu et somme les tailles."""
    total_chars = len(agent_content)  # l'agent lui-même
    # Patterns : LOAD path, exec="path", read _gsane/...
    paths_found = re.findall(
        r'(?:LOAD|exec="|exec=\'|read\s+)([^\s"\'<>\n]+\.(?:md|yaml|yml|csv))',
        agent_content, re.IGNORECASE
    )
    for rel_path in paths_found:
        candidate = ROOT / rel_path.lstrip("{project-root}/")
        if candidate.exists():
            total_chars += candidate.stat().st_size
    return total_chars // CHARS_PER_TOKEN


def analyse_budget(corpus_unused: str) -> list[dict]:
    over_budget = []
    for agent_dir in AGENT_DIRS:
        if not agent_dir.exists():
            continue
        for p in agent_dir.iterdir():
            if not p.is_file() or p.suffix not in AGENT_EXTS:
                continue
            content = _read(p)
            name    = _extract_frontmatter_name(content) or p.stem
            tokens  = _estimate_load_tokens(content)
            if tokens > BUDGET_THRESHOLD:
                over_budget.append({
                    "file":   str(p.relative_to(ROOT)),
                    "name":   name,
                    "tokens": tokens,
                    "threshold": BUDGET_THRESHOLD,
                })
    return over_budget


# ── Analyse 3 — Fichiers Morts dans _gsane/ ──────────────────────────────────

def _build_full_corpus_paths() -> tuple[str, list[Path]]:
    """Corpus étendu (tout le projet) + liste des fichiers gsane à analyser."""
    all_files: list[Path] = []
    content_parts: list[str] = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(excl in str(p) for excl in [".git/", ".venv/", "__pycache__", ".mypy_cache"]):
            continue
        if p.suffix in SEARCH_EXTS:
            content_parts.append(_read(p))
            all_files.append(p)
    return "\n".join(content_parts), all_files


def analyse_dead_files() -> list[dict]:
    full_corpus, _ = _build_full_corpus_paths()
    dead = []

    for p in _all_files(DEAD_FILE_ROOT, DEAD_EXTS):
        # Exclure les dossiers bannis
        rel = p.relative_to(ROOT)
        rel_str = str(rel).replace("\\", "/")
        if any(excl in rel_str for excl in DEAD_EXCLUDE_DIRS):
            continue
        # Un fichier est "mort" si son chemin relatif (ou son stem) n'est cité nulle part
        stem = p.stem
        rel_posix = rel.as_posix()
        hits = full_corpus.count(rel_posix) + full_corpus.count(stem)
        # Le fichier se cite lui-même → compter à partir de 2
        if hits <= 1:
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")
            dead.append({
                "file":          rel_posix,
                "last_modified": mtime,
                "stem":          stem,
            })
    return dead


# ── Score & Rapport ───────────────────────────────────────────────────────────

def compute_score(orphans: list, over_budget: list, dead_files: list) -> int:
    score = 100
    score -= len(orphans)    * 10
    score -= len(over_budget) * 5
    score -= len(dead_files) * 2
    return max(0, score)


def print_report(score: int, orphans: list, over_budget: list, dead_files: list) -> None:
    sep = "─" * 60
    print(f"\n{'═'*60}")
    print(f"  HARMONY AUDIT — zav-sandbox")
    print(f"  Score: {score}/100")
    print(f"{'═'*60}")

    print(f"\n{sep}")
    print(f"  Agents orphelins : {len(orphans)}")
    for o in orphans:
        print(f"    ⚠  {o['name']}  ({o['file']})")

    print(f"\n{sep}")
    print(f"  Budget dépassé   : {len(over_budget)} agents (seuil : {BUDGET_THRESHOLD} tokens)")
    for b in over_budget:
        print(f"    ⚠  {b['name']}  — {b['tokens']:,} tokens  ({b['file']})")

    print(f"\n{sep}")
    print(f"  Fichiers morts   : {len(dead_files)}")
    for d in dead_files:
        print(f"    💀  {d['file']}  (modifié : {d['last_modified']})")

    print(f"\n{'═'*60}\n")


def save_json(score: int, orphans: list, over_budget: list, dead_files: list) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "score":        score,
        "orphan_agents":  orphans,
        "budget_exceeded": over_budget,
        "dead_files":     dead_files,
    }
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  → Rapport JSON sauvegardé : {OUTPUT_PATH.relative_to(ROOT)}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("🔍 Lancement du HarmonyAudit…")
    corpus  = _collect_reference_corpus()
    orphans    = analyse_orphan_agents(corpus)
    over_budget = analyse_budget(corpus)
    dead_files  = analyse_dead_files()
    score       = compute_score(orphans, over_budget, dead_files)
    print_report(score, orphans, over_budget, dead_files)
    save_json(score, orphans, over_budget, dead_files)


if __name__ == "__main__":
    main()
