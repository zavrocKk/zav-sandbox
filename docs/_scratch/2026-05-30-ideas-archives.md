# IDEAS — Archives

> Idées appliquées via ADR ou correctifs framework. Déplacé depuis `IDEAS.md`
> le 2026-05-30 pour alléger le fichier actif. Valeur historique uniquement.

---

## Archives — traitées (🟢)

### 2026-05-02 — Pas de fast-track / mode allégé pour les workflows

**Idée originale** : pas de mode officiel pour alléger les workflows complets sur les demandes simples → risque de drift.

**Traitement** : Phase 6 — résolu par le **Panel** (Party Mode par défaut). Pas de mode allégé séparé : la sélection intelligente des agents convoque un seul persona sur une demande mono-domaine, l'équipe pertinente sur du multi-angles. La verbosité par tour relève de `/light` (Phase 5.8).

**Référence** : `docs/architecture/2026-05-30-party-mode-panel-vs-debate.md`, `agents/protocols/light-panel.md`

**Date de traitement** : 2026-05-30

**Statut** : 🟢 traitée

---

### 2026-05-02 — Brainstorming : workflow standalone ou phase ?

**Idée originale** : permettre une session de brainstorming structurée — workflow standalone ou phase amont ?

**Traitement** : Phase 6 — tranché. Le brainstorming est le moteur du **Débat** (`/debate`), surcouche du Panel, pas un workflow standalone. Livrable : note de délibération (`docs/decisions/` si ADR, sinon `docs/_scratch/YYYY-MM-DD-debate-<topic>.md`). Filtre 6 VISION respecté : le Débat se clôt toujours par une synthèse Scribe committée.

**Référence** : `agents/protocols/debate.md`, `.github/copilot-instructions.md` (table de localisation)

**Date de traitement** : 2026-05-30

**Statut** : 🟢 traitée

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

**Idée originale** : 0 des 5 workflows ne référençaient les 3 checklists de Phase 3. Les checklists existaient mais n'étaient jamais invoquées par les workflows. Cause directe du drift identifié dans `test-notes.md` ("Solo drift ou oublie de créer les artefacts de synthèse").

**Traitement** : Phase 5.3 — actions 1.a, 1.c, 1.e du prompt de correctifs. Branchement effectué :
- `incident-response.md` → référence `incident-triage.md` (phase 1)
- `code-analysis.md` → référence `security-review.md` (phase 4)
- `feature-development.md` → référence `pre-deploy.md` (phase 6)

**Validation** : Phase 5.4-bis — la checklist `incident-triage.md` a bien été mentionnée par l'orchestrator face à un prompt ambigu.

**Référence** : `docs/decisions/0002-audit-existant.md` + `docs/decisions/0003-test-mvp-frictions.md`

**Date de traitement** : 2026-05-02

**Statut** : 🟢 traitée

---

## Entrées conditionnelles ouvertes (🟡) — Phase 5.7.B

> Ces entrées étaient en "attente conditionnelle" à la validation empirique de
> Phase 5.7.B. Archivées ici pour alléger IDEAS.md actif.

### 2026-05-10 — Cas A — Boucle infinie de clarification (THÉORIQUE)

**Idée** : Risque structurel projeté : la règle `default-to-clarification` sans
seuil de sortie peut produire une boucle. Correctif théorique : `max_clarification_turns = 2`.

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md` — Cas A.

**Statut** : 🟡 ouverte — conditionnelle à validation empirique.

---

### 2026-05-10 — Cas B — Amnésie graduelle du prompt système (THÉORIQUE)

**Idée** : Dilution mécanique de l'attention sur le système prompt au fil des tours.
Correctifs : re-grounding périodique + session kill-switch.

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md` — Cas B.

**Statut** : 🟡 ouverte — conditionnelle.

---

### 2026-05-10 — Cas C — Dégradation du rapport Signal/Bruit (THÉORIQUE)

**Idée** : Verbosité compensatoire par accumulation de patterns protocole en contexte.
Correctifs : budget tracking + session kill-switch.

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md` — Cas C.

**Statut** : 🟡 ouverte — conditionnelle.

---

### 2026-05-10 — Résilience 1-4 (THÉORIQUES)

Quatre mécanismes de résilience spécifiés dans ADR-0005 :
1. `max_clarification_turns` (anti-boucle)
2. Re-grounding périodique
3. Session kill-switch (SNR < 30 %)
4. Budget tracking explicite

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md`.

**Statut** : 🟡 ouvertes — conditionnelles à Phase 5.7.B.

---

## Diagnostic empirique (✅ clos)

### 2026-05-10 — Overhead orchestrator n'est PAS le levier de performance (EMPIRIQUE)

**Résultat** : overhead mesuré = ~2 750–4 370 tokens (~6 % du budget). Le levier dominant
est le thinking étendu (~9K tokens/tour), pas l'orchestrator. Décision : ne pas
refactorer pour la performance — le refactoring ADR-0006 est justifié uniquement par
la maintenabilité (navigabilité contributeurs).

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md`.

**Statut** : ✅ diagnostic clos.
