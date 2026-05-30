---
type: workflow
used_by: [orchestrator]
audience: [new-user]
---

# Workflow — Onboarding (5 minutes)

> Ce workflow guide un nouvel utilisateur de zéro à sa première session productive.
> Il n'y a **rien à installer** — le framework est 100 % Markdown.

---

## Prérequis (1 min)

- VS Code installé
- Extension **GitHub Copilot Chat** activée (compte Copilot requis)
- Ce repo ouvert dans VS Code : `File → Open Folder → zav-sandbox/`

---

## Étape 1 — Activer l'agent Orchestrator (1 min)

1. Ouvre la vue **Chat** (`Ctrl+Alt+I` Windows / `⌃⌘I` macOS)
2. Clique sur le **dropdown des agents** (à côté du champ texte, il affiche « Ask »
   ou « Agent » par défaut)
3. Sélectionne **orchestrator** dans la liste

> Si `orchestrator` n'apparaît pas : recharge la fenêtre
> (`Ctrl+Shift+P` → `Developer: Reload Window`).

---

## Étape 2 — Premier message (30 s)

Tape simplement :

```
Bonjour, c'est ma première session. Montre-moi comment ça fonctionne.
```

L'orchestrator se présente, liste les personas disponibles et invite à décrire
ton besoin.

---

## Étape 3 — Cas de référence : analyser un incident fictif (3 min)

Copie-colle ce message tel quel :

```
L'API /checkout renvoie du 502 depuis 10 minutes. Le dashboard montre
une explosion de latence. Aide-moi.
```

**Ce que tu vas voir :**

1. `## 🎼 Analyse` — reformulation de la demande
2. `## 🎼 Plan` — table avec les personas convoqués et leurs livrables
3. Demande de confirmation : *« Valide-tu ce plan ? (oui / ajuste / `/quick`) »*
4. Réponds `oui` → l'orchestrator enchaîne les personas, le Scribe produit un
   post-mortem dans `docs/incidents/`

---

## Commandes à retenir

| Commande | Effet |
|---|---|
| `/quick` | Saute la confirmation du plan — utile en urgence ou demande simple |
| `/light` | Format compact (moins de tokens par tour) |
| `/debate` | Bascule en mode brainstorming multi-rounds (N rounds, défaut 3) |
| `/checkpoint` | Sauvegarde l'état de la session pour y revenir plus tard |
| `/memory-list` | Liste les checkpoints actifs dans `docs/_scratch/memory/` |
| `/persona <nom>` | Force un persona unique pour la réponse suivante |

---

## Structure du repo en 30 secondes

```
agents/personas/       → Les 8 experts (DevOps, Dev, QA, Security, Architect, PA, DE, Scribe)
agents/workflows/      → Les recettes par type de problème (incident, feature, archi...)
agents/skills/         → Modules de connaissance invocables à la demande
docs/                  → Tous les livrables produits par le Scribe
docs/_scratch/memory/  → Checkpoints inter-sessions (reprendre un fil)
```

---

## Prochaines étapes

- Essaie une vraie demande (incident récent, feature à cadrer, audit de code)
- Explore les workflows : [`agents/workflows/`](../workflows/)
- Active les hooks optionnels : [`agents/hooks/README.md`](../hooks/README.md)
- Contribue : [`CONTRIBUTING.md`](../../CONTRIBUTING.md)
