import os
import glob
from pathlib import Path

MAPPING = {
    "concierge.md": "master.md",
    "concierge.prompt.md": "master.prompt.md",
    "concierge.agent.md": "master.agent.md",
    "concierge.agent.yaml": "master.agent.yaml",
    "core-concierge.customize.yaml": "core-master.customize.yaml",
    "concierge": "master",
    "Concierge": "Master"
}

# Add exceptions to avoid renaming unrelated things like strings in Python that we want to keep
TARGET_EXTENSIONS = {'.md', '.yaml', '.yml', '.json', '.csv', '.sh'}
TARGET_FOLDERS = ['_gsane', '.github', 'AGENTS.md']

def get_target_files():
    files_to_process = []
    for root_folder in TARGET_FOLDERS:
        if os.path.isfile(root_folder):
            files_to_process.append(root_folder)
            continue
        if not os.path.exists(root_folder):
            continue
        for root, _, files in os.walk(root_folder):
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
    print("\n--- Phase 2: Renommage des fichiers ---")
    # Dossiers en premier (bottom-up pour éviter les problèmes de chemins modifiés)
    for folder in TARGET_FOLDERS:
        if os.path.isfile(folder):
            continue
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder, topdown=False):
            # Renommer les fichiers
            for file in files:
                if 'concierge' in file.lower():
                    old_path = os.path.join(root, file)
                    new_file_name = file.replace('concierge', 'master').replace('Concierge', 'Master')
                    new_path = os.path.join(root, new_file_name)
                    os.rename(old_path, new_path)
                    print(f"🔄 Renommé (fichier) : {old_path} -> {new_path}")
            
            # Renommer les dossiers
            for dir_name in dirs:
                if 'concierge' in dir_name.lower():
                    old_path = os.path.join(root, dir_name)
                    new_dir_name = dir_name.replace('concierge', 'master').replace('Concierge', 'Master')
                    new_path = os.path.join(root, new_dir_name)
                    os.rename(old_path, new_path)
                    print(f"📁 Renommé (dossier) : {old_path} -> {new_path}")

if __name__ == "__main__":
    phase1_replace_content()
    phase2_rename_files_and_folders()
