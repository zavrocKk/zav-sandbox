---
type: decision
number: 0004
status: accepted
date: 2026-05-09
deciders: [zavrocKk]
tags: [field-report, phase-5-7, hardening, frictions]
supersedes: none
---

# ADR-0004 — Analyse Field Report (5 jours d'usage réel) et ouverture Phase 5.7

> Document d'analyse du premier Field Report de période réelle d'utilisation du framework Agentic Team, du 2026-05-04 au 2026-05-08. Identifie 6 frictions, retient 3 majeures pour traitement immédiat (Phase 5.7), reporte 3 vers phases ultérieures (7, 8). Ouvre formellement la Phase 5.7 — Hardening usage réel.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-05-09
**Décideurs** : utilisateur (zavrocKk)

## Contexte

À l'issue de la Phase 5.5 (clôture chapitre 5, MVP validé 8/8), le projet est entré dans une période d'**usage réel non-supervisé** sur le quotidien d'analyste technique, du 2026-05-04 au 2026-05-08 (5 jours).

Cette période visait à confirmer que les résultats obtenus sur le test synthétique Phase 5.4 (notification-api 5xx) se reproduisaient sur des cas réels, avant d'engager les phases ultérieures (Party Mode contextuel, mémoire persistante, skills techniques).

L'utilisateur a synthétisé ses 5 jours d'observations dans un Field Report unique (vs un par session, choix méthodologique validé) selon le template livré en Phase 5.5. Cet ADR-0004 analyse formellement ce Field Report.

## Méthode d'analyse

Lecture du Field Report → identification des frictions individuelles → questionnement ciblé pour décoder les patterns → classification par gravité → décision de traitement.

L'analyse a été menée en conversation avec Claude (claude.ai) avec questionnement progressif pour distinguer :
- Drift autonome vs interprétation extensive (Friction 1)
- Patterns de non-délégation vs heuristiques de seuil (Friction 2)
- Sous-frictions cachées dans une même observation (Friction 3)

## Verdict général Field Report

| Métrique | Valeur |
|---|---|
| Score qualitatif | **3/5** (ok) |
| Verdict ROI | **Gain confirmé** (~2x plus rapide vs manuel, qualité supérieure) |
| Frictions identifiées | **6** |
| Frictions critiques (action immédiate) | **3** (F1, F2, F3) |
| Frictions reportées | **3** (F4, F5 partiel, F6) |

**Lecture stratégique** : le framework livre de la valeur (ROI gain confirmé, qualité supérieure) mais souffre de **manque de discipline d'application** des règles existantes. L'usage réel a révélé 3 patterns que le test synthétique Phase 5.4 n'avait pas exposés.

## Frictions détaillées

### F1 — Drift hors-projet (initialement classée critique, reclassée majeure)

**Observation utilisateur** : *« Surprise mi-utile mi-rebelle : sorti du dossier projet pour piocher des skills d'un autre repo afin d'utiliser l'outil AWS, sans instruction. »*

**Diagnostic après questionnement** :
- L'utilisateur a mentionné un autre projet où ça marchait pendant la session
- Le framework a interprété cette mention comme un signal d'autorisation implicite
- Pas de drift autonome, mais **interprétation extensive** d'une mention utilisateur

**Cause racine identifiée** : aucun des 22 fichiers framework n'explicite que *« mentionner un autre projet ≠ autoriser son accès »*. Le périmètre projet n'est pas posé comme règle absolue.

**Gravité finale** : 🟠 majeure (pas critique car l'utilisateur a partiellement participé, mais nécessite un correctif de protection contre ce pattern).

### F2 — Orchestrator ne délègue pas

**Observation utilisateur** : *« Orchestrator reste lui-même au lieu de déléguer »*

**Diagnostic après questionnement** :
- Pattern (a) : réponse directe sans persona — observé
- Pattern (b) : PLAN listé mais pas exécuté — observé
- Pattern (c) : pas d'en-têtes visuels — rare, sessions longues
- Sur demandes complexes (b) ET demandes simples (d) — heuristique de seuil floue
- Conséquence : utilisateur redémarre la session (c) ou récupère un livrable dégradé (d)

**Cause racine identifiée** : pas de règle binaire et vérifiable du type *« toute réponse au fond technique DOIT avoir un en-tête persona »*. L'orchestrator improvise un seuil qui varie selon les sessions.

**Gravité finale** : 🟠 majeure — touche directement à la promesse VISION.md du framework (multiplicité des perspectives).

### F3 — Discipline de production absente

**Observation utilisateur** : *« artefacts placés n'importe où, aucun standard de template pour les bilans, exécute parfois un prompt ambigu sans demander clarification »*

**Diagnostic après questionnement** : 3 sous-frictions distinctes :
- **3-A** : artefacts mal placés (mélange de problèmes — sous-dossier, racine, scratch, naming)
- **3-B** : pas de template pour bilans de fin de session (vrai trou détecté)
- **3-C** : PRE-FLIGHT inconsistant, surtout sessions longues, supposition silencieuse au lieu de clarification

**Cause racine identifiée** : (a) référentiel de localisation éclaté entre 3 fichiers, (b) template manquant `session-summary.md`, (c) PRE-FLIGHT pas configuré en *default-to-clarification*.

**Gravité finale** : 🟠 majeure — touche à la fiabilité opérationnelle quotidienne.

### F4 — Mémoire/contexte fragiles, sessions longues

**Observation utilisateur** : *« sessions longues qui perdent le fil »*

**Diagnostic** : connu, déjà noté dans IDEAS.md (entrée 2026-05-02 « Mécanisme de session longue »).

**Décision** : 🟡 reporté — Phase 7 (mémoire persistante). Mitigation immédiate : sessions courtes 30-40 min max, ouvrir/fermer Copilot Chat plus souvent.

### F5 — Pas de connexion native aux outils + mauvais agent invoqué

**Observation utilisateur** : *« pas de connexion native aux outils, mauvais agent invoqué pour certaines tâches »*

**Diagnostic** : 2 problèmes en 1.
- Connexion outils → Phase 8 prévue (skills techniques + MCP)
- Mauvais agent → recouvre largement F2 (correctifs F2 traiteront indirectement)

**Décision** : 🟡 connexion outils → Phase 8. Mauvais agent → traité indirectement par correctifs F2.

### F6 — Coût en tokens élevé

**Observation utilisateur** : *« Orchestrator reste lui-même au lieu de déléguer, demandes de confirmation à chaque étape »*

**Diagnostic** : conséquence directe de F2. Si l'Orchestrator répond lui-même au lieu de déléguer, il génère plus de tokens. Si la délégation est correcte, le coût baisse.

**Décision** : 🟡 traité indirectement par correctifs F2.

## Insight unifiant

> **Le framework a des règles bien posées, mais elles ne sont pas appliquées avec discipline systématique. Surtout quand le contexte sature ou quand l'orchestrator est tenté d'improviser.**

Les 3 frictions majeures (F1, F2, F3) partagent toutes une **cause commune** : l'absence de mécanismes anti-improvisation explicites. Quand le contrat n'oblige pas formellement, l'orchestrator improvise — souvent dans le bon sens, parfois dans le mauvais.

## Décision

**Ouverture de la Phase 5.7 — Hardening usage réel** avec un objectif unique :

> Renforcer les contrats du framework pour éliminer les zones grises où l'orchestrator improvise, sans alourdir les cas où le framework fonctionne déjà bien.

**Découpage en 2 sous-phases** :

### Phase 5.7.A — Discipline & contrats (priorité HAUTE)

7 correctifs traitant les fondations structurelles :

| # | Correctif | Friction couverte |
|---|---|---|
| 1 | 1.A — Règle Périmètre projet | F1 |
| 2 | 1.B — Pattern Avouer l'échec | F1 |
| 3 | 2.A — Règle délégation obligatoire | F2 |
| 4 | 2.B — Contrat PLAN→EXECUTION | F2 |
| 5 | 3.A — Table de localisation centralisée | F3-A |
| 6 | 3.B — Création template session-summary.md | F3-B |
| 7 | 3.C — PRE-FLIGHT default-to-clarification | F3-C |

**Estimation** : 1h-1h30 dans VSCode + Copilot Chat avec Sonnet 4.6.

### Phase 5.7.B — Affinages & vigilance (priorité MOYENNE, conditionnel)

4 correctifs d'affinage, à appliquer **uniquement si les frictions persistent après 5.7.A** :

| # | Correctif | Friction couverte |
|---|---|---|
| 8 | 1.C — PRE-FLIGHT Q5 ressources externes | F1 |
| 9 | 2.C — Auto-check saturation | F2 |
| 10 | 2.D — Anti-bavardage Orchestrator | F2 |
| 11 | 3.D — Auto-check Scribe avant création | F3-A |

**Estimation** : 30-45 min.

**Déclenchement conditionnel** : 5.7.B est activée seulement si après période de test entre 5.7.A et 5.7.B, le Field Report intermédiaire montre que des frictions persistent. Sinon archivée.

## Conséquences

### Positives
- Renforcement de l'anti-drift par design (déjà revendiqué dans VISION.md, mais pas systématiquement appliqué)
- Création d'un template manquant identifié (`session-summary.md`)
- Single source of truth sur la localisation des artefacts
- Pattern « avouer l'échec » nouveau dans le framework (innovation interne)

### Négatives
- Charge de travail Phase 5.7 plus élevée que Phase 5.3 (11 correctifs potentiels vs 10+2)
- Complexification potentielle du contrat orchestrator (à surveiller)
- Phase 6 (Party Mode) reportée d'au moins 1-2 sessions

### Neutres
- Frictions F4, F5 (partiel), F6 reportées dans IDEAS.md — pas de surprise
- Méthodologie Field Report validée (rapport multi-sessions a bien fonctionné)

## Pré-requis pour exécution Phase 5.7.A

1. ✅ ADR-0004 produit (ce document)
2. Mise à jour IDEAS.md avec frictions reportées + insight unifiant
3. Mise à jour ROADMAP.md avec Phase 5.7 (et Phase 6 reportée)
4. Branche dédiée `feat/phase-5-7-A-hardening-discipline` créée à partir de main

## Critères de succès Phase 5.7

Validation par un nouveau Field Report 1-2 semaines après application Phase 5.7.A :

- ✅ Score qualitatif Field Report ≥ 4/5 (vs 3/5 actuel)
- ✅ Aucun drift hors-projet observé sur la période
- ✅ Délégation systématique observée (en-têtes persona présents)
- ✅ Discipline de production stable (artefacts au bon endroit, templates utilisés)

Si critères tous satisfaits → 5.7.B archivée, GO Phase 6.
Si critères partiellement satisfaits → 5.7.B activée avec correctifs ciblés.

## Implémentation

Application en 2 sessions VSCode + Copilot Chat selon `prompt-phase-5-7-A.md` (livré séparément).

Garde-fous d'exécution :
- Une étape à la fois, validation utilisateur entre chaque
- Pas de modif hors-périmètre des 7 correctifs listés
- Commits séparés par correctif (ou groupe cohérent : tous les correctifs F1 ensemble par exemple)
- Pas de `git push` automatique
- Aucun refactor inputs/outputs (reporté Phase 6.0)

## Méthode validée pour les futurs Field Reports

L'expérience de cet ADR-0004 valide une méthode reproductible :

1. **Field Report multi-sessions** (1 rapport par période, pas par session) — adapté TDAH
2. **Lecture en conversation** avec questionnement par friction
3. **Diagnostic en 3 niveaux** : symptôme observé → pattern technique → cause racine
4. **Classification par gravité** avec 3 niveaux (critique / majeure / moyenne / mineure)
5. **Correctifs proposés en groupes** (par friction, avec priorisation HAUTE/MOYENNE)
6. **Découpage en sous-phases** quand le pack de correctifs dépasse ~5 items
7. **Insight unifiant** recherché systématiquement entre frictions

À reproduire pour les Field Reports suivants.

## Références

- `VISION.md` — boussole stratégique
- `ROADMAP.md` — feuille de route, à mettre à jour avec Phase 5.7
- `IDEAS.md` — parking lot, à mettre à jour avec frictions reportées
- `docs/decisions/0002-audit-existant.md` — audit Phase 5.1
- `docs/decisions/0003-test-mvp-frictions.md` — clôture chapitre 5
- Field Report période 2026-05-04 → 2026-05-08 (transmis en chat, non versionné dans le repo par contrainte de confidentialité)

---

## Conclusion

La Phase 5.5 avait clos le chapitre 5 sur un MVP validé en lab. Le Field Report ouvre la Phase 5.7 sur un MVP qui doit **survivre à l'usage quotidien**.

C'est une étape attendue dans la maturation d'un framework. La période d'usage réel a révélé exactement le type de frictions qu'elle devait révéler — celles invisibles au test synthétique.

**Le projet entre désormais dans son sous-chapitre 5.7** : transformer un framework qui marche en lab en un framework qui résiste à l'usage quotidien réel.
