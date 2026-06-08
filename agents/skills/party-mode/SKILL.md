---
name: party-mode
version: "1.1.0"
description: >
  Ancre le protocole d'orchestration multi-personas (Panel inline, Débat, et Party Real sous-agents).
  À charger quand une session implique plusieurs personas, que le mode Panel/Débat/Party-Real doit
  être rappelé, ou qu'un checkpoint de reprise est à traiter. Ne pas utiliser pour une tâche
  mono-persona ou une question simple.
---

# Party Mode — Protocole d'orchestration multi-personas

Référence opérationnelle rapide pour l'orchestrateur. Pour la définition complète et les
formats, voir les protocoles sources :

- Panel (défaut) → [`agents/protocols/light-panel.md`](../../../agents/protocols/light-panel.md)
- Débat (sur invocation) → [`agents/protocols/debate.md`](../../../agents/protocols/debate.md)
- Décision d'architecture → [`docs/architecture/2026-05-30-party-mode-panel-vs-debate.md`](../../../docs/architecture/2026-05-30-party-mode-panel-vs-debate.md)

---

## Choix du mode — règle ternaire (automatique, décidée par l'orchestrateur)

| Condition | Mode | Déclenchement |
|---|---|---|
| Problème **fermé**, 1 persona | **Persona unique inline** | Automatique |
| Problème **fermé**, 2-3 personas, session courte | **Panel inline** | Automatique |
| Problème **fermé**, 4+ personas OU workflow complet | **Party Real (sous-agents)** | **Automatique** — l'utilisateur ne tape rien |
| Problème **ouvert** + `/debate` explicite | **Débat** (inline uniquement) | Commande utilisateur |

> **L'utilisateur n'a jamais à taper `/party-real`.** L'orchestrateur choisit le mode au moment du PLAN et l'annonce : `Mode : Party Real (sous-agents) — N personas détectés`.
>
> **⚠️ Incompatibilité `/debate` + Party Real** : le Débat exige que les personas voient les réactions des autres en temps réel (même fenêtre). Les sous-agents reçoivent chacun une fenêtre fraîche — la dynamique de réaction inter-rounds est impossible. **`/debate` fonctionne exclusivement en mode inline (impersonation).**

---

## Critères de déclenchement Panel

Convoquer le Panel **si au moins un critère est vrai** :
- 2+ expertises distinctes requises
- Tâche implique analyse ET implémentation ET validation simultanément
- Modification touchant 3+ composants distincts

Doute → persona unique d'abord ; élargir si un angle manque.

---

## Reprise de session (checkpoint)

À l'ouverture, vérifier `docs/_scratch/memory/` :

```
SI fichier <thread-slug>.md présent
→ lire silencieusement
→ annoncer : "Checkpoint détecté : <fichier>. Session reprise."
SI aucun checkpoint → démarrage à zéro, pas de mention
```

---

## Cycle Panel inline (rappel)

```
Orchestrateur sélectionne personas (critères ci-dessus)
→ Chaque persona : carte d'angle 3 lignes max
    ─── 🛠️ DevOps — Angle ───
    Position : <1 ligne>
    Risque clé : <1 ligne>
    Reco : <1 ligne>
→ Scribe : synthèse (Convergences / Divergences / Options / Reco)
→ Contradiction directe → signaler + proposer /debate, ne pas trancher
```

---

## Cycle Party Real (sous-agents, 4+ personas — automatique)

```
1. Orchestrateur écrit .party/context.md (template agents/templates/party-context.md)
   → objectif, scope, contraintes, séquence agents (≤ 500 tokens)
   → DéCLARATION dans le PLAN : "Mode : Party Real (sous-agents) — N personas détectés"

2. Pour chaque agent dans la séquence :
   runSubagent("<agent>")
   → l'agent lit .party/context.md + tous les .party/handoff-*.md existants
   → l'agent produit son travail
   → l'agent écrit .party/handoff-<agent>.md (≤ 500 tokens)

3. Orchestrateur lit handoff-scribe.md (quality gate)

4. Orchestrateur DOIT supprimer .party/ à la clôture
   (dossier transitoire, .gitignore-d)

Fallback si runSubagent échoue :
→ orchestrateur impersonne le persona
→ écrit le handoff manuellement dans .party/
→ continue la séquence
```

**Agents disponibles** : `devops`, `developer`, `security`, `architect`, `qa`, `product-analyst`, `scribe`
**Fichiers agents** : `.github/agents/<agent>.agent.md`
**Budget tokens** : `context.md` ≤ 500 tokens, `handoff-*.md` ≤ 500 tokens chacun

---

## Cycle Débat — uniquement sur `/debate` explicite

```
Round 1 = Panel (positions initiales)
Rounds 2..N = réactions croisées entre personas
Garde-fou : N=3 par défaut (ajustable /debate max=N)
À N rounds : Scribe force la synthèse, même sans convergence
```

---

## Anti-patterns (violations bloquantes)

| Violation | Correction |
|---|---|
| Débat déclenché sans `/debate` | Revenir au Panel |
| Carte d'angle > 3 lignes | Retailler |
| Persona réagit à un autre en mode Panel | Couper ou basculer `/debate` |
| Cycle clos sans synthèse Scribe | Ajouter avant de terminer |
| Dépassement N rounds sans synthèse | Couper, forcer le Scribe |
| `/party-real` sans nettoyage `.party/` à la clôture | Supprimer `.party/` |
| `context.md` ou `handoff-*.md` > 500 tokens | Condenser avant de passer au suivant |
