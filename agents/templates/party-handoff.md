# Party mode (sous-agents) — handoff-{agent}.md

<!-- Budget : le NÉCESSAIRE d'abord — cible ≤ 500 tokens (hors lignes de preuve).
  Au-delà de 1000 tokens / 4000 chars : ouvrir par « Budget dépassé : <raison> » —
  dépassement dense et prouvé = accepté ; silencieux = non conforme (ADR-0018). -->
<!-- Règle binaire : une info qui existe dans un fichier du repo est RÉFÉRENCÉE (voir path), jamais recopiée. -->
<!-- Au-delà de la cible, chaque ligne doit être du signal (findings, contexte critique) — pas de transcription. -->
<!-- Créé par chaque sous-agent à la fin de son tour. -->
<!-- Supprimé par l'orchestrateur à la clôture de session. -->

## handoff-{agent}
Findings : <!-- Résumé conclusif de ce que l'agent a produit / découvert.
  Règle binaire : chaque finding porte son pointeur de preuve FALSIFIABLE
  (fichier:ligne, requête + fenêtre UTC, lien doc) — une affirmation
  invérifiable est non conforme (rejetée par le gate). -->
Tâches ouvertes : <!-- Ce que le prochain agent doit traiter — dont toute action
  requérant un outil que tu n'as pas : « exécuter X — requiert terminal → devops »
  (matrice de capacités : module party-mode). -->
Contexte critique : <!-- Ce que le suivant NE DOIT PAS perdre -->
Risques : <!-- Points d'attention transmis -->
