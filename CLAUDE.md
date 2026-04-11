# CLAUDE.md — zav-sandbox

> Instructions pour Claude Code. Lire ce fichier en premier avant toute action.

## Projet

**zav-sandbox** — Framework GSANE (Governance System for AI-Native Execution).
Système multi-agents à 5 agents core (Strike Team) orchestré par Langis (Master).

- **Propriétaire** : Mon Seigneur
- **Langue de communication** : Français
- **Langue des documents** : Français
- **Dossier de sortie** : `_gsane-output/`

## Structure

```
_gsane/                       ← Runtime GSANE
  agents/                     ← 5 agents : master, dev, qa, architect, bond
  workflows/                  ← Workflows actifs (markdown exécutable)
  _config/                    ← Manifestes YAML, delegation-matrix, agent-manifest
  _memory/                    ← Mémoire persistante (failure-museum, decision-log, trace)
  tools/                      ← Outils CLI (security_gate.py, flywheel-rollback.sh)
_gsane-output/                ← Artefacts générés (Delivery Contracts, audits)
src/                          ← Code applicatif Python
tests/                        ← Tests pytest (unit/, integration/, compliance/, performance/, e2e/)
.github/workflows/            ← CI/CD GitHub Actions
```

## Commandes essentielles

```bash
bash gsane.sh validate        # Quality gate : pytest + qa-linter + CHANGELOG check
bash gsane.sh vera            # Security checks : prompt injection + CI permissions
bash gsane.sh benchmark       # Benchmarks MCP (4 métriques)
bash gsane.sh mutation        # Mutation testing sur src/
bash gsane.sh doctor          # Health check global
bash gsane.sh dc --validate   # Valider un Delivery Contract
bash gsane.sh trace --summary # Métriques agrégées depuis trace.log
```

## Tests

```bash
pytest tests/ -q                              # Tous les tests (190+)
pytest tests/unit/ -m unit                    # Tests unitaires
pytest tests/integration/ -m integration      # Tests intégration
pytest tests/compliance/ -m compliance        # Tests conformité GSANE
pytest tests/performance/ -m benchmark        # Benchmarks
```

Markers : `unit`, `integration`, `compliance`, `behavioral`, `benchmark`, `token_budget`.

## Conventions

### Git
- **Jamais** de commit direct sur `main` — toujours branche `feature/*` ou `fix/*`
- Conventional Commits : `feat(scope):`, `fix(scope):`, `chore(scope):`, `docs(scope):`
- PR obligatoire avec description remplie
- CHANGELOG.md mis à jour pour tout changement dans `src/` ou `_gsane/`

### Code
- Python 3.11+ compatible
- `ruff check .` doit passer (import sorting I001 inclus)
- `bandit -r src/ _gsane/mcp-server/ _gsane/tools/ -ll` pour SAST
- `pythonpath` configuré dans `pyproject.toml` — pas de `sys.path.insert`
- `# nosec B603 B607` format espace-séparé pour Bandit

### GSANE
- **Delivery Contract requis** avant toute implémentation modifiant ≥1 fichier
- **TDD strict** : code et tests livrés ensemble
- **5 agents core** : Langis (Master), Amelia (Dev), Quinn (QA), Winston (Architect), Bond (Builder)
- **Delegation obligatoire** : Langis ne code pas, ne teste pas — il orchestre
- **JIT Loading** : charger uniquement ce qui est nécessaire, quand c'est nécessaire

## Strike Team

| Agent | Rôle | Spécialité |
|-------|------|------------|
| 🧙 Langis (Master) | Orchestrateur | Delivery Contracts, routage, arbitrage |
| 💻 Amelia (Dev) | Développeur | TDD, implémentation, chaque ligne trace vers un AC |
| 🧪 Quinn (QA) | QA Engineer | Quality gate, PASS/FAIL binaire |
| 🏗️ Winston (Architect) | Architecte | Design système, ADR, outillage, CI/CD |
| 🤖 Bond (Builder) | Agent Builder | Création/validation agents GSANE |

## Configuration

- Config globale : `_gsane/config.yaml`
- Manifeste agents : `_gsane/_config/agent-manifest.yaml`
- Matrice de routage : `_gsane/_config/delegation-matrix.yaml`
- Manifeste workflows : `_gsane/_config/workflow-manifest.yaml`

## Sécurité

- SHA-pin toutes les GitHub Actions
- `security_gate.py` : scan secrets, Bandit, pip-audit, prompt injection, CI permissions
- Pas de secrets hardcodés — jamais
- `bash gsane.sh vera` avant tout merge

## Workflows clés

| Workflow | Déclencheur | Fichier |
|----------|-------------|---------|
| Delegation | Toute requête agent | `_gsane/workflows/delegation/workflow.md` |
| CC-Verify | Avant déclaration terminé | `_gsane/workflows/cc-verify/workflow.md` |
| Git Workflow | Tout commit GSANE | `_gsane/workflows/git-workflow/workflow.md` |
| Party Mode | Changement GSANE | `_gsane/workflows/party-mode/workflow.md` |
| Post-Session | Fin de session | `_gsane/workflows/post-session-analysis/workflow.md` |
| Flywheel | Tous les N sessions | `_gsane/workflows/flywheel/workflow.md` |

## Mémoire

- `_gsane/_memory/failure-museum.md` — Catalogue des erreurs passées (append-only)
- `_gsane/_memory/decision-log.md` — Décisions architecturales
- `_gsane/_memory/trace.log` — JSONL événements runtime
- `_gsane/_memory/sessions/` — État de session et logs d'analyse

## Ne jamais faire

- Commiter sur `main` directement
- Modifier des fichiers GSANE sans Delivery Contract
- Ignorer un test rouge
- Utiliser `sys.path.insert` (pythonpath dans pyproject.toml)
- Pousser sans `bash gsane.sh validate` → EXIT 0
- **Merger une PR, push --force, ou supprimer une branche distante sans approbation explicite de l'utilisateur**
