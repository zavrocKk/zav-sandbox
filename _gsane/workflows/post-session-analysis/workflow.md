# Post-Session Analysis Workflow

**Workflow ID:** post-session-analysis
**Trigger:** Automatically at the end of EVERY session with ANY GSANE agent, before dismissal.
**Mode:** Silent — no user interaction required. Run and output a single status line.

---

## STEP 1 — Collect session data

Extract from current session context:
- `{session_date}` — today's date (YYYY-MM-DD)
- `{agent_active}` — which agent was active this session
- `{workflow_run}` — which workflow(s) were executed (comma-separated)
- `{tasks_completed}` — list of tasks marked done
- `{budget_consumed_end}` — budget consommé en fin de session (pourcentage ou ratio observé)
- `{tokens_observed}` — any token/context patterns worth noting (optional)
- `{issues_encountered}` — any errors, dead paths, or blockers (optional)

## STEP 2 — Update session state

Write to `_gsane/_memory/sessions/session-state.md`:
- Update `last_session_date` with `{session_date}`
- Update `last_agent_active` with `{agent_active}`
- Update `last_workflow_run` with `{workflow_run}`
- Update `next_step` with a concise 1-sentence summary of what to do next

If `session-state.md` does not exist, create it with template fields.

Important: `session-state.md` is an audit/continuité file. It must not be treated as the current project truth by active runtime surfaces.

## STEP 3 — Append to session analysis log

Append the following block to `_gsane/_memory/sessions/session-analysis-log.md`:

```
## Session: {session_date} — Agent: {agent_active}
- workflows_run: [{workflow_run}]
- tasks_completed: [{tasks_completed}]
- budget_consumed_end: {budget_consumed_end}
- circuit_breaker_triggered: false
- hup_rouge_count: 0
- trust_score_avg: null
- sage_recommended: false
- compliance: PASS | FAIL
- corrections_applied: []
- open_items: []
- notes: "{tokens_observed} | {issues_encountered}"
```

Important: `session-analysis-log.md` is an audit trail for PSA and flywheel. It is not a source of truth for the present state of the project.

## STEP 3b — Recommandation budget sur tendance

1. Lire les 3 dernières sessions disponibles dans `_gsane/_memory/sessions/session-analysis-log.md`
2. Calculer la moyenne de `budget_consumed_end`
3. Comparer cette moyenne au seuil warning du budget (`context_budget.warning_threshold`, soit 75% par défaut)
4. Si la moyenne des 3 dernières sessions est > 75% du budget, écrire `sage_recommended: true` dans la nouvelle entrée
5. Sinon, conserver `sage_recommended: false`

## STEP 3b-bis — Filtres d'événements exclus

Les event_types suivants ne sont PAS analysés comme patterns d'optimisation token et sont exclus de toute recommandation d'auto-correction :
- `benchmark_result`
- `benchmark_regression`
- `mutation_score`
- `mutation_survivor`

Ces events sont des métriques de qualité (propriété Quinn). Ils ne signalent pas de gaspillage token ni d'inefficience à optimiser. Le flywheel et le post-session NE DOIVENT PAS recommander de les réduire ou de les éliminer.

## STEP 3c — Détection solo-creep

SOLO-CREEP est détecté (sévérité **HIGH** systématique) si AU MOINS UN de ces critères est vrai :

1. **Fichier modifié hors périmètre** : Langis a modifié un fichier `.py`, `.sh`, `.yaml`, ou `.md` hors de `_gsane-output/` et `_gsane/_memory/` sans DC actif référencé.
2. **Code produit sans DC** : Langis a produit du code dans sa réponse sans Delivery Contract référencé.
3. **Agent modifié sans Bond** : Langis a modifié un fichier `_gsane/agents/*.md` sans que Bond soit impliqué (via `runSubagent`).
4. **Workflow modifié sans Winston** : Langis a modifié un fichier `_gsane/workflows/**/*.md` sans que Winston soit impliqué (via `runSubagent`).

**Action sur détection** :
- Logger `solo_creep_alert: HIGH` dans l'entrée session-analysis-log.md
- Ajouter `open_items: ["SOLO-CREEP détecté — critère {N} — revoir délégation"]`
- Si aucun critère déclenché : logger `solo_creep_alert: NOMINAL`

## STEP 4 — Check flywheel trigger

1. Count total `## Session:` headers in `_gsane/_memory/sessions/session-analysis-log.md`
2. Read `flywheel.trigger_every_n_sessions` from `_gsane/config.yaml` (default: 5)
3. If `session_count % trigger_every_n_sessions == 0` → trigger flywheel workflow (`_gsane/workflows/flywheel/workflow.md`)
4. Otherwise → skip flywheel

## STEP 5 — Output status line

Output exactly one line:
```
[PSA] ✅ Session logged — {session_date} | Agent: {agent_active} | Next: {next_step}
```

If flywheel triggered: append `| 🔄 Flywheel triggered`

## STEP 6 — Afficher le rapport

Afficher le rapport : `bash gsane.sh session --report`

---

**Output:** Single status line (never verbose unless flywheel fires).

---

## Note : Intégration flywheel

Après écriture de l'entrée dans session-analysis-log.md, POST-SESSION-ANALYSIS doit :
1. Lire `_gsane/_memory/.session_count` et incrémenter de 1
2. Comparer avec `_gsane/config.yaml → flywheel.trigger_every_n_sessions` (défaut : 5)
3. Si session_count % trigger_every_n_sessions == 0 → appeler `.github/hooks/flywheel-trigger.sh`
4. Cette logique garantit que le flywheel se déclenche automatiquement sans intervention humaine.
