# Master Sidecar — project-state

> État de session de Langis (Master). Mis à jour en fin de session.

last_session: null
plan_active: null
decisions_session: []
open_items:
	- id: BACKLOG-002
		title: Compresser master.md
		reason: master.md ~5825 tokens est un risque de budget et consomme ~73% du budget session à lui seul
		target: "< 3500 tokens sans perte de précision opérationnelle"
		timing: "Après P6 complet"
	- id: TODO-P6G-001
		title: Simuler Vera sur un changeset témoin via Quinn/cc-verify
		reason: workflow non simulé après création du subagent
		timing: "Maintenant"
	- id: TODO-P6G-002
		title: Simuler Sage sur un dépassement warning_threshold via session-start.sh
		reason: activation non simulée après création du subagent
		timing: "Maintenant"
	- id: TODO-P6G-003
		title: Câbler Vera dans le flux Quinn / cc-verify
		reason: le subagent existe mais aucune intégration runtime explicite n'a été ajoutée
		timing: "Maintenant"
	- id: TODO-P6G-004
		title: Câbler Sage dans session-start.sh au-dessus de warning_threshold
		reason: le subagent existe mais le hook ne l'active pas encore
		timing: "Maintenant"
	- id: TODO-P6G-005
		title: Enregistrer Vera et Sage dans github-copilot.yaml
		reason: les fichiers .github/agents existent, mais le manifeste IDE ne les expose pas encore
		timing: "Maintenant"
	- id: TODO-P6F-001
		title: Enregistrer session-resume dans workflow-manifest.yaml
		reason: le workflow existe sur disque mais n'est pas encore indexé dans le manifeste des workflows
		timing: "Maintenant"
