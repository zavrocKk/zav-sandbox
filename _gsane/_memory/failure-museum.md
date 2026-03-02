# 🏛️ Failure Museum — GSANE

> Mémoire collective des défaillances. Chaque pattern documenté ici **ne doit plus jamais se reproduire**.
> Format : ID | Pattern | Root Cause | Résolution | Date | Agent
> Mise à jour : automatique via `post-session-analysis` (Step 2b) + manuelle si HIGH severity.

---

## Comment utiliser ce fichier

**Avant tout commit / implémentation :**
Vérifier : « Ce pattern a-t-il déjà échoué ici ? »
→ Si oui → appliquer la résolution documentée, ne pas répéter l'erreur.

**À chaque violation HIGH :**
L'agent qui détecte la violation doit ajouter une entrée ici AVANT de loguer dans `session-analysis-log.md`.

---

## Catalogue des défaillances

---

### FM-001 — Solo Execution sur actions GSANE

| Champ | Valeur |
|---|---|
| **ID** | FM-001 |
| **Pattern** | Exécution directe de `git add/commit/push` ou modification de fichiers GSANE sans passer par Party Mode ni vérifier la matrice de délégation |
| **Root Cause 1** | Absence d'entrée dans `agent-delegation-matrix.csv` pour les mots-clés `implement`, `fix`, `git commit` |
| **Root Cause 2** | PRE-EXECUTION GATE implicite — existait en prose, non traité comme règle prioritaire bloquante |
| **Root Cause 3** | `git-workflow/workflow.md` n'avait pas de Step 0 — l'IA entrait dans le workflow sans vérification préalable |
| **Résolution** | PRE-EXECUTION GATE ajouté comme **première section** de `copilot-instructions.md` + Step 0 ajouté dans git-workflow + keywords `git commit;git add;git push` dans `implement-changes` de la matrice |
| **Fichiers corrigés** | `.github/copilot-instructions.md`, `_gsane/core/workflows/git-workflow/workflow.md`, `_gsane/_config/agent-delegation-matrix.csv` |
| **Date** | 2026-03-01 |
| **Agents impliqués** | Gsane Master (party: Aria, Léo, Wendy) |
| **Sévérité** | HIGH |
| **Statut** | ✅ Corrigé — commit `c78844a` |

---

### FM-002 — Fichiers _bmad orphelins non trackés dans Git

| Champ | Valeur |
|---|---|
| **ID** | FM-002 |
| **Pattern** | Des centaines de fichiers GSANE (`.github/agents/gsane-*`, `.github/prompts/gsane-*`, `_gsane/`) existaient localement mais n'avaient jamais été `git add`-és. Ils n'apparaissaient pas sur GitHub. |
| **Root Cause** | Le refactoring BMAD→GSANE a créé les nouveaux fichiers sans les stager. L'ancien `git add -u` (lors du nettoyage _bmad) ne stage que les fichiers déjà trackés — les nouveaux sont ignorés. |
| **Résolution** | `git add _gsane/ .github/agents/gsane-* .github/prompts/gsane-*` explicite + vérification `git ls-files` avant tout push |
| **Prévention** | Après tout refactoring, toujours exécuter `git status --short` et vérifier les `??` (untracked) |
| **Fichiers corrigés** | 507 fichiers ajoutés — `_gsane/`, `.github/agents/gsane-*`, `.github/prompts/gsane-*` |
| **Date** | 2026-03-01 |
| **Agents impliqués** | Gsane Master |
| **Sévérité** | HIGH |
| **Statut** | ✅ Corrigé — commit `fix/track-gsane-directory-2026-03-01` |

---

### FM-003 — Commits multi-sujets sur une seule branche

| Champ | Valeur |
|---|---|
| **ID** | FM-003 |
| **Pattern** | Plusieurs changements de nature différente (governance fix + gh CLI removal + docs + cleanup) committés sur la même branche `feature/project-a1-audit-fixes-2026-03-01` |
| **Root Cause** | Absence de règle explicite "1 branche = 1 unité logique" dans `git-workflow/workflow.md` et `CONTRIBUTING.md` |
| **Résolution** | Règle ajoutée dans Step 2 de git-workflow (callout ⚠️) + §3 dans CONTRIBUTING.md avec exemples ✅/❌ et exception documentée |
| **Fichiers corrigés** | `_gsane/core/workflows/git-workflow/workflow.md`, `CONTRIBUTING.md` |
| **Date** | 2026-03-01 |
| **Agents impliqués** | Gsane Master (party: Aria, Wendy) |
| **Sévérité** | MEDIUM |
| **Statut** | ✅ Corrigé — commit `ec374cf` |

---

### FM-004 — GitHub CLI (`gh`) introducit sans validation

| Champ | Valeur |
|---|---|
| **ID** | FM-004 |
| **Pattern** | La commande `gh pr create` a été ajoutée dans `git-workflow/workflow.md` sans vérifier si Mon Seigneur utilisait cet outil, créant une dépendance non souhaitée |
| **Root Cause** | Ajout automatique lors d'un fix CI sans Party Mode — aucun agent n'a validé la nouvelle dépendance externe |
| **Résolution** | Toutes les références `gh` CLI supprimées de 7 fichiers — les PRs se créent via URL compare GitHub + body template collé manuellement |
| **Prévention** | Toute nouvelle dépendance outil externe (CLI, MCP, extension) = sévérité HIGH = Party Mode obligatoire |
| **Fichiers corrigés** | `git-workflow/workflow.md`, `flywheel/workflow-apply.md`, `README.md`, `copilot-instructions.md`, `validate-pr.yml`, `gsane-framework/SKILL.md`, `hooks/hooks.json` |
| **Date** | 2026-03-01 |
| **Agents impliqués** | Gsane Master (party: Aria, Léo) |
| **Sévérité** | MEDIUM |
| **Statut** | ✅ Corrigé — commit `0afec4d` |

---

## Ajouter une entrée

Copier ce template :

```markdown
### FM-XXX — {Titre court}

| Champ | Valeur |
|---|---|
| **ID** | FM-XXX |
| **Pattern** | Description du comportement défaillant observé |
| **Root Cause** | Cause racine identifiée |
| **Résolution** | Ce qui a été fait pour corriger |
| **Prévention** | Comment éviter que ça se reproduise |
| **Fichiers corrigés** | Liste des fichiers modifiés |
| **Date** | YYYY-MM-DD |
| **Agents impliqués** | Agent(s) responsable(s) |
| **Sévérité** | LOW / MEDIUM / HIGH |
| **Statut** | ✅ Corrigé / 🔄 En cours / ⚠️ Ouvert |
```
