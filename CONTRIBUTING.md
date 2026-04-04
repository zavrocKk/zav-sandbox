# 🤝 Comment Contribuer : Directives de la Strike Team

Ce document fixe les lois immuables du développement sous l'autorité de l'architecture "Grimoire-kit". Tout contributeur ou agent IA DOIT respecter ce rituel.

## La Doctrine du Code

1. **Règle 1 : Delivery Contract Obligatoire**
   Amelia (Dev) n'a pas le droit de créer ou modifier de fichier métier src/ sans avoir reçu un document formel détaillant sa mission (*Mission Goal, Architectural Constraints, Acceptance Criteria, Command Gate*). L'Orchestrateur Langis DOIT le rédiger initialement.

2. **Règle 2 : TDD Strictly Enforced**
   Tout code est accompagné d'un test qui valide sa logique et ses *Edge Cases* (Exception, String Vide, Ponctuation, etc.). Le développement est asynchrone : Amelia écrit les tests avec l'implémentation, et Quinn les exécute.

3. **Règle 3 : Zero-Touch Fix-Loop**
   Il est formellement interdit de s'arrêter à la première erreur et de remonter l'alerte à l'humain. 
   La pipeline (Circuit Breaker) est programmée pour reboucler.
   - Quinn exécute ash gsane.sh validate. 
   - Si les tests échouent (Exit 1), Quinn analyse le rapport d'erreur.
   - Quinn renvoie automatiquement les traces à Amelia pour correction (Refactoring).
   - Seul le succès total (Exit 0) certifie l'achèvement de la tâche !
