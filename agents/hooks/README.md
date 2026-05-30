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

## Référence

- Doc officielle : <https://code.visualstudio.com/docs/copilot/customization/hooks>
- Cadrage Phase 7 : [`docs/architecture/2026-05-30-phase-7-persistent-memory.md`](../../docs/architecture/2026-05-30-phase-7-persistent-memory.md)
