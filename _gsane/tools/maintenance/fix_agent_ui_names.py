#!/usr/bin/env python3
"""
fix_agent_ui_names.py - Nettoie les champs `name:` du frontmatter YAML
des fichiers agents pour alléger l'interface VS Code.
Seul le champ `name:` est modifié. Aucun contenu Markdown n'est touché.
"""
import os
import re

# Dictionnaire de mapping approuvé : nom de fichier (sans .agent.md) -> nom UI propre
MAPPING = {
    "gsane-agent-bmb-aria":                    "Aria (GSANE QA)",
    "gsane-agent-bmb-bond":                    "Bond (Agent Builder)",
    "gsane-agent-bmb-morgan":                  "Morgan (Module Builder)",
    "gsane-agent-bmb-wendy":                   "Wendy (Workflow Builder)",
    "gsane-agent-cis-analyst":                 "Mary (Analyst)",
    "gsane-agent-cis-architect":               "Winston (Architect)",
    "gsane-agent-cis-brainstorming-coach":     "Carson (Brainstorming)",
    "gsane-agent-cis-creative-problem-solver": "Creative Solver",
    "gsane-agent-cis-design-thinking-coach":   "Maya (Design Thinking)",
    "gsane-agent-cis-dev":                     "Amelia (Dev)",
    "gsane-agent-cis-innovation-strategist":   "Victor (Innovation)",
    "gsane-agent-cis-pm":                      "John (PM)",
    "gsane-agent-cis-presentation-master":     "Caravaggio (Presentation)",
    "gsane-agent-cis-qa":                      "Quinn (QA)",
    "gsane-agent-cis-quick-flow-solo-dev":     "Barry (Quick Dev)",
    "gsane-agent-cis-sm":                      "Bob (SM)",
    "gsane-agent-cis-storyteller":             "Sophia (Storyteller)",
    "gsane-agent-cis-tech-writer":             "Paige (Tech Writer)",
    "gsane-agent-cis-ux-designer":             "Sally (UX Designer)",
    "gsane-agent-core-optimizer":              "Sentinel (Optimizer)",
    "gsane-agent-tea-tea":                     "Murat (Test Architect)",
    "master":                                  "Master",
    "optimizer":                               "Sentinel (Optimizer)",
}

FRONTMATTER_PATTERN = re.compile(r'^(```\w+\n)?(---\n)(.*?)(---\n)', re.DOTALL)
NAME_LINE_PATTERN   = re.compile(r"^(name:\s*)(.+)$", re.MULTILINE)


def process_file(filepath: str, new_name: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    m = FRONTMATTER_PATTERN.match(raw)
    if not m:
        print(f"  ⚠️  Pas de frontmatter détecté : {filepath}")
        return False

    code_fence  = m.group(1) or ""
    delim_open  = m.group(2)
    fm_body     = m.group(3)
    delim_close = m.group(4)
    rest        = raw[m.end():]

    name_match = NAME_LINE_PATTERN.search(fm_body)
    if name_match:
        old_value = name_match.group(2).strip().strip('"').strip("'")
        if old_value == new_name:
            print(f"  ✔  Déjà correct : {filepath}")
            return False
        new_fm = NAME_LINE_PATTERN.sub(f'\\g<1>"{new_name}"', fm_body, count=1)
        print(f'  🔄 {filepath}\n     "{old_value}" -> "{new_name}"')
    else:
        # Ajoute le champ name: en tête du frontmatter
        new_fm = f'name: "{new_name}"\n' + fm_body
        print(f'  ➕ {filepath}  (champ name: ajouté → "{new_name}")')

    new_raw = code_fence + delim_open + new_fm + delim_close + rest
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_raw)
    return True


def main():
    changed = 0
    folders = [".github/agents", "_gsane/core/agents"]
    extensions = (".agent.md", ".md")

    for folder in folders:
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            if not any(fname.endswith(ext) for ext in extensions):
                continue
            # Décoder la clé de mapping à partir du nom de fichier
            stem = fname
            for ext in (".agent.md", ".prompt.md", ".md"):
                if stem.endswith(ext):
                    stem = stem[: -len(ext)]
                    break

            if stem in MAPPING:
                fpath = os.path.join(folder, fname)
                if process_file(fpath, MAPPING[stem]):
                    changed += 1

    print(f"\n✅ Terminé — {changed} fichier(s) mis à jour.")


if __name__ == "__main__":
    main()
