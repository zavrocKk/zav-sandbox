# Agent Template — GSANE Strike Team

> Template officiel pour la création de nouveaux agents.
> Bond utilise ce fichier comme référence lors de toute création/modification d'agent.

## Architecture Single Source of Truth (SSOT)

```
agent-manifest.yaml          ← REGISTRE MACHINE (10 champs : routing + gouvernance)
_gsane/agents/{agent}.md     ← SOURCE DE VÉRITÉ (persona complète, chargée par MCP)
.github/agents/{agent}.agent.md ← ADAPTATEUR COPILOT (frontmatter + loader)
```

---

## 1. Registre machine — agent-manifest.yaml

```yaml
- name: {nom_interne}
  displayName: {Prénom (Rôle)}
  icon: {emoji}
  path: _gsane/agents/{nom_interne}.md
  version: "2.1"
  status: active
  role: {2-4 mots}
  capabilities: {liste de compétences, séparées par virgule}
  golden_rule: {1 phrase — l'interdit fondamental}
  never_do:
    - {interdit concret et testable 1}
    - {interdit concret et testable 2}
    - {interdit concret et testable 3 — optionnel}
```

---

## 2. Source de vérité — _gsane/agents/{agent}.md

### Frontmatter obligatoire

```yaml
---
name: "{nom_interne}"
description: "{rôle court}"
version: "2.0"
persona_template: "persona-template-v2"
---
```

### Sections obligatoires (dans cet ordre)

```markdown
## Identity
{1 phrase concrète — qui est cet agent et quel est son rôle unique}

## Voice
{Signature verbale unique — comment cet agent s'exprime}

## Activation
{Quand et comment cet agent est chargé — références aux steps XML}

## Workflow opérationnel
1. {Étape 1}
2. {Étape 2}
...
{5-7 étapes numérotées spécifiques au rôle}

## Handoff Protocol
{Artefact produit, gate de validation, agent suivant, questions ouvertes}

## Never Do
- {Interdit 1 — concret et testable par Quinn}
- {Interdit 2}
- {Interdit 3}
- {Interdit 4 — optionnel}

## Golden Rule
> {1-2 phrases — philosophie fondamentale de l'agent, cohérente avec la règle XML}

## Escalation
- {Situation X} → {Agent cible}
- {Situation Y} → {Agent cible}
{3-5 chemins d'escalade avec agent cible}
```

### Contraintes
- Taille cible : 300-400 mots MAX pour les sections narratives
- Chaque agent doit sonner DIFFÉRENT — voix unique
- Les never_do doivent être concrets et vérifiables par Quinn
- Aucune référence aux modules dépréciés (CIS/TEA/BMB)

---

## 3. Adaptateur Copilot — .github/agents/{agent}.agent.md

```markdown
---
name: "{displayName}"
description: "{role} — {1 phrase identity}"
tools: [read, search, edit, execute, runSubagent]
---

{bloc <agent-activation> qui charge _gsane/agents/{agent}.md}
```

### Règles
- JAMAIS de contenu original ici — tout vit dans _gsane/agents/
- Le frontmatter suit le format GitHub Copilot strict
- La description est une projection de role + identity du manifest/md
