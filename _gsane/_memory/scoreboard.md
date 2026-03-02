# GSANE Scoreboard

> Généré automatiquement par flywheel-aggregate — ne pas éditer manuellement.
> Overwritten à chaque cycle flywheel.
> Cycle initial : 2026-03-01 | Sessions analysées : 5 | Total : 6

---

## 📊 Agent Performance

| Agent | Sessions Actives | Compliance | Token Impact | Prompt Signals | Score |
|---|---|---|---|---|---|
| gsane-master | 6 | 83% | medium | none yet | A |
| aria (qa-gsane) | 6 | 83% | low | none yet | A |
| leo (gsane-optimizer) | 6 | 83% | low | none yet | A |
| murat (tea) | 1 | 100% | low | none yet | A+ |
| bond (agent-builder) | 1 | 100% | low | none yet | A+ |
| wendy (workflow-builder) | 1 | 100% | low | none yet | A+ |
| morgan (module-builder) | 1 | 100% | low | none yet | A+ |
| carson (brainstorming) | 1 | 100% | low | none yet | A+ |
| victor (innovation) | 1 | 100% | low | none yet | A+ |
| dr-quinn (problem-solver) | 1 | 100% | low | none yet | A+ |
| maya (design-thinking) | 1 | 100% | low | none yet | A+ |
| caravaggio (presentation) | 1 | 100% | low | none yet | A+ |
| sophia (storyteller) | 1 | 100% | low | none yet | A+ |

**Scoring :** A+ = 100% compliance + low token | A = ≥80% | B = 60-80% ou medium token | C = <60% ou high severity flagué

---

## 📋 Workflow Performance

| Workflow | Exécutions | Corrections Générées | Patterns Flagués | Score |
|---|---|---|---|---|
| post-session-analysis | 6 | 3 | 5 (unnecessary-load, manifest-sync, config-reload-waste) | A |
| party-mode | 2 | 0 | 3 (profile-overload, unnecessary-load) | B+ |
| flywheel-aggregate | 1 | 2 | 0 | A+ |
| flywheel-apply | 1 | 2 | 0 | A+ |
| git-workflow | 3 | 0 | 0 | A+ |
| delegation | 4 | 0 | 0 | A+ |

---

## 📝 Prompt Health

| Catégorie | Total | Corrections ce cycle | Améliorations confirmées | Santé |
|---|---|---|---|---|
| agents (.github/prompts/gsane-agent-*) | 13 | 0 | 0 | ✅ Sain |
| workflows (.github/prompts/gsane-*workflow*) | 3 | 0 | 0 | ✅ Sain |
| skills (.github/skills/**/SKILL.md) | 3 | 1 (JIT Protocol ajouté) | 0 | ✅ Amélioré |

> ⚠️ **Note** : `prompt_improvement_signals` commence à être collecté à partir de la session 7.
> Les cycles suivants auront des données observées versus les cycles précédents pour validation croisée.

---

## 🔄 Flywheel Métriques

| Métrique | Valeur |
|---|---|
| Cycle actuel | 1 |
| Sessions par cycle | 5 |
| Compliance globale | 83% |
| Trend | stable ➡️ (1er cycle — pas de baseline comparative) |
| Dernier cycle | 2026-03-01 |
| Prochain déclenchement | session 10 |
| Auto-corrections ce cycle | 2 |
| High severity manuelle | 0 |
| Deferred | 0 |

---

## 🧪 Validation Flywheel

- [x] Cycle 1 déclenché correctement à session 5
- [x] workflow-aggregate exécuté → flywheel-report.md écrit
- [x] workflow-apply exécuté → 2 corrections appliquées
- [x] flywheel-history.md mis à jour
- [ ] prompt_improvement_signals collectés (début session 7)
- [ ] Comparaison cross-cycle disponible (début cycle 2, session 10)
