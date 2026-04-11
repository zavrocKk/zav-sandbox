# 🤝 Guide de Contribution — GSANE Strike Team

Ce document fixe les règles de développement pour la Strike Team.  
Tout contributeur humain ou agent IA **DOIT** s'y conformer strictement.

---

## 📖 Concepts Clés

| Terme | Définition |
|---|---|
| **Delivery Contract** | Document Markdown formel (rédigé par *Langis/Master*) fixant les critères d'acceptation avant toute ligne de code |
| **Zero-Touch Fix-Loop** | QA renvoie les erreurs à Dev jusqu'à Exit 0 — sans intervention humaine |
| **Quality Gate** | `bash gsane.sh validate` — exécute pytest + qa-linter + vérification CHANGELOG |
| **Party Mode** | Mode de brainstorming structuré : Niveau 1 Huddle → APPROVE/BLOCK, Niveau 2 Devil's Advocate |

---

## 💻 Setup Développeur

Voir le [README.md](README.md) pour l'installation complète.

Installation rapide : `pip install -e ".[mcp,test]"`

Avant tout commit :
```bash
# Quality Gate locale (structurelle + MCP, sans les tests comportementaux shell)
bash gsane.sh validate

# Vérification MCP
bash gsane.sh mcp --health

# Tests complets (incluant comportementaux — nécessite Git Bash)
python -m pytest tests/
```

### Prérequis Windows

`bash gsane.sh` requiert un environnement Bash. Options :

| Option | Commande | Notes |
|--------|----------|-------|
| **WSL (recommandé)** | `wsl --install -d Ubuntu` | Aligné avec le CI GitHub Actions (Ubuntu) |
| **Git Bash** | `"C:\Program Files\Git\bin\bash.exe" gsane.sh validate` | Fonctionne pour la plupart des commandes |
| **CI uniquement** | Pousser sur branche feature, le CI valide | Aucune dépendance locale requise |

Sans Bash, la validation structurelle Python reste accessible directement :
```powershell
python -m pytest tests/ -m "not behavioral"
```

Le CI GitHub Actions est la **validation de référence** — `gsane.sh doctor` affiche un warning si WSL/Bash n'est pas détecté.

---

## 🔄 Workflow Git — OBLIGATOIRE

### Règle absolue : jamais de commit direct sur `main`

```
Créer branche → Commit → Push → Ouvrir PR → Merge après review
```

**Nommage des branches :**
- `feature/{description}-{date}` — nouvelle fonctionnalité
- `fix/{description}-{date}` — correction de bug

Le nom de branche doit décrire le **problème corrigé** ou la **valeur ajoutée** — pas le mécanisme interne.

| ✅ Bon | ❌ Mauvais |
|---|---|
| `fix/prevent-narrative-solo-creep` | `feature/agent-signature-001` |
| `fix/routing-false-positives` | `fix/dc-context-opt-002` |
| `feat/agent-session-report` | `feat/p6-batch1` |
| `feat/jit-skills-applyto` | `fix/rigor-2-sprint-2026-04-10` |

**Format des commits (Conventional Commits) :**
```
feat(core): ajout de la fonction X
fix(mcp): correction du chemin relatif dans compression_tool
chore(deps): mise à jour de mcp[cli]
```

**PRs :**
- Description obligatoire (titre + corps template)
- Jamais de PR avec description vide

---

## 🛡️ Qualité et TDD

- Tout code dans `src/` exige des tests associés dans `tests/`
- Toute nouvelle fonctionnalité finalisée dans `src/` doit avoir une entrée dans `CHANGELOG.md`
- Les agents GSANE sont couverts par `tests/qa-linter.py` (structure, legacy refs, hooks, manifests)
- Les outils MCP sont couverts par `tests/test_mcp.py` (imports, paths, smoke tests)
- Les Delivery Contracts sont validés structurellement par `bash gsane.sh dc --validate <fichier.md>`

---

## 🤖 Modifier un Agent GSANE

1. Éditer `_gsane/agents/{nom-agent}.md`
2. Mettre à jour `_gsane/_config/agent-manifest.yaml`
3. Bumper la `version` (semver X.Y.Z) et `updated_at` dans `agent-manifest.yaml`
4. Si nouvelles routes : mettre à jour `_gsane/_config/delegation-matrix.yaml` (schéma : `trigger` + `agent`)
5. Relancer `bash gsane.sh validate`

Règles supplémentaires obligatoires :
- Les 8 sections sont obligatoires pour TOUS les agents, y compris les subagents. Si une section manque, `tests/qa-linter.py` doit échouer.
- Tout nouvel agent doit avoir un fichier `.customize.yaml` dédié dans `_gsane/_config/agents/`.
- Chaque `.customize.yaml` doit contenir au minimum `agent`, `status`, `scope` et `constraints` avec des valeurs non vides et cohérentes avec le manifest.

**Ne jamais bypasser Party Mode** pour les modifications non-triviales aux agents.

---

## 🔌 Modifier le Serveur MCP

Le point d'entrée unique est `_gsane/mcp-server/compression_tool.py`.  
`server.py` est archivé — **ne pas l'utiliser**.

Règles :
- Tous les chemins fichiers via `Path(__file__).parent.parent / "..."` — jamais de chemins relatifs au cwd
- Tout nouvel outil doit appeler `_log_mcp_invocation()` pour la traçabilité
- Tout nouvel outil doit avoir un test dans `tests/test_mcp.py`
- Après modification : `bash gsane.sh mcp --smoke-test`

---

## 💬 Communication

Bug ou changement architectural : ouvrir une **Issue** GitHub ou lancer `@Langis` dans Copilot Chat.
