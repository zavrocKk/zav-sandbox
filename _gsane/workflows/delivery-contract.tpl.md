---
task_id: ""
owner: ""
validation_agent: ""
risk_level: "LOW"   # LOW | MEDIUM | HIGH
depends_on: []
parallel_group: ""
done_definition: ""
---

# Delivery Contract — {task_id}

## Mission Goal (Objectif)
[Décrire ici l'objectif principal de la mission]

## Architectural Constraints (Où modifier le code)
[Lister les fichiers, les répertoires ou les patterns architecturaux à respecter]

## Acceptance Criteria (Les conditions de réussite pour la QA)
- [ ] [Critère 1 — précis et mesurable]
- [ ] [Critère 2 — vérifiable par le validation_agent]

## Risques et contraintes
[Lister les risques identifiés. risk_level=HIGH → validation humaine obligatoire avant exécution.]

## Quality Gate Command
bash gsane.sh validate
