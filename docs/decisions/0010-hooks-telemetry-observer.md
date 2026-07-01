---
type: adr
number: "0010"
status: accepted
date: 2026-07-01
deciders: [Zav]
tags: [hooks, observability, telemetry, subagents, non-invasive]
---

# ADR-0010 — Couche télémétrie observateur via hooks non bloquants

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-01
**Décideurs** : Zav

---

## Contexte

Le socle `agents/hooks/` (opt-in, non auto-chargé — voir [Phase 7](../architecture/2026-05-30-phase-7-persistent-memory.md))
couvre aujourd'hui deux besoins :

- **Sécurité** : `security-guard` (`PreToolUse`) → confirmation sur pattern destructif.
- **Mémoire** : `memory-nudge` (`PreCompact` + `Stop`) → nudge `/checkpoint` non bloquant.

Il manquait un moyen **déterministe** d'observer l'activité de l'agent pour :

- **Performance** : combien d'appels d'outils par session, fréquence des échecs.
- **Suivi des sous-agents** : le mode `/party-real` ([ADR-0008](0008-subagents-party-real.md),
  [ADR-0009](0009-abaisser-seuil-panel-inline.md)) spawne des sous-agents dont le cycle de vie
  n'est pas tracé.
- **Volumétrie** : taille des payloads échangés par événement.

La doc officielle [Automating with Hooks](https://awesome-copilot.github.com/learning-hub/automating-with-hooks/)
formalise plusieurs événements adaptés à ce besoin. ⚠️ **VS Code (Preview) ne supporte que 8
événements** (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`,
`SubagentStart`, `SubagentStop`, `Stop`) — l'événement `PostToolUseFailure` de la doc awesome-copilot
est propre à **Copilot CLI / Claude Code** et n'existe pas dans VS Code. Contrainte forte :
**ne rien casser** et **ne jamais influer sur le flux**.

---

## Décision

Ajouter un **unique script observateur** `agent-telemetry.{ps1,sh}` branché sur trois événements
non bloquants supportés par VS Code (`PostToolUse`, `SubagentStart`, `SubagentStop`), suivant
strictement le **pattern Observateur** :

1. **Écriture seule, jamais de décision** : le hook append une ligne JSONL de métadonnées et
   n'émet **aucun** `permissionDecision` / `decision: block` / `response`. Il ne peut donc pas
   bloquer ni détourner le flux.
2. **`exit 0` inconditionnel** : toute la logique est encadrée par `try/catch` (PowerShell) et un
   bloc `{ … } 2>/dev/null || true` (bash, sans `set -e`). Une panne de télémétrie est absorbée
   silencieusement.
3. **Aucun contenu sensible loggé** : seuls `timestamp`, `event` et `payloadBytes` (taille) sont
   enregistrés. Ni prompt, ni commande, ni sortie d'outil. Choix vie privée / sécurité.
4. **Pas de surface d'injection** : le nom d'événement vient d'un **argument de confiance** dans
   `hooks.json`, jamais extrait du payload. Il est de plus filtré sur un charset sûr.
5. **Log gitignoré** : `docs/_scratch/telemetry/agent-telemetry.jsonl`, couvert par un `.gitignore`
   dédié. Jamais versionné.
6. **Reste opt-in** : les hooks vivent dans `agents/hooks/` (hors `.github/hooks/`) → chargés
   uniquement si l'utilisateur active `chat.hookFilesLocations`. Aucune modification de
   l'architecture centrale (markdown + orchestrateur + Git).
7. **Rotation automatique** : le log est basculé vers `agent-telemetry.jsonl.1` (un seul backup)
   au-delà de ~1 Mo. Best-effort, encadré comme le reste ; le dossier peut être purgé à la main.

Format d'une ligne : `{"ts":"2026-07-01T09:12:34.567Z","event":"PostToolUse","payloadBytes":842}`.

---

## Alternatives considérées

### Option A — `preToolUse` avec instrumentation

- Description : mesurer via le hook `PreToolUse` existant.
- **Pourquoi rejetée** : `PreToolUse` est un point **bloquant** (peut refuser un outil). Y greffer
  de la télémétrie mélange responsabilités sécurité et observation, et augmente le risque qu'un bug
  d'observation bloque une action. Séparation des préoccupations violée.

### Option B — Hook HTTP vers un service d'audit distant

- Description : `type: "http"` POST vers un endpoint centralisé.
- **Pourquoi rejetée** : introduit une dépendance réseau et un point de latence/échec dans une
  boucle synchrone, contraire au filtre fiabilité (VISION 5). Sur-dimensionné pour un sandbox mono-utilisateur.

### Option C — Logger le contenu complet des outils/prompts

- Description : enrichir le JSONL avec le nom d'outil et les arguments.
- **Pourquoi rejetée** : risque de fuite de données sensibles (secrets dans une commande) et de
  corruption JSON (échappement). La métadonnée `payloadBytes` suffit pour le suivi perf/volumétrie.

---

## Conséquences

**Positives** :

- Observabilité déterministe des sessions (perf, sous-agents, volumétrie) sans dépendre de la mémoire du LLM.
- Zéro impact sur le flux : pattern observateur + `exit 0` inconditionnel = blast radius nul.
- Cohérent avec l'existant : mêmes conventions (`.ps1` + `.sh`, ASCII-safe, dependency-free, opt-in).
- Base pour de futures analyses (agrégation par `event`, corrélation `SubagentStart`/`SubagentStop`).

**Négatives / risques** :

- Événements `PostToolUse`/`Subagent*` en **Preview** VS Code — noms/comportement susceptibles de changer
  (déjà signalé dans le README). À revalider après mise à jour majeure.
- Pas de suivi dédié des échecs d'outils : VS Code n'expose pas d'événement `PostToolUseFailure`
  (limitation plateforme, pas de contournement propre sans parser le transcript instable).
- Léger surcoût I/O par appel d'outil (timeout serré à 5 s, écriture d'une ligne + stat de rotation).
- Le log est borné par rotation (~1 Mo, 1 backup) — pas d'accumulation illimitée.

**Mesures de mitigation** :

- Timeout `5 s` par entrée (kill automatique en cas de blocage improbable).
- Documentation de test manuel ajoutée au README (`Tester agent-telemetry`).

---

## Références

- Doc source : [Automating with Hooks](https://awesome-copilot.github.com/learning-hub/automating-with-hooks/)
- README des hooks : [`agents/hooks/README.md`](../../agents/hooks/README.md)
- Config : [`agents/hooks/hooks.json`](../../agents/hooks/hooks.json)
- Cadrage opt-in : [`docs/architecture/2026-05-30-phase-7-persistent-memory.md`](../architecture/2026-05-30-phase-7-persistent-memory.md)
- Sous-agents (contexte suivi) : [`0008-subagents-party-real.md`](0008-subagents-party-real.md), [`0009-abaisser-seuil-panel-inline.md`](0009-abaisser-seuil-panel-inline.md)
