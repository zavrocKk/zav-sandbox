# Delivery Contract: Text Analyzer

## Mission Goal (Objectif)
Créer un module utilitaire src/text_analyzer.py contenant une fonction nalyze_text(text: str) -> dict qui retourne le nombre de mots, le nombre de phrases (basé sur . ! ?) et un score de lisibilité (mots/phrases). Si le texte est vide ou None, lever une ValueError.
Créer les tests correspondants dans 	ests/test_text_analyzer.py avec au moins 3 tests (normal, vide, sans ponctuation finale).

## Architectural Constraints (Où modifier le code)
- src/text_analyzer.py
- 	ests/test_text_analyzer.py

## Acceptance Criteria (Les conditions de réussite pour la QA)
- La fonction nalyze_text est implémentée avec la signature correcte.
- 3 tests au minimum sont présents et couvrent les cas demandés.
- ValueError est bien levée pour les entrées vides ou None.

## Quality Gate Command
bash gsane.sh validate
