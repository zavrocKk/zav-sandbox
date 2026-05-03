# Roadmap — Agentic Team Framework

Document de référence sur l'avancement du projet et les prochaines étapes.
Mis à jour au fur et à mesure des sessions avec Claude.

## Vue d'ensemble

✅ Phase 0 — Setup
✅ Phase 1 — Fiabilité
✅ Phase 2 — Templates
✅ Phase 3 — Checklists
✅ Phase 4 — Test d'intégration
✅ Phase 4.5 — Clarification stratégique (vision, cible, différenciation)
🟡 Phase 5 — MVP basé sur la vision (À DÉFINIR ENSEMBLE)
⬜ Phase 6 — Party Mode (exécution parallèle)
⬜ Phase 7 — Mémoire persistante (artefacts de contexte)
⬜ Phase 8 — Skills techniques (Helm, K8s, Terraform, etc.)
⬜ Phase 9 — Brainstoming et comparer avec ce qui a au marché.

## Détail des phases terminées

### ✅ Phase 0 — Setup

- Structure de dossiers créée (`.github/agents/`, `agents/personas/`, `agents/workflows/`, etc.)
- Migration de `.chatmode.md` (ancien format) vers `.agent.md` (nouveau format VSCode)
- Orchestrateur visible dans le dropdown des agents

### ✅ Phase 1 — Fiabilité

- Patch pour forcer le respect du flux ANALYSE → PLAN → CONFIRM → EXECUTE → SYNTHESIS
- Patch Scribe pour que les livrables du PLAN soient des engagements, pas des suggestions
- Validation via test nginx routing

### ✅ Phase 2 — Templates

- `agents/templates/incident-report.md` — post-mortem blameless
- `agents/templates/adr.md` — Architecture Decision Record (Michael Nygard)
- `agents/templates/prd.md` — Product Requirements Document léger
- Validation via test post-mortem Postgres disque plein

### ✅ Phase 3 — Checklists

- `agents/checklists/incident-triage.md` — pour DevOps en début d'incident
- `agents/checklists/security-review.md` — pour Security en audit
- `agents/checklists/pre-deploy.md` — avant mise en prod
- Personas DevOps et Security mis à jour pour les référencer

### ✅ Phase 4 — Test d'intégration

- Test final : audit sécurité d'un endpoint /admin/users sans auth
- Résultat : audit de qualité professionnelle, mobilisation Security + Developer + Architect + Scribe
- 2 livrables produits automatiquement (rapport d'audit + ADR-0001)
- Tous les critères critiques + qualité validés

### ✅ Phase 4.5 — Clarification stratégique

**Décisions prises** :

- **Cible** : analystes techniques + équipes DevOps/CI-CD/Platform/SRE
- **Différenciation** : 100% markdown, natif VSCode + Copilot, pour les techs
  qui ne sont pas devs à 100%
- **Position éthique** : ambassadeur IA, pas de contrainte IP, prudence quand
  même (reconstruction propre, pas copier-coller du système au bureau)
- **Ambition** : framework officiel d'équipe, puis ouverture publique

**Voir** : `VISION.md` pour les détails complets.

## Personas actuellement définis

8 personas dans `agents/personas/` :

- 🎯 Orchestrator (méta-agent)
- 🛠️ DevOps
- 💻 Developer
- 🔒 Security
- 🏗️ Architect
- 🧪 QA
- 📊 Product Analyst
- 🗄️ Data Engineer
- 📝 Scribe (toujours invoqué en fin)

## Workflows actuellement définis

Dans `agents/workflows/` :

- `incident-response.md`
- `code-analysis.md`
- `feature-development.md`
- `architecture-design.md`
- `data-pipeline.md`

## Détail des phases à venir

### 🟡 Phase 5 — MVP basé sur la vision

**À définir ensemble lors de la prochaine session.**

Questions à trancher :

- Que garde-t-on tel quel de ce qui a été construit en Phase 0-3 ?
- Que faut-il adapter pour mieux servir la cible (analystes + DevOps) ?
- Quel est le "premier vrai usage" qui validera la vision ?
- Dans quel ordre on attaque les phases 6-9 ?

### ⬜ Phase 6 — Party Mode (exécution parallèle)

**Concept** : permettre à plusieurs personas de travailler en parallèle sur
une même demande, plutôt que séquentiellement.

**Inspiration** : système au bureau qui fait ça avec optimisation tokens (~70%).

**À explorer** :

- Architecture conceptuelle (orchestrateur dispatcher → agrégation)
- Comment l'implémenter dans le format `.agent.md` de VSCode
- Quand le déclencher (toutes les sessions ? sur demande ? automatique selon
  complexité ?)

### ⬜ Phase 7 — Mémoire persistante

**Concept** : artefacts de contexte qui persistent entre sessions, permettant
au framework de "reprendre où il s'était arrêté".

**Inspiration** : système au bureau qui produit un artefact mémoire, reset
le contexte, et relit pour reprendre sans perte.

**À explorer** :

- Format des artefacts (markdown structuré ? YAML ?)
- Quand sauvegarder (fin de session ? checkpoint manuel ?)
- Comment le rendre invisible mais utile pour l'utilisateur

### ⬜ Phase 8 — Skills techniques

**Concept** : ajouter des skills spécialisées pour les technologies qu'utilisent
les équipes cibles.

**Candidates prioritaires** :

- Helm / Kubernetes
- Terraform / IaC
- GitHub Actions / GitLab CI
- AWS (EKS, ECS, IAM, etc.)
- Observabilité (Prometheus, Datadog, Splunk)
- Java / Python (analyse de stack traces)
- Méthodologies (5 Pourquoi Toyota, RCA, RACI)

### ⬜ Phase 9 — Ouverture

**Concept** : sortir le framework du contexte personnel pour le rendre
utilisable par d'autres.

**Étapes possibles** :

1. Test interne avec l'équipe
2. Documentation publique (README, guide démarrage, exemples)
3. Repo GitHub public
4. Site/blog de référence ("how-to construire un framework agentique")
5. Communication communautaire

## Principes directeurs (boussole)

À chaque décision future, on se réfère à ces principes :

1. **Pour qui ?** Analystes techniques + équipes DevOps/CI-CD avant tout.
2. **Configuration ?** En markdown, lisible et modifiable par non-devs.
3. **Outils ?** VSCode + Copilot natif, rien d'autre à installer.
4. **Complexité ?** Si un dev senior est nécessaire pour configurer, on a échoué.
5. **Drift ?** Anti-drift par design, fiabilité avant fonctionnalités.
6. **Livrables ?** Markdown structurés dans `docs/`, prêts à committer.

## Parking lot (idées en attente)

Voir `IDEAS.md` pour la liste complète des idées notées au fil des sessions.
