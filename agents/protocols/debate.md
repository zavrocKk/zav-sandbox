---
type: protocol
used_by: [orchestrator]
scope: multi-personas
related: [agents/protocols/light-panel.md, docs/architecture/2026-05-30-party-mode-panel-vs-debate.md]
---

# Protocole DÉBAT — Brainstorming sur invocation (`/debate`, N rounds)

> Sémantique figée par
> [`docs/architecture/2026-05-30-party-mode-panel-vs-debate.md`](../../docs/architecture/2026-05-30-party-mode-panel-vs-debate.md).
> Le Débat est la **surcouche** au-dessus du [Panel](light-panel.md) : même brique
> de sélection d'agents, mais **N rounds** au lieu d'une passe.

## Règle binaire

> **DÉBAT** : les personas **réagissent entre eux** sur **N rounds**, sous conduite
> de l'orchestrateur. Garde-fou **max rounds**, puis le Scribe **force la synthèse**.

À l'inverse du Panel (borné par construction), le Débat est volontairement plus
coûteux en tokens — d'où le garde-fou obligatoire.

## Quand l'appliquer

- **Uniquement sur invocation explicite `/debate`.** Jamais auto-déclenché
  (l'auto-détection « exploratoire vs exécutable » est **hors scope**).
- Problème **ouvert** : brainstorming, arbitrage, idéation, on bloque ou on explore.
- Si le problème est fermé (une réponse à trouver) → c'est le **Panel**, pas le Débat.

## Garde-fou — max rounds

- **N = 3 rounds par défaut** (valeur ajustable par l'utilisateur en début de débat :
  « /debate max=N »).
- Un *round* = un tour de parole complet de chaque persona convoqué.
- À l'atteinte de N rounds, l'orchestrateur **coupe** et passe la main au Scribe
  pour synthèse forcée — **même si le débat n'a pas convergé**.
- L'orchestrateur peut clore **avant** N rounds si convergence manifeste.

## Conduite du débat (rôle de l'orchestrateur)

1. **Cadrer** : énoncer le sujet ouvert, convoquer l'équipe pertinente (sélection
   intelligente, comme le Panel), annoncer N.
2. **Round 1 = un Panel** : chaque persona pose sa carte d'angle initiale
   (Position / Risque clé / Reco). Sert de socle.
3. **Rounds 2..N — réaction** : chaque persona réagit aux angles des autres
   (accord, objection, angle mort soulevé). Tours de parole tenus par l'orchestrateur.
4. **Anti-dérive** : l'orchestrateur recadre si le débat tourne en rond, relance
   sur les angles morts, coupe la redondance.
5. **Clôture** : à convergence OU à N rounds, handoff forcé vers le Scribe.

## Format — prise de parole en round de réaction

```text
─── 🛠️ DevOps — Round 2 ───
Réagit à : <persona(s) / point visé>
Position : <maintient / révise — 1 ligne>
Apport : <objection, angle mort, ou appui — 1-2 lignes>
```

## Format — synthèse Scribe (fixe)

```text
─── 📝 Scribe — Synthèse débat ───
Sujet exploré : …
Personas convoqués (et pourquoi) : …
Positions / angles : …
Convergences : …
Désaccords persistants : …
Options dégagées : …
Reco / question ouverte : …
```

## Livrable

Le Débat se clôt **toujours** par une synthèse Scribe committée (filtre 6 VISION).
Emplacement selon la nature du résultat — voir la **table de localisation** de
[`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) :

- Débat qui débouche sur une décision structurante → **ADR** dans `docs/decisions/`.
- Débat exploratoire (pas de décision ferme) → **note de délibération** dans
  `docs/_scratch/` au format `YYYY-MM-DD-debate-<topic>.md`.

## Orthogonalité des commandes

| Commande | Effet | Interaction avec le Débat |
| --- | --- | --- |
| `/quick` | Saute CONFIRM | Le débat démarre sans validation intermédiaire |
| `/light` | Allège le FORMAT seulement | Prises de parole compactes ; rounds et garde-fou inchangés |
| `/debate` | Bascule Panel → Débat | Active ce protocole |

`/quick`, `/light` et `/debate` restent **orthogonaux et cumulables**.

## Conséquences d'une violation

- Débat lancé sans `/debate` explicite → violation : revenir au Panel.
- Dépassement de N rounds sans synthèse → violation : couper, forcer le Scribe.
- Débat clos sans synthèse Scribe committée → l'ajouter avant de terminer.
