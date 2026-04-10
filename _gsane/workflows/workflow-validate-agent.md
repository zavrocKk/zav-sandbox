---
name: workflow-validate-agent
description: "Gate finale de conformité d'un agent GSANE avant livraison."
version: 1.0
---

# Workflow : Validate Agent

> Workflow obligatoire après toute création ou modification d'un agent GSANE, de son manifest, ou d'une surface de persona associée.

---

## Surfaces concernées

- `_gsane/agents/*.md`
- `_gsane/_config/agent-manifest.yaml`
- `_gsane/_config/ides/*.yaml` si l'exposition IDE change
- `_gsane/_config/gsane-help.yaml` si un routage/help agent change

---

## Étape 1 — Intégrité structurelle

Exécuter les vérifications suivantes avant toute validation humaine :

```bash
python - <<'PY'
from pathlib import Path
import yaml

for file_path in sorted(Path("_gsane/_config").rglob("*.yaml")):
    with file_path.open(encoding="utf-8") as handle:
        yaml.safe_load(handle)
PY
```

Objectif : aucun YAML cassé sur les manifests actifs ni sur les personnalisations d'agents.

---

## Étape 2 — Conformité agent

Exécuter :

```bash
python tests/qa-linter.py _gsane/agents/*.md
bash gsane.sh validate
```

Conditions attendues :
- `qa-linter.py` retourne `0`
- `bash gsane.sh validate` retourne `0`
- aucun chemin de workflow référencé par l'agent n'est manquant

---

## Étape 3 — Gate Quinn

Quinn (QA) vérifie le lot final avec au minimum :

- présence des sections requises dans le fichier agent concerné
- cohérence du manifest agent et des chemins de workflow référencés
- verdict final `[CC] PASS` ou `[CC] FAIL`

Sans verdict Quinn explicite, la livraison est bloquée.

---

## Résultat attendu

```text
[AGENT-VALIDATION] PASS — {agent_name} — {date}
ou
[AGENT-VALIDATION] FAIL — {agent_name} — {raison bloquante}
```

Si FAIL : retour à Bond pour correction immédiate avant toute livraison.