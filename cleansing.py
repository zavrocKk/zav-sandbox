import os
import glob
import re

print("Starting Namespace Cleansing...")

# 1. Rename files in _gsane/_config/agents/
d = '_gsane/_config/agents'
if os.path.exists(d):
    for f in os.listdir(d):
        m = re.match(r'^(bmb|cis|core|tea)-(.+)$', f)
        if m:
            old_p = os.path.join(d, f)
            new_p = os.path.join(d, m.group(2))
            if os.path.exists(new_p):
                os.remove(old_p)
            else:
                os.rename(old_p, new_p)
            print(f"Renamed: {f} -> {m.group(2)}")

# 2. Clean up _gsane/agents/*.md
for ap in glob.glob('_gsane/agents/*.md'):
    with open(ap, 'r', encoding='utf-8') as file:
        c = file.read()
    
    # regex 1: `bmb-bond.customize.yaml` -> `bond.customize.yaml`
    c = re.sub(r'(?:bmb|cis|core|tea)-([a-zA-Z0-9_\-]+\.customize\.yaml)', r'\1', c)
    
    # regex 2: replace text instructions about modules
    c = re.sub(r'derive path from module [^\.]+?\.', '', c, flags=re.IGNORECASE)
    c = re.sub(r"derive path from module \([^)]+\)", '', c, flags=re.IGNORECASE)
    
    with open(ap, 'w', encoding='utf-8') as file:
        file.write(c)

# 3. Clean delegation-matrix
dm = '_gsane/_config/delegation-matrix.yaml'
if os.path.exists(dm):
    with open(dm, 'r', encoding='utf-8') as file:
        c = file.read()
    c = re.sub(r'^[ \t]*target_module:\s*[^\n\r]+\r?\n', '', c, flags=re.MULTILINE)
    with open(dm, 'w', encoding='utf-8') as file:
        file.write(c)

# 4. Agent manifest
am = '_gsane/_config/agent-manifest.yaml'
if os.path.exists(am):
    with open(am, 'r', encoding='utf-8') as file:
        c = file.read()
    c = re.sub(r'\b(bmb|cis|core|tea)-', '', c)
    with open(am, 'w', encoding='utf-8') as file:
        file.write(c)

print("Cleansing complete.")
