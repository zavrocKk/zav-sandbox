# zav-sandbox — Système d'agents virtuels mono-session

Un orchestrateur unique (custom chat mode VS Code) qui simule une **équipe d'experts virtuels** — DevOps, Developer, QA, Security, Architect, Product Analyst, Data Engineer, Scribe — au sein d'**une seule conversation**. Inspiré de [BMAD-METHOD](https://github.com/bmadcode/BMAD-METHOD), mais radicalement simplifié.

## Philosophie : mono-session vs BMAD multi-session

| Aspect                | BMAD-METHOD (multi-session)                       | Ce système (mono-session)                            |
| --------------------- | ------------------------------------------------- | ---------------------------------------------------- |
| Architecture          | Plusieurs agents dans plusieurs sessions/fichiers | **1 orchestrateur** qui incarne tour à tour les rôles |
| État partagé          | Fichiers d'état entre agents                      | Aucun — l'historique de la conversation suffit       |
| Transitions           | Switch de session                                 | En-têtes visuels `───── 🛠️ DevOps — Titre ─────`     |
| Coût d'entrée         | Élevé (multi-session, conventions, fichiers)      | Faible : 1 agent + des fichiers de référence         |
| Cas d'usage           | Projets longs, équipes, workflows complexes       | Single-dev, sandbox, prototypage, support quotidien  |

L'idée : conserver le **bénéfice cognitif** de la multiplicité des perspectives sans la complexité opérationnelle du multi-agent.

## Modes multi-personas — Panel & Débat

Le travail multi-personas se décline en **deux réglages de la même mécanique** —
la sélection intelligente des agents par l'orchestrateur. Ils ne diffèrent que par
le nombre de passes. Détails et justification :
[docs/architecture/2026-05-30-party-mode-panel-vs-debate.md](docs/architecture/2026-05-30-party-mode-panel-vs-debate.md).
Protocoles opérationnels : [agents/protocols/light-panel.md](agents/protocols/light-panel.md)
(Panel) et [agents/protocols/debate.md](agents/protocols/debate.md) (Débat).

| | **Panel** (défaut) | **Débat** (sur invocation `/debate`) |
|---|---|---|
| Quand | Problème **fermé** : une réponse à trouver | Problème **ouvert** : on bloque ou on brainstorme |
| Travail type | Incident, analyse, doc, design | Brainstorming, arbitrage, idéation |
| Mécanique | Chaque expert → son angle **une fois** → synthèse Scribe | Les experts se répondent sur **N rounds** → synthèse Scribe |
| Friction | Coûteuse → évitée | Productive → recherchée |
| Coût tokens | Borné par construction | Volontairement plus élevé (assumé) |

> **Règle binaire** — Panel : aucun persona ne réagit à un autre (une passe).
> Débat : les personas réagissent entre eux (max N rounds), puis le Scribe force
> la synthèse. Dans les deux cas, le **Scribe ferme toujours** par un livrable.

## Structure du dépôt

```
.
├── .github/
│   ├── agents/
│   │   └── orchestrator.agent.md        # Le custom agent
│   └── copilot-instructions.md          # Instructions globales (français, livrables, sécu)
├── agents/
│   ├── personas/
│   │   ├── orchestrator.md              # 🎼 Meta-agent
│   │   ├── devops.md                    # 🛠️ Infra, CI/CD, monitoring
│   │   ├── developer.md                 # 💻 Code, tests, debug
│   │   ├── qa.md                        # 🧪 Stratégie tests, edge cases, couverture
│   │   ├── security.md                  # 🔒 OWASP, secrets, threat modeling
│   │   ├── architect.md                 # 🏗️ Patterns, ADR, diagrammes
│   │   ├── product-analyst.md           # 📊 User stories, critères d'acceptation, métriques
│   │   ├── data-engineer.md             # 🗄️ Schémas, pipelines, ETL/ELT, qualité data
│   │   └── scribe.md                    # 📝 Synthèse, doc, post-mortems
│   ├── workflows/
│   │   ├── incident-response.md         # Panne / alerte production
│   │   ├── code-analysis.md             # Audit / review d'un module
│   │   ├── feature-development.md       # Nouvelle fonctionnalité
│   │   ├── architecture-design.md       # Choix techno, refonte
│   │   └── data-pipeline.md             # ETL, migration, modélisation BI
│   ├── templates/
│   │   ├── incident-report.md           # Post-mortem blameless
│   │   ├── adr.md                       # Architecture Decision Record (Nygard)
│   │   ├── memory-checkpoint.md         # Checkpoint de mémoire inter-sessions (Phase 7)
│   │   └── prd.md                       # Product Requirements Document léger
│   └── hooks/                           # Agent hooks VS Code (opt-in, OFF par défaut)
│       ├── security-guard.ps1/.sh       # PreToolUse : confirmation sur commandes destructives
│       ├── memory-nudge.ps1/.sh         # PreCompact/Stop : rappel /checkpoint
│       └── hooks.json                   # Config (activation manuelle via settings)
├── docs/                                # Tous les livrables produits par le Scribe
│   ├── incidents/                       # Post-mortems
│   ├── architecture/                    # Notes d'architecture
│   ├── decisions/                       # ADRs (NNNN-slug.md)
│   └── _scratch/memory/                 # Checkpoints de mémoire inter-sessions (Phase 7)
└── README.md
```

## Activer l'agent Orchestrator dans VS Code

1. Ouvre le workspace `zav-sandbox` dans VS Code (avec l'extension **GitHub Copilot Chat**).
2. Ouvre la vue **Chat** (raccourci : `Ctrl+Alt+I` sur Windows/Linux, `⌃⌘I` sur macOS).
3. En haut de la vue Chat, ouvre le **dropdown des agents** (à côté du champ de saisie, là où il est écrit « Ask », « Edit » ou « Agent » par défaut).
4. Sélectionne l'**agent Orchestrator** dans le dropdown (Configure Custom Agents). VS Code détecte automatiquement les `.agent.md` sous `.github/agents/`.
5. (Optionnel) Vérifie via la palette de commandes (`Ctrl+Shift+P`) → `Chat: Configure Custom Agents` que `orchestrator` est bien listé.

> Si `orchestrator` n'apparaît pas : recharge la fenêtre (`Developer: Reload Window`), vérifie que le fichier est bien à `.github/agents/orchestrator.agent.md` et que son frontmatter YAML est valide.

## Exemple de cycle complet — Incident en production

**Demande utilisateur :**
> « L'API `/checkout` renvoie du 502 depuis 10 minutes, le dashboard montre une explosion de la latence. Help. »

**Réponse de l'orchestrateur :**

```
## 🎼 Analyse
Incident production — API checkout, 502 + latence anormale, depuis ~10 min. Workflow : incident-response.

## 🎼 Plan
| # | Persona      | Tâche                                          | Livrable                              |
|---|--------------|------------------------------------------------|---------------------------------------|
| 1 | 🛠️ DevOps    | Triage : sévérité, périmètre, changements récents | Observation + hypothèses             |
| 2 | 🛠️ DevOps    | Mitigation candidate (rollback ?)              | Plan d'action — confirmation requise  |
| 3 | 💻 Developer | Si cause applicative : analyse code + patch    | Diff + tests                          |
| 4 | 🏗️ Architect | Durcissement (circuit breaker ? timeout ?)     | Reco + ADR si structurant             |
| 5 | 📝 Scribe    | Post-mortem blameless                          | docs/incidents/2026-05-02-checkout-502.md |

Confirmes-tu ce plan ? (oui / ajuste / `/quick`)
```

→ Après confirmation utilisateur, l'orchestrateur enchaîne les personas avec leurs en-têtes visuels, puis le **Scribe ferme** avec bilan + livrable créé dans `docs/incidents/`.
## Exemple rapide — Cadrage d'une feature

**Demande utilisateur :**
> « Je veux ajouter un système de notifications push pour les utilisateurs mobile. »

**Réponse de l'orchestrateur :**

```
## 🎼 Analyse
Nouvelle feature. Besoin à cadrer avant tout design. Workflow : feature-development.

## 🎼 Plan
| # | Persona            | Tâche                                               | Livrable                                  |
|---|--------------------|-----------------------------------------------------|-------------------------------------------|
| 1 | 📊 Product Analyst  | Problème, segments, user stories, critères accept.  | PRD léger                                 |
| 2 | 🏗️ Architect       | Options d'implémentation (FCM, SSE, WebPush...)      | Reco + diagramme séquence                 |
| 3 | 🔒 Security        | Threat model : tokens de device, opt-in, permissions | Contrôles à intégrer                       |
| 4 | 💻 Developer        | Implémentation + tests unitaires                    | Diff + tests                              |
| 5 | 🧪 QA             | Matrix de tests : permission rejetée, token expiré  | Gaps + tests E2E                          |
| 6 | 🛠️ DevOps          | Config infra push service, alertes taux délivraison  | IaC + pipeline                            |
| 7 | 📝 Scribe          | PRD final + ADR si décision structurante              | docs/2026-05-02-feature-push-notifs.md    |

Confirmes-tu ce plan ? (oui / ajuste / `/quick`)
```
## Comment ajouter un persona

1. Crée `agents/personas/<nom>.md` avec les sections : `Identité`, `Ton`, `Domaines`, `Quand intervenir`, `Output type`, `Handoffs`, `Anti-patterns`.
2. Ajoute son emoji et sa ligne dans la table des personas de l'agent (`.github/agents/orchestrator.agent.md`).
3. Mets à jour le mapping `demande → workflow → personas` de l'agent si ce persona ouvre de nouveaux types de demandes.

## Comment ajouter un workflow

1. Crée `agents/workflows/<nom>.md` avec : un **diagramme Mermaid** des phases, une **table persona par étape**, des **règles spécifiques**, des **anti-patterns**, un **livrable final**.
2. Ajoute une ligne dans le mapping de l'agent reliant un type de demande à ce workflow.

## Comment ajouter un template

1. Crée `agents/templates/<nom>.md` avec une structure prête à remplir (placeholders entre `<…>`).
2. Référence-le dans le persona Scribe ou dans le workflow concerné.

## Conventions transversales

- Tous les `.md` sont en **français**, le code et les identifiants en **anglais**.
- Diagrammes : **Mermaid uniquement**.
- Citations de fichier : `chemin/relatif.ext:ligne`.
- Aucun secret en clair.
- Confirmation utilisateur obligatoire pour toute action destructive.
- Le **Scribe ferme toujours** le cycle.

Voir [.github/copilot-instructions.md](.github/copilot-instructions.md) pour les règles globales détaillées.
