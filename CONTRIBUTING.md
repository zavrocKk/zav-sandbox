# 🤝 Guide de Contribution (Strike Team)

Ce document fixe les règles de développement et de collaboration de l'architecture "Strike Team". Tout contributeur humain ou agent IA **DOIT** s'y conformer strictement.

## 📖 Glossaire GSANE
Avant de commencer, familiarisez-vous avec ces trois concepts piliers :
- **Delivery Contract** : Un document Markdown formel (rédigé par l'agent *Master*) validant les critères d'acceptation et les contraintes techniques *avant* d'écrire la moindre ligne de code métier.
- **Zero-Touch Fix-Loop** : Notre boucle de correction asynchrone. L'agent QA vérifie le code de l'agent Dev, et lui renvoie les erreurs de la console jusqu'à obtenir un succès parfait (Exit 0), sans jamais solliciter l'aide de l'humain.
- **Quality Gate** : Le script impitoyable `bash gsane.sh validate` qui exécute la suite de tests et vérifie la conformité documentaire.

## 💻 Setup Développeur
Veuillez suivre les étapes d'installation de base détaillées dans le [README.md](README.md).
Avant de commiter la moindre modification, **vous devez toujours valider localement votre code** :
`ash
# Vérifie le code, les tests et l'historique :
bash gsane.sh validate

# Ou exécuter juste les tests isolément :
python -m pytest tests/
`

## 🔄 Workflow Collaboratif
### 1. Conventions de Nommage (Branches)
Il est **strictement interdit** de pousser du code en direct sur la branche main.
Créez systématiquement une branche selon la convention suivante :
- eature/{description}-{date}
- ix/{description}-{date}

### 2. Format des Commits
Nous utilisons les **Conventional Commits**. Votre message de commit doit ressembler à :
- eat(core): ajout de la fonction X
- ix(docs): correction de la typo Y
- chore(deps): mise à jour de pytest

### 3. Pull Requests (PR)
- Soumettez votre PR vers main.
- La description de la PR **doit obligatoirement être remplie**. Notre CI Github crashera si la description est vide (règle définie dans copilot-instructions.md).

## 🛡️ Style et Qualité de Code
- **Linter/Formatteur** : Bien que nous n'imposions pas encore d'outils comme Ruff ou Flake8 de manière bloquante, le code doit être propre et typé (Python 3).
- **Couverture de Tests (TDD)** : Tout code ajouté dans src/ exige 100% de tests associés dans le répertoire `tests/`. Si le coverage ou l'assertion échoue, votre Pull Request sera refusée.
- **Documentation Continue (Micro-Token Rule)** : Pour chaque nouvelle fonctionnalité finalisée dans src/, **vous devez ajouter une ligne descriptive dans CHANGELOG.md**. Le pipeline bash rejettera le code source si le changelog a été ignoré.

## 🤖 Ajouter un Nouvel Agent
Si la Strike Team doit s'agrandir :
1. Créez la personnalité de l'agent dans le dossier plat : _gsane/agents/[nom-agent].md.
2. Enregistrez ses compétences et outils dans _gsane/_config/agent-manifest.yaml.
3. Ajoutez ses routes de communication dans _gsane/_config/delegation-matrix.yaml.

## 💬 Communication
Si vous rencontrez un bug ou que vous souhaitez discuter d'un changement d'architecture majeur, ouvrez une **Issue** sur GitHub ou lancez une session @Langis (Master) dans Copilot Chat.
