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

### 2026-05-09 — F4 — Mémoire/contexte fragiles (confirmée Field Report)

**Idée** : Le Field Report 2026-05-04→08 confirme concrètement la friction mémoire
en usage réel : les sessions longues perdent le fil, l'orchestrator réexplique des
choses déjà établies, la cohérence se dégrade après ~40 min.

**Mitigation immédiate appliquée** : sessions courtes 30-40 min max, ouvrir/fermer
Copilot Chat plus souvent.

**Questions sous-jacentes** :
- Quel format de checkpoint minimal (artefact markdown, résumé structuré YAML ?) ?
- Le Scribe doit-il produire automatiquement un checkpoint en fin de session ?
- Comment le rendre transparent pour l'utilisateur (pas de charge cognitive) ?

**Référence** : `docs/decisions/0004-field-report-analysis-phase-5-7.md` — Friction F4.

**Phase d'examen suggérée** : Phase 7 (mémoire persistante).

**Statut** : 🟡 ouverte

---

### 2026-05-09 — F5 — Connexion native aux outils (MCP / APIs externes)

**Idée** : Field Report 2026-05-04→08 confirme que l'absence de connexion native
aux outils génère des frictions de workflow : l'utilisateur doit copier-coller
des résultats d'outils externes (AWS, Datadog, Splunk…) au lieu que l'orchestrator
les interroge directement.

**Questions sous-jacentes** :
- Quels outils prioritaires pour la cible (analystes DevOps/SRE) ?
- MCP servers disponibles vs à créer ?
- Comment éviter que la connexion outils devienne une dépendance de setup complexe
  (principe : rien d'autre à installer que VSCode + Copilot) ?

**Référence** : `docs/decisions/0004-field-report-analysis-phase-5-7.md` — Friction F5.

**Phase d'examen suggérée** : Phase 8 (Skills techniques + MCP).

**Statut** : 🟡 ouverte

---

### 2026-05-09 — F6 — Coût tokens élevé (à surveiller post-5.7.A)

**Idée** : Field Report 2026-05-04→08 note un coût en tokens perçu comme élevé.
Diagnostic : conséquence directe de F2 (Orchestrator répond lui-même au lieu de
déléguer). Si la délégation est correcte, le coût devrait baisser naturellement.

**Traitement** : dépendant des correctifs F2 (Phase 5.7.A — correctifs 2.A et 2.B).
À réévaluer après Field Report intermédiaire post-5.7.A.

**Questions sous-jacentes** (si friction persiste post-5.7.A) :
- Règle anti-bavardage Orchestrator (correctif 2.D dans 5.7.B) ?
- Heuristique de longueur de réponse par persona ?
- Peut-on quantifier le coût réel par workflow pour valider l'impact ?

**Référence** : `docs/decisions/0004-field-report-analysis-phase-5-7.md` — Friction F6.

**Phase d'examen suggérée** : réévaluation après Phase 5.7.A. Si persistant → Phase 5.7.B (correctif 2.D).

**Statut** : 🟡 ouverte (conditionnel — peut se fermer automatiquement post-5.7.A)

---

### 2026-05-09 — Insight unifiant — Zones grises anti-improvisation

**Idée** : L'analyse du Field Report 2026-05-04→08 révèle un pattern transversal à
toutes les frictions majeures : l'orchestrator improvise dans les zones grises où
le contrat ne l'oblige pas formellement.

> *« Le framework a des règles bien posées, mais elles ne sont pas appliquées avec
> discipline systématique. Surtout quand le contexte sature ou quand l'orchestrator
> est tenté d'improviser. »*

**Implication stratégique** : l'axe de progrès du framework n'est plus « ajouter
des règles » mais « rendre les règles existantes non-contournables par design ».
Règles binaires et vérifiables > règles narratives sujettes à interprétation.

**À surveiller comme méta-critère** dans les futurs Field Reports :
- Les nouveaux correctifs ajoutent-ils des règles binaires ou narratives ?
- Le score d'improvisation observée diminue-t-il session après session ?

**Référence** : `docs/decisions/0004-field-report-analysis-phase-5-7.md` — Section « Insight unifiant ».

**Phase d'examen suggérée** : méta-axe permanent — à évaluer à chaque Field Report.

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

### 2026-05-09 — Mécanisme de session longue (mitigation immédiate + Phase 7)
**Idée** : Confirmé par Field Report — les sessions longues dégradent l'application 
des contrats par l'orchestrator. Mitigation immédiate : sessions courtes 30-40 min, 
ouvrir/fermer Copilot Chat plus souvent. Solution structurelle : Phase 7 (mémoire 
persistante avec checkpoints, résumés contextuels automatiques).

**Source** : Field Report 2026-05-04 → 2026-05-08, Friction 4.

**Déjà partiellement notée** : entrée IDEAS du 2026-05-02 sur le même sujet. 
Cette entrée ré-itère et confirme par observation terrain.

**Phase d'examen suggérée** : Phase 7. Mitigation immédiate dispo.

**Statut** : 🟡 ouverte (déjà confirmée par usage)

---

### 2026-05-09 — Connexion native aux outils (Datadog, Splunk, AWS, kubectl)
**Idée** : Le framework actuel est 100% markdown — il ne peut pas exécuter de 
commandes ni récupérer de données depuis Datadog/Splunk/AWS/etc. L'utilisateur 
doit faire du copier-coller manuel. Sur des incidents complexes, ça limite la 
valeur ajoutée.

**Source** : Field Report 2026-05-04 → 2026-05-08, Friction 5 (partie 1).

**Approches possibles à explorer** :
- MCP servers (Anthropic Model Context Protocol) — natif Claude, à vérifier 
  côté Copilot/VSCode
- Extensions VSCode dédiées (Datadog VSCode, AWS Toolkit) — moins intégré 
  conceptuellement
- Skills techniques structurées qui guident l'utilisateur sur les commandes 
  à exécuter manuellement (intermédiaire)

**Risque** : altère la promesse VISION.md *« 100% markdown, pas de Python à 
coder »*. À mettre en balance avec la valeur ajoutée réelle.

**Phase d'examen suggérée** : Phase 8 (skills techniques) — déjà prévu.

**Statut** : 🟡 ouverte

---

### 2026-05-09 — Coût en tokens élevé (consequence dérivée de F2)
**Idée** : Le Field Report mentionne un coût tokens élevé. Diagnostic : 
conséquence directe de Friction 2 (Orchestrator ne délègue pas → réponses 
plus longues + demandes de confirmation à chaque étape qui multiplient les 
prompts).

**Décision** : pas de correctif dédié. Si Phase 5.7.A résout F2 correctement, 
le coût tokens devrait baisser mécaniquement. À revérifier au prochain Field 
Report (mesure : nb de tokens approximatif par session, vs avant 5.7.A).

**Si la baisse n'arrive pas** : creuser des optimisations spécifiques 
(seuil de confirmation explicite par défaut sur Y, batch handoffs entre 
personas, etc.).

**Source** : Field Report 2026-05-04 → 2026-05-08, Friction 6.

**Phase d'examen suggérée** : à reévaluer après Phase 5.7.A.

**Statut** : 🟡 ouverte (mesure post-5.7.A)

---

### 2026-05-09 — Insight unifiant : « règles posées mais pas appliquées avec discipline »
**Idée stratégique** (pas un correctif mais un principe directeur) : 
l'analyse des 3 frictions majeures (F1 drift, F2 délégation, F3 discipline 
production) révèle un fil conducteur :

> Le framework a des règles bien posées dans ses fichiers, mais elles ne 
> sont pas appliquées avec discipline systématique. Surtout quand le 
> contexte sature ou quand l'orchestrator est tenté d'improviser.

**Conséquence pour les futures phases** : tout nouveau correctif framework 
doit se demander *« cette règle est-elle vérifiable de manière binaire dans 
la sortie du framework ? Ou laisse-t-elle place à de l'improvisation ? »*. 
Privilégier les règles binaires.

**Application concrète Phase 5.7.A** : 
- Correctif 2.A (délégation obligatoire) → règle binaire : sortie a un 
  en-tête persona OU c'est un bug
- Correctif 3.A (table localisation) → règle binaire : path correspond à la 
  table OU c'est un bug

**À garder en tête pour Phase 6 (Party Mode)** : le risque d'improvisation 
augmente avec le nombre de personas en parallèle. Concevoir Phase 6 avec 
ce principe en tête dès le départ.

**Source** : Field Report 2026-05-04 → 2026-05-08, analyse globale (ADR-0004).

**Phase d'examen suggérée** : principe directeur, applicable à toutes les 
phases.

**Statut** : 🟢 principe acté (pas une idée à examiner)

## Format pour ajouter une nouvelle idée

```markdown
### YYYY-MM-DD — Titre court
**Idée** : ...
**Questions sous-jacentes** : ...
**Phase d'examen suggérée** : ...
**Statut** : 🟡 ouverte
```
---