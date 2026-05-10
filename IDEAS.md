# Parking lot — Idées et questions ouvertes

Ce fichier collecte les idées et questions qui débordent du focus actuel. **Rien ici n'est urgent.** On y reviendra à la phase appropriée selon la feuille de route.

---

## 📑 Sommaire

| Section | Contenu | Volume |
|---|---|---|
| [Format](#format) | Convention pour ajouter une nouvelle idée | référence |
| [En attente](#en-attente) | Idées 🟡 ouvertes à examiner aux phases prévues | 13 entrées |
| [Principes directeurs](#principes-directeurs) | 🟢 Méta-règles actées du framework | 2 entrées |
| [Archives — traitées](#archives--traitées) | 🟢 Idées appliquées via ADR ou correctifs | 5 entrées |

**Convention d'hygiène** : quand un correctif est appliqué via un ADR, l'entrée IDEAS.md correspondante doit être passée en 🟢 traitée et déplacée vers la section Archives **au moment du commit du correctif** — pas plus tard.

---

## Format

Chaque entrée :

- **Date** : quand l'idée a émergé (YYYY-MM-DD)
- **Idée** : description brève
- **Questions sous-jacentes** : (optionnel) interrogations à explorer
- **Phase d'examen suggérée** : quand on devrait y revenir
- **Statut** : 🟡 ouverte / 🟢 traitée / 🟢 principe acté / 🔴 abandonnée

Format pour ajouter une nouvelle idée :

```markdown
### YYYY-MM-DD — Titre court
**Idée** : ...
**Questions sous-jacentes** : ...
**Phase d'examen suggérée** : ...
**Statut** : 🟡 ouverte
```

---

## En attente

### 2025-05-02 — Cycle de vie des artefacts (cleanup post-session)

**Idée** : Comment faire le ménage des artefacts qui ne sont plus utiles après une session terminée ? Certains livrables (post-mortems, ADR, runbooks) doivent être conservés pour toujours. D'autres (notes de session, drafts, fichiers de scratch) sont temporaires et devraient être archivés ou supprimés.

**Questions sous-jacentes** :
- Distinguer "artefact pérenne" vs "artefact de session" dès la création ?
- Convention de nommage / dossier dédié pour le temporaire ?
- Politique de rétention (auto-clean après N jours ?) ?
- Le Scribe devrait-il proposer ce qui peut être archivé en fin de session ?

**Phase d'examen suggérée** : Phase 7 (mémoire persistante) — la distinction pérenne/éphémère et le cleanup automatique sont structurellement liés à la mémoire.

**Statut** : 🟡 ouverte

---

### 2025-05-02 — Dossier scratch / inputs temporaires

**Idée** : Où mettre les artefacts de travail temporaires que je donne à l'orchestrateur pour analyse (logs, configs, dumps, exports) ? Pas de dossier `inputs/` ou `scratch/` actuellement.

**Questions sous-jacentes** :
- Convention : `scratch/` à la racine ? `docs/_scratch/` ?
- Doit-il être dans `.gitignore` (probablement oui — ce sont des artefacts éphémères, parfois sensibles) ?
- L'orchestrateur doit-il être instruit de chercher là en priorité quand on dit "analyse ce log" ?
- Auto-cleanup après N jours ?

**Phase d'examen suggérée** : Phase 6.0 ou Phase 7 — partiellement traité par `docs/_scratch/` créé en Phase 5.5-bis, mais la convention complète reste à formaliser.

**Statut** : 🟡 ouverte (partiellement avancée)

---

### 2025-05-02 — Personas "découvrables" même sans agent sélectionné

**Idée** : Observé pendant Phase 3 : Copilot en Agent par défaut a adopté le format "📝 Scribe" pour son bilan final, alors que l'orchestrator n'était pas sélectionné. Probablement parce qu'il a lu `agents/personas/scribe.md` via les outils `codebase`/`search` pendant l'exécution.

**Questions sous-jacentes** :
- Est-ce un comportement souhaitable (les personas sont "disponibles" partout) ou problématique (confusion entre "qui parle" — orchestrateur vs Agent par défaut) ?
- Doit-on limiter la découvrabilité des personas via instructions dans `copilot-instructions.md` ?
- Ou au contraire en profiter : transformer les personas en "skills" partagés que tout agent peut invoquer ?

**Phase d'examen suggérée** : Phase 8 (skills techniques) — c'est exactement la question qui se pose au moment de promouvoir un persona en skill.

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Sections "Différence avec X" à systématiser

**Idée** : 3 personas (`qa.md`, `product-analyst.md`, `data-engineer.md`) ont une section explicite "Différence avec...". C'est excellent pour éviter les chevauchements de périmètre. À propager pour les autres.

**Questions sous-jacentes** :
- DevOps vs Developer (debug applicatif vs debug infra) — utile ?
- Architect vs Developer (design vs implé) — utile ?
- Security vs DevOps (qui possède quoi en hardening infra ?) — utile ?

**Phase d'examen suggérée** : Phase 5.7.B (si activée) ou Phase 6 — pas critique pour le MVP.

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Pas de fast-track / mode allégé pour les workflows

**Idée** : Tous les workflows sont conçus pour le cas complet (5-7 phases). Un user qui a une demande simple va sauter des phases sans mode officiel pour le faire. Risque de drift.

**Questions sous-jacentes** :
- Concevoir un mode "allégé" (3-4 phases) pour les cas simples ?
- Ou utiliser le futur Party Mode (Phase 6) pour faire la sélection contextuelle qui évite les phases inutiles ?
- Comment l'orchestrator décide-t-il du mode (complet vs allégé) — signal explicite de l'utilisateur ? heuristique ?

**Phase d'examen suggérée** : Phase 6 (Party Mode) — c'est probablement la solution naturelle, pas un mode allégé séparé.

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Workflow problem-resolution (5 Pourquoi / Ishikawa)

**Idée** : Workflow pour traiter des problèmes complexes qui ne sont ni un incident urgent ni un audit de code localisé. Cas type : *« notre process de déploiement est lent et personne ne sait pourquoi »*.

**Différenciation avec l'existant** :
- vs `incident-response` : pas d'urgence, pas de prod down
- vs `code-analysis` : pas de module spécifique, problème transverse
- vs `architecture-design` : pas de choix techno, problème opérationnel

**Questions sous-jacentes** :
- Méthodologie de RCA : 5 Pourquoi (Toyota), Ishikawa/fishbone, ou les deux selon le type de problème ?
- Personas mobilisés : Product Analyst (cadrage) + variable selon nature (DevOps / Architect / Dev) + Scribe ?
- Risque de chevauchement avec les **skills méthodologiques** prévues en Phase 8 (5 Pourquoi, RCA, RACI). Faut-il faire le workflow OU les skills, pas les deux ?

**Phase d'examen suggérée** : Phase 6 ou Phase 8 — décision à trancher : workflow ou skill ?

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Brainstorming : workflow standalone ou phase ?

**Idée** : Permettre à l'orchestrator de mener une session de brainstorming structurée. Mais à arbitrer : workflow standalone OU phase initiale disponible dans plusieurs workflows existants ?

**Tension à résoudre** :
- Si workflow standalone → quel **livrable markdown** est produit ? (filtre 6 VISION : tout doit produire un livrable)
- Si phase amont → l'attacher à `feature-development.md`, `architecture-design.md`, `problem-resolution.md` (si retenu) ?

**Inspiration BMAD** : Carson (brainstorming-coach) au bureau est un agent dédié dans le module CIS. Mais on a dit : pas de copie BMAD. À reconcevoir proprement.

**Questions sous-jacentes** :
- Format livrable possible : `docs/brainstorming/YYYY-MM-DD-slug.md` avec sections "Question initiale / Idées générées / Clusters / Top 3 retenues / Next steps" ?
- Quand l'utilisateur veut un brainstorming pur, c'est pas pour produire un livrable, c'est pour explorer. Conflit avec le filtre 6 ?
- Pourrait-on en faire une **phase optionnelle** (drapeau `--with-brainstorm`) dans certains workflows ?

**Phase d'examen suggérée** : Phase 6 (lié au Party Mode — brainstorming est un cas idéal de multi-personas).

**Statut** : 🟡 ouverte

---

### 2026-05-02 — Pentest-remediation : skill plutôt que workflow ?

**Idée** : Workflow ou skill pour traiter les findings d'un pentest externe et appliquer les corrections priorisées.

**Pourquoi probablement skill plutôt que workflow** : un pentest-remediation est une **séquence préfabriquée** des workflows existants :
- `code-analysis` pour analyser les findings
- `security-review.md` (checklist) pour valider la couverture OWASP
- `feature-development` pour implémenter chaque correction
- `architecture-design` si la correction est structurante
- `incident-response` si une faille est exploitée en prod

→ Faire un workflow dédié reviendrait à dupliquer ce qui existe.

**Approche skill (préférée)** : créer une skill `pentest-remediation` activable dans n'importe quel workflow, qui apporte :
- Le format standard d'un pentest report (CVSS, CWE, exploitabilité)
- La méthodologie de priorisation (impact × exploitabilité × effort)
- Les patterns de correction par catégorie OWASP
- Les checks de non-régression à ajouter en CI

**Questions sous-jacentes** :
- Skill ou workflow ? **Décision préliminaire : skill.**
- Quel template de remediation report (`docs/security/pentest-NNN-remediation.md`) ?
- Comment relier au persona Security existant ?

**Phase d'examen suggérée** : Phase 8 (skills techniques) — c'est exactement le pattern d'usage prévu pour les skills.

**Statut** : 🟡 ouverte

---

### 2026-05-03 — Format de questionnement structuré (template ou tool)

**Idée** : Améliorer le format des questions PRE-FLIGHT pour réduire le risque de re-prompts incomplets. Deux pistes à investiguer :

**Piste A — Template markdown contraint** : tableau pré-formaté que l'utilisateur remplit ligne par ligne, validé par l'orchestrator avant de continuer.

**Piste B — Tool natif Copilot/VSCode** : le tool `askQuestions` **existe** dans GitHub Copilot Chat (confirmé utilisateur). À investiguer techniquement pour l'invoquer depuis un custom Orchestrator agent.

**Critère de déclenchement potentiel** : utiliser `askQuestions` quand le PRE-FLIGHT détecte ≥ 2 ambiguïtés à réponses fermées. Conserver le format markdown pour les questions ouvertes.

**Bénéfice attendu** : réduction du nombre de re-prompts. UX plus proche d'un formulaire que d'un chat libre.

**Risque** : couplage à VSCode (le framework devient moins portable vers d'autres clients Copilot ou autres LLMs). À mettre en balance avec la différenciation VISION : *"natif VSCode + GitHub Copilot"*.

**Phase d'examen suggérée** : Phase 6 (Party Mode) ou plus tôt si besoin se fait sentir lors d'un usage réel intensif.

**Statut** : 🟡 ouverte

---

### 2026-05-03 — Restructurer inputs vs outputs (séparation cycles de vie)

**Idée** : Distinguer 3 zones dans le repo selon le cycle de vie :
- `agents/` + `.github/` = code framework (versionné, stable)
- `inputs/` = matière fournie au framework par l'utilisateur (éphémère, potentiellement gitignored)
- `outputs/` = livrables produits par le framework (à conserver, potentiellement partageables)

**Bénéfices** :
- Clarté mentale : on sait toujours où chercher quoi
- Confidentialité : possibilité de gitignore les inputs sensibles
- Préparation pour Phases 7-8 : la mémoire persistante et les skills consomment/produisent dans des dossiers identifiés

**Coût de migration** :
- Renommage de tous les chemins dans personas, workflows, orchestrator, copilot-instructions
- Mise à jour des fichiers existants dans le repo

**Phase d'examen suggérée** : Phase 6.0 ou Phase 7 (mémoire persistante) — la migration sera structurellement nécessaire à ce moment, on la fait avec une vraie raison technique.

**Origine** : question utilisateur du 2026-05-03 — instinct juste mais pas urgent.

**Statut** : 🟡 ouverte

---

### 2026-05-09 — F4 — Mémoire/contexte fragiles (confirmée Field Report)

**Idée** : Le Field Report 2026-05-04→08 confirme concrètement la friction mémoire en usage réel : les sessions longues perdent le fil, l'orchestrator réexplique des choses déjà établies, la cohérence se dégrade après ~40 min.

**Mitigation immédiate appliquée** : sessions courtes 30-40 min max, ouvrir/fermer Copilot Chat plus souvent.

**Questions sous-jacentes** :
- Quel format de checkpoint minimal (artefact markdown, résumé structuré YAML ?) ?
- Quand déclencher un checkpoint (manuel ? automatique selon longueur ?) ?
- Le Scribe doit-il produire automatiquement un checkpoint en fin de session ?
- Comment reprendre proprement après un reset (relire le dernier checkpoint) ?
- Comment le rendre transparent pour l'utilisateur (pas de charge cognitive) ?

**Référence** : `docs/decisions/0004-field-report-analysis-phase-5-7.md` — Friction F4.

**Phase d'examen suggérée** : Phase 7 (mémoire persistante).

**Statut** : 🟡 ouverte (mitigation immédiate dispo, solution structurelle reportée)

---

### 2026-05-09 — F5 — Connexion native aux outils (MCP / APIs externes)

**Idée** : Le Field Report 2026-05-04→08 confirme que l'absence de connexion native aux outils génère des frictions de workflow : l'utilisateur doit copier-coller des résultats d'outils externes (AWS, Datadog, Splunk, kubectl…) au lieu que l'orchestrator les interroge directement.

**Approches possibles à explorer** :
- MCP servers (Anthropic Model Context Protocol) — natif Claude, à vérifier côté Copilot/VSCode
- Extensions VSCode dédiées (Datadog VSCode, AWS Toolkit) — moins intégré conceptuellement
- Skills techniques structurées qui guident l'utilisateur sur les commandes à exécuter manuellement (intermédiaire)

**Questions sous-jacentes** :
- Quels outils prioritaires pour la cible (analystes DevOps/SRE) ?
- MCP servers disponibles vs à créer ?
- Comment éviter que la connexion outils devienne une dépendance de setup complexe (principe : rien d'autre à installer que VSCode + Copilot) ?

**Risque** : altère la promesse VISION.md *« 100% markdown, pas de Python à coder »*. À mettre en balance avec la valeur ajoutée réelle.

**Référence** : `docs/decisions/0004-field-report-analysis-phase-5-7.md` — Friction F5.

**Phase d'examen suggérée** : Phase 8 (skills techniques + MCP).

**Statut** : 🟡 ouverte

---

### 2026-05-09 — F6 — Coût tokens élevé (à surveiller post-5.7.A)

**Idée** : Le Field Report 2026-05-04→08 note un coût en tokens perçu comme élevé. Diagnostic : conséquence directe de F2 (Orchestrator répond lui-même au lieu de déléguer → réponses plus longues + demandes de confirmation à chaque étape qui multiplient les prompts).

**Décision** : pas de correctif dédié pour l'instant. Si Phase 5.7.A résout F2 correctement (correctifs 2.A et 2.B), le coût tokens devrait baisser mécaniquement.

**Mesure proposée** : compter le nombre de tokens approximatif par session avant et après 5.7.A pour valider l'impact.

**Questions sous-jacentes** (si la friction persiste post-5.7.A) :
- Règle anti-bavardage Orchestrator (correctif 2.D dans 5.7.B) ?
- Heuristique de longueur de réponse par persona ?
- Peut-on quantifier le coût réel par workflow pour valider l'impact ?

**Référence** : `docs/decisions/0004-field-report-analysis-phase-5-7.md` — Friction F6.

**Phase d'examen suggérée** : réévaluation après Phase 5.7.A. Si persistant → Phase 5.7.B (correctif 2.D).

**Statut** : 🟡 ouverte (conditionnel — peut se fermer automatiquement post-5.7.A)

---

## Principes directeurs

> Méta-règles actées qui guident toutes les futures décisions du framework. Ne sont pas des idées à examiner, mais des principes à appliquer.

---

### 2026-05-09 — Insight unifiant : règles binaires > règles narratives

**Principe directeur** :

> Le framework a des règles bien posées dans ses fichiers, mais elles ne sont pas appliquées avec discipline systématique. Surtout quand le contexte sature ou quand l'orchestrator est tenté d'improviser.
>
> **Conséquence** : tout nouveau correctif framework doit se demander *« cette règle est-elle vérifiable de manière binaire dans la sortie du framework ? Ou laisse-t-elle place à de l'improvisation ? »*. Privilégier les règles binaires.

**Application concrète Phase 5.7.A** :
- Correctif 2.A (délégation obligatoire) → règle binaire : sortie a un en-tête persona OU c'est un bug
- Correctif 3.A (table localisation) → règle binaire : path correspond à la table OU c'est un bug

**À garder en tête pour Phase 6 (Party Mode)** : le risque d'improvisation augmente avec le nombre de personas en parallèle. Concevoir Phase 6 avec ce principe en tête dès le départ.

**À surveiller comme méta-critère** dans les futurs Field Reports :
- Les nouveaux correctifs ajoutent-ils des règles binaires ou narratives ?
- Le score d'improvisation observée diminue-t-il session après session ?

**Source** : Field Report 2026-05-04 → 2026-05-08, analyse globale (ADR-0004).

**Statut** : 🟢 principe acté

---

### 2026-05-09 — Confirmations proportionnelles au risque

**Principe directeur** :

> Le nombre de confirmations doit être proportionnel au risque de l'action, pas à la complexité de la séquence.

**Application concrète pour les futures phases** :

| Type d'action | Confirmation requise ? |
|---|---|
| Création nouveau fichier | ✅ Oui (geste créateur) |
| Modif fichier framework cœur (orchestrator, copilot-instructions) | ✅ Oui (impact systémique) |
| Petite modif syntaxe/typo | ❌ Non (négligeable) |
| Ajout section déjà discutée à la conception | ❌ Non (déjà validée) |
| Commit | ✅ Oui (mais peut être groupé par lot logique) |
| Passage entre correctifs d'un même lot | ❌ Non (juste enchaînement logique) |

**Approche recommandée pour les futurs prompts (5.7.B, 6, 7+)** : grouper les correctifs par **lots logiques** (ex: tous les correctifs d'une même friction = 1 lot = 1 confirmation), avec commits séparés à l'intérieur du lot.

**Anti-pattern à éviter** :
- Sur-confirmation = "validation fatigue" → l'utilisateur valide sans lire après quelques itérations
- Sous-confirmation = perte de contrôle sur les actions à risque

**Décision pour Phase 5.7.A** : on garde le cap actuel (7 confirmations) pour ne pas re-livrer le prompt. Principe appliqué à partir des futurs prompts.

**Origine** : observation utilisateur fin de session Phase 5.7 du 2026-05-09.

**Statut** : 🟢 principe acté

---

## Archives — traitées

> Idées qui ont été appliquées via un ADR ou un correctif framework. Conservées pour traçabilité historique.

---

### 2026-05-02 — Templates manquants pour runbook et architecture

**Idée originale** : 2 templates avoués manquants dans `orchestrator.agent.md` (mentionnés comme "pas encore de template — structure libre"). Sans template, le Scribe improvise → drift sur le format des livrables runbook et architecture.

**Traitement** : Phase 5.3 — actions 9 et 10 du prompt de correctifs.
- Création `agents/templates/runbook.md`
- Création `agents/templates/architecture.md`

**Référence** : `docs/decisions/0002-audit-existant.md`

**Date de traitement** : 2026-05-02

**Statut** : 🟢 traitée

---

### 2026-05-02 — Refactor orchestrator en protocoles externes (DRY)

**Idée originale** : `orchestrator.agent.md` (205 lignes) répétait plusieurs règles (PRE-FLIGHT, anti-drift, contrat Scribe, anti-patterns) à plusieurs endroits. Découper en `agents/protocols/*.md` chargés par référence pour réduire la duplication et la charge contexte.

**Traitement** : Phase 5.3 — action 3 du prompt de correctifs. Refactor effectué : externalisation de PRE-FLIGHT et du contrat Scribe.

**Référence** : `docs/decisions/0002-audit-existant.md`

**Date de traitement** : 2026-05-02

**Statut** : 🟢 traitée

---

### 2026-05-02 — Référence aux checklists incohérente entre personas

**Idée originale** : Seuls `devops.md` et `security.md` avaient une section "Checklists à consulter". Les 6 autres personas n'en avaient pas, alors que `pre-deploy.md` concerne aussi Developer/QA/Architect.

**Traitement** : Phase 5.3 — action 1.f du prompt de correctifs. Section "Checklists à consulter" ajoutée à Developer, QA, Architect.

**Référence** : `docs/decisions/0002-audit-existant.md`

**Date de traitement** : 2026-05-02

**Statut** : 🟢 traitée

---

### 2026-05-02 — Contrat Scribe à centraliser

**Idée originale** : Le contrat Scribe (Type A/B + procédure templates obligatoires + anti-pattern interdit) était éclaté entre `scribe.md` et `orchestrator.agent.md`. À unifier pour single source of truth.

**Traitement** : Phase 5.3 — action 2 du prompt de correctifs. Contrat Scribe centralisé dans `scribe.md`. Pointeur unique depuis `orchestrator.agent.md`.

**Référence** : `docs/decisions/0002-audit-existant.md`

**Date de traitement** : 2026-05-02

**Statut** : 🟢 traitée

---

### 2026-05-02 — Workflows orphelins de leurs checklists (CRITIQUE)

**Idée originale** : 0 des 5 workflows ne référençaient les 3 checklists de Phase 3. Les checklists existaient mais n'étaient jamais invoquées par les workflows. Cause directe du drift identifié dans `test-notes.md` ("Solo difrt ou oublie de créer les artefacts de synthèse").

**Traitement** : Phase 5.3 — actions 1.a, 1.c, 1.e du prompt de correctifs. Branchement effectué :
- `incident-response.md` → référence `incident-triage.md` (phase 1)
- `code-analysis.md` → référence `security-review.md` (phase 4)
- `feature-development.md` → référence `pre-deploy.md` (phase 6)

**Validation** : Phase 5.4-bis — la checklist `incident-triage.md` a bien été mentionnée par l'orchestrator face à un prompt ambigu.

**Référence** : `docs/decisions/0002-audit-existant.md` + `docs/decisions/0003-test-mvp-frictions.md`

**Date de traitement** : 2026-05-02

**Statut** : 🟢 traitée

### 2026-05-09 — Orchestrator.agent.md trop lourd (202+ lignes)

**Idée** : Le fichier orchestrator.agent.md fait actuellement 202+ lignes 
après Phase 5.7.A. Hypothèse utilisateur : ce volume excessif pourrait 
être une cause directe de Friction 2 (l'orchestrator ne délègue pas) et 
Friction 4 (mémoire/contexte fragiles sur sessions longues). À chaque 
interaction, l'orchestrator doit charger 200+ lignes de règles, ce qui 
sature son contexte plus vite et dégrade sa discipline d'application.

**Comparaison** :
- Personas individuels : 50-100 lignes
- Workflows : 40-60 lignes
- Templates : 30-90 lignes
- Orchestrator.agent.md : 202+ lignes ← anomalie

**Cible Phase 5.3 (non atteinte)** : ~80 lignes (frontmatter + flux + 
mapping + références aux protocoles externes).

**Pistes de correctif** :
- Externaliser les 5 nouvelles sections de Phase 5.7.A vers 
  agents/protocols/*.md (Périmètre projet, Délégation, PLAN→EXECUTION, 
  PRE-FLIGHT renforcé, Avouer l'échec)
- L'orchestrator devient une table d'orchestration + références
- Charge contextuelle réduite à chaque interaction

**Mesure proposée** : compter la dégradation de discipline observée 
sur sessions longues avant/après allègement.

**Phase d'examen suggérée** : Phase 5.7.B (si activée) ou Phase 5.7.C 
dédiée à l'allègement structurel. **À traiter AVANT Phase 6 (Party Mode)** 
car le Party Mode va probablement encore alourdir si on ne fait rien.

**Origine** : observation utilisateur fin de session 5.7.A (2026-05-09) 
— intuition forte sur la corrélation lourdeur ↔ frictions.

**Statut** : 🟡 ouverte (priorité haute pour Phase 5.7.B)

### 2026-05-09 — Orchestrator.agent.md trop lourd — cause structurelle de F2/F4

**Intuition utilisateur initiale** : `orchestrator.agent.md` à 202+ lignes 
après Phase 5.7.A pourrait être la cause directe des Frictions F2 
(orchestrator ne délègue pas) et F4 (mémoire/contexte fragiles sur 
sessions longues).

**Validation par analyse technique Copilot (2026-05-09)** :

#### Mesures de tokens

| Élément | Taille | Tokens estimés |
|---|---|---|
| `orchestrator.agent.md` | ~13 KB | ~3 700 tk |
| `copilot-instructions.md` | ~4 KB | ~1 100 tk |
| Sous-total system prompt | | ~4 800 tk |
| Personas (chargés à la demande) | ~1-2 KB | ~300-600 tk/persona |
| Historique session 30 min | variable | ~3 000-8 000 tk |
| **Total session typique** | | ~8 000-14 000 tk |
| **Session longue (60+ min)** | | ~18 000-30 000 tk |

#### Le vrai problème n'est pas le contexte absolu

Claude Sonnet 4.6 dispose de 200K de contexte — le plafond n'est PAS 
atteint. **Le vrai problème est la dilution d'attention** :
- Effet "lost in the middle" documenté pour les LLMs (le modèle prête 
  moins d'attention aux règles situées au milieu d'un long contexte)
- À chaque échange, tout le contexte est retokenisé → coût linéaire 
  croissant
- Sur sessions longues, les règles critiques sont "noyées" dans les 
  échanges récents

#### Problèmes structurels identifiés dans le fichier

**1. Redondance des anti-patterns (~400 tk dupliqués)** :
- `## ❌ Anti-pattern à NE JAMAIS faire` (liste générique)
- `## Anti-pattern — improvisation silencieuse` (commit 0ec984b)
- `## Pattern « Avouer l'échec »` (commit cda0500)

Les 3 sections traitent du même domaine sémantique (gestion de l'échec/
blocage) mais avec des angles différents. Redondance ≈ 15-20% du fichier.

**2. Hiérarchie d'attention défavorable** :
- `## Démarrage` est en ligne 149 (fin de fichier) → faible poids 
  d'attention (biais de récence inverse)
- `PRE-FLIGHT` en tête → bon
- Règles de délégation et de périmètre **au milieu** → zone d'attention 
  faible (effet lost in the middle)

**3. Formatage qui peut affecter le tokenizer** :
- Lignes vides manquantes avant certains `##` (déjà identifié et corrigé 
  partiellement dans cda0500 amendé)

#### Conflits observés ↔ causes identifiées

| Conflit observé en Field Report | Cause structurelle probable |
|---|---|
| Perte de règle en session longue (F4) | PRE-FLIGHT "loin" dans le contexte, éclipsé par les échanges récents |
| Supposition silencieuse (F3-C) | La règle default-to-clarification est "oubliée" après 30 min |
| Anti-patterns ignorés | Anti-patterns en fin de fichier, faible poids d'attention |
| Personas non incarnés (F2) | Règle de délégation au milieu du fichier, pas répétée |

#### Pistes de correctif Phase 5.7.B (réduction estimée ~25%, ~1 200 tk)

1. **Fusionner les 3 sections anti-pattern** en une seule (gain ~300-400 tk + cohérence)
2. **Remonter `## Démarrage` en début de fichier** après le frontmatter (règle de récence)
3. **Extraire le mapping workflow** dans un fichier séparé chargé à la demande (gain ~600 tk systématiques)
4. **Ajouter un "résumé des règles critiques"** de 5 lignes max en tête (ancre d'attention pour sessions longues)

**Risque à surveiller** : externaliser sans précaution pourrait créer un 
problème de chargement (l'orchestrator doit charger les fichiers externes 
au bon moment). À tester.

#### Mesure proposée pour valider

**Avant correctif (état actuel)** : compter sur 5 sessions longues 
(>30 min) post-5.7.A le nombre d'occurrences de :
- Réponses sans en-tête persona
- Suppositions silencieuses (réponse sans clarification sur prompt ambigu)
- Anti-patterns violés (création silencieuse de fichier, etc.)

**Après correctif** : même mesure. Si réduction significative → 
hypothèses validées.

#### Conseil stratégique

À traiter **AVANT Phase 6 (Party Mode)** parce que Party Mode = plusieurs 
personas en parallèle = encore plus de charge contexte cumulée. Si la 
lourdeur orchestrator n'est pas traitée avant, Party Mode risque 
d'amplifier les frictions au lieu de les résoudre.

#### Décision actuelle (Chemin A acté)

**Pas d'action immédiate.** L'utilisateur va d'abord tester Phase 5.7.A 
en usage réel sur 3-5 sessions, observer les frictions résiduelles, et 
décider de l'urgence de l'allègement en Phase 5.7.B sur données réelles.

**Phase d'examen suggérée** : Phase 5.7.B (priorité haute si frictions 
F2/F4 persistent).

**Origine** : intuition utilisateur (lourdeur ressentie) + analyse 
technique Copilot (mesures et biais d'attention) — convergence des deux 
diagnostics, 2026-05-09.

**Référence** : ADR-0004 (Frictions F2 et F4).

**Statut** : 🟡 ouverte (priorité haute, à traiter avant Phase 6 si confirmé en test usage réel)