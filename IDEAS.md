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

## Format pour ajouter une nouvelle idée

```markdown
### YYYY-MM-DD — Titre court
**Idée** : ...
**Questions sous-jacentes** : ...
**Phase d'examen suggérée** : ...
**Statut** : 🟡 ouverte
```
---