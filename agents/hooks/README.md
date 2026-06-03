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
| `security-guard.ps1` / `.sh` | `PreToolUse` | Scanne la commande avant exécution ; sur pattern destructif (`rm -rf`, `DROP TABLE`, `git push --force`, `--no-verify`, `terraform destroy`, `kubectl delete`…) → renvoie `permissionDecision: ask` (confirmation requise). **N'exécute jamais la commande.** | 🟢 nul |
| `memory-nudge.ps1` / `.sh` | `PreCompact` + `Stop` | `systemMessage` non bloquant : rappelle de lancer `/checkpoint` avant compaction/fin de session. **Ne bloque pas l'agent** (pas de `decision: block`). | 🟢 nul |

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

> Si le message n’apparaît pas, vérifie la section **Output → GitHub Copilot Chat Hooks** pour détecter une erreur de parsing ou de chargement.
