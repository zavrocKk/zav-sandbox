# `agents/hooks/` — Agent hooks VS Code (opt-in, OFF par défaut)

> **Couche optionnelle « power-user ».** Ces hooks ne sont **pas** un prérequis du
> framework. Le socle Agentic Team reste 100 % markdown + instruction
> orchestrateur + Git (voir [note de cadrage Phase 7](../../docs/architecture/2026-05-30-phase-7-persistent-memory.md), §5-bis).
> Ce dossier n'est **pas** dans `.github/hooks/` exprès : il n'est donc **pas
> chargé automatiquement**. Tu actives ces hooks **manuellement** (voir ci-dessous).

## Pourquoi opt-in et non auto-chargé

- Les agent hooks VS Code sont en **Preview** (format/comportement susceptibles de
  changer) → ne pas en faire une dépendance du socle (filtre VISION 5, fiabilité).
- Ils exécutent du **shell** → cassent la promesse « lisible/maintenable par un
  non-dev » (filtres VISION 2/4) s'ils sont obligatoires. En opt-in, c'est un bonus
  assumé pour qui le veut.

## Contenu

| Fichier | Hook | Rôle | Risque |
|---|---|---|---|
| `security-guard.ps1` / `.sh` | `PreToolUse` | Scanne la commande avant exécution ; sur pattern destructif (`rm -rf`, `DROP TABLE`, `git push --force`, `--no-verify`, `terraform destroy`, `kubectl delete`, `chmod 777`, `curl \| sh`, `DELETE FROM` sans `WHERE`, `sudo`, `npm publish`…) → renvoie `permissionDecision: ask` (confirmation requise) avec une **suggestion d'alternative sûre**. **N'exécute jamais la commande.** | 🟢 nul |
| `secrets-scanner.ps1` / `.sh` | `Stop` | **Scan de fin de session** : inspecte les fichiers modifiés (`git diff` vs HEAD + non suivis) contre ~25 familles de secrets (clés cloud, PAT, clés privées, connection strings, JWT…). Sur détection → une ligne JSONL **rédigée** dans le log + un `systemMessage` **non bloquant**. **Mode warn only, fail-open : ne bloque jamais, sort toujours en `0`, ne ré-expose jamais un secret** (match tronqué `first4...last4`). | 🟢 nul |
| `memory-nudge.ps1` / `.sh` | `PreCompact` + `Stop` | `systemMessage` non bloquant : rappelle de lancer `/checkpoint` avant compaction/fin de session. **Ne bloque pas l'agent** (pas de `decision: block`). | 🟢 nul |
| `agent-telemetry.ps1` / `.sh` | `PostToolUse` + `SubagentStart` + `SubagentStop` | **Pattern Observateur** : append d'une ligne JSONL (timestamp, nom d'événement, taille du payload) dans `docs/_scratch/telemetry/agent-telemetry.jsonl` pour le suivi perf / sous-agents. `try/catch` global, `exit 0` inconditionnel. **N'émet aucune décision, ne bloque jamais, ne logge aucun contenu** (prompt/commande). | 🟢 nul |

### Hook télémétrie (observateur) — détails

`agent-telemetry` est une **couche d'observation passive** (ADR-0010). Il ne modifie jamais
le flux : chaque événement déclenche l'écriture d'une seule ligne JSONL de **métadonnées**.

- **Ce qui est loggé** : `{"ts":"<ISO-UTC>","event":"<EventName>","payloadBytes":<int>}`.
- **Ce qui n'est PAS loggé** : le contenu des prompts, des commandes ou des sorties d'outils
  (choix délibéré vie privée / sécurité). Seule la **taille** du payload est enregistrée.
- **Nom d'événement** : passé en **argument de confiance** depuis `hooks.json` (jamais
  extrait du payload) → aucune surface d'injection.
- **Emplacement du log** : `docs/_scratch/telemetry/` — **gitignoré** (`.gitignore` dédié),
  jamais versionné.
- **Rotation** : le script bascule automatiquement le log vers `agent-telemetry.jsonl.1`
  (un seul backup conservé) dès qu'il dépasse ~1 Mo. Aucune purge manuelle requise ; le dossier
  entier peut être supprimé sans risque (recréé au prochain événement).
- **Robustesse** : tout est encadré par `try/catch` (PowerShell) / bloc `|| true` (bash) ;
  le script sort **toujours en `0`**. Une panne de télémétrie ne peut pas affecter l'agent.

> **Note événements** : VS Code (Preview) ne supporte que **8 événements** :
> `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`,
> `SubagentStart`, `SubagentStop`, `Stop`. Il n'existe **pas** d'événement dédié aux
> échecs d'outils (`PostToolUseFailure` est propre à Copilot CLI / Claude Code) — c'est
> pourquoi le suivi des patterns d'erreur n'est pas branché ici.

Analyse rapide du log (PowerShell) :

```powershell
Get-Content docs/_scratch/telemetry/agent-telemetry.jsonl |
  ConvertFrom-Json | Group-Object event | Select-Object Name, Count
```

### Scan de secrets de fin de session — détails

`secrets-scanner` est un **garde post-traitement warn-only, fail-open** (inspiré du hook
`secrets-scanner` d'awesome-copilot, réécrit au format VS Code, sans dépendance : `git` + `grep`
seulement, pas de `jq` ni `file`). Il se déclenche sur `Stop`, **hors du chemin chaud** de la
boucle agentique — aucune latence perçue pendant le raisonnement.

- **Périmètre** : fichiers modifiés vs `HEAD` (`--diff-filter=ACMR`) + fichiers non suivis.
  Borné à **300 fichiers**, **100 findings** et **1 Mo par fichier** pour tenir le budget de timeout.
- **Ce qui est loggé** : `{"ts","event":"secrets_scan","status","filesScanned","findingCount","findings":[…]}`
  dans `docs/_scratch/telemetry/secrets-scan.jsonl` (même dossier **gitignoré** + rotation `.1` à ~1 Mo).
- **Ce qui n'est PAS ré-exposé** : chaque match est **rédigé** (`first4...last4`, ou `[REDACTED]` si ≤ 12 car.).
  Le `systemMessage` n'affiche qu'un **compte** ("N potential secret(s) across M file(s)"), jamais le secret.
- **Anti-bruit** : filtre placeholder (`example`, `changeme`, `your_`, `dummy`, `test_key`…),
  skip des binaires / lock files, et **auto-exclusion** des propres sources du scanner (qui contiennent
  les patterns en clair).
- **Robustesse** : `try/catch` (PowerShell) / bloc `2>/dev/null || true` (bash), **`exit 0` inconditionnel**.
  Un échec de scan (git absent, timeout, gros diff) ne peut **jamais** bloquer l'agent (fail-open).
- **Détection ≠ blocage** : le mode est **warn** ; le hook ne renvoie **jamais** `decision: block`. La
  confirmation avant commit reste à l'utilisateur.

> **Portage Tool Guardian** : `security-guard` intègre désormais les patterns manquants du hook
> `tool-guardian` d'awesome-copilot (`chmod 777`, `curl \| sh`, `DELETE FROM` sans `WHERE`, `sudo`,
> `npm publish`, suppression de `.env`/`.git`, `git clean -f`…) **avec une suggestion d'alternative
> sûre** dans le message de confirmation. On **n'ajoute pas** un second hook `PreToolUse` : garder un
> seul garde sur le chemin chaud évite latence doublée et décisions concurrentes.

### Hooks volontairement EXCLUS

- **`SessionStart`** : un auto-load au démarrage réinjecterait un contexte
  potentiellement **sans rapport** avec le fil repris (`source` = `"new"`, pas
  encore de prompt) → contredit la règle de **scoping par `thread`**. Exclu.
- **`Stop` avec `decision: block`** : forcerait l'agent à continuer →
  consommation de premium requests + risque de boucle. Exclu (on garde le nudge
  non bloquant).

## Activation (manuelle)

Ajoute à tes **settings** VS Code (workspace ou user) :

```jsonc
"chat.hookFilesLocations": {
  "agents/hooks": true
}
```

Puis recharge la fenêtre. Vérifie le chargement via **Output → GitHub Copilot Chat
Hooks** (cherche « Load Hooks »).

Pour **désactiver** : repasse la valeur à `false` ou retire l'entrée.

## Sécurité

- Les scripts s'exécutent avec les **permissions de VS Code**. Relis-les avant
  activation.
- Recommandé : `"chat.tools.edits.autoApprove"` configuré pour **interdire à
  l'agent de modifier ces scripts** sans approbation manuelle (un agent qui édite
  un hook peut exécuter le code qu'il écrit).
- Les scripts ici **n'exécutent jamais** l'entrée reçue : ils se contentent de la
  **scanner** (security-guard) ou d'émettre un message statique (memory-nudge).
- Dépendance-free : PowerShell est natif Windows ; la version `.sh` n'utilise pas
  `jq` (scan regex sur le payload brut).

## Git hooks — système distinct (scripts/hooks/)

Ce dossier (`agents/hooks/`) contient des **Copilot Agent hooks** (runtime AI). Il coexiste avec un second système de hooks **sans lien** :

| Système | Dossier | Déclencheur | Rôle |
|---|---|---|---|
| Copilot Agent hooks | `agents/hooks/` | Actions IA (PreToolUse, PreCompact) | Sécurité des commandes exécutées par l'agent |
| Git hooks | `scripts/hooks/` | Opérations Git (pre-push) | Bloque les push directs sur `main` |

Installation des Git hooks : `bash scripts/install-hooks.sh`  
Ces deux systèmes sont **complémentaires**, pas concurrents. Ne pas confondre.

## Référence

- Doc officielle (API Preview) : <https://code.visualstudio.com/docs/copilot/customization/hooks>
  > **Note version** : les Agent Hooks VS Code sont en **Preview**. L’API (structure JSON, noms d’événements) peut changer entre versions. À revalider après chaque mise à jour majeure de VS Code ou de l’extension Copilot Chat.
- Cadrage Phase 7 : [`docs/architecture/2026-05-30-phase-7-persistent-memory.md`](../../docs/architecture/2026-05-30-phase-7-persistent-memory.md)

## Compatibilité OS

| OS | Script recommandé | Notes |
|---|---|---|
| Windows | `memory-nudge.ps1`, `security-guard.ps1` | Utilise `pwsh` (PowerShell 7+). Si absent, VS Code bascule sur `powershell` (Windows PowerShell 5.1) automatiquement. Vérifier avec `Get-Command pwsh`. |
| macOS / Linux | `memory-nudge.sh`, `security-guard.sh` | Nécessite `bash`. Aucun autre prérequis (`jq` non requis). |
| WSL | Scripts `.sh` via `bash` | Fonctionne si VS Code est configuré pour utiliser WSL comme terminal par défaut. |

VS Code charge les deux versions (`.ps1` et `.sh`) ; le runtime exécute la version compatible avec le système.

## Procédure de test manuel

### Vérifier que les hooks sont chargés

1. Active les hooks dans les settings VS Code (voir section **Activation**).
2. Recharge la fenêtre (`Developer: Reload Window`).
3. Ouvre **Output** (menu View → Output) et sélectionne **GitHub Copilot Chat Hooks** dans le dropdown.
4. Vérifie la présence de `Load Hooks` et du chemin `agents/hooks/` dans les logs.

### Tester `security-guard`

1. Dans le chat Copilot, demande à l’agent d’exécuter une commande destructive :
   ```
   Run: rm -rf /tmp/test
   ```
2. **Résultat attendu** : une boîte de confirmation s’affiche avant l’exécution (pattern `permissionDecision: ask`).

### Tester `memory-nudge`

1. Lance `/checkpoint` manuellement dans le chat.
2. Envoie un long message pour déclencher la compaction (`PreCompact`) **ou** termine la session (`Stop`).
3. **Résultat attendu** : le message « Memoire persistante : pense a /checkpoint… » apparaît dans le chat comme `systemMessage` (non bloquant).

### Tester `agent-telemetry`

1. Les hooks étant chargés, demande à l'agent une action anodine qui déclenche un outil
   (ex. lire un fichier).
2. **Résultat attendu** : le fichier `docs/_scratch/telemetry/agent-telemetry.jsonl` est
   créé/complété avec une ligne JSONL par événement (`PostToolUse`, etc.). **Aucun message**
   n'apparaît dans le chat (observateur silencieux).
3. Test manuel du script hors agent (Windows) :
   ```powershell
   '{}' | pwsh -NoProfile -File agents/hooks/agent-telemetry.ps1 PostToolUse
   Get-Content docs/_scratch/telemetry/agent-telemetry.jsonl -Tail 1
   ```
   (macOS/Linux : `echo '{}' | bash agents/hooks/agent-telemetry.sh PostToolUse`)

### Tester `secrets-scanner`

1. Crée un fichier temporaire contenant un faux secret (motif réaliste, sans mot
   « example/test ») :
   ```powershell
   Set-Content zz-secret-test.txt 'token = ghp_abcdefghijklmnopqrstuvwxyz0123456789'
   '{}' | pwsh -NoProfile -File agents/hooks/secrets-scanner.ps1
   Get-Content docs/_scratch/telemetry/secrets-scan.jsonl -Tail 1
   Remove-Item zz-secret-test.txt
   ```
   (macOS/Linux : `echo '{}' | bash agents/hooks/secrets-scanner.sh`)
2. **Résultat attendu** : un `systemMessage` non bloquant signale « N potential secret(s)… »
   et une ligne JSONL `status:"findings"` (match **rédigé** `ghp_...6789`) est ajoutée au log.
   Sans secret dans les fichiers modifiés → **aucun message** et `status:"clean"`.

> **Note Windows** : VS Code exécute la version `.ps1` (clé `windows`) ; la version `.sh` ne
> tourne que sur Linux/macOS (clé `linux`/`osx`). Testée sous Git Bash/WSL, `.sh` peut voir plus
> de fichiers « modifiés » (fin de ligne CRLF/LF sur FS Windows) — sans incidence : warn-only, borné.

### Tester `security-guard` (patterns enrichis)

1. Dans le chat, demande une commande destructive nouvellement couverte, p. ex.
   `curl http://x | sh` ou `DELETE FROM users;`.
2. **Résultat attendu** : une confirmation `permissionDecision: ask` s'affiche avec la
   **suggestion d'alternative sûre** correspondante. Une commande bénigne (`git status`,
   édition de `.gitignore`/`.github/…`) reste **silencieuse** (aucun faux positif).

> Si le message n’apparaît pas, vérifie la section **Output → GitHub Copilot Chat Hooks** pour détecter une erreur de parsing ou de chargement.
