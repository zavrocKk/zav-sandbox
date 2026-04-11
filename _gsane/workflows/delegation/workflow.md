---
name: delegation-workflow
description: "Routage intelligent des requêtes : extraction intent → scoring agents → routing → brief → audit"
version: 3.0
author: "Bond (Agent Builder)"
---

# Workflow de Délégation GSANE v3.0

> **RÈGLE FONDAMENTALE** : Ce workflow est la seule voie d'entrée vers tout agent Strike Team.
> Jamais de bypass. Jamais d'auto-exécution. Toujours tracer.
> Toute délégation directe sans brief structuré = violation immédiate.

> **IDENTITÉ LANGIS** : Langis est un orchestrateur pur.
> Il produit des Delivery Contracts. Il ne produit PAS de code, de tests, de configurations, ni d'artefacts techniques.
> 
> **Exceptions autorisées** (Langis peut agir seul) :
> - Répondre à une question d'analyse (pas d'artefact fichier produit)
> - Produire ou mettre à jour un Delivery Contract (c'est son artefact propre)
> - Lancer un workflow de délégation (pas de fichier modifié)
> - Mettre à jour sa mémoire sidecar (`_gsane/_memory/`)

---

## STEP 1 — Extraction intent & domaines

**Objectif** : Décomposer la requête entrante en signal actionnable et structuré.

```
INPUT: {user_request}

EXTRACT:
  primary_intent   : verbe_principal + objet
                     ex: "implémenter API REST" → primary_intent = "implémenter API"

  secondary_intents: liste d'intentions secondaires détectées
                     ex: ["ajouter tests TDD", "documenter endpoint"]

  domains[]        : chaque domaine détecté parmi:
                     [code, architecture, test, agent_design, workflow, gouvernance, brainstorming]
                     RÈGLE: un domaine est retenu si ≥ 1 keyword le désigne explicitement

  keywords[]       : mots significatifs normalisés
                     - lowercase
                     - sans stopwords (le, la, de, à, est, une, des, du, et, ou, je, tu...)
                     - conserver verbes d'action, noms techniques, acronymes

  complexity       : LOW    (1 domaine détecté)
                     MEDIUM (2 domaines détectés)
                     HIGH   (3+ domaines détectés)

OUTPUT: {primary_intent}, {secondary_intents}, {domains[]}, {keywords[]}, {complexity}
```

**Exemple complet** :
- Requête : "Ajoute un agent de monitoring avec tests et enregistre la décision"
- `primary_intent` → `ajouter agent`
- `secondary_intents` → `["ajouter tests", "enregistrer décision"]`
- `domains[]` → `[agent_design, test, gouvernance]`
- `keywords[]` → `[ajouter, agent, monitoring, tests, enregistrer, décision]`
- `complexity` → `HIGH`

---

## STEP 2 — Scoring via delegation-matrix.yaml

**Objectif** : Identifier l'agent le plus qualifié via correspondance pondérée + historique de confiance.

```
SOURCE: _gsane/_config/delegation-matrix.yaml
SOURCE TRUST: _gsane-output/delegation-audit.md

POUR chaque agent dans delegation-matrix.yaml:

  score = COUNT( keywords[] ∩ agent.trigger_keywords )

  trust_bonus:
    Lire delegation-audit.md
    SI cet agent a ≥ 1 entrée avec même domaine que {domains[0]} ET verdict = ✅ SUCCESS:
      trust_bonus = +1
    SINON:
      trust_bonus = 0

  final_score = score + trust_bonus

RETENIR:
  max_score   = MAX(final_scores de tous agents)
  winners[]   = [agents où final_score == max_score]
```

**Table de lecture du score** :

| final_score | Signal                                        |
|-------------|-----------------------------------------------|
| 0           | Aucun match — ambiguïté totale                |
| 1           | Match faible — potentiellement concerné       |
| 2+          | Match fort — agent prioritaire                |
| +1 bonus    | Confiance historique confirmée sur ce domaine |

---

## STEP 3 — Cas de routing

**Objectif** : Choisir le chemin d'exécution selon le résultat du scoring.

### CAS A — Agent dominant (1 agent avec score strictement supérieur)

```
IF len(winners[]) == 1:
  → Générer le brief structuré (STEP 4)
  → Appeler runSubagent(agent_name, brief)
  → Logger dans delegation-audit.md (STEP 5)
```

### CAS B — Tie (2+ agents avec même score max ≥ 1)

```
IF len(winners[]) > 1 AND max_score >= 1:
  → Déclencher HUDDLE ciblé
  → Charger _gsane/workflows/party-mode/workflow.md niveau 1
  → Passer en contexte: {agents_en_tie[], user_request, primary_intent}
  → NE PAS router individuellement avant résolution du HUDDLE
```

### CAS C — Score nul (aucun agent ≥ 1 keyword)

```
IF max_score == 0:
  → NE PAS router
  → Formuler UNE question de clarification ciblée:

    Format imposé:
    "Je n'ai pas pu identifier le domaine avec certitude. S'agit-il de :
     - [Option A : description courte] → routé vers [Agent A]
     - [Option B : description courte] → routé vers [Agent B]"

  → Attendre réponse utilisateur
  → Re-déclencher STEP 1 avec requête enrichie + réponse reçue
  → JAMAIS router sur une ambiguïté non résolue
```

### GARDE-FOU OUTPUT — Tâches produisant des fichiers

```
AVANT toute exécution (CAS A, B, ou C résolu):

IF la tâche produit ou modifie ≥ 1 fichier (code, test, config, agent, workflow):
  → L'agent routé NE PEUT PAS être master
  → Si scoring a routé vers master ET la tâche produit un fichier:
    → Re-scorer en excluant master
    → Router vers l'agent avec le score le plus élevé restant
    → Si aucun agent restant ≥ 1: demander clarification (CAS C)
```

---

## STEP 4 — Brief structuré

**Objectif** : Formaliser la délégation de façon claire et traçable avant toute exécution.

Chaque délégation produit ce brief au format YAML :

```yaml
brief:
  objective: "description claire en 1 phrase de ce qui est demandé"
  context: "contexte projet pertinent (branch, dernière décision, fichiers concernés)"
  constraints:
    - "contraintes techniques ou de gouvernance applicables"
    - "ex: respecter la structure frontmatter GSANE v3"
  expected_output: "ce que l'agent doit livrer exactement (fichier, format, critères)"
  cross_validate_with: "agent secondaire qui doit valider (selon mapping expertise ci-dessous)"
  trust_score_target: 70
```

### Mapping `cross_validate_with`

| Type de livrable                | Validateur(s) obligatoire(s)       |
|---------------------------------|------------------------------------|
| Code modifié (`src/`, `tests/`) | Quinn (QA)                         |
| Architecture système            | Quinn + Winston (croisé)           |
| Fichier `agents/*.md`           | Bond                               |
| Workflow (`workflows/*.md`)     | Master + Quinn                     |
| Décision haute sévérité         | Tous les agents concernés          |
| Fichier de config manifest      | Bond + Master                      |

**Règles de génération du brief** :
- Sans brief valide → l'agent NE PEUT PAS s'exécuter
- Le brief est passé directement à `runSubagent` comme contexte d'entrée
- Si `cross_validate_with` est vide → violation governance (toujours croiser)

---

## STEP 4b — CHALLENGE ROUTING

**Objectif** : Router les challenges P2P en priorité, hors du flux normal de délégation.

Quand un agent émet `[CHALLENGE]` :

1. Le challenge **bypass le routing normal** (STEP 1-3 ne s'appliquent pas)
2. Langis le reçoit **en priorité** sur toute tâche en cours
3. **Validation de forme** : vérifier que source, cible et argument technique sont présents
   - Si argument vague ou manquant → rejeter : "CHALLENGE invalide — argument insuffisant"
4. **Notification** : transmettre le challenge complet à l'agent cible
5. **Délai de réponse** : 1 échange (pas de silence autorisé — l'agent cible DOIT répondre)
6. **Résolution** :
   - Consensus → logger et continuer
   - Pas de consensus → Langis arbitre (décision FINALE)
7. **Logging obligatoire** : `gsane_emit_event('challenge_resolved', ...)` dans trace.log

---

## STEP 5 — Exécution & Audit

**Objectif** : Lancer le subagent, récupérer l'output, calculer le trust_score, tracer tout.

```
EXÉCUTION:
  1. Appeler runSubagent(agent_name, brief)
  2. Attendre OUTPUT du subagent (livrables + statut)
  3. Faire valider par cross_validate_with agent (brief.cross_validate_with)

CALCULER trust_score de l'output (0-100):
  factual_accuracy    (0-25): les faits cités existent dans les fichiers du projet
  logical_coherence   (0-25): les étapes sont logiquement enchaînées
  constraint_alignment(0-25): les règles GSANE ont été respectées
  feasibility         (0-25): la solution est implémentable immédiatement

  trust_score = somme des 4 composantes

APPENDER à _gsane-output/delegation-audit.md:

  Format header (si fichier nouveau ou vide):
  | timestamp | agent | task_id | intent | verdict | trust_score |
  |-----------|-------|---------|--------|---------|-------------|

  Format ligne:
  | {timestamp ISO 8601} | {agent_name} | {task_id} | {primary_intent} | {verdict} | {trust_score} |

  Valeurs verdict:
    ✅ SUCCESS  — output validé par cross_validate_with agent
    ❌ FAIL     — output rejeté ou critères non remplis

SI verdict = ❌ FAIL:
  → Logger aussi dans _gsane/_memory/failure-museum.md
  → Escalader vers Langis (Master)
  → NE PAS relancer silencieusement plus de 1 fois

SI delegation-audit.md > 200 entrées:
  → Archiver dans _gsane-output/delegation-audit-archive-{YYYYMMDD}.md
  → Réinitialiser _gsane-output/delegation-audit.md avec header uniquement
```

**Exemple de lignes d'audit** :

```
| timestamp | agent | task_id | intent | verdict | trust_score |
|-----------|-------|---------|--------|---------|-------------|
| 2026-04-04T14:32:00Z | Amelia (Dev) | A-20260404-001 | implémenter API REST | ✅ SUCCESS | 87 |
| 2026-04-04T15:10:00Z | Bond         | B-20260404-002 | créer agent monitoring | ❌ FAIL  | 42 |
```

---

## Règles de gouvernance

```
1. Ce workflow ne peut pas être bypassé.
   Toute délégation directe sans brief structuré = violation.

2. Si un agent est inconnu dans agent-manifest.yaml:
   → STOP immédiat
   → Retourner erreur: "Agent '{name}' introuvable dans agent-manifest.yaml — routing impossible."
   → NE PAS tenter d'exécuter

3. Audit obligatoire même pour les délégations qui échouent.
   Un FAIL non logué est une violation autant qu'un bypass.

4. Si delegation-audit.md dépasse 200 entrées:
   → Archiver avant toute nouvelle entrée
   → Le fichier actif doit toujours rester lisible

5. agents_can_self_execute = false (défini dans _gsane/config.yaml)
   Aucun agent ne peut déclencher une autre délégation sans repasser par ce workflow.

6. Ambiguïté → 1 seule question, 2 options max, jamais plus.
   Ne jamais router sur hypothèse non confirmée.
```

---

## Référence rapide — Flux global

```
{user_request}
      │
      ▼
[STEP 1] Extraction intent & domaines
      │
      ▼
[STEP 2] Scoring agents (delegation-matrix + trust bonus)
      │
      ├─ score MAX == 0 ────────────────────► [CAS C] Clarification → retour STEP 1
      │
      ├─ 1 winner ─────────────────────────► [CAS A] Brief → runSubagent → Audit
      │
      └─ tie (2+ winners, score ≥ 1) ──────► [CAS B] HUDDLE party-mode niveau 1
                                                          │
                                                          ▼
                                             Brief → runSubagent → Audit
```

> **Source de vérité** : `_gsane/config.yaml` → `delegation.enforcement_mode: strict`
> Toute violation est loguée dans `_gsane/_memory/failure-museum.md` et remontée au Master.
