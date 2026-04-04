#!/usr/bin/env python3
"""
_gsane/tools/fix_agent_names_v2.py — Renommage robuste des champs name: agents.
Approche : clé = nom de fichier (Path.name.split(".")[0]), pas le contenu actuel.

Usage:
  python _gsane/tools/fix_agent_names_v2.py          # dry-run (affiche le plan)
  python _gsane/tools/fix_agent_names_v2.py --apply  # applique les changements
"""
import re
import sys
from pathlib import Path

# ── Mapping approuvé ──────────────────────────────────────────────────────────

MAPPING = {
    "gsane-agent-cis-dev":                  "Amelia (Dev)",
    "gsane-agent-cis-qa":                   "Quinn (QA)",
    "gsane-agent-cis-tech-writer":          "Paige (Tech Writer)",
    "gsane-agent-cis-ux-designer":          "Sally (UX Designer)",
    "gsane-agent-cis-architect":            "Winston (Architect)",
    "gsane-agent-cis-pm":                   "John (PM)",
    "gsane-agent-cis-analyst":              "Mary (Analyst)",
    "gsane-agent-cis-sm":                   "Bob (Scrum Master)",
    "gsane-agent-cis-quick-flow-solo-dev":  "Barry (Quick Dev)",
    "gsane-agent-core-optimizer":           "Sentinel (Optimizer)",
    "gsane-agent-bmb-aria":                 "Aria (GSANE QA)",
    "gsane-agent-bmb-morgan":               "Morgan (Module Builder)",
    "gsane-agent-bmb-bond":                 "Bond (Agent Builder)",
    "gsane-agent-bmb-wendy":                "Wendy (Workflow Builder)",
    "gsane-agent-cis-brainstorming-coach":  "Carson (Brainstorming)",
    "gsane-agent-cis-creative-problem-solver": "Alex (Creative Solver)",
    "gsane-agent-cis-innovation-strategist": "Victor (Innovation)",
    "gsane-agent-cis-design-thinking-coach": "Maya (Design Thinking)",
    "gsane-agent-cis-storyteller":          "Sophia (Storyteller)",
    "gsane-agent-cis-presentation-master":  "Caravaggio (Presentation)",
    "gsane-agent-tea-tea":                  "Murat (Test Architect)",
    "master":                               "Langis (Master)",
    "concierge":                            "Langis (Master)",
}

AGENT_DIRS = [
    Path(".github/agents"),
    Path("_gsane/core/agents"),
]

# ── Helpers ───────────────────────────────────────────────────────────────────

NAME_RE = re.compile(r"^(name:\s*)([^\n]*)", re.MULTILINE)
# Accepte frontmatter optionnellement précédé d'un code-fence (```chatagent)
FM_RE   = re.compile(r"^(```\w+\n)?(---\n)(.*?)(---\n)", re.DOTALL)


def file_key(path: Path) -> str:
    """Extrait la clé de mapping depuis le nom de fichier.
    Ex: gsane-agent-cis-dev.agent.md → gsane-agent-cis-dev
        master.agent.md              → master
    """
    return path.name.split(".")[0]


def current_name(content: str) -> str | None:
    """Retourne la valeur actuelle du champ name: dans le frontmatter, ou None."""
    m = FM_RE.match(content)
    if not m:
        return None
    fm_body = m.group(3)
    nm = NAME_RE.search(fm_body)
    if not nm:
        return None
    raw = nm.group(2).strip().strip('"').strip("'")
    return raw


def set_name(content: str, new_name: str) -> str | None:
    """Remplace (ou ajoute) le champ name: dans le frontmatter.
    Retourne le nouveau contenu, ou None si pas de frontmatter trouvé."""
    m = FM_RE.match(content)
    if not m:
        return None

    fence       = m.group(1) or ""
    delim_open  = m.group(2)
    fm_body     = m.group(3)
    delim_close = m.group(4)
    rest        = content[m.end():]

    if NAME_RE.search(fm_body):
        new_fm = NAME_RE.sub(f'\\g<1>"{new_name}"', fm_body, count=1)
    else:
        new_fm = f'name: "{new_name}"\n' + fm_body

    return fence + delim_open + new_fm + delim_close + rest


# ── Plan & Appliquer ──────────────────────────────────────────────────────────

def build_plan() -> list[dict]:
    plan = []
    for agent_dir in AGENT_DIRS:
        if not agent_dir.exists():
            continue
        for p in sorted(agent_dir.iterdir()):
            if not p.is_file() or p.suffix not in {".md"}:
                continue
            key = file_key(p)
            if key not in MAPPING:
                continue
            new_name = MAPPING[key]
            content  = p.read_text(encoding="utf-8", errors="ignore")
            before   = current_name(content) or "(champ absent)"
            plan.append({
                "path":     p,
                "key":      key,
                "before":   before,
                "after":    new_name,
                "content":  content,
            })
    return plan


def print_plan(plan: list[dict]) -> None:
    if not plan:
        print("Aucun fichier à modifier.")
        return
    print(f"\n{'─'*62}")
    print(f"  {'FICHIER':<46}  AVANT → APRÈS")
    print(f"{'─'*62}")
    for item in plan:
        fname = item["path"].name
        before = item["before"]
        after  = item["after"]
        changed = "✏️ " if before != after else "✔  "
        print(f"  {changed}{fname}")
        print(f"      [AVANT]  name: {before}")
        print(f"      [APRÈS]  name: {after}")
    print(f"{'─'*62}")
    print(f"  Total : {len(plan)} fichiers concernés\n")


def apply_plan(plan: list[dict]) -> None:
    applied = 0
    for item in plan:
        if item["before"] == item["after"]:
            print(f"  ✔  Déjà correct : {item['path'].name}")
            continue
        new_content = set_name(item["content"], item["after"])
        if new_content is None:
            print(f"  ❌ Pas de frontmatter détecté : {item['path'].name}")
            continue
        item["path"].write_text(new_content, encoding="utf-8")
        print(f"  OK Mis a jour : {item['path'].name}  ('{item['before']}' -> '{item['after']}')")
        applied += 1
    print(f"\n  {applied} fichier(s) modifié(s) sur disque.\n")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    apply = "--apply" in sys.argv

    plan = build_plan()
    print_plan(plan)

    if not apply:
        print("  ℹ️  Mode DRY-RUN. Aucun fichier modifié.")
        print("  → Relancez avec --apply pour appliquer : python _gsane/tools/fix_agent_names_v2.py --apply\n")
    else:
        print("  ▶ Application des changements…\n")
        apply_plan(plan)
