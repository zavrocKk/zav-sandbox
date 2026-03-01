# Flywheel End-to-End Test Checklist

> Utilisé par Murat (TEA) pour valider que le Cognitive Flywheel fonctionne à tout coup.
> Exécuter manuellement ou via Murat en mode test.

---

## 🧪 Test 1 — Déclenchement du compteur (Step 6 de post-session-analysis)

**Objectif :** Vérifier que session_count est calculé et que le trigger se déclenche au bon moment.

**Procédure :**
1. Ouvrir `_bmad/_memory/session-analysis-log.md`
2. Compter le nombre de headers `## Session:`
3. Diviser par `trigger_every_n_sessions` (config = 5)
4. Vérifier que le ratio est entier → le flywheel DOIT avoir tiré

**Gate Murat :**
- [ ] session_count % 5 == 0 → marker `## 🔄 FLYWHEEL TRIGGERED` présent dans le log
- [ ] Le marker apparaît AVANT l'entrée de session qui a déclenché le cycle
- [ ] `Status: ✅ complété` dans le marker (pas `running`)

**Résultat attendu :** ✅ PASS si markers présents et count exact

---

## 🧪 Test 2 — Écriture du flywheel-report.md (workflow-aggregate Step 5)

**Objectif :** Vérifier que le rapport est généré avec les bonnes données.

**Procédure :**
1. Lire `_bmad/_memory/flywheel-report.md`
2. Vérifier que `sessions_analyzed` == trigger_n (5)
3. Vérifier que les patterns CONFIRMED ont ≥3 occurrences dans le log
4. Vérifier que les patterns NOISE (1 occurrence) sont absents du rapport

**Gate Murat :**
- [ ] `generated:` date == date de la session qui a déclenché le cycle
- [ ] Chaque pattern CONFIRMED a count ≥ 3 (vérifiable dans les entrées Léo du log)
- [ ] Aucun pattern avec count=1 dans le rapport
- [ ] `Status: pending` présent pour les corrections non encore appliquées

**Résultat attendu :** ✅ PASS si rapport cohérent avec le log

---

## 🧪 Test 3 — Application des corrections (workflow-apply Step 4)

**Objectif :** Vérifier que les corrections low/medium sont auto-appliquées et que high != auto-applied.

**Procédure :**
1. Lire l'historique `_bmad/_memory/flywheel-history.md`
2. Vérifier que le cycle le plus récent a `Applied > 0` pour corrections low/medium
3. Vérifier qu'aucune correction `high` n'apparaît dans "Applied"
4. Vérifier que le nombre de corrections ≤ 5 (Gate 1)

**Gate Murat :**
- [ ] Corrections low/medium → status `applied` dans history
- [ ] Corrections high → status `manual review required`, pas `applied`
- [ ] count(applied) ≤ 5 (Gate 1 Murat respectée)
- [ ] Branch `fix/flywheel-{date}` créée (vérifiable avec `git branch -a`)
- [ ] PR créée avec body complet (pas une URL vide)

**Résultat attendu :** ✅ PASS si gates respectées

---

## 🧪 Test 4 — Prompt Improvement Tracking (NEW)

**Objectif :** Vérifier que le signal `prompt_improvement_signals` est collecté et corrélé.

**Procédure :**
1. Après une session où vous observez une amélioration de réponse agent
2. Vérifier que l'entrée de session dans le log contient `📈 Prompt Signals`
3. Après le prochain cycle flywheel, vérifier dans `flywheel-history.md` que les signaux `flywheel-prompt-confirmed` sont listés

**Gate Murat :**
- [ ] Section `📈 Prompt Signals` présente dans les nouvelles entrées de session
- [ ] Signal `flywheel-prompt-confirmed` ou `prompt-quality-up` capturé si vous avez commenté positivement
- [ ] `scoreboard.md` → colonne "Améliorations confirmées" > 0 après cycle 2

**Résultat attendu :** ✅ PASS après cycle 2 (session 10+)

---

## 🧪 Test 5 — Scoreboard Cohérence

**Objectif :** Vérifier que le scoreboard reflète fidèlement les données du log.

**Procédure :**
1. Lire `_bmad/_memory/scoreboard.md`
2. Pour chaque agent, compter manuellement ses sessions dans le log
3. Calculer le taux de compliance (PASS / total)
4. Comparer avec le scoreboard

**Gate Murat :**
- [ ] Sessions actives par agent cohérentes avec le log (±1 tolérance)
- [ ] Compliance rate cohérent (±5% tolérance)
- [ ] Score correct selon la formule : A+ 100%/low, A ≥80%, B 60-80%, C <60%
- [ ] Prochain déclenchement = session_count actuel + (trigger_n - session_count % trigger_n)

**Résultat attendu :** ✅ PASS si données cohérentes

---

## 🧪 Test 6 — Test de Régression (après chaque cycle)

**Objectif :** Vérifier que le flywheel n'introduit pas de régression dans les fichiers corrigés.

**Procédure :**
1. Lire chaque fichier modifié par le dernier cycle
2. Vérifier que le frontmatter YAML est intact
3. Vérifier qu'aucune variable `{project-root}` est brisée
4. Vérifier qu'aucun chemin déprécié `_bmad/bmm/` n'a été réintroduit

**Gate Murat (Gate 3 de workflow-apply) :**
- [ ] YAML frontmatter intact dans tous les fichiers modifiés
- [ ] Variables `{project-root}`, `{communication_language}` non brisées
- [ ] Chemins `_bmad/core/` (pas `_bmad/bmm/`) dans tous les fichiers modifiés
- [ ] `get_errors` → 0 erreurs après corrections

**Résultat attendu :** ✅ PASS sur tous les fichiers modifiés

---

## 📊 Résumé des Tests

| Test | Statut | Dernière exécution | Notes |
|---|---|---|---|
| T1 — Compteur & trigger | ✅ PASS | 2026-03-01 | Cycle 1 déclenché session 5 |
| T2 — flywheel-report.md | ✅ PASS | 2026-03-01 | 2 patterns CONFIRMED |
| T3 — Auto-corrections | ✅ PASS | 2026-03-01 | 2 corrections, 0 high auto-applied |
| T4 — Prompt signals | ⏳ PENDING | — | début session 7+ |
| T5 — Scoreboard cohérence | ✅ PASS | 2026-03-01 | Cycle 1 initial |
| T6 — Régression | ✅ PASS | 2026-03-01 | 0 régression introduite |

---

## 🔧 En cas d'échec

| Symptôme | Cause probable | Action |
|---|---|---|
| Marker FLYWHEEL TRIGGERED absent | Step 6 post-session non exécuté | Vérifier que DA est câblé dans l'agent |
| flywheel-report.md vide | workflow-aggregate non chargé | Vérifier le chemin dans config.yaml |
| Corrections jamais appliquées | Gate 1 ou 2 bloquée | Lire flywheel-history.md → "Failed" section |
| Scoreboard non mis à jour | workflow-aggregate Step 5b sauté | Re-exécuter workflow-aggregate manuellement |
| Prompt signals = "none" toujours | Léo ne détecte pas les signaux | Vérifier que post-session Step 2 inclut `prompt_improvement_signals` |
