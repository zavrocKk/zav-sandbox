---
name: party-mode
description: "Deux niveaux : Huddle ciblé (validation) + Full brainstorming (exploration). Gouvernance collective avant toute décision GSANE significative."
version: 2.0
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
APPROVE >= 2  +  BLOCK = 0               -> consensus positif     -> procéder
APPROVE >= 2  +  BLOCK = 1               -> consensus conditionnel -> appliquer suggestion du BLOCK
BLOCK >= 2                               -> consensus négatif      -> STOP + présenter objections à l'utilisateur
APPROVE = 1,  BLOCK = 1,  ABSTAIN >= 1  -> CONFLIT                -> escalade Master (Step 1.5)
Tous ABSTAIN                             -> escalade Master avec note "Huddle non concluant"
```

---

### 1.5 Escalade Master (sur CONFLIT ou ABSTAIN total)

```
1. Assembler le HUDDLE BRIEF + tous les votes détaillés
2. Appeler runSubagent(master, {huddle_brief + votes})
3. Master statue :
   - RESOLVE {décision} : la décision est forcée avec justification
   - ESCALATE_USER      : le conflit dépasse l'autorité interne -> présenter à l'utilisateur
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
