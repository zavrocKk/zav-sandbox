# Parking lot — Idées et questions ouvertes

Ce fichier collecte les idées et questions qui débordent du focus actuel. **Rien ici n'est urgent.** On y reviendra à la phase appropriée selon la feuille de route.

## Format

Chaque entrée :

- **Date** : quand l'idée a émergé
- **Idée** : description brève
- **Phase d'examen suggérée** : quand on devrait y revenir
- **Statut** : 🟡 ouverte / 🟢 traitée / 🔴 abandonnée

---

## En attente

### 2025-05-02 — Cycle de vie des artefacts (cleanup post-session)

**Idée** : Comment faire le ménage des artefacts qui ne sont plus utiles après une session terminée ? Certains livrables (post-mortems, ADR, runbooks) doivent être conservés pour toujours. D'autres (notes de session, drafts, fichiers de scratch) sont temporaires et devraient être archivés ou supprimés.

**Questions sous-jacentes** :

- Distinguer "artefact pérenne" vs "artefact de session" dès la création ?
- Convention de nommage / dossier dédié pour le temporaire ?
- Politique de rétention (auto-clean après N jours ?) ?
- Le Scribe devrait-il proposer ce qui peut être archivé en fin de session ?

**Phase d'examen suggérée** : Phase 4 (vrai usage) — on aura accumulé des artefacts réels et on saura ce qui pollue vs ce qui sert.

**Statut** : 🟡 ouverte

---

### 2025-05-02 — Dossier scratch / inputs temporaires

**Idée** : Où mettre les artefacts de travail temporaires que je donne à l'orchestrateur pour analyse (logs, configs, dumps, exports) ? Pas de dossier `inputs/` ou `scratch/` actuellement.

**Questions sous-jacentes** :

- Convention : `scratch/` à la racine ? `docs/_scratch/` ?
- Doit-il être dans `.gitignore` (probablement oui — ce sont des artefacts éphémères, parfois sensibles) ?
- L'orchestrateur doit-il être instruit de chercher là en priorité quand on dit "analyse ce log" ?
- Auto-cleanup après N jours ?

**Phase d'examen suggérée** : Phase 4 (vrai usage) — on saura précisément quand on aura un cas concret de log à analyser.

**Statut** : 🟡 ouverte

---

### 2025-05-02 — Personas "découvrables" même sans agent sélectionné

**Idée** : Observé pendant Phase 3 : Copilot en Agent par défaut a adopté le format "📝 Scribe" pour son bilan final, alors que l'orchestrator n'était pas sélectionné. Probablement parce qu'il a lu `agents/personas/scribe.md` via les outils `codebase`/`search` pendant l'exécution.

**Questions sous-jacentes** :

- Est-ce un comportement souhaitable (les personas sont "disponibles" partout) ou problématique (confusion entre "qui parle" — orchestrateur vs Agent par défaut) ?
- Doit-on limiter la découvrabilité des personas via instructions dans `copilot-instructions.md` ?
- Ou au contraire en profiter : transformer les personas en "skills" partagés que tout agent peut invoquer ?

**Phase d'examen suggérée** : Phase 5 (skills) — c'est exactement la question qui se pose au moment de promouvoir un persona en skill.

**Statut** : 🟡 ouverte

---
### 2026-05-02 — Templates manquants pour runbook et architecture
**Idée** : 2 templates avoués manquants dans `orchestrator.agent.md` (mentionnés 
comme "pas encore de template — structure libre"). Sans template, le Scribe 
improvise → drift sur le format des livrables runbook et architecture.

**Questions sous-jacentes** :
- Quelle structure standard pour un runbook ?
- Quelle structure pour un document d'architecture (C4 niveau 2 par défaut) ?
- Faut-il prévoir un template "data-pipeline-doc" aussi ?

**Phase d'examen suggérée** : Phase 5.3 (déjà actée — actions 9-10 du prompt 
de correctifs).

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Mécanisme de session longue (checkpoint/résumé)
**Idée** : Aucun mécanisme dans l'orchestrator pour gérer une session qui 
déborde (incident long, audit complexe). Pas de checkpoint, pas de reset 
propre, pas de résumé contextuel automatique.

**Questions sous-jacentes** :
- Quand déclencher un checkpoint (manuel ? automatique selon longueur ?) ?
- Format du résumé contextuel (markdown structuré ? YAML ?) ?
- Comment reprendre proprement après un reset (relire le dernier checkpoint) ?

**Phase d'examen suggérée** : Phase 7 (mémoire persistante) — c'est probablement 
la base de ce qui sera la mémoire inter-sessions.

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Refactor orchestrator en protocoles externes (DRY)
**Idée** : `orchestrator.agent.md` (205 lignes) répète plusieurs règles 
(PRE-FLIGHT, anti-drift, contrat Scribe, anti-patterns) à plusieurs endroits. 
Découper en `agents/protocols/*.md` chargés par référence pour réduire la 
duplication et la charge contexte.

**Questions sous-jacentes** :
- Quels protocoles méritent un fichier dédié ? (preflight, scribe-contract, 
  parallel-block ?)
- Comment Copilot charge-t-il un fichier référencé ? (via @include ? via 
  mention dans le mapping ?)
- Risque : éclatement excessif rendant la lecture plus difficile pour un 
  non-dev.

**Phase d'examen suggérée** : Phase 5.3 (déjà actée — action 3 du prompt 
de correctifs).

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Référence aux checklists incohérente entre personas
**Idée** : Seuls `devops.md` et `security.md` ont une section "Checklists 
à consulter". Les 6 autres personas n'en ont pas, alors que `pre-deploy.md` 
concerne aussi Developer/QA/Architect.

**Questions sous-jacentes** :
- Faut-il propager systématiquement la section dans tous les personas ?
- Ou centraliser dans `orchestrator.agent.md` (mapping demande → checklist) ?
- Compromis : les deux ? (section optionnelle dans personas + mapping 
  central).

**Phase d'examen suggérée** : Phase 5.3 (action 1.f du prompt de correctifs 
— propagation actée pour Developer/QA/Architect).

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Sections "Différence avec X" à systématiser
**Idée** : 3 personas (`qa.md`, `product-analyst.md`, `data-engineer.md`) 
ont une section explicite "Différence avec...". C'est excellent pour éviter 
les chevauchements de périmètre. À propager pour les autres.

**Questions sous-jacentes** :
- DevOps vs Developer (debug applicatif vs debug infra) — utile ?
- Architect vs Developer (design vs implé) — utile ?
- Security vs DevOps (qui possède quoi en hardening infra ?) — utile ?

**Phase d'examen suggérée** : Phase 5.3 ou Phase 6 — pas critique pour le MVP.

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Contrat Scribe à centraliser
**Idée** : Le contrat Scribe (Type A/B + procédure templates obligatoires + 
anti-pattern interdit) est éclaté entre `scribe.md` et `orchestrator.agent.md`. 
À unifier pour single source of truth.

**Questions sous-jacentes** :
- Où centraliser : dans `scribe.md` (orienté persona) ou dans 
  `orchestrator.agent.md` (orienté orchestration) ?
- Choix retenu : `scribe.md` (le persona Scribe est propriétaire de son 
  propre contrat).

**Phase d'examen suggérée** : Phase 5.3 (déjà actée — action 2 du prompt 
de correctifs).

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Workflows orphelins de leurs checklists (CRITIQUE)
**Idée** : 0 des 5 workflows ne référencent les 3 checklists de Phase 3. 
Les checklists existent mais ne sont jamais invoquées par les workflows. 
C'est probablement la cause directe du drift identifié dans `test-notes.md` 
("Solo difrt ou oublie de créer les artefacts de synthèse").

**Questions sous-jacentes** :
- Pourquoi cette dette est-elle apparue ? (Phase 3 livrée en silo, jamais 
  ré-intégrée dans les workflows existants)
- Quelle gouvernance pour éviter que ça se reproduise ? (checklist de 
  cohérence entre artefacts ? meta-audit régulier ?)

**Phase d'examen suggérée** : Phase 5.3 (déjà actée — actions 1.a, 1.c, 1.e 
du prompt de correctifs).

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Pas de fast-track / mode allégé pour les workflows
**Idée** : Tous les workflows sont conçus pour le cas complet (5-7 phases). 
Un user qui a une demande simple va sauter des phases sans mode officiel 
pour le faire. Risque de drift.

**Questions sous-jacentes** :
- Concevoir un mode "allégé" (3-4 phases) pour les cas simples ?
- Ou utiliser le futur Party Mode (Phase 6) pour faire la sélection 
  contextuelle qui évite les phases inutiles ?
- Comment l'orchestrator décide-t-il du mode (complet vs allégé) — 
  signal explicite de l'utilisateur ? heuristique ?

**Phase d'examen suggérée** : Phase 6 (Party Mode) — c'est probablement la 
solution naturelle, pas un mode allégé séparé.

**Statut** : 🟡 ouverte

### 2026-05-XX — Workflow problem-resolution (5 Pourquoi / Ishikawa)
**Idée** : Workflow pour problèmes complexes non-urgents et non-localisés 
(différent de incident-response et de code-analysis).
**Phase d'examen suggérée** : Phase 5.5 (après test MVP) ou Phase 8.
**Statut** : 🟡 ouverte

### 2026-05-XX — Brainstorming : phase ou workflow ?
**Idée** : À arbitrer — soit workflow standalone, soit phase initiale 
disponible dans plusieurs workflows existants.
**Phase d'examen suggérée** : Phase 5.5 ou Phase 6 (lié au Party Mode).
**Statut** : 🟡 ouverte

### 2026-05-XX — Workflow pentest-correction (probablement → skill)
**Idée** : Plutôt qu'un workflow dédié, créer une skill 
"pentest-remediation" activable dans les workflows existants 
(security-review + code-analysis + feature-development).
**Phase d'examen suggérée** : Phase 8 (skills techniques).
**Statut** : 🟡 ouverte

### 2026-05-02 — Workflow problem-resolution (5 Pourquoi / Ishikawa)
**Idée** : Workflow pour traiter des problèmes complexes qui ne sont ni un 
incident urgent ni un audit de code localisé. Cas type : "notre process 
de déploiement est lent et personne ne sait pourquoi".

**Différenciation avec l'existant** :
- vs `incident-response` : pas d'urgence, pas de prod down
- vs `code-analysis` : pas de module spécifique, problème transverse
- vs `architecture-design` : pas de choix techno, problème opérationnel

**Questions sous-jacentes** :
- Méthodologie de RCA : 5 Pourquoi (Toyota), Ishikawa/fishbone, ou les deux 
  selon le type de problème ?
- Personas mobilisés : Product Analyst (cadrage) + variable selon nature 
  (DevOps / Architect / Dev) + Scribe ?
- Risque de chevauchement avec les **skills méthodologiques** prévues en 
  Phase 8 (5 Pourquoi, RCA, RACI). Faut-il faire le workflow OU les skills, 
  pas les deux ?

**Phase d'examen suggérée** : Phase 5.5 (après test MVP) ou Phase 8 — 
décision : workflow ou skill ?

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Brainstorming : workflow standalone ou phase ?
**Idée** : Permettre à l'orchestrator de mener une session de brainstorming 
structurée. Mais à arbitrer : workflow standalone OU phase initiale 
disponible dans plusieurs workflows existants ?

**Tension à résoudre** :
- Si workflow standalone → quel **livrable markdown** est produit ? 
  (filtre 6 VISION : tout doit produire un livrable)
- Si phase amont → l'attacher à `feature-development.md`, 
  `architecture-design.md`, `problem-resolution.md` (si retenu) ?

**Inspiration BMAD** : Carson (brainstorming-coach) au bureau est un agent 
dédié dans le module CIS. Mais on a dit : pas de copie BMAD. À reconcevoir 
proprement.

**Questions sous-jacentes** :
- Format livrable possible : `docs/brainstorming/YYYY-MM-DD-slug.md` avec 
  sections "Question initiale / Idées générées / Clusters / Top 3 retenues / 
  Next steps" ?
- Quand l'utilisateur veut un brainstorming pur, c'est pas pour produire un 
  livrable, c'est pour explorer. Conflit avec le filtre 6 ?
- Pourrait-on en faire une **phase optionnelle** (drapeau `--with-brainstorm`) 
  dans certains workflows ?

**Phase d'examen suggérée** : Phase 5.5 ou Phase 6 (lié au Party Mode — 
brainstorming est un cas idéal de multi-personas).

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Pentest-remediation : skill plutôt que workflow ?
**Idée** : Workflow ou skill pour traiter les findings d'un pentest 
externe et appliquer les corrections priorisées.

**Pourquoi probablement skill plutôt que workflow** : un pentest-remediation 
est une **séquence préfabriquée** des workflows existants :
- `code-analysis` pour analyser les findings
- `security-review.md` (checklist) pour valider la couverture OWASP
- `feature-development` pour implémenter chaque correction
- `architecture-design` si la correction est structurante
- `incident-response` si une faille est exploitée en prod

→ Faire un workflow dédié reviendrait à dupliquer ce qui existe.

**Approche skill (préférée)** : créer une skill `pentest-remediation` 
activable dans n'importe quel workflow, qui apporte :
- Le format standard d'un pentest report (CVSS, CWE, exploitabilité)
- La méthodologie de priorisation (impact × exploitabilité × effort)
- Les patterns de correction par catégorie OWASP
- Les checks de non-régression à ajouter en CI

**Questions sous-jacentes** :
- Skill ou workflow ? **Décision préliminaire : skill.**
- Quel template de remediation report (`docs/security/pentest-NNN-remediation.md`) ?
- Comment relier au persona Security existant ?

**Phase d'examen suggérée** : Phase 8 (skills techniques) — c'est exactement 
le pattern d'usage prévu pour les skills.

**Statut** : 🟡 ouverte

### 2026-05-03 — Format de questionnement structuré (template ou tool)
**Idée** : Améliorer le format des questions PRE-FLIGHT pour réduire le risque 
de re-prompts incomplets. Deux pistes à investiguer :

**Piste A — Template markdown contraint** : tableau pré-formaté que l'utilisateur 
remplit ligne par ligne, validé par l'orchestrator avant de continuer.

**Piste B — Tool natif Copilot/VSCode** : vérifier si GitHub Copilot Chat 
expose un mécanisme structuré pour questions multi-choix ou formulaire 
(équivalent du tool `ask_user_input_v0` de Claude.ai). À ce jour, **non vérifié 
si ce tool existe** côté Copilot.

**Phase d'examen suggérée** : Phase 6 (Party Mode) ou Phase 8 (skills techniques) 
selon la piste retenue. Pas avant.

**Risque de drift** : moyen — l'idée vient d'une comparaison avec claude.ai, 
pas d'une friction réelle observée pendant le test 5.4-bis. Le format actuel 
(questions numérotées + format de réponse explicite) marche déjà.

**Statut** : 🟡 ouverte

### 2026-05-03 — Restructurer inputs vs outputs (séparation cycles de vie)
**Idée** : Distinguer 3 zones dans le repo selon le cycle de vie :
- `agents/` + `.github/` = code framework (versionné, stable)
- `inputs/` = matière fournie au framework par l'utilisateur (éphémère, 
  potentiellement gitignored)
- `outputs/` = livrables produits par le framework (à conserver, 
  potentiellement partageables)

**Bénéfices** :
- Clarté mentale : on sait toujours où chercher quoi
- Confidentialité : possibilité de gitignore les inputs sensibles
- Préparation pour Phases 7-8 : la mémoire persistante et les skills 
  consomment/produisent dans des dossiers identifiés

**Coût de migration** :
- Renommage de tous les chemins dans personas, workflows, orchestrator, 
  copilot-instructions
- Mise à jour des fichiers existants dans le repo

**Phase d'examen suggérée** : Phase 7 (mémoire persistante) — la migration 
sera structurellement nécessaire à ce moment, on la fait à ce moment-là 
avec une vraie raison technique.

**Origine** : question utilisateur du 2026-05-03 — instinct juste mais 
pas urgent.

**Statut** : 🟡 ouverte

## Format pour ajouter une nouvelle idée

```markdown
### YYYY-MM-DD — Titre court
**Idée** : ...
**Questions sous-jacentes** : ...
**Phase d'examen suggérée** : ...
**Statut** : 🟡 ouverte
```
---