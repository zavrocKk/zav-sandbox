---
name: party-mode
description: "Trois phases : Huddle ciblé (validation) + Full brainstorming (exploration) + Planning (artefacts d'exécution). Gouvernance collective avant toute décision GSANE significative."
version: 3.0
phases:
  - huddle
  - brainstorm
  - planning
---

# Workflow : Party Mode

> Gouvernance collective à deux niveaux. Tout agent qui détecte un déclencheur DOIT activer le niveau approprié avant de procéder.

---

## NIVEAU 1 — HUDDLE CIBLÉ

### 1.1 Déclencheurs

Ce niveau s'active automatiquement si **l'une des conditions suivantes** est remplie :

- Sujet multi-domaine (`domains[]` >= 2 dans l'analyse PAE)
- Output contradictoire détecté entre deux agents
- Confiance JAUNE sur une décision à impact MEDIUM ou HIGH
- Tie dans le scoring de délégation (CAS B)
- Modification d'un fichier `_gsane/` non-triviale

---

### 1.2 Scoring des participants

```
POUR chaque agent dans agent-manifest.yaml:
  keyword_score  = nombre de keywords du topic qui matchent les triggers de l'agent (0-3 pts)
  domain_score   = nombre de domains[] du topic qui matchent les capabilities de l'agent (0-2 pts)
  independence   = +1 si l'agent n'est PAS le producteur initial de l'output à valider

  total = keyword_score + domain_score + independence

RETENIR : agents avec total >= 3, max 3 participants
  Si 0 agents >= 3      -> abaisser le seuil à >= 2
  Si toujours 0         -> retenir les 2 agents avec les scores les plus élevés (minimum 2)
```

---

### 1.3 Exécution du Huddle

> **Règle des Voters Actifs** : L'agent orchestrateur (celui qui a initié le Party Mode) NE VOTE PAS dans les sessions qu'il orchestre lui-même. Les voters actifs sont les agents NON orchestrateurs présents en session (maximum 4 : Winston, Amelia, Quinn, Bond). L'orchestrateur conserve son rôle de trancheur en cas de CONFLIT (voir 1.5).

```
1. Générer un HUDDLE BRIEF :
   topic:     {sujet du désaccord ou de la décision}
   context:   {fichiers concernés, outputs en conflit si applicable}
   question:  {question précise à trancher}
   time_box:  7 échanges maximum

2. Appeler runSubagent(agent, HUDDLE_BRIEF) pour chaque agent sélectionné — EN PARALLÈLE

3. Chaque agent retourne :
   position:   APPROVE | BLOCK | ABSTAIN
   rationale:  justification en 1-3 phrases
   suggestion: correction recommandée (si BLOCK)
```

---

### 1.4 Protocole de consensus

```
voters_actifs = agents présents en session MOINS l'orchestrateur
majorité = ceil(len(voters_actifs) / 2)
  ex: 4 voters → majorité = 2
  ex: 3 voters → majorité = 2
  ex: 2 voters → majorité = 1

APPROVE >= majorité  +  BLOCK = 0               -> consensus positif     -> procéder
APPROVE >= majorité  +  BLOCK = 1               -> consensus conditionnel -> appliquer suggestion du BLOCK
BLOCK >= 2                                       -> consensus négatif      -> STOP + présenter objections à l'utilisateur
APPROVE = 1,  BLOCK = 1,  ABSTAIN >= 1          -> CONFLIT                -> escalade orchestrateur (Step 1.5)
Tous ABSTAIN                                     -> escalade orchestrateur avec note "Huddle non concluant"

CAS SPÉCIAL — 1 seul voter actif :
  Le voter unique ne peut pas former de majorité à lui seul.
  -> escalation automatique vers l'orchestrateur qui statue directement
  -> l'orchestrateur documente sa décision dans le party-mode-audit.md
```

---

### 1.5 Escalade Orchestrateur (sur CONFLIT, ABSTAIN total ou voter unique)

```
1. Assembler le HUDDLE BRIEF + tous les votes détaillés
2. L'orchestrateur (celui qui a lancé le Party Mode) statue directement :
   - RESOLVE {décision} : la décision est forcée avec justification
   - ESCALATE_USER      : le conflit dépasse l'autorité interne -> présenter à l'utilisateur

NOTE ANTI-DEADLOCK : L'orchestrateur TRANCHE — il ne s'escalade jamais à lui-même.
Si l'orchestrateur estime ne pas avoir assez de contexte, il ESCALATE_USER.
Le pattern "Langis escalade vers Langis" est structurellement impossible.
```

---

### 1.6 Livrable obligatoire à la fermeture

Quel que soit le résultat, **appender** dans `_gsane-output/party-mode-audit.md` :

```markdown
## Huddle — {timestamp}
- Topic: {topic}
- Question: {question}
- Participants: {agent1} ({score}pts), {agent2} ({score}pts), ...
- Votes: APPROVE={n} | BLOCK={n} | ABSTAIN={n}
- Décision: {consensus positif / conditionnel / négatif / conflit}
- Recommandation: {texte si conditionnel ou conflit}
- Vote détaillé:
  - {agent}: {position} — {rationale}
```

> Si CONFLIT : escalader à Master avec ce même bloc + "Décision requise de l'utilisateur."

---

---

## NIVEAU 2 — FULL BRAINSTORMING

### 2.1 Déclencheurs

Ce niveau s'active si **l'une des conditions suivantes** est remplie :

- Mots-clés dans la requête : `stratégie | architecture | brainstorming | explorer | options | alternatives | conception | redesign`
- OU : `complexity = HIGH` (`domains[]` >= 3) ET requête multi-étapes

---

### 2.2 Dispatch simultané

```
1. Scorer TOUS les agents (même algorithme que 1.2 mais seuil = 0.4 sur score normalisé)
   normalisé = total / (3 + 2 + 1) = total / 6

2. Appeler runSubagent(agent, BRAINSTORM_BRIEF) pour tous les agents scorés >= 0.4 — EN PARALLÈLE

   BRAINSTORM_BRIEF = {
     topic: {sujet},
     angle: {angle spécifique de l'agent selon son domaine},
       Master   -> "Gouvernance et faisabilité opérationnelle",
       Winston  -> "Architecture et scalabilité",
       Amelia   -> "Implémentabilité et effort d'implémentation",
       Quinn    -> "Risques qualité et points de validation",
       Bond     -> "Cohérence avec le framework GSANE"
     question: "Donne ton évaluation depuis cet angle. Format: Avantages | Risques | Recommandation"
   }
```

---

### 2.3 Mécanisme Devil's Advocate

```
APRÈS collecte des outputs :
  Calculer le taux d'accord :
  taux = (agents_avec_recommandation_similaire) / (agents_total)

  SI taux >= 0.8 (consensus trop facile) :
    -> Désigner DEVIL'S ADVOCATE = agent avec le score le plus bas parmi les participants
    -> Le Devil's Advocate NE PEUT PAS être le producteur de l'output original
    -> Envoyer :
      "Le consensus est à {taux*100}%. Ta mission : trouver LA faille fatale
      dans cette approche. Sois impitoyable.
      Format: FAILLE | IMPACT | MITIGATION_POSSIBLE"
    -> Intégrer la faille dans le Round 1

  SINON :
    -> Passer directement à la synthèse (2.5)
```

---

### 2.4 Rounds de débat (max 2)

```
Round 1 (si Devil's Advocate utilisé) :
  - Partager la faille avec tous les participants
  - Chaque agent peut :
      AMEND    sa recommandation initiale
      MAINTAIN + réfuter la faille (justification obligatoire)

Round 2 (si désaccord majeur persiste après Round 1) :
  - Master présente un résumé neutre des positions
  - Chaque agent vote : ADOPT_FLAW | MITIGATE | DISMISS
  - Si toujours désaccord -> escalade utilisateur

APRÈS 2 rounds maximum :
  -> Passer à la synthèse (2.5) — JAMAIS de Round 3
```

---

### 2.5 Synthèse Master

```markdown
## Synthèse BRAINSTORM — {topic}

### Recommandation consolidée
[Résumé de la recommandation majoritaire en 2-4 phrases]

### Points d'accord (>= 60% des agents)
- ...

### Points de débat (< 60% accord)
- {point} : {position_A} (agents: ...) vs {position_B} (agents: ...)

### Faille Devil's Advocate (si applicable)
- Faille: ...
- Impact: ...
- Mitigation retenue: ...

### Décision finale recommandée
[1-2 phrases max]
```

**Documentation obligatoire** — appender dans `_gsane/_memory/decision-log.md` :

```
DL-{prochain_id} | {date} | {topic} | {décision} | {agents_consultés}
```

---

---

## PHASE 3 — Planning

### 3.0 Déclencheur

La Phase 3 s'active automatiquement si **l'une des conditions suivantes** est remplie :

- La décision finale (section 2.5) contient un **verbe d'action** : `créer | modifier | implémenter | refactorer | migrer | déployer | ajouter | supprimer`
- Un Huddle (Niveau 1) conclut sur une action avec impact **MEDIUM** ou **HIGH**

La Phase 3 est **optionnelle et ignorée** si le Niveau 1 résout un point trivial sans action structurante.

> ⚠️ `risk_level=HIGH` ne déclenche **pas** un nouveau Party Mode. Il impose une validation humaine ou le mode [THINK] avant exécution. Jamais de récursion Party Mode → plan → Party Mode.

---

### 3.1 Setup du chemin de session

```
DATE_ID    = format : {YYYY-MM-DD}-{HH-MM}
SESSION_DIR = _gsane-output/sessions/{DATE_ID}/

Créer si nécessaire :
  _gsane-output/sessions/{DATE_ID}/
  _gsane-output/sessions/{DATE_ID}/contracts/
```

---

### 3.2 Production des artefacts

Le Master produit **3 artefacts** dans `SESSION_DIR` :

```
1. brainstorm-brief.md
   Contenu : archive du sujet, contributions brutes des agents, contexte de consultation
   Format  : Markdown libre
   Accès   : jamais affiché par défaut — disponible sur demande explicite

2. design-conclusion.md
   Contenu : conclusion consolidée, décisions retenues, failles mitigées
   Format  : Markdown structuré, lisible par humain
   Accès   : disponible sur demande explicite

3. execution-plan.yaml
   Contenu : plan parseable par le Master pour exécution
   Format  : YAML — schéma obligatoire (voir _gsane/workflows/party-mode/templates/execution-plan.yaml)
   Accès   : parsé et consommé par le Master pour génération des Delivery Contracts
```

**Schéma `execution-plan.yaml`** (champs obligatoires) :

```yaml
plan_id:           "{date-id}-{slug}"
session_date:      "{YYYY-MM-DD}"
source_brief:      "sessions/{date-id}/brainstorm-brief.md"
source_conclusion: "sessions/{date-id}/design-conclusion.md"
objective:         "[objectif en 1 phrase]"
scope:             "[périmètre des fichiers et systèmes impactés]"
decisions:
  - id: D1
    decision:    "[décision retenue]"
    rationale:   "[justification]"
    source_agent: "[agent qui a proposé]"
tasks:
  - id: T1
    description:      "[livrable atomique]"
    owner:            "[agent principal]"
    depends_on:       []
    parallel_group:   "A"
    validation_agent: "[agent qui valide]"
    done_definition:  "[critère observable]"
    risk_level:       LOW | MEDIUM | HIGH
    acceptance_criteria:
      - "[critère 1]"
```

**Règles de qualité du plan** :

```
- Maximum 7 tâches par plan
- Une tâche = un owner principal
- Une tâche = un livrable vérifiable
- Pas de dépendance circulaire
- parallel_group identique = exécution parallèle possible
- risk_level=HIGH → arrêt avant dispatch automatique, validation humaine requise
```

---

### 3.3 Sortie haute-niveau utilisateur

> **Règle UX** : jamais de dump brut. Ne jamais afficher `brainstorm-brief.md`, `design-conclusion.md` ou le contenu complet de `execution-plan.yaml` sauf demande explicite.

Le Master présente **uniquement** la synthèse suivante :

```
Résumé proposé :

Décision : [résumé en 1-2 phrases]

Plan :
  {owner_1} : [travail]
  {owner_2} : [travail]
  ...

Parallélisme :
  Groupe A : [tâches]
  Groupe B : [tâches]

Risques :
  [1-3 points maximum — risk_level MEDIUM ou HIGH uniquement]

---
Est-ce que ce plan aligne bien ton intention initiale ?
▷ oui    → j'exécute
▷ ajuste → je corrige le plan avant exécution
```

---

### 3.4 Confirmation utilisateur

```
SI "oui" (ou équivalent) :
  → Passer à 3.5 — exécution des Delivery Contracts

SI "ajuste" (ou équivalent) :
  → Reprendre les points modifiés dans execution-plan.yaml
  → Re-présenter la synthèse haute-niveau (retourner à 3.3)
  → Ne jamais relancer Niveau 1 ou Niveau 2 pour un simple ajustement de plan

SI risk_level=HIGH présent dans le plan :
  → Afficher avant la question :
    "⚠️ Tâche(s) HIGH : {liste}. Validation humaine requise avant dispatch."
  → Ne jamais dispatcher automatiquement les tâches HIGH
```

---

### 3.5 Remise au Master pour exécution

```
Après confirmation utilisateur :

1. Fournir au Master le chemin : sessions/{date-id}/execution-plan.yaml
2. Master exécute l'enchaînement :
   a. Parser execution-plan.yaml
   b. Grouper les tâches par parallel_group
   c. Résoudre depends_on en ordre topologique (couches)
   d. Pour chaque tâche (hors HIGH non confirmées) :
      → Copier delivery-contract.tpl.md → sessions/{date-id}/contracts/dc-{task_id}.md
      → Remplir le frontmatter YAML (task_id, owner, validation_agent, risk_level,
        depends_on, parallel_group, done_definition)
      → Copier dc-{task_id}.md → _gsane-output/current-delivery-contract.md (contrat actif)
      → Dispatcher via runSubagent(owner, current-delivery-contract.md)
   e. Tâches du même parallel_group sans depends_on bloquant → dispatch simultané
   f. Attendre la fin d'un groupe avant de lancer le groupe dépendant suivant
   g. Quinn valide chaque livrable → CONTRACT ARCHIVING (règle master.md) s'applique
```

---

---

## Règles de gouvernance (les deux niveaux)

```
1. Chaque huddle ou brainstorming est tracé dans _gsane-output/party-mode-audit.md
2. Le Devil's Advocate ne peut pas être le producteur de l'output original
3. Timeout : si un agent ne répond pas -> ABSTAIN automatique (jamais bloquer le flux)
4. Un même topic ne peut pas déclencher plus de 2 rounds de débat
5. La décision finale appartient toujours à l'utilisateur si conflit persistant
6. Les deux niveaux peuvent être enchaînés : un Huddle peut upgrader vers un Brainstorming
   si le consensus révèle une complexité inattendue (domains[] remonte à >= 3)
```

---

## Matrice de sélection du niveau

| Condition détectée                        | Niveau déclenché           |
|-------------------------------------------|----------------------------|
| domains[] = 2, confiance JAUNE, tie       | Niveau 1 — Huddle ciblé    |
| Fichier `_gsane/` non-trivial modifié     | Niveau 1 — Huddle ciblé    |
| Mots-clés brainstorming dans la requête   | Niveau 2 — Full brainstorm |
| complexity = HIGH + requête multi-étapes  | Niveau 2 — Full brainstorm |
| Huddle révèle complexity >= 3             | Upgrade -> Niveau 2        |
| Conflit non résolu après Niveau 1         | Escalade utilisateur       |
| Décision contient un verbe d'action       | Phase 3 — Planning         |
| Huddle N1 → impact MEDIUM ou HIGH         | Phase 3 — Planning         |
| risk_level=HIGH dans le plan              | Validation humaine / THINK |
