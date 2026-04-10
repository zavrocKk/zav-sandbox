---
name: prompt-engineering
description: "Structure un Delivery Contract, un brief agent, ou une requête composée pour maximiser la qualité de réponse."
applyTo: "**"
---

# Prompt Engineering — GSANE

## 1. Structure d'un Delivery Contract valide

Champs obligatoires : **TÂCHE**, **FICHIERS CIBLES**, **CONTRAINTES**, **CRITÈRES D'ACCEPTANCE**, **AGENT**.

Règle : pas de DC = pas de code. Amelia refuse toute implémentation sans DC signé par Langis.

### Bon DC

```
DC-20260410-001 | Amelia (Dev) | 2026-04-10

TÂCHE : Ajouter validation email dans src/notes_service.py

FICHIERS CIBLES :
- src/notes_service.py
- tests/test_notes_service.py

CONTRAINTES :
- Regex RFC 5322 simplifié
- Pas de dépendance externe

CRITÈRES D'ACCEPTANCE :
- AC-1 : notes_service.validate_email("bad") retourne False
- AC-2 : notes_service.validate_email("a@b.com") retourne True
- AC-3 : pytest tests/test_notes_service.py EXIT 0

AGENT PRINCIPAL : Amelia (Dev)
VALIDATION : Quinn (QA)
```

### Mauvais DC (trop vague)

```
TÂCHE : Améliorer le service de notes
CRITÈRES : Ça doit mieux fonctionner
```

Pourquoi mauvais : pas de fichiers cibles, pas de contraintes, AC non testable ("mieux" n'est pas mesurable).

## 2. Formuler les Critères d'Acceptance

Quinn valide par PASS/FAIL — chaque AC doit être vérifiable par une commande ou un assert.

**Format** : `action` + `résultat mesurable`

| Bon AC | Mauvais AC |
|--------|-----------|
| `pytest tests/test_X.py` EXIT 0 | "les tests passent" |
| Fichier `X.md` contient section `## Setup` | "documentation à jour" |
| `ruff check src/` retourne 0 erreur | "code propre" |
| Réponse API retourne HTTP 201 + body JSON avec `id` | "l'API fonctionne bien" |

## 3. Structurer une requête complexe

### Décomposition en sous-tâches

Numéroter chaque étape avec agent cible :
1. **Analyser** — lire fichiers X, Y (Master)
2. **Concevoir** — proposer architecture (Winston)
3. **Implémenter** — modifier fichier Z (Amelia)
4. **Valider** — exécuter tests + [CC] (Quinn)

### Quand party-mode vs exécution directe

| Signal | Mode |
|--------|------|
| 1 domaine, 1 agent, AC clairs | Exécution directe |
| 3+ domaines, choix d'architecture | Party mode |
| Mots-clés : "stratégie", "options", "alternatives" | Party mode |

### Signaux d'un mauvais brief

- Pas de verbe d'action en tête de tâche
- AC absent ou non mesurable
- Mélange analyse + implémentation dans un seul prompt
- Format de sortie non spécifié
