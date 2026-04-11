# CHALLENGE — Émettre une contestation technique

Émettre un [CHALLENGE] formel sur une décision ou un output.

## Instructions

1. Cible du challenge : $ARGUMENTS
2. Formuler l'argument technique précis (pas de contestation vague)
3. Identifier l'agent source et l'agent cible
4. Inclure : fichier concerné, ligne/section, argument technique, contre-proposition
5. Logger via `gsane_emit_event('challenge_issued', ...)`

## Protocole de résolution

1. L'agent cible reçoit le challenge complet
2. L'agent cible répond avec son argument (1 échange)
3. Si consensus → continuer
4. Si pas de consensus → Langis arbitre (décision FINALE)
5. Logger via `gsane_emit_event('challenge_resolved', ...)`

## Règle

Un CHALLENGE sans argument technique précis est invalide.
Un CHALLENGE ne peut jamais être ignoré — il doit être résolu.
