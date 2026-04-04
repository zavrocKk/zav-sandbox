import os
import yaml
from pathlib import Path
import re

manifest_path = Path('_gsane/_config/agent-manifest.yaml')
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = yaml.safe_load(f)

manifest_dict = {item['name']: item for item in manifest}

file_to_key = {
    'gsane-agent-bmb-aria.agent.md': 'aria',
    'gsane-agent-bmb-bond.agent.md': 'bond',
    'gsane-agent-bmb-morgan.agent.md': 'morgan',
    'gsane-agent-bmb-wendy.agent.md': 'wendy',
    'gsane-agent-cis-analyst.agent.md': 'analyst',
    'gsane-agent-cis-architect.agent.md': 'architect',
    'gsane-agent-cis-brainstorming-coach.agent.md': 'brainstorming-coach',
    'gsane-agent-cis-creative-problem-solver.agent.md': 'creative-problem-solver',
    'gsane-agent-cis-design-thinking-coach.agent.md': 'design-thinking-coach',
    'gsane-agent-cis-dev.agent.md': 'dev',
    'gsane-agent-cis-innovation-strategist.agent.md': 'innovation-strategist',
    'gsane-agent-cis-pm.agent.md': 'pm',
    'gsane-agent-cis-presentation-master.agent.md': 'presentation-master',
    'gsane-agent-cis-qa.agent.md': 'qa',
    'gsane-agent-cis-quick-flow-solo-dev.agent.md': 'quick-flow-solo-dev',
    'gsane-agent-cis-sm.agent.md': 'sm',
    'gsane-agent-cis-storyteller.agent.md': 'storyteller',
    'gsane-agent-cis-tech-writer.agent.md': 'tech-writer',
    'gsane-agent-cis-ux-designer.agent.md': 'ux-designer',
    'gsane-agent-core-optimizer.agent.md': 'optimizer',
    'gsane-agent-tea-tea.agent.md': 'tea',
    'master.agent.md': 'master'
}

tools_map = {
    'analyst': '[read, search]',
    'architect': '[read, search]',
    'pm': '[read, search]',
    'dev': '[read, search, edit]',
    'tech-writer': '[read, search, edit]',
    'ux-designer': '[read, search, edit]',
    'qa': '[read, search, edit, execute]',
    'sm': '[read, search, edit, execute]',
    'quick-flow-solo-dev': '[read, search, edit, execute]',
    'bond': '[read, search, edit, execute]',
    'wendy': '[read, search, edit, execute]',
    'morgan': '[read, search, edit, execute]',
    'aria': '[read, search, edit, execute]',
    'master': '[read, search, agent]'
}

default_tools = '[read, search, edit]'

agents_dir = Path('.github/agents')
for fname, mkey in file_to_key.items():
    fpath = agents_dir / fname
    if not fpath.exists():
        print(f"Skipping {fname} (not found)")
        continue
    
    m_item = manifest_dict.get(mkey, {})
    display_name = m_item.get('displayName', mkey)
    description = m_item.get('description', m_item.get('title', ''))
    description = description.replace('"', '\\"')
    tools = tools_map.get(mkey, default_tools)
    
    frontmatter = f'---\nname: "{display_name}"\ndescription: "{description}"\ntools: {tools}\n---\n'
    
    content = fpath.read_text('utf-8')
    content = re.sub(r'^---\n(.*?)\n---\n', '', content, flags=re.DOTALL)
    
    new_content = frontmatter + content
    fpath.write_text(new_content, 'utf-8')
    print(f'Updated frontmatter for {fname}')

print("\n--- Fixing Health Check Script ---\n")

hc_file = Path('_gsane/tools/gsane_health_check.py')
hc_content = hc_file.read_text('utf-8')

# Patching Section B
regex_b = re.compile(
    r'    # SECTION B — Cohérence du registre d\'agents\n'
    r'.*?'
    r'    else:\n'
    r'        hc\.add_missing\("Section B", "Dossier \.github/agents/ absent\.", is_critical=True\)\n'
    r'        hc\.add_missing\("Section B", "Dossier \.github/agents/ absent\.", is_critical=True\)\n',
    re.DOTALL
)

new_section_b = """    # SECTION B — Cohérence du registre d'agents
    print("\\nSECTION B — Cohérence du registre d'agents")
    
    # B1: Cohérence interne (fichiers dans _gsane/)
    if manifest_data and isinstance(manifest_data, list):
        missing_internal = []
        for item in manifest_data:
            if 'path' in item:
                target_path = WORKSPACE_ROOT / item['path']
                if not target_path.exists():
                    missing_internal.append(item['path'])
        if missing_internal:
            hc.add_partial("B1: Fichiers internes (manifest -> _gsane/)", f"Fichiers manquants : {', '.join(missing_internal)}")
        else:
            hc.add_ok("B1: Tous les agents du manifeste ont leur fichier interne .md correspondant.")
    else:
        hc.add_missing("B1: Vérification du manifeste", "Manifeste vide ou illisible.")

    # B2: Cohérence VS Code (.agent.md)
    if agents_dir_exists:
        agent_files = list(agents_dir.glob("*.agent.md"))
        missing_names = []
        for af in agent_files:
            fields = check_agent_frontmatter(af)
            if "name" not in fields:
                missing_names.append(af.name)
        if missing_names:
            hc.add_partial("B2: Fichiers VS Code (.agent.md) valides", f"Champ 'name' manquant dans : {', '.join(missing_names)}")
        else:
            hc.add_ok("B2: Tous les fichiers .agent.md ont un champ 'name' dans leur frontmatter.")
    else:
        hc.add_missing("B2: Section VS Code", "Dossier .github/agents/ absent.", is_critical=True)
"""

if regex_b.search(hc_content):
    hc_content = regex_b.sub(new_section_b, hc_content)
    hc_file.write_text(hc_content, 'utf-8')
    print("Updated gsane_health_check.py (Section B fixed)")
else:
    print("WARNING: Could not find Section B to patch in gsane_health_check.py")
