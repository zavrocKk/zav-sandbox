# zav-sandbox — Guide de contribution

## Bienvenue

Tu veux améliorer le projet ? Excellent. Voici comment fonctionne le processus.

---

## Structure du projet

```
zav-sandbox/
├── AGENTS.md                          # Point d'entrée universel — lire en premier
├── CONTRIBUTING.md                    # Ce fichier
├── CHANGELOG.md                       # Historique des modifications — OBLIGATOIRE à chaque commit
├── README.md                          # Vue d'ensemble, score de maturité, conventions
├── instructions.md                    # Prompt d'amélioration maturité agentique 65/65
│
├── .github/
│   ├── copilot-instructions.md        # Règles globales GitHub Copilot — impacte TOUS les agents
│   ├── agents/                        # 13 fichiers .agent.md — sous-agents Copilot
│   ├── prompts/                       # Slash commands /gsane-* (46 prompts)
│   ├── skills/                        # 3 skills : gsane-framework, agent-design-patterns, cognitive-flywheel
│   ├── hooks/                         # Hooks de cycle de vie (pre-commit, session-start/stop, flywheel)
│   └── workflows/
│       ├── validate-pr.yml            # CI : CHANGELOG, PR body, structure, agents, chemins dépréciés
│       └── cleanup-branches.yml       # Nettoyage automatique des branches mergées
│
└── _gsane/
    ├── _config/                       # Manifests CSV + matrice de délégation
    │   ├── agent-manifest.csv         # Registre des 13 agents (index JIT)
    │   ├── workflow-manifest.csv      # Registre des workflows
    │   ├── agent-delegation-matrix.csv  # Routing des requêtes — impacte TOUT le système
    │   └── ...
    ├── _memory/                       # Mémoire persistante (scoreboard, flywheel, sessions)
    ├── core/                          # Gsane Master + workflows fondamentaux + flywheel
    │   ├── agents/gsane-master.md     # Orchestrateur principal
    │   ├── config.yaml               # Config globale : user, langue, sévérité, flywheel
    │   ├── tasks/                    # Tâches réutilisables (workflow.xml, editorial review...)
    │   └── workflows/               # party-mode, delegation, git-workflow, flywheel...
    ├── bmb/                          # Module Builders — Bond, Morgan, Wendy, Aria
    ├── cis/                          # Module Creative/Innovation/Storytelling — 6 agents
    ├── tea/                          # Module Test Architecture — Murat
    └── _gsane-output/               # Artefacts générés (ne pas committer sur main)
```

---

## Règles fondamentales

### 1. Tout agent doit respecter le format GSANE

Chaque fichier `.agent.md` dans `.github/agents/` doit avoir le frontmatter YAML et le bloc `<agent>` XML :

```yaml
---
name: mon-agent
description: "Description courte"
tools: []
user-invokable: false
orchestrated-by: gsane-master
---
```

```xml
<agent id="mon-agent.agent.yaml" name="Persona" title="Titre complet" icon="🔧">
  <activation critical="MANDATORY">
    <step n="1">Load persona from this file</step>
    <step n="2">Load {project-root}/_gsane/{module}/config.yaml — store user_name, communication_language</step>
    <!-- 8-11 steps max -->
    <rules>
      <r>ALWAYS communicate in {communication_language}</r>
    </rules>
  </activation>
  <persona>...</persona>
  <menu>...</menu>
</agent>
```

Voir `.github/skills/agent-design-patterns/SKILL.md` pour le guide complet.

### 2. Jamais de commit direct sur `main`

```bash
# ✅ Correct
git checkout -b feature/ma-feature-2026-03-01

# ❌ Interdit — le hook pre-commit et le CI bloquent
git push origin main
```

### 3. CHANGELOG.md obligatoire avant tout commit

Toute modification sans entrée CHANGELOG sera bloquée par le CI. Format GSANE :

```markdown
### [Core]
**[feat]** Description fonctionnelle claire
- Agent: {nom_agent} | Workflow: {workflow_utilisé} | Initié par: {ton_nom}
- Impact: {ce qui est affecté}
```

**Modules valides :** `[Core]` `[BMB]` `[CIS]` `[TEA]` `[Infrastructure]`

**Types valides :** `[feat]` `[fix]` `[breaking]` `[security]` `[refactor]` `[docs]` `[chore]`

### 4. Party Mode pour les modifications GSANE de sévérité medium/high

| Sévérité | Exemples | Règle |
|---|---|---|
| **Low** | Correction typo, append CHANGELOG | Solo autorisé |
| **Medium** | Modifier un agent, un workflow | Party mode recommandé |
| **High** | Modifier `agent-delegation-matrix.csv`, règles core, `copilot-instructions.md` | Party mode **obligatoire** — validation ≥ 2 agents avant écriture |

Activer le party mode : `/gsane-party-mode` dans Copilot Chat.

---

## Ajouter un agent

Les agents GSANE vivent en **deux endroits** : le fichier `.agent.md` (Copilot) + le fichier `.md` de profil (GSANE).

### 1. Créer le fichier `.agent.md` dans `.github/agents/`

Nommage : `{module}-{nom}.agent.md`

Structure minimale obligatoire — voir `.github/skills/agent-design-patterns/SKILL.md` pour le template complet.

### 2. Créer le profil agent dans le module

```bash
# Exemple pour un agent dans le module bmb
_gsane/bmb/agents/mon-agent.md
```

### 3. Mettre à jour `agent-manifest.csv`

Ajouter une ligne dans `_gsane/_config/agent-manifest.csv` :

```csv
"mon-agent","Persona","Titre","🔧","capability1, capability2","Rôle","Identité","Style","Principes","module","_gsane/{module}/agents/mon-agent.md"
```

### 4. Créer le prompt slash command

```bash
.github/prompts/gsane-mon-agent.prompt.md
```

### 5. Ajouter dans la matrice de délégation si pertinent

Dans `_gsane/_config/agent-delegation-matrix.csv` :

```csv
mon-cas-usage,mon-agent,module,_gsane/{module}/agents/mon-agent.md,🔧,Description courte,keyword1;keyword2;keyword3
```

> ⚠️ La matrice est **sévérité HIGH** — party mode obligatoire avant modification.

### 6. Mettre à jour les manifests et CHANGELOG

- `_gsane/_config/agent-manifest.csv` — ligne agent ajoutée
- `CHANGELOG.md` — entrée `[feat]` dans le bon module

---

## Ajouter un workflow

Les workflows GSANE sont soit **`.md`** (exécution directe) soit **`.yaml`** (via workflow engine `workflow.xml`).

### Workflow `.md` (simple, séquentiel)

```
_gsane/{module}/workflows/{nom-workflow}/workflow.md
```

Frontmatter obligatoire :

```yaml
---
name: mon-workflow
description: "Description courte — affiché dans le manifest"
---
```

### Workflow `.yaml` (multi-steps avec engine)

```
_gsane/{module}/workflows/{nom-workflow}/workflow.yaml
```

Le workflow engine `_gsane/core/tasks/workflow.xml` est chargé avant toute exécution YAML.

### Enregistrer dans le manifest

Ajouter une ligne dans `_gsane/_config/workflow-manifest.csv`.

### Ajouter le prompt slash command

```
.github/prompts/gsane-{nom-workflow}.prompt.md
```

---

## Ajouter un module

Un module GSANE = un dossier autonome avec agents + workflows + config.

```
_gsane/{module}/
├── agents/
├── workflows/
├── teams/
├── config.yaml
└── module-help.csv
```

Structure minimale de `config.yaml` :

```yaml
user_name: Mon Seigneur
communication_language: Français
output_folder: "{project-root}/_gsane-output"
```

Puis mettre à jour :
- `AGENTS.md` — section structure et tableau agents
- `README.md` — section structure
- `_gsane/_config/manifest.yaml` — enregistrement du module

---

## Modifier `agent-delegation-matrix.csv`

⚠️ **Ce fichier est le cerveau du système de routing.** Tout changement a un impact global.

Avant de modifier :
1. Activer le party mode — validation de Aria (qa-gsane) + Gsane Master
2. Vérifier qu'aucune entrée existante ne couvre déjà le cas
3. Éviter les chevauchements de trigger keywords

Format d'une ligne :

```csv
request_type,target_agent,module,path,icon,description,trigger_keywords
run-tests,tea,tea,_gsane/tea/agents/tea.md,🧪,Description,keyword1;keyword2;keyword3
```

---

## Modifier `copilot-instructions.md`

⚠️ Ce fichier est chargé par **tous les agents Copilot** à chaque session. Sévérité HIGH.

- Party mode obligatoire (Aria + Gsane Master minimum)
- Ne jamais supprimer le bloc `## ⛔ PRE-EXECUTION GATE`
- Documenter dans le CHANGELOG

---

## Tester localement

Simulation complète du CI `validate-pr.yml` sous PowerShell :

```powershell
# T1 — CHANGELOG
Test-Path "CHANGELOG.md"
Select-String "CHANGELOG.md" -Pattern "\[Unreleased\]" -Quiet
# Attendu : True, True

# T2 — Chemins dépréciés
(Get-ChildItem ".github\prompts","_gsane" -Recurse -File |
  Select-String "_gsane/bmm/").Count
# Attendu : 0

# T3 — .agent.md count
(Get-ChildItem ".github\agents" -Filter "*.agent.md").Count
# Attendu : 13 (ou plus si tu as ajouté un agent)

# T4 — Structure GSANE
@("_gsane","_gsane/core","_gsane/core/agents","_gsane/core/workflows",
  "_gsane/_config","_gsane/_memory",".github/agents",".github/prompts",".github/skills") |
  ForEach-Object { "$_ : $(Test-Path $_)" }
# Attendu : True partout

# T5 — Hooks
@("pre-commit.sh","hooks.json","flywheel-trigger.sh","session-start.sh","session-stop.sh") |
  ForEach-Object { "$_ : $(Test-Path ".github\hooks\$_")" }
# Attendu : True partout

# T6 — Manifests
@("agent-manifest.csv","workflow-manifest.csv","agent-delegation-matrix.csv","gsane-help.csv") |
  ForEach-Object { "$_ : $(Test-Path "_gsane\_config\$_")" }
# Attendu : True partout
```

### Smoke test agent

Après avoir ajouté un agent, vérifie les champs obligatoires :

```powershell
Select-String ".github\agents\{module}-{nom}.agent.md" -Pattern "user-invokable|orchestrated-by|name:"
```

### Vérification sync manifest

```powershell
$manifestCount = (Get-Content "_gsane\_config\agent-manifest.csv").Count - 1
$agentMdCount  = (Get-ChildItem ".github\agents" -Filter "*.agent.md").Count
"Manifest: $manifestCount | .agent.md: $agentMdCount"
# Attendu : valeurs égales
```

---

## Format des commits

```
type(catégorie): description courte (max 72 chars)

- détail 1
- détail 2
```

**Types :** `feat` `fix` `docs` `refactor` `test` `chore`

**Catégories :** `core` `bmb` `cis` `tea` `governance` `ci` `agents` `workflows`

**Exemples :**

```
feat(tea): add run-tests entry to delegation matrix

- agent-delegation-matrix.csv: new row routing test/validate requests to Murat
- Covers: tester, valider le projet, check ci, smoke test, regression check
```

```
fix(governance): add PRE-EXECUTION GATE to copilot-instructions

- Block solo execution before mandatory delegation matrix check
- 3-step checklist + keyword table added as first section
```

```
docs(root): add CONTRIBUTING.md

- Full contributor guide: structure, rules, agent/workflow/module creation
- CI simulation commands, commit format, PR body template
```

---

## Workflow de contribution pas à pas

```bash
# 1. Partir de main à jour
git checkout main && git pull origin main

# 2. Créer la branche
git checkout -b feature/{description}-{YYYY-MM-DD}
# ou : git checkout -b fix/{description}-{YYYY-MM-DD}

# 3. Implémenter et mettre à jour CHANGELOG.md

# 4. Committer
git add {fichiers} CHANGELOG.md
git commit -m "type(catégorie): description"

# 5. Pousser
git push -u origin {nom-branche}

# 6. Ouvrir la PR via l'URL compare
# https://github.com/zavrocKk/zav-sandbox/compare/main...{nom-branche}
# → Remplir le titre et coller le body template dans la description
```

**Body template PR :**

```markdown
## Description
{description de la modification}

## Type de changement
- [ ] ✨ Fonctionnalité
- [ ] 🐛 Correction
- [ ] 📚 Documentation
- [ ] 🔧 Configuration

## Fichiers modifiés
- {fichier1}
- {fichier2}

## Checklist
- [ ] CHANGELOG.md mis à jour
- [ ] Conventions GSANE respectées
- [ ] Aucun chemin déprécié `_gsane/bmm/` introduit
- [ ] Structure GSANE intacte
- [ ] Party mode appliqué si sévérité medium/high
```

> Le CI `validate-pr.yml` **refuse les PRs sans description**. Ne soumets pas une PR avec un body vide.

---

## Questions ?

Utilise `/gsane-help` dans Copilot Chat pour obtenir des conseils contextuels, ou ouvre une issue avec le label approprié :

- `bug` — quelque chose ne fonctionne pas
- `enhancement` — proposition d'amélioration
- `new-agent` — proposition d'un nouvel agent
- `new-workflow` — proposition d'un nouveau workflow
- `governance` — question sur les règles GSANE

