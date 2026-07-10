# Parking lot — Idées et questions ouvertes

Ce fichier collecte les idées et questions qui débordent du focus actuel. **Rien ici n'est urgent.** On y reviendra à la phase appropriée selon la feuille de route.

---

## 📑 Sommaire

| Section | Contenu | Volume |
|---|---|---|
| [Format](#format) | Convention pour ajouter une nouvelle idée | référence |
| [En attente](#en-attente) | Idées 🟡 ouvertes à examiner aux phases prévues | 13 entrées |
| [Principes directeurs](#principes-directeurs) | 🟢 Méta-règles actées du framework | 2 entrées |
| [Cas théoriques et résiliences](#cas-théoriques-et-résiliences--phase-57b-conditionnels) | 🟡 Projections théoriques non confirmées — Phase 5.7.B | 7 entrées |

**Convention d’hygiène** : quand un correctif est appliqué via un ADR, l’entrée IDEAS.md correspondante est **supprimée** de ce fichier — pas archivée. La traçabilité est assurée par l’ADR ou le doc de phase concerné. La règle s’applique au moment du commit du correctif, pas plus tard.

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

### 2026-05-02 — Cycle de vie des artefacts (cleanup post-session)

**Idée** : Comment faire le ménage des artefacts qui ne sont plus utiles après une session terminée ? Certains livrables (post-mortems, ADR, runbooks) doivent être conservés pour toujours. D'autres (notes de session, drafts, fichiers de scratch) sont temporaires et devraient être archivés ou supprimés.

**Questions sous-jacentes** :
- Distinguer "artefact pérenne" vs "artefact de session" dès la création ?
- Convention de nommage / dossier dédié pour le temporaire ?
- Politique de rétention (auto-clean après N jours ?) ?
- Le Scribe devrait-il proposer ce qui peut être archivé en fin de session ?

**Phase d'examen suggérée** : Phase 7 (mémoire persistante) — la distinction pérenne/éphémère et le cleanup automatique sont structurellement liés à la mémoire.

**Statut** : 🟡 ouverte — **partiellement traitée le 2026-07-09** : le volet
« retrouver » est livré (registre [`docs/index.md`](docs/index.md) + règle
d'index binaire dans copilot-instructions + règle de clôture des post-mortems :
action items cochés ou transférés, sinon `in-review`). **Reste** : politique de
purge/archivage de `_scratch/` — examen après la session 0 (H5 mesure
maintenant l'efficacité de l'index, plus l'existence du problème).

---

### 2026-05-02 — Dossier scratch / inputs temporaires

**Idée** : Où mettre les artefacts de travail temporaires que je donne à l'orchestrateur pour analyse (logs, configs, dumps, exports) ? Pas de dossier `inputs/` ou `scratch/` actuellement.

**Questions sous-jacentes** :
- Convention : `scratch/` à la racine ? `docs/_scratch/` ?
- Doit-il être dans `.gitignore` (probablement oui — ce sont des artefacts éphémères, parfois sensibles) ?
- L'orchestrateur doit-il être instruit de chercher là en priorité quand on dit "analyse ce log" ?
- Auto-cleanup après N jours ?

**Phase d'examen suggérée** : Phase 6.0 ou Phase 7 — partiellement traité par `docs/_scratch/` créé en Phase 5.5-bis, mais la convention complète reste à formaliser.

**Statut** : 🟡 ouverte (partiellement avancée)

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

### 2026-07-02 — security-guard : scanner le seul champ commande du payload (audit SEC-01)

**Idée** : `security-guard` (`.ps1`/`.sh`) matche ses patterns destructifs sur le **payload stdin entier** au lieu du seul champ commande → faux positifs quand l'agent édite un fichier dont le contenu cite `rm -rf`, `sudo`, `DROP TABLE`… (cas réel : `copilot-instructions.md`, le README des hooks). Correctif : parser le JSON du payload et ne scanner que le champ commande.

**Questions sous-jacentes** :
- Structure exacte du payload `PreToolUse` (API VS Code Preview) — quel chemin JSON pour la commande selon l'outil (`runInTerminal` vs autres) ?
- Le hook doit-il rester silencieux pour les outils sans champ commande (editFiles, readFile) ?
- Parsing JSON sans dépendance côté `.sh` (pas de `jq` — promesse dependency-free) ?

**Phase d'examen suggérée** : après revalidation de l'API hooks (le README impose déjà une revalidation à chaque mise à jour majeure VS Code/Copilot). La limite est documentée dans `agents/hooks/README.md` depuis l'audit 2026-07-02.

**Statut** : 🟡 ouverte

---

### 2026-07-02 — Dé-dupliquer les règles répétées (budget handoff ×5, playbook ×4) (audit TOK-01)

**Idée** : le budget handoff est défini en ≥ 5 endroits (module party-mode, chaque `.agent.md`, template `party-handoff.md`, skill party-mode, orchestrator) et le mode playbook en 4. Chaque copie porte une obligation de synchro manuelle → risque de drift. Piste : faire du template/module la source unique et remplacer les copies par des pointeurs.

**Questions sous-jacentes** :
- Un sous-agent en fenêtre fraîche suit-il fiablement un pointeur « voir template » au lieu d'un format inline ? (à valider en test terrain — risque de dégrader la conformité des handoffs)
- Tension avec le principe « ancre d'attention » (les règles critiques sont dupliquées exprès contre la dilution en session longue) — trancher copie par copie.
- Lien avec la rationalisation de `agents/templates/party-handoff.md` (aujourd'hui jamais référencé par un fichier agent) et des stubs `agents/personas/*` (maintenus pour le check CI de parité).

**Phase d'examen suggérée** : après le test terrain job (protocole du 2026-07-01) — on aura des observations réelles sur la conformité des handoffs.

**Statut** : 🟡 ouverte

---

### 2026-07-02 — `model:` par sous-agent (coût par persona) (audit TOK-02)

**Idée** : aucun frontmatter `.agent.md` ne fixe de modèle — tous les sous-agents (y compris le Scribe, purement rédactionnel) tournent sur le modèle par défaut. Si les custom agents VS Code supportent un champ `model:`, affecter un modèle plus léger aux personas rédactionnels réduirait le coût des sessions Party mode (sous-agents).

**Questions sous-jacentes** :
- Le champ `model:` est-il supporté (et stable) dans les custom agents VS Code Copilot ? (**NON VÉRIFIÉ** au 2026-07-02)
- Quels personas tolèrent un modèle plus léger sans perte de qualité (Scribe ? Product Analyst ?) ?

**Phase d'examen suggérée** : quand la dépense en premium requests devient un point de friction mesuré (télémétrie).

**Statut** : 🟡 ouverte

---

### 2026-07-02 — Tests automatisés des scripts de hooks (Pester / bats) (audit OBS-01)

**Idée** : les 8 scripts de `agents/hooks/` n'ont qu'une procédure de test **manuelle** (README). Un smoke test automatisé (Pester pour `.ps1`, bats pour `.sh`) en CI validerait : payload bénin → silence + exit 0, payload destructif → `ask`, parité `.ps1`/`.sh` sur un jeu de cas partagé.

**Questions sous-jacentes** :
- CI Windows (runner `windows-latest` pour pwsh) ou pwsh sur ubuntu suffit-il ?
- Tension avec la promesse « 100 % markdown, lisible par un non-dev » (filtre VISION) — les tests restent dans `scripts/` ou `agents/hooks/tests/` ?

**Phase d'examen suggérée** : à la prochaine évolution des hooks (l'audit 2026-07-02 a modifié les regex de `security-guard` — les cas de test existent déjà dans la procédure manuelle du README).

**Statut** : 🟡 ouverte

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

### 2026-07-07 — Workflow documentation (la doc comme objectif demandé)

**Idée** : Aucun workflow n'a la documentation comme **objectif de la demande** — le Scribe ferme
les cycles, mais « produis/rafraîchis un runbook », « documente ce système », « audite la doc
existante » n'ont pas de route dans le mapping. Constat de l'analyse du 2026-07-07 (même session
qu'ADR-0014) : c'est le 2ᵉ cas d'usage métier de l'utilisateur (bilans pour correctif **ou**
pour documentation).

**Questions sous-jacentes** :

- Un workflow dédié, ou des scénarios ad-hoc suffisent-ils (le runbook est déjà dans la table de localisation) ?
- Quelles phases : inventaire de la doc existante → gaps → production → validation par qui ?
- Chevauchement de routage avec `bilan-remediation` (un bilan peut viser la doc) — désambiguïsation à prévoir.

**Phase d'examen suggérée** : après le test terrain job (protocole 2026-07-01) — déclencheur : ≥ 2 sessions réelles de type documentation mal routées ou sans structure.

**Statut** : 🟡 ouverte

---

### 2026-07-07 — Traçabilité finding → ticket

**Idée** : Les findings des bilans/audits citent `fichier:ligne`, mais rien ne relie un finding
à un identifiant suivi (JIRA/SNOW) ni à son état de traitement — un finding sans état de
traitement est un finding perdu. Le front-matter du bilan (ADR-0014) trace le cycle du
**document**, pas celui des findings individuels.

**Questions sous-jacentes** :

- Un champ `ticket:` optionnel par finding dans le template `bilan.md` (référence textuelle pure, pas d'intégration) suffit-il ?
- Tension avec l'exclusion explicite des intégrations JIRA/ServiceNow/Confluence — rester markdown copiable tant qu'elle tient.
- La table de vérification (phase 6 du workflow) fait-elle déjà office d'état par finding ?

**Phase d'examen suggérée** : après le test terrain, conjointement avec le critère « besoin JIRA/SNOW ressenti à chaque session » du protocole §3 (chantier templates de sortie).

**Statut** : 🟡 ouverte

---

### 2026-07-07 — Migrer les règles binaires mécaniques vers des hooks

**Idée** : étage supérieur au principe « règles binaires > narratives » : *une règle dans un
prompt est probabiliste, un hook est déterministe*. Toute règle binaire **mécaniquement
vérifiable** qui drifte en session devrait migrer du markdown vers un script, le prompt
gardant le jugement. Candidats par ordre de valeur : (1) **gate handoff scripté** — chars et
sections des `.party/handoff-*.md`, la règle 4000 chars/plafond 1000 tokens est déjà
mécanique, l'orchestrateur la vérifie aujourd'hui « à l'œil » à chaque handoff ;
(2) **détecteur d'en-têtes persona manquants** au Stop (warn-only, comme secrets-scanner) —
vérifie la règle « sortie sans en-tête `───` = bug » ; (3) autres règles du preflight selon drift observé.

**Questions sous-jacentes** :

- L'API hooks VS Code (Stop) expose-t-elle assez de contexte pour scanner la dernière réponse ?
- Parité `.ps1`/`.sh` et tests automatisés — lien direct avec OBS-01.
- Quel seuil de drift observé justifie la migration d'une règle (≥ 2 violations en test terrain ?) ?

**Phase d'examen suggérée** : après le test terrain — prioriser selon les règles réellement violées en session réelle.

**Statut** : 🟡 ouverte

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

## Cas théoriques et résiliences — Phase 5.7.B (conditionnels)

> Ces entrées sont des projections théoriques de la note d'architecture Phase 5.7.B.
> Non confirmées empiriquement. À traiter uniquement si les cas sont observés en usage réel.
> Référence : `docs/decisions/0005-theoretical-analysis-phase-5-7-B.md`.

---

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

**Statut** : 🟡 ouverte — conditionnelle.
