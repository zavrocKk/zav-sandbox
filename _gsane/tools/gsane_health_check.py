#!/usr/bin/env python3
"""
_gsane/tools/gsane_health_check.py

Audit de santé GSANE en lecture seule stricte.
Aucune modification n'est effectuée sur le système de fichiers.
"""

import os
import re
import yaml
from pathlib import Path

# --- Configuration ---
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
TOTAL_CHECKS = 13
PTS_PER_CHECK = 100 / TOTAL_CHECKS

class HealthCheck:
    def __init__(self):
        self.score = 0.0
        self.critical_gaps = 0
        self.minor_gaps = 0
        self.results = []
    
    def add_ok(self, desc):
        self.score += PTS_PER_CHECK
        self.results.append(f"  ✅ OK     — {desc}")
        
    def add_missing(self, desc, suggestion, is_critical=False):
        if is_critical:
            self.critical_gaps += 1
        else:
            self.minor_gaps += 1
        self.results.append(f"  ❌ MANQUANT — {desc} → Suggestion : {suggestion}")
        
    def add_partial(self, desc, detail, proportion=0.5):
        self.score += (PTS_PER_CHECK * proportion)
        self.minor_gaps += 1
        self.results.append(f"  ⚠️ PARTIEL  — {desc} → Détail : {detail}")

def check_agent_frontmatter(file_path):
    """Vérifie le frontmatter d'un agent pour les 4 champs obligatoires."""
    try:
        content = file_path.read_text('utf-8')
        # Extraire le frontmatter YAML
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}
        
        fm_content = match.group(1)
        parsed = yaml.safe_load(fm_content)
        if not isinstance(parsed, dict):
            return {}
        
        return parsed
    except Exception:
        return {}

def run_audit():
    hc = HealthCheck()
    
    print("\n🔍 DÉMARRAGE DE L'AUDIT DE SANTÉ GSANE 🔍")
    print("=" * 50)
    
    # SECTION A — Gouvernance
    print("\nSECTION A — Gouvernance (Fichiers fondamentaux)")
    
    # 1
    p1 = WORKSPACE_ROOT / ".github" / "copilot-instructions.md"
    if p1.exists(): hc.add_ok(".github/copilot-instructions.md existe.")
    else: hc.add_missing(".github/copilot-instructions.md", "Créer le fichier avec les règles GSANE globales.", is_critical=True)
        
    # 2
    p2 = WORKSPACE_ROOT / "_gsane" / "_config" / "agent-manifest.yaml"
    # Support typo in user prompt "agents-manifest.yaml"
    if not p2.exists():
        p2 = WORKSPACE_ROOT / "_gsane" / "_config" / "agents-manifest.yaml"
        
    if p2.exists():
        try:
            with open(p2, 'r', encoding='utf-8') as f:
                manifest_data = yaml.safe_load(f)
                hc.add_ok(f"{p2.name} existe et est valide YAML.")
        except Exception as e:
            hc.add_partial(f"{p2.name} existe", f"YAML invalide ({e})", 0.0)
            manifest_data = None
    else:
        hc.add_missing("_gsane/_config/agent-manifest.yaml", "Créer le registre YAML des agents.", is_critical=True)
        manifest_data = None

    # 3
    p3 = WORKSPACE_ROOT / "_gsane" / "_memory" / "failure-museum.md"
    if p3.exists(): hc.add_ok("_gsane/_memory/failure-museum.md existe.")
    else: hc.add_missing("_gsane/_memory/failure-museum.md", "Créer le musée des erreurs pour la mémoire long-terme.")

    # 4
    p4 = WORKSPACE_ROOT / "_gsane" / "core" / "templates" / "delivery-contract.tpl.md"
    if p4.exists(): hc.add_ok("_gsane/core/templates/delivery-contract.tpl.md existe.")
    else: hc.add_missing("_gsane/core/templates/delivery-contract.tpl.md", "Créer le template de contrat de livraison.")

    # 5
    p5 = WORKSPACE_ROOT / "_gsane" / "tools" / "validate.sh"
    if p5.exists(): hc.add_ok("_gsane/tools/validate.sh existe.")
    else: hc.add_missing("_gsane/tools/validate.sh", "Créer le script de validation d'architecture.")


    # SECTION B & E Setup
    agents_dir = WORKSPACE_ROOT / ".github" / "agents"
    agents_dir_exists = agents_dir.exists() and agents_dir.is_dir()
    
    if not agents_dir_exists:
        print("\n[!] GAP CRITIQUE : Dossier .github/agents/ introuvable. Sections B et E ignorées (-20 pts).")
        hc.score -= 20.0
        hc.critical_gaps += 1
    
    # SECTION B — Cohérence du registre d'agents
    print("\nSECTION B — Cohérence du registre d'agents")
    
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

    # SECTION C — CI/CD et Hooks
    print("\nSECTION C — CI/CD et Hooks")
    # 8
    p8 = WORKSPACE_ROOT / ".github" / "workflows"
    if p8.exists() and any(p8.glob("*.yml")):
        hc.add_ok("Au moins un workflow .yml actif trouvé dans .github/workflows/")
    else:
        hc.add_missing(".github/workflows/ contient des .yml", "Créer un workflow CI basique.")
        
    # 9
    p9_precommit = WORKSPACE_ROOT / ".pre-commit-config.yaml"
    has_hook = False
    if p9_precommit.exists():
        has_hook = True
    else:
        # Check hooks
        hooks_dir = WORKSPACE_ROOT / ".github" / "hooks"
        if hooks_dir.exists():
            for hook in hooks_dir.glob("*.sh"):
                if "validate.sh" in hook.read_text('utf-8'):
                    has_hook = True
                    break
    
    if has_hook:
        hc.add_ok("Crochet de validation (pre-commit ou hook sh) configuré.")
    else:
        hc.add_missing("Validation distante/hook", "Créer .pre-commit-config.yaml ou référencer validate.sh dans un hook.")

    # SECTION D — Documentation
    print("\nSECTION D — Documentation")
    # 10
    p10 = WORKSPACE_ROOT / "README.md"
    if p10.exists():
        content = p10.read_text('utf-8').lower()
        missing_sections = []
        for sec in ["installation", "usage", "agents", "architecture"]:
            if sec not in content:
                missing_sections.append(sec.capitalize())
        
        if missing_sections:
            hc.add_partial("README.md sections requises", f"Manque : {', '.join(missing_sections)}")
        else:
            hc.add_ok("README.md contient toutes les sections requises.")
    else:
        hc.add_missing("README.md", "Créer le README avec Installation, Usage, Agents, Architecture.")

    # 11
    p11 = WORKSPACE_ROOT / "CONTRIBUTING.md"
    if p11.exists(): hc.add_ok("CONTRIBUTING.md existe.")
    else: hc.add_missing("CONTRIBUTING.md", "Créer le guide de contribution.")

    # 12
    p12 = WORKSPACE_ROOT / "CHANGELOG.md"
    if p12.exists(): hc.add_ok("CHANGELOG.md existe.")
    else: hc.add_missing("CHANGELOG.md", "Créer un CHANGELOG pour le suivi des versions.")

    # SECTION E — Intégrité des fichiers .agent.md
    print("\nSECTION E — Intégrité des fichiers .agent.md")
    if agents_dir_exists:
        required_fields = {"name", "description", "tools", "instructions"}
        files_with_missing_fields = {}
        files_with_missing_tools = {}
        
        for af in agent_files:
            fields = check_agent_frontmatter(af)
            missing = required_fields - set(fields.keys())
            if missing:
                files_with_missing_fields[af.name] = missing
            
            if "tools" in fields:
                tools = fields["tools"]
                if not isinstance(tools, list):
                    files_with_missing_tools[af.name] = ["'tools' n'est pas une liste"]
                else:
                    missing_tools = []
                    if "edit" not in tools: missing_tools.append("edit")
                    if "read" not in tools: missing_tools.append("read")
                    if missing_tools:
                        files_with_missing_tools[af.name] = [f"manque '{t}' dans tools" for t in missing_tools]
                
        if files_with_missing_fields or files_with_missing_tools:
            details_list = []
            for fname, miss in files_with_missing_fields.items():
                details_list.append(f"{fname} ({', '.join(miss)})")
            for fname, miss_tools in files_with_missing_tools.items():
                details_list.append(f"{fname} ({', '.join(miss_tools)})")
            
            details = ", ".join(details_list)
            hc.add_partial("Frontmatter des agents (.agent.md) complet", f"Erreurs : {details}")
        else:
            hc.add_ok("Tous les agents .agent.md ont un frontmatter YAML complet et outils valides.")
    else:
        hc.add_missing("Section E", "Dossier .github/agents/ absent.", is_critical=True)


    # Rendu des scores
    print("\n" + "=" * 50)
    for res in hc.results:
        print(res)
        
    print("\n" + "=" * 50)
    final_score = max(0, min(100, hc.score))
    print(f"  SCORE FINAL : {final_score:.0f}/100")
    print(f"  GAPS CRITIQUES : {hc.critical_gaps}")
    print(f"  GAPS MINEURS : {hc.minor_gaps}")
    print("  Commande pour relancer l'audit : python _gsane/tools/gsane_health_check.py")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    run_audit()
