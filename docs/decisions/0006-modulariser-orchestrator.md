---
type: adr
number: "0006"
status: accepted
date: 2026-05-30
deciders: [Zav]
tags: [orchestrator, architecture, performance, context-window]
---

# ADR-0006 — Modulariser orchestrator.agent.md avant ouverture publique

> Format Michael Nygard. Décision unique, immuable une fois `accepted`.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-05-30
**Décideurs** : Zav
**Supersedes** : —
**Contexte source** : Audit exhaustif v0.1.4 (Pilier 1.2 + Pilier 4.3)
**Résultat réel** : 310 → 234 lignes (−24 %). Cible de 180 lignes était aspirationnelle — les règles opérationnelles core restantes (délégation, contrat PLAN, saturation) sont non-compressibles sans perte de robustesse.

---

## Contexte

L'audit v0.1.4 identifie `orchestrator.agent.md` comme le fichier le plus critique du framework — et le plus monolithique (310 lignes). Il combine en un seul bloc :

- Règles de comportement général (PRE-FLIGHT, règles critiques, délégation)
- Mécanique **Party Mode** (Panel + Débat)
- Mécanique **Skills** (progressive disclosure, chargement scopé)
- Mécanique **Mémoire persistante** (checkpoints inter-sessions)
- Mapping demande → workflow → personas
- Commandes spéciales

**Problème observé :** toutes ces sections sont injectées en contexte à chaque session, même pour une demande triviale à un seul persona (ex. « relis ce fichier config »). Le poids mesuré de l'orchestrator est de ~2 100–3 400 tokens (ADR-0005), ce qui est acceptable aujourd'hui — mais la tendance est à la croissance : chaque phase ajoute des sections, et la Phase 9 (ouverture publique) va entraîner des demandes d'extension.

**Contrainte additionnelle :** quand un utilisateur veut modifier une règle (ex. changer le garde-fou Débat de 3 à 5 rounds), il doit naviguer 310 lignes pour trouver la section. Le coût de maintenance augmente proportionnellement à la densité du fichier.

**Mesure empirique de référence (ADR-0005) :** overhead framework = ~2 750–4 370 tokens (~6 % du budget), dont ~2 100–3 400 pour l'orchestrator. L'extraction modulaire vise à ramener ce chiffre à ~1 000–1 500 tokens pour les sessions simples (chargement du core uniquement).

---

## Décision

Nous allons **extraire les trois blocs autonomes** (Party Mode, Skills, Mémoire persistante) de `orchestrator.agent.md` vers des fichiers de référence dédiés dans `.github/agents/modules/`, et remplacer chaque bloc par une référence courte (≤ 5 lignes) pointant vers le fichier correspondant.

L'orchestrator conserve :
- PRE-FLIGHT et règles critiques
- Règle de délégation et contrat PLAN → EXECUTION
- Tableau personas et mapping demande → workflow
- Commandes spéciales (une ligne par commande, description minimale)
- Flux obligatoire (ANALYSE → PLAN → CONFIRM → EXECUTE → SYNTHESIS → CLOSE)
- Format en-têtes persona + anti-patterns

**Cible** : `orchestrator.agent.md` ≤ 180 lignes (core), trois modules ≤ 80 lignes chacun.

---

## Alternatives considérées

### Option A — Extraction modulaire (retenue)
- **Description** : 3 nouveaux fichiers `party-mode.md`, `skills.md`, `memory.md` dans `.github/agents/modules/`. L'orchestrator référence chaque module par un lien cliquable et une description d'une ligne.
- **Avantages** : réduction du core à ~180 lignes ; chaque module est modifiable de façon isolée ; maintenabilité améliorée pour les contributeurs externes.
- **Inconvénients** : l'orchestrator doit maintenant coordonner 3 fichiers supplémentaires ; risque de désynchronisation si un module évolue sans mise à jour de l'orchestrator ; les modules ne sont pas chargés automatiquement — Copilot ne les lit que si l'orchestrator y pointe explicitement et si le modèle suit les liens.
- **Pourquoi retenue** : seule option qui réduit structurellement le poids du contexte core ET améliore la navigabilité pour les contributeurs.

### Option B — Compression sur place (garder un seul fichier)
- **Description** : réécrire chaque section en réduisant sa verbosité sans extraire de fichiers.
- **Avantages** : aucune nouvelle dépendance, structure inchangée.
- **Inconvénients** : la verbosité est en partie fonctionnelle (les garde-fous comportementaux doivent être explicites pour que le LLM les applique). Compression ≠ clarté. Risque de régresser des règles binaires en les raccourcissant trop.
- **Pourquoi rejetée** : gain de tokens limité (~20 %), fragilise les règles comportementales.

### Option C — Statu quo
- **Description** : ne rien modifier, documenter le problème dans un ADR pour référence future.
- **Avantages** : zéro risque de régression.
- **Inconvénients** : dette qui croît à chaque phase. Dès la Phase 9, des contributeurs externes vont modifier le fichier et créer des incohérences.
- **Pourquoi rejetée** : l'audit identifie ce point comme critique bloquant sur sessions longues ; ne pas agir maintenant rend le problème plus coûteux à traiter plus tard.

---

## Plan d'implémentation

### Fichiers à créer

| Fichier | Contenu extrait |
|---|---|
| `.github/agents/modules/party-mode.md` | Section complète Party Mode (Panel + Débat) |
| `.github/agents/modules/skills.md` | Section complète Skills (règles progressive disclosure + tableau des skills) |
| `.github/agents/modules/memory.md` | Section complète Mémoire persistante (lecture, écriture, scoping) |

### Modifications dans orchestrator.agent.md

Chaque section extraite est remplacée par un bloc de référence :

```markdown
## Party Mode & Débat
Protocoles dans [`.github/agents/modules/party-mode.md`](modules/party-mode.md).
Résumé : Panel = une passe multi-angles (défaut) ; `/debate` = N rounds inter-persona.
```

### Invariants — ne pas toucher

- PRE-FLIGHT (checklist 4 questions) — doit rester dans l'orchestrator pour être chargé systématiquement
- Règles critiques (5 lignes en haut du fichier) — ancre d'attention, doit rester
- Flux ANALYSE → PLAN → CONFIRM → EXECUTE → SYNTHESIS → CLOSE — rester dans le core

---

## Conséquences

### Positives
- Orchestrator core ≤ 180 lignes → réduction de ~40 % du fichier chargé à chaque session
- Chaque module est modifiable isolément sans toucher au core
- Navigabilité améliorée : un contributeur qui veut modifier le Débat va directement dans `modules/party-mode.md`
- Scalabilité : chaque future Phase peut ajouter un module sans alourdir le core

### Négatives
- 3 fichiers supplémentaires dans `.github/agents/modules/` — à créer et maintenir
- Risque de désynchronisation core/modules si une modification impacte les deux (ex. ajouter une commande spéciale `/debate` dans les commandes ET dans party-mode.md)
- Les modules ne sont pas chargés automatiquement : si Copilot ne suit pas les liens, les règles détaillées ne sont pas appliquées. Mitigation : les règles binaires critiques restent dans le core sous forme condensée ; les modules n'ont que les détails et exemples.

### Neutres
- La commande `/checkpoint`, `/debate`, etc. reste dans la section « Commandes spéciales » du core (1 ligne par commande avec lien vers le module)
- Le tableau Skills reste dans `modules/skills.md` ; l'orchestrator conserve uniquement la règle de chargement scopé (2 lignes)

---

## Risques & mitigation

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Copilot ne charge pas les modules (liens non suivis) | Moyen | Élevé | Garder les règles binaires dans le core ; modules = détails et exemples uniquement |
| Désynchronisation core/module lors d'une future modification | Faible | Moyen | Ajouter une note d'en-tête dans chaque module : « Ce fichier est référencé par orchestrator.agent.md — toute modification doit être répercutée » |
| Régression de règles comportementales lors de la compression | Moyen | Critique | Tests manuels de session après refactoring (30 min, 3 scénarios de référence) |

---

## Critères de succès

- [ ] `orchestrator.agent.md` ≤ 180 lignes
- [ ] Les 3 modules existent dans `.github/agents/modules/`
- [ ] Aucune règle binaire (délégation, plan obligatoire, Scribe ferme) n'est absente du core
- [ ] Une session test de 30 min avec 3 scénarios (incident, feature, question simple) ne montre pas de régression comportementale
