import os
import glob
from pathlib import Path

# 1. Dictionnaire de mapping explicite (À valider avant exécution)
MAPPING = {
    "gsane-agent-gsane-master": "concierge",
    "gsane-master": "concierge",
    "gsane-agent-dev": "dev",
    "gsane-dev": "dev",
    "gsane-agent-qa": "qa",
    "gsane-qa": "qa",
    "gsane-agent-architect": "architect",
    "gsane-architect": "architect",
    "gsane-agent-analyst": "analyst",
    "gsane-analyst": "analyst",
    "gsane-agent-pm": "pm",
    "gsane-pm": "pm",
    "gsane-agent-sm": "sm",
    "gsane-sm": "sm",
    "gsane-agent-ux-designer": "ux-designer",
    "gsane-ux-designer": "ux-designer",
    "gsane-optimizer": "optimizer",
    "qa-gsane": "aria",
    "agent-builder": "bond",
    "module-builder": "morgan",
    "workflow-builder": "wendy"
}

TARGET_EXTENSIONS = {'.md', '.yaml', '.yml', '.json', '.csv', '.sh'}
TARGET_FOLDERS = ['_gsane', '.github']

def get_target_files():
    files_to_process = []
    for folder in TARGET_FOLDERS:
        if not os.path.exists(folder):
            continue
        for root, _, files in os.walk(folder):
            for file in files:
                if Path(file).suffix in TARGET_EXTENSIONS:
                    files_to_process.append(os.path.join(root, file))
    return files_to_process

def phase1_replace_content():
    print("--- Phase 1: Remplacement du contenu ---")
    files = get_target_files()
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for old_name, new_name in MAPPING.items():
                new_content = new_content.replace(old_name, new_name)
                
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Mis à jour (contenu) : {file_path}")
        except Exception as e:
            print(f"❌ Erreur lors de la lecture/écriture de {file_path}: {e}")

def phase2_rename_files_and_folders():
    print("\n--- Phase 2: Renommage des fichiers et dossiers ---")
    # Dossiers en premier (bottom-up pour éviter les problèmes de chemins modifiés)
    for folder in TARGET_FOLDERS:
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder, topdown=False):
            # Renommer les fichiers
            for file in files:
                for old_name, new_name in MAPPING.items():
                    if old_name in file:
                        old_path = os.path.join(root, file)
                        new_file_name = file.replace(old_name, new_name)
                        new_path = os.path.join(root, new_file_name)
                        os.rename(old_path, new_path)
                        print(f"🔄 Renommé (fichier) : {old_path} -> {new_path}")
                        break # Passer au fichier suivant après renommage
            
            # Renommer les dossiers
            for dir_name in dirs:
                for old_name, new_name in MAPPING.items():
                    if old_name in dir_name:
                        old_path = os.path.join(root, dir_name)
                        new_dir_name = dir_name.replace(old_name, new_name)
                        new_path = os.path.join(root, new_dir_name)
                        os.rename(old_path, new_path)
                        print(f"📁 Renommé (dossier) : {old_path} -> {new_path}")
                        break

if __name__ == "__main__":
    print("🚀 Début du refactoring des agents...")
    phase1_replace_content()
    phase2_rename_files_and_folders()
    print("✨ Refactoring terminé ! N'oubliez pas de lancer votre vérification d'intégrité.")
