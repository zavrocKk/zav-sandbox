═══════════════════════════════════════════════
  FIELD REPORT — Agentic Team
═══════════════════════════════════════════════

Date : 2026-05-04 → 2026-05-08
Type de tâche : [ ] incident   [ ] change   [ ] audit
                [ ] doc       [ ] analyse  [x] autre : observations multi-sessions sur 5 jours
Workflow utilisé : multi-workflows (audit, incident-response, ADR, cleanup)
Durée totale (prompt → livrable) : ~5 jours d'observations cumulées

───────────────────────────────────────────────
1. CE QUI A MARCHÉ (1-3 bullets)
   • Analyse, bilans et documentation de qualité
   • Suit bien les instructions et incarne ses personas à la demande

───────────────────────────────────────────────
2. CE QUI A FRICTIONNÉ (1-3 bullets)
   • Mémoire/contexte fragiles et outillage mal exploité (sessions longues qui perdent le fil, pas de connexion native aux outils, mauvais agent invoqué pour certaines tâches)
   • Discipline de production absente (artefacts placés n'importe où, aucun standard de template pour les bilans, exécute parfois un prompt ambigu sans demander clarification)
   • Coût en tokens élevé (Orchestrator reste lui-même au lieu de déléguer, demandes de confirmation à chaque étape qui multiplient les prompts)

───────────────────────────────────────────────
3. SCORE QUALITATIF (entoure)
   1 = inutilisable   2 = frustrant   3 = ok
   4 = bon            5 = excellent

   Score :  1   2  (3)  4   5

   En 1 ligne, pourquoi ce score :
   Exécute toujours la demande mais peu autonome (reprises fréquentes) ; faible intégration outils + coût tokens élevé pèsent fortement.

───────────────────────────────────────────────
4. RÔLE DU FRAMEWORK
   J'aurais fait ça à la main en :  plusieurs heures (~2× le temps avec framework, framework livrant en quelques minutes)
   Avec une qualité :  [ ] inférieure  [ ] équivalente  [x] supérieure
   → Verdict ROI :  [x] gain  [ ] neutre  [ ] perte

───────────────────────────────────────────────
5. NOTE LIBRE pour Claude (idée, friction, surprise)
   Surprise mi-utile mi-rebelle : sorti du dossier projet pour piocher des skills d'un autre repo
   afin d'utiliser l'outil AWS, sans instruction. Questionne le périmètre d'autonomie acceptable.
═══════════════════════════════════════════════
