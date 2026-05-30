# Parking lot — Idées et questions ouvertes

Ce fichier collecte les idées et questions qui débordent du focus actuel. **Rien ici n'est urgent.** On y reviendra à la phase appropriée selon la feuille de route.

---

## 📑 Sommaire

| Section | Contenu | Volume |
|---|---|---|
| [Format](#format) | Convention pour ajouter une nouvelle idée | référence |
| [En attente](#en-attente) | Idées 🟡 ouvertes à examiner aux phases prévues | 13 entrées |
| [Principes directeurs](#principes-directeurs) | 🟢 Méta-règles actées du framework | 2 entrées |
| [Archives — traitées](#archives--traitées) | 🟢 Idées appliquées via ADR ou correctifs | 7 entrées |

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

---

### 2026-05-09 — Mode /light officiel — 3 niveaux de workflow

**Idée** : Le framework actuel a un mode unique qui s'applique à toutes les 
demandes, peu importe leur complexité. Conséquence : les demandes simples 
("résume ce fichier", "vérification git", "petite question") sont traitées 
avec le même protocole complet (ANALYSE → PLAN → CONFIRM → EXECUTE → 
SYNTHESIS → CLOSE) que les incidents complexes.

**Source** : analyse Copilot "simulation 5 sessions" du 2026-05-09 — 
session 1 (demande simple) identifie un surcoût massif :
- Input de base : ~4 800 à 6 500 tokens
- Réponse utile réelle : ~300 à 600 tokens
- **Surcoût process : ~800 à 1 500 tokens pour respecter le rituel**

→ Pour une question simple, le framework consomme parfois plus de tokens 
à respecter son rituel qu'à répondre au besoin.

**Risque observé/anticipé** :
- L'utilisateur contourne l'Orchestrator et revient à l'Agent par défaut 
  pour les petites tâches
- Le framework devient perçu comme "bureaucratique"
- Perte d'adoption progressive sur les usages quotidiens légers

**Limite du mode `/quick` actuel** : 
- `/quick` saute uniquement la phase CONFIRM
- Ne définit pas clairement quand éviter le Scribe
- Ne définit pas quand utiliser un persona unique
- Ne définit pas quand ne produire AUCUN livrable
- C'est un raccourci, pas un vrai mode léger

**Proposition — 3 niveaux officiels de workflow** :

| Mode | Cas d'usage | Règles |
|---|---|---|
| `/light` | Question simple, vérification, conseil rapide | Persona unique, pas de Scribe sauf livrable Type A explicite, pas de PLAN détaillé, réponse courte, pas de création de fichier par défaut |
| `standard` (défaut) | Tâche normale (analyse, doc, refacto léger) | PLAN court, personas ciblés, Scribe si livrable durable utile |
| `/deep` | Incident, ADR, architecture, doc durable | Full workflow (Phase 5.7.A complet) |

**Critères de déclenchement à concevoir** :
- Auto-détection par l'orchestrator selon longueur/nature du prompt ?
- Activation explicite par drapeau `/light` `/deep` ?
- Heuristique mixte (auto par défaut + override possible) ?

**Impact estimé (selon analyse Copilot)** :
- Réduction de 30-50% du coût sur petites demandes
- Amélioration UX immédiate sur les questions courantes
- Moins de tentation d'abandonner l'Orchestrator pour l'Agent par défaut

**Distinction avec d'autres entrées IDEAS.md** :
- *Différent* de "Pas de fast-track / mode allégé" (2026-05-02) — cette 
  entrée précise comment, pas juste si
- *Différent* de "Orchestrator trop lourd" (2026-05-09) — celle-ci traite 
  la STRUCTURE du fichier, le mode /light traite la GRADUATION du protocole
- *Complémentaire* avec les correctifs Phase 5.7.A (2.A délégation, 2.B 
  PLAN→EXECUTION) — le mode /light n'annule pas ces règles, il les 
  contextualise selon la complexité

**Phase d'examen suggérée** : Phase 6 (Party Mode) — le mode /light est 
naturellement lié à la sélection contextuelle de personas que prévoit 
Phase 6. Mais à reconsidérer en Phase 5.7.B si l'usage réel post-5.7.A 
confirme que la lourdeur est le frein principal.

**Risque à surveiller** : si on introduit /light avant Party Mode, on crée 
peut-être 2 sélections contextuelles différentes (graduation par complexité 
+ sélection de personas). Risque de friction conceptuelle.

**Origine** : analyse Copilot simulation 5 sessions, session 1 (demande 
simple) — surcoût ~800-1 500 tokens identifié comme problème structurel 
non couvert par /quick actuel.

**Référence** : ADR-0004, Friction F2 (orchestrator ne délègue pas vs 
demande simple où c'est légitime), Friction F6 (coût tokens élevé).

**Statut** : 🟡 ouverte (priorité haute pour Phase 6, possible préemption en 5.7.B)

---

### 2026-05-30 — Règle thinking hybride — Low par défaut (RAISONNÉE, non instrumentée)

**Contexte** : la Phase 5.8 vise à réduire la consommation de contexte par tour
pour repousser le seuil de dégradation (~30K observé). Le thinking étendu (~9K
tokens/tour) est le levier dominant identifié. Question : quand l'activer ?

**Statut épistémique** : règle **raisonnée**, PAS validée empiriquement. Basée sur
une simulation introspective (`docs/2026-05-30-thinking-high-vs-low-eval.md`, dont
les chiffres sont des estimations non instrumentées explicitement étiquetées comme
telles) + un raisonnement de design sur l'asymétrie coût/bénéfice. À confirmer ou
infirmer par l'usage réel.

**Asymétrie fondatrice** : le coût du thinking est **constant** (~9K/tour, qu'il
serve ou non) ; son bénéfice est **conditionnel** à la nature de la tâche. La
politique optimale exploite cette asymétrie : ne payer le coût que quand le bénéfice
est probable.

---

#### RÈGLE (opérationnelle — à évaluer avant chaque tâche)

**Mode nominal : `Thinking Low`.**

**Bascule `High` si la tâche touche à :**
- (a) concurrence / atomicité
- (b) analyse de dump / heap / trace
- (c) flux financier ou intégrité transactionnelle

Évaluation binaire et instantanée : « est-ce que ça touche (a), (b) ou (c) ? » →
oui/non. Zéro délibération requise au moment du choix.

---

#### NOTE (rationale — à comprendre, PAS à évaluer en live)

Ces trois déclencheurs sont des **proxies observables** d'un critère plus profond :
*« la tâche a-t-elle une seule réponse correcte difficile à atteindre, où un chemin
plausible-mais-faux est coûteux ? »*

La liste existe **parce que ce critère est vrai mais non évaluable a priori** :
savoir si une tâche a une réponse unique demande souvent d'avoir déjà commencé à
raisonner. C'est un critère de post-mortem, pas de décision. Les proxies (a/b/c)
sont eux évaluables instantanément, avant de produire.

**Pas de clause « doute → High »** : le doute étant l'état par défaut en début de
tâche, une telle clause reviendrait à « High presque toujours » et annulerait la
politique Low-par-défaut. Rejetée explicitement.

---

#### Discipline d'enrichissement

La liste de déclencheurs est **incomplète par construction** et s'améliore par
apprentissage, pas par contournement :

> Si un cas hors liste se révèle **a posteriori** avoir mérité le High (un Low a
> produit un résultat faux qu'un High aurait évité), on **ajoute un déclencheur**
> à la liste, avec la raison documentée. La liste ne se contourne jamais par une
> clause floue — elle se complète par retour d'expérience.

---

#### Conséquence sur le mode `/light`

Le rapport de simulation suggère que `/light` est *« utile mais pas indispensable »* :
il change le débit (verbosité) mais pas la qualité technique. **Décision** : reporter
`/light`. Appliquer d'abord la règle thinking hybride seule, et observer si elle
suffit à restaurer une performance acceptable en session. Si oui → `/light` reste
au parking lot. Si non → réexaminer `/light` comme correctif complémentaire.

**Statut** : ✅ règle adoptée comme mode de travail, étiquetée raisonnée/non
instrumentée. Validation par usage réel en continu (discipline d'enrichissement).

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

**Idée originale** : 0 des 5 workflows ne référençaient les 3 checklists de Phase 3. Les checklists existaient mais n'étaient jamais invoquées par les workflows. Cause directe du drift identifié dans `test-notes.md` ("Solo difrt ou oublie de créer les artefacts de synthèse").

**Traitement** : Phase 5.3 — actions 1.a, 1.c, 1.e du prompt de correctifs. Branchement effectué :
- `incident-response.md` → référence `incident-triage.md` (phase 1)
- `code-analysis.md` → référence `security-review.md` (phase 4)
- `feature-development.md` → référence `pre-deploy.md` (phase 6)

**Validation** : Phase 5.4-bis — la checklist `incident-triage.md` a bien été mentionnée par l'orchestrator face à un prompt ambigu.

**Référence** : `docs/decisions/0002-audit-existant.md` + `docs/decisions/0003-test-mvp-frictions.md`

**Date de traitement** : 2026-05-02

**Statut** : 🟢 traitée

### 2026-05-10 — Cas A — Boucle infinie de clarification (THÉORIQUE)

**Idée** : Risque structurel projeté par analyse théorique (`field_report_2.md`,
section 5) : la règle `default-to-clarification` (correctif 3.C de 5.7.A) sans
seuil de sortie peut produire une boucle de clarifications successives où chaque
nouvelle réponse utilisateur introduit de nouvelles ambiguïtés. Une demande réelle
contient toujours des ambiguïtés résiduelles → un agent maximiseur de clarification
ne peut pas sortir de la boucle seul.

**Indicateur observable** : >2 cycles consécutifs ANALYSE→CONFIRM sans phase
EXECUTE atteinte. ~600–900 tokens brûlés par cycle.

**Origine** : 🔴 THÉORIQUE — projection mathématique, non confirmée empiriquement.

**Correctif théorique disponible** : `max_clarification_turns = 2` +
fallback `proceed-with-stated-assumptions`. Spécifié en ADR-0005 (Lot 1).

**Phase d'examen suggérée** : Phase 5.7.B (si activée par Field Report empirique).

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md` — Cas A.

**Statut** : 🟡 ouverte — conditionnelle à validation empirique.

---

### 2026-05-10 — Cas B — Amnésie graduelle du prompt système (THÉORIQUE)

**Idée** : Mécanisme projeté combinant attention diluée (poids relatif du système
prompt décroît mécaniquement de 100 % à ~25 % entre début et saturation contexte)
et biais de récence RoPE (tokens récents favorisés indépendamment de leur importance
sémantique). Conséquence projetée : non-respect progressif des règles binaires
après ~5 interactions complexes avec thinking étendu actif.

**Convergence avec l'observation empirique** : F2 ("Orchestrator ne délègue pas")
de l'ADR-0004 a été observé *principalement en sessions longues, jamais sur la
première interaction*. C'est la signature exacte de ce mécanisme.

**Implication critique** : les correctifs textuels de 5.7.A retardent le phénomène
sans le résoudre. Seuls des mécanismes structurels (re-grounding périodique,
kill-switch SNR) peuvent y résister.

**Origine** : 🔴 THÉORIQUE — explication mathématique d'une observation empirique
existante. Plausible mais non démontrée.

**Correctifs théoriques disponibles** : re-grounding périodique (Lot 2 ADR-0005)
et session kill-switch (Lot 1 ADR-0005).

**Phase d'examen suggérée** : Phase 5.7.B (si activée). Long terme : Phase 7
(mémoire persistante avec checkpoints).

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md` — Cas B.
Lien direct avec entrée existante "F4 — Mémoire/contexte fragiles" (2026-05-09).

**Statut** : 🟡 ouverte — conditionnelle à validation empirique post-5.7.A.

---

### 2026-05-10 — Cas C — Dégradation du rapport Signal/Bruit (THÉORIQUE)

**Idée** : Accumulation projetée de patterns protocole (ANALYSE/PLAN/CONFIRM/EXECUTE/
SYNTHESIS) en contexte qui biaise les prédictions vers la reproduction de patterns
formels au détriment du contenu substantiel. Aboutit à une "verbosité compensatoire" :
plus de tokens pour atteindre la même qualité perçue, accélérant la dégradation.

**Indicateurs observables** :
- Longueur des tables PLAN : 4–5 lignes (interaction 1) → 8–12 lignes redondantes (interaction 10)
- Ratio contenu/formatage EXECUTE : 70/30 → 35/65
- Densité recommandations actionables : ~4/page → ~1.5/page

**Convergence empirique** : F6 ("Coût tokens élevé") de l'ADR-0004 est cohérent avec
la verbosité compensatoire. La gravité observée du F6 sera un indicateur direct de
ce cas.

**Origine** : 🔴 THÉORIQUE — modélisation de l'in-context learning à rebours.

**Correctifs théoriques disponibles** : budget tracking explicite (Lot 2 ADR-0005)
et session kill-switch (Lot 1 ADR-0005).

**Phase d'examen suggérée** : Phase 5.7.B (si activée). Lien avec entrée existante
"F6 — Coût tokens élevé (à surveiller post-5.7.A)" (2026-05-09).

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md` — Cas C.

**Statut** : 🟡 ouverte — conditionnelle à validation empirique post-5.7.A.

---

### 2026-05-10 — Résilience 1 — max_clarification_turns (THÉORIQUE)

**Idée** : Seuil numérique anti-boucle de clarification. Au-delà de 2 cycles
ANALYSE→CONFIRM consécutifs, l'orchestrator passe automatiquement en mode
`proceed-with-stated-assumptions` (énonce ses hypothèses et avance avec).

**Spécification minimale** :
- Compteur de cycles clarification dans le contexte de session
- Seuil : `max_clarification_turns = 2` (configurable)
- Fallback : pattern textuel "Hypothèses retenues : [...]. Procédons. Si erronées, recale-moi."

**Origine** : 🔴 THÉORIQUE — issue de la note d'architecture, section 6.

**Phase d'examen suggérée** : Phase 5.7.B Lot 1 (si activée).

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md`.

**Statut** : 🟡 ouverte — conditionnelle.

---

### 2026-05-10 — Résilience 2 — Re-grounding périodique (THÉORIQUE)

**Idée** : Réinjection automatique des 5 règles binaires critiques (délégation
obligatoire, périmètre projet, PRE-FLIGHT, Pattern avouer l'échec, contrat
PLAN→EXECUTION) tous les 4–5 tours, pour contrer la dilution mécanique
d'attention sur le système prompt.

**Spécification minimale** :
- Nouveau fichier `agents/protocols/re-grounding.md` listant les 5 règles
- Trigger : compteur d'interactions modulo 4–5 OU détection seuil 70 % contexte
- Format de réinjection : bloc compact <= 200 tokens, pas une copie verbatim du système prompt

**Risque connexe** : si la réinjection est trop verbeuse, elle aggrave le SNR
au lieu de le corriger. Calibrage critique.

**Origine** : 🔴 THÉORIQUE — note d'architecture section 6.

**Phase d'examen suggérée** : Phase 5.7.B Lot 2 (si activée).

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md`.

**Statut** : 🟡 ouverte — conditionnelle.

---

### 2026-05-10 — Résilience 3 — Session kill-switch (SNR < 30 %) (THÉORIQUE)

**Idée** : Détection automatique d'effondrement qualitatif et proposition d'ouverture
nouvelle session. Si l'orchestrator estime le SNR sous 30 % (heuristique sur
verbosité compensatoire + ratio contenu/formatage), il propose explicitement à
l'utilisateur de fermer la session avec un session-summary et de redémarrer.

**Spécification minimale** :
- Heuristique d'estimation SNR (à concevoir, probablement basée sur ratio
  formatage/contenu sur les 3 dernières réponses)
- Message de proposition standardisé
- Chaînage automatique avec template `session-summary.md` (déjà créé en 5.7.A
  correctif 3.B)

**Bénéfice secondaire** : transforme la dégradation en signal explicite plutôt
qu'en frustration silencieuse.

**Origine** : 🔴 THÉORIQUE — note d'architecture section 6.

**Phase d'examen suggérée** : Phase 5.7.B Lot 1 (si activée).

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md`.

**Statut** : 🟡 ouverte — conditionnelle.

---

### 2026-05-10 — Résilience 4 — Budget tracking explicite (THÉORIQUE)

**Idée** : Affichage discret en début de chaque réponse Orchestrator du nombre
d'interactions restantes avant seuil 70 % contexte (ex: `Budget: ~7 interactions`).
Rend visible la dégradation projetée et invite à l'arbitrage utilisateur.

**Spécification minimale** :
- Estimation par interaction = ~9 375 tokens (avec thinking) ou ~2 500 tokens (sans)
- Calcul tour par tour, affichage minimal type `Budget: ~N tours`
- Seuil d'alerte visuelle à 3 tours restants

**Risque connexe** : ajouter de la métrique en surface peut détourner l'attention
de la tâche. À tester sur 2–3 sessions avant déploiement complet.

**Origine** : 🔴 THÉORIQUE — note d'architecture section 6.

**Phase d'examen suggérée** : Phase 5.7.B Lot 2 (si activée).

**Référence** : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md`.

### 2026-05-10 — Diagnostic performance sessions : overhead n'est PAS le levier (EMPIRIQUE)

**Contexte** : investigation déclenchée par observation empirique d'une dégradation
de performance (lenteur + baisse qualité) au-delà de ~30K tokens en session. Hypothèse
initiale : l'overhead de chargement de l'orchestrator était trop lourd. **Hypothèse
infirmée par la mesure.**

**Mesures empiriques réalisées** :

| Source | Tokens mesurés | % fenêtre 64K |
|---|---|---|
| `orchestrator.agent.md` | ~2 100–3 400 | ~4,5 % |
| `copilot-instructions.md` | ~650–970 | ~1,3 % |
| **Total overhead framework** | **~2 750–4 370** | **~6 %** |

**Confirmation empirique du lazy-loading** : l'orchestrator interrogé directement
liste seulement 3 fichiers chargés au démarrage (copilot-instructions, orchestrator,
git-workflow en mémoire non-lu). Les 9 personas, workflows, checklists, templates
ne sont PAS chargés — lus à la demande uniquement. **Le framework fait déjà du
lazy-loading natif. Les personas ne sont pas un problème de tokens.**

**Cause racine de la dégradation à 30K** : ce n'est pas l'overhead de démarrage
(~6 %, négligeable). C'est l'**accumulation par interaction** :
- Thinking étendu : ~9K tokens/tour (levier dominant)
- Verbosité protocole (en-têtes, tables PLAN, cérémonial) : ~1,5–3K/tour
- Historique cumulé : croissant

À ~9–12K/tour, le seuil 30K est atteint en 3–4 interactions. L'overhead initial
est une goutte d'eau à côté.

**Leviers réels par ordre d'impact** :
1. 🔴 **Désactiver thinking étendu pour tâches simples** — gratuit, immédiat, peut
   tripler le nombre d'interactions avant saturation
2. 🟠 Sessions courtes/fréquentes — déjà acté ADR-0004 F4
3. 🟠 Mode `/light` (réduction verbosité protocole) — récurrent, voir entrée dédiée
4. 🟡 Recyclage de contexte (compaction/checkpoint) — Phase 7, long terme
5. ⚪ Refactor overhead orchestrator — gain marginal (~2 interactions), propreté seulement

**Décision** : NE PAS refactorer l'orchestrator pour la performance (gain ~2
interactions pour une session de travail = mauvais ROI). Prioriser le réglage
thinking + explorer le mode `/light`.

**Garde-fou méta** : ce diagnostic a évité un refactor inutile. L'hypothèse la
plus visible (overhead) n'était pas la cause racine (accumulation par tour).

**Statut** : ✅ diagnostic clos, empirique. Action thinking testable immédiatement.
**Statut** : 🟡 ouverte — conditionnelle.
---
### 2026-05-10 — Diagnostic performance sessions : overhead n'est PAS le levier (EMPIRIQUE)

**Contexte** : investigation déclenchée par observation empirique d'une dégradation
de performance (lenteur + baisse qualité) au-delà de ~30K tokens en session. Hypothèse
initiale : l'overhead de chargement de l'orchestrator était trop lourd. **Hypothèse
infirmée par la mesure.**

**Mesures empiriques réalisées** :

| Source | Tokens mesurés | % fenêtre 64K |
|---|---|---|
| `orchestrator.agent.md` | ~2 100–3 400 | ~4,5 % |
| `copilot-instructions.md` | ~650–970 | ~1,3 % |
| **Total overhead framework** | **~2 750–4 370** | **~6 %** |

**Confirmation empirique du lazy-loading** : l'orchestrator interrogé directement
liste seulement 3 fichiers chargés au démarrage (copilot-instructions, orchestrator,
git-workflow en mémoire non-lu). Les 9 personas, workflows, checklists, templates
ne sont PAS chargés — lus à la demande uniquement. **Le framework fait déjà du
lazy-loading natif. Les personas ne sont pas un problème de tokens.**

**Cause racine de la dégradation à 30K** : ce n'est pas l'overhead de démarrage
(~6 %, négligeable). C'est l'**accumulation par interaction** :
- Thinking étendu : ~9K tokens/tour (levier dominant)
- Verbosité protocole (en-têtes, tables PLAN, cérémonial) : ~1,5–3K/tour
- Historique cumulé : croissant

À ~9–12K/tour, le seuil 30K est atteint en 3–4 interactions. L'overhead initial
est une goutte d'eau à côté.

**Leviers réels par ordre d'impact** :
1. 🔴 **Désactiver thinking étendu pour tâches simples** — gratuit, immédiat, peut
   tripler le nombre d'interactions avant saturation
2. 🟠 Sessions courtes/fréquentes — déjà acté ADR-0004 F4
3. 🟠 Mode `/light` (réduction verbosité protocole) — récurrent, voir entrée dédiée
4. 🟡 Recyclage de contexte (compaction/checkpoint) — Phase 7, long terme
5. ⚪ Refactor overhead orchestrator — gain marginal (~2 interactions), propreté seulement

**Décision** : NE PAS refactorer l'orchestrator pour la performance (gain ~2
interactions pour une session de travail = mauvais ROI). Prioriser le réglage
thinking + explorer le mode `/light`.

**Garde-fou méta** : ce diagnostic a évité un refactor inutile. L'hypothèse la
plus visible (overhead) n'était pas la cause racine (accumulation par tour).

**Statut** : ✅ diagnostic clos, empirique. Action thinking testable immédiatement.~~~~

