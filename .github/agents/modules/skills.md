---
type: module
referenced_by: .github/agents/orchestrator.agent.md
---

# Module — Skills techniques (progressive disclosure)

> Ce fichier est référencé par `orchestrator.agent.md`. Toute modification du tableau
> des skills ou des règles de chargement doit être répercutée dans l'orchestrator.

---

Les **skills** sont des modules markdown de connaissance/méthodologie qu'un persona
charge **à la demande** pendant l'EXECUTE, sans dupliquer les workflows. Elles
vivent dans [`agents/skills/<slug>/SKILL.md`](../../../agents/skills/) (format **Agent
Skills** : front-matter `name`+`description`). Cadre complet :
[`docs/architecture/2026-05-30-phase-8-skills.md`](../../../docs/architecture/2026-05-30-phase-8-skills.md).

**Frontière à respecter** : skill = **SAVOIR** (≠ persona = QUI parle, ≠ workflow =
ORDRE des phases). Une skill est invoquée *par* un persona, elle n'orchestre rien.

## Règles de chargement

- Tu ne charges le **corps** d'un `SKILL.md` que si sa `description` matche la
  demande **ET** que le persona courant en a besoin **maintenant**. Sinon, rien.
- Budget variable : tâche `tiny` → souvent le titre/`description` suffit ; tâche
  `deep` → corps complet + fichiers `reference/*` pertinents (un seul niveau de
  profondeur).
- **Jamais** « toutes les skills » ni un balayage de `agents/skills/`. En cas de
  doute sur la pertinence → ne pas charger.
- **Sécurité provenance** : n'invoque qu'une skill du repo (source de confiance).
  Une skill du socle est 100 % markdown statique, sans appel réseau, sans script
  exécuté — toute skill d'origine externe doit être auditée avant adoption.

## Skills disponibles

| Skill | Fichier | Quand l'invoquer |
|---|---|---|
| 🔍 root-cause-analysis | [`agents/skills/root-cause-analysis/SKILL.md`](../../../agents/skills/root-cause-analysis/SKILL.md) | Remonter d'un symptôme à sa cause systémique (5 Pourquoi / Ishikawa) — phase « Cause racine » d'un incident, problème opérationnel récurrent |
| 🎉 party-mode | [`agents/skills/party-mode/SKILL.md`](../../../agents/skills/party-mode/SKILL.md) | Ancre du protocole Panel + Débat — session multi-personas, reprise de checkpoint, rappel des règles Panel/Débat/anti-patterns |

> Registre complet et procédure d'ajout : [`agents/skills/README.md`](../../../agents/skills/README.md).
