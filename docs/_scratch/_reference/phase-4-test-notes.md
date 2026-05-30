# Test Notes

## Test [date]

-Test 1; Bonjour
-Test 2: Simuler une vrai session de débuggage, avec des artefacts de synthèse à la fin (rapport d'audit, ADR, runbook). Voir ce qui marche, ce qui cloche, et ajustements à faire dans l'orchestrateur (persona, instructions, etc.) pour mieux accompagner la création de ces artefacts. Observer aussi les personas surutilisés / sous-utilisés.

### Ce qui a bien marché

- Il a répondu; Oui, je suis là.

Je suis l'Orchestrateur — une équipe virtuelle d'experts (Dev, Archi, QA, Sécurité, DevOps…) que j'incarne tour à tour selon ton besoin.

Décris-moi ce sur quoi tu veux travailler.

### Ce qui a cloché

-Solo difrt ou oublie de créer les artefacts de synthèse (rapport d'audit, ADR) à la fin de la session.

### À ajuster dans l'orchestrateur

-Allégé son fichier persona et voir pour des références ailleurs (checklists, templates) pour éviter les oublis.  Voir aussi pour des skills ou d'autre mécanisme de partage de connaissances entre agents.

### Personas surutilisés / sous-utilisés

-Pas encore eu assez de tests pour en conclure quoi ce soit, mais il semble que le Scribe soit systématiquement invoqué à la fin, même quand l'orchestrateur n'est pas sélectionné (ex: en Agent par défaut). Peut-être parce qu'il a lu son persona via les outils codebase/search pendant l'exécution. À creuser : est-ce un comportement souhaitable ou problématique ? Doit-on limiter la découvrabilité des personas via instructions dans copilot-instructions.md ? Ou au contraire en profiter : transformer les personas en "skills" partagés que tout agent peut invoquer ?
