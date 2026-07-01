---
type: adr
number: "0011"
status: accepted
date: 2026-07-01
deciders: [Zav]
tags: [hooks, security, secrets, tool-guardian, awesome-copilot, opt-in, zero-break]
---

# ADR-0011 — Intégration sélective des hooks awesome-copilot (Tool Guardian + Secrets Scanner)

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-01
**Décideurs** : Zav

---

## Contexte

La collection communautaire [awesome-copilot/hooks](https://awesome-copilot.github.com/hooks/)
propose 4 hooks de sécurité/supervision candidats à l'intégration dans le socle `agents/hooks/`
(opt-in, non auto-chargé — voir [Phase 7](../architecture/2026-05-30-phase-7-persistent-memory.md),
[ADR-0010](0010-hooks-telemetry-observer.md)) :

1. **Governance Audit** — scan des prompts (exfiltration, escalade, prompt injection…), events `sessionStart`/`sessionEnd`/`userPromptSubmitted`.
2. **Session Logger** — journalisation start/end/prompt.
3. **Secrets Scanner** — scan des fichiers modifiés en fin de session (secrets/credentials), event `sessionEnd`.
4. **Tool Guardian** — blocage des opérations d'outils dangereuses avant exécution, event `preToolUse`.

Deux contraintes structurantes :

- **Constat d'incompatibilité de runtime** : ces hooks ciblent le **GitHub Copilot coding agent**
  (runtime cloud/CLI), pas les **VS Code Agent Hooks (Preview)** du socle. Divergences bloquantes :
  noms d'événements (camelCase vs PascalCase), exécuteur (`bash:` seul vs `windows/linux/osx`),
  **signal de blocage** (exit code ≠ 0 vs JSON `permissionDecision` sur stdout), dépendances
  (`jq`/`bc`/`file` vs **zéro dépendance**). Les scripts `.sh` amont **ne tournent pas nativement
  sur Windows/pwsh** et leur `exit 1` **ne bloque rien** dans VS Code. « Intégrer » = **réécrire**
  la logique au format VS Code, pas copier-coller.
- **Contrainte "zero-break"** : l'intégration ne doit ni bloquer, ni ralentir, ni corrompre la
  boucle agentique (réactivité des outils, contexte, raisonnement). Invariants du socle :
  **opt-in**, **zéro dépendance**, **fail-open non bloquant**, **aucun contenu sensible loggé**.

Le socle couvre déjà : `security-guard` (`PreToolUse`), `memory-nudge` (`PreCompact`/`Stop`),
`agent-telemetry` (`PostToolUse`/`Subagent*`).

---

## Décision

Intégrer **2 des 4** hooks, réécrits au format VS Code, et **rejeter les 2 autres** :

| Hook | Décision | Motif principal |
|---|---|---|
| **Tool Guardian** | ✅ **Fusionné dans `security-guard`** | Redondant avec le garde `PreToolUse` existant → on **enrichit** plutôt que d'ajouter un 2ᵉ hook sur le chemin chaud. |
| **Secrets Scanner** | ✅ **Intégré** (`secrets-scanner.{ps1,sh}`, event `Stop`) | Couvre un **angle mort réel** : secrets *écrits* par l'agent. Hors chemin chaud. |
| **Governance Audit** | ❌ **Rejeté** | Détection regex de prompts trop bruitée ; seul mode sûr (audit-only) = un log de plus. Pas de besoin de conformité formel. |
| **Session Logger** | ❌ **Rejeté** | Redondant à ~70 % avec `agent-telemetry`. Journaliser les prompts = 2 lignes à ajouter à l'observateur, pas un 3ᵉ système. |

**Modalités d'implémentation (invariants respectés)** :

1. **`security-guard` enrichi** : +10 patterns portés de Tool Guardian (`chmod 777`, `curl|sh`,
   `wget|sh`, `curl --data @`, `DELETE FROM` sans `WHERE`, `git clean -f`, suppression `.env`/`.git`,
   `sudo`, `npm publish`) **avec suggestion d'alternative sûre** dans le message. Signal =
   `permissionDecision: ask` (confirmation), **jamais `deny`**. Le texte de la commande n'est
   **jamais** réinjecté (anti-injection / anti-pollution de contexte).
2. **`secrets-scanner`** : event `Stop` (**hors chemin chaud**), mode **warn only**, **fail-open**
   (`try/catch` + `exit 0` inconditionnel). Périmètre `git diff` vs HEAD + non suivis, borné
   (300 fichiers / 100 findings / 1 Mo). Matches **rédigés** (`first4...last4`). Log JSONL dans
   `docs/_scratch/telemetry/` (gitignoré, rotation). `systemMessage` non bloquant **uniquement**
   sur détection ; **jamais** de `decision: block`.

---

## Alternatives considérées

### Option A — Intégrer les 4 hooks tels quels
- Description : copier les dossiers awesome-copilot dans `agents/hooks/`.
- Avantages : rapide, fidèle à l'amont.
- Inconvénients : `.sh` non portables sur Windows/pwsh ; `exit 1` inopérant dans VS Code ;
  dépendances `jq`/`bc` ; **double garde `PreToolUse`** (Tool Guardian × security-guard) →
  latence doublée + décisions concurrentes ; bruit de Governance/Session Logger.
- **Pourquoi rejetée** : viole les invariants (zéro dépendance, zero-break) et casse le runtime.

### Option B — Ajouter Tool Guardian comme hook `PreToolUse` séparé
- Description : conserver `security-guard` **et** ajouter `tool-guardian` sur le même événement.
- Avantages : séparation des responsabilités, fidélité à l'amont.
- Inconvénients : **2 scripts sur le chemin le plus chaud** → latence cumulée × nb d'outils ;
  décisions potentiellement contradictoires (`ask` vs `exit 1` non interprété).
- **Pourquoi rejetée** : conflit direct ; fusionner dans un garde unique élimine le risque.

### Option C — Intégrer les 4, Governance/Logger en mode audit-only
- Description : tout intégrer, mais Governance en `open` et Logger en métadonnées.
- Avantages : couverture maximale, traçabilité des prompts.
- Inconvénients : Governance = bruit regex sans valeur bloquante ; Logger redondant avec
  `agent-telemetry` → 3ᵉ système d'observation à maintenir.
- **Pourquoi rejetée** : faible valeur ajoutée / coût de maintenance ; principe YAGNI.

---

## Conséquences

### Positives
- Couverture de sécurité accrue sur **ce que l'agent fait** (commandes + fichiers écrits),
  là où la valeur est haute et le bruit maîtrisable.
- Un seul garde `PreToolUse` : pas de latence doublée, pas de décisions concurrentes.
- Détection de secrets **hors chemin chaud** (event `Stop`) : zéro impact réactivité.
- Invariants du socle préservés (opt-in, zéro dépendance, fail-open, redaction, gitignore).

### Négatives
- Détection **par pattern** (regex) : faux positifs possibles en mode warn (ex. secrets dans la
  doc, fixtures) et sur `PreToolUse` (confirmation superflue). Atténué par filtres placeholder,
  auto-exclusion des sources du scanner, et le fait que `PreToolUse` demande (ne refuse pas).
- Pas de protection anti-prompt-injection (Governance rejeté) : angle non couvert, assumé.
- Divergence cross-shell sous Windows : le `git` de Git-Bash/WSL peut voir plus de fichiers
  « modifiés » (CRLF/LF). Sans incidence (VS Code exécute `.ps1` sur Windows ; warn-only + borné).

### Neutres / À surveiller
- Réévaluer Governance Audit si un besoin de **conformité formelle** apparaît.
- Les Agent Hooks VS Code restent en **Preview** : revalider après mises à jour majeures.
- Surveiller le taux de faux positifs du scanner ; ajuster patterns / allowlist si nécessaire.

---

## Implémentation

- [x] `security-guard.{ps1,sh}` : +10 règles avec suggestions (rules table).
- [x] `secrets-scanner.{ps1,sh}` : nouveau, event `Stop`, warn-only, fail-open, ~25 patterns.
- [x] `hooks.json` : entrée `Stop` ajoutée (timeout 20 s), coexiste avec `memory-nudge`.
- [x] `docs/_scratch/telemetry/.gitignore` : commentaire étendu (couvre `secrets-scan.jsonl`).
- [x] `agents/hooks/README.md` : tableau, section détails, procédures de test.
- [x] Tests d'exécution réels (pwsh + bash `-n`/fonctionnel) : détection, cas propre, placeholder,
  auto-exclusion, absence de faux positifs bénins. 3 bugs trouvés et corrigés (`[ordered]@{}`,
  `Get-Content` 1 ligne, `grep --no-verify`).

## Références
- [Bilan d'impact & GO/NO-GO](https://awesome-copilot.github.com/hooks/) (analyse en session).
- [ADR-0010 — Télémétrie observateur](0010-hooks-telemetry-observer.md) (pattern & invariants).
- [Note de cadrage Phase 7](../architecture/2026-05-30-phase-7-persistent-memory.md) (§5-bis, opt-in).
- Sources amont : `awesome-copilot/hooks/{tool-guardian,secrets-scanner,governance-audit,session-logger}`.
- [`agents/hooks/README.md`](../../agents/hooks/README.md) (documentation opérationnelle).
