# Roadmap — Agentic Team Framework

Document de référence sur l'avancement du projet et les prochaines étapes.
Mis à jour au fur et à mesure des sessions avec Claude.

## Vue d'ensemble

✅ Phase 0 — Setup
✅ Phase 1 — Fiabilité
✅ Phase 2 — Templates
✅ Phase 3 — Checklists
✅ Phase 4 — Test d'intégration
✅ Phase 4.5 — Clarification stratégique (vision, cible, différenciation)
✅ Phase 5 — MVP basé sur la vision (MVP validé 8/8 — clôturé Phase 5.5)
✅ Phase 5.7 — Hardening usage réel — discipline (5.7.A appliquée, 5.7.B recyclée vers 5.8)
✅ Phase 5.8 — Hardening usage réel — performance & contexte (correctifs framework livrés ; levier thinking côté utilisateur)
✅ Phase 6 — Party Mode : Panel (défaut) + Débat (sur invocation)
✅ Phase 7 — Mémoire persistante (cadrage + 7.1 mécanisme livrés ; cleanup à venir)
✅ Phase 8 — Skills techniques (cadrage + 8.1 garde-fous + 8.2 1ʳᵉ skill RCA livrés)
✅ Phase 9 — Correctifs DevX (Audit 2026-05-30)
✅ Phase 9.1 — Sous-agents réels (`/party-real`) — fenêtres fraîches par persona, ~80 % tokens en moins sur workflows 4+ personas (ADR-0008)
✅ Phase 9.2 — Abaissement seuil Panel ≤ 2 personas + allègement orchestrateur −29 % (ADR-0009)
⬜ Phase 10 — Ouverture

### ✅ Phase 9 — Correctifs DevX (Audit 2026-05-30)

**Objectif** : adresser les 18 points identifiés lors de l'audit technique complet du 2026-05-30.
Plan détaillé : [`docs/decisions/0007-plan-correctifs-audit-2026-05-30.md`](docs/decisions/0007-plan-correctifs-audit-2026-05-30.md)

| Lot | Contenu | Urgence |
|---|---|---|
| A — Sécurité & Infra | `.gitignore` + `docs/_scratch/` protection + CI Markdown | Critique |
| B — Cohérence doc | CHANGELOG + ADR-0002 déplacement + dates IDEAS | Élevé |
| C — Déduplication | `orchestrator.md` stub + versioning skills | Élevé |
| D — Onboarding UX | Test rapide + table commandes + badge + recalibration | Élevé |
| E — Rétention | Policy `closed` → archive + template | Élevé |
| F — Scripts & Hooks | `install-hooks.sh` robustesse + compat OS/version | Moyen |
| G — Skills & Templates | `TEMPLATE.md` + métadonnées + parité `code-analysis` | Moyen |
| H — Personas | Section "Différence avec" 5 personas | Faible |

**Critères de succès** : Lots A-E en une session (~2h), CI Markdown vert, README testable < 5 min.

---

### ✅ Phase 9.1 — Sous-agents réels (`/party-real`)

**Objectif** : remplacer l'impersonation séquentielle par de vrais sous-agents sur les workflows 4+ personas, réduisant les tokens input de ~80 % sur les sessions longues.

**Livrables** :

- 7 fichiers `.github/agents/<persona>.agent.md` avec tools restreints par domaine
- Mécanisme `.party/` (contexte + handoffs transitoires, gitignore-d)
- Mode `/party-real` **automatique** (l'orchestrateur décide, l'utilisateur ne tape rien)
- Skill `party-mode` v1.1.0 (Panel inline + Party Real + Débat)
- Templates `party-context.md` et `party-handoff.md`
- ADR-0008 (décision architecturale)

**Critères de succès** : workflow `feature-development` complet (7 personas) via Party Real sans saturation de contexte. ✔

---

### ✅ Phase 9.2 — Abaissement seuil Panel + allègement orchestrateur

**Objectif** : abaisser le seuil de bascule Panel → Party Real de ≤ 3 à ≤ 2 personas, et réduire la charge contextuelle de `orchestrator.agent.md` sans perdre d'information.

**Livrables** :

- ADR-0009 (seuil ≤ 2 personas — raffinement d'ADR-0008)
- `orchestrator.agent.md` : 284 → 202 lignes (−29 %) par extraction vers modules
- Nouveau module `.github/agents/modules/core-rules.md` (périmètre, délégation, contrat PLAN)
- `agents/protocols/preflight.md` étendu : « default to clarification » + « Pattern Avouer l'échec »
- `.github/agents/modules/party-mode.md` étendu : cycle Party Real complet (Qui/Quand/Pourquoi + flow)

**Critères de succès** : orchestrateur allégé, markdownlint 0 erreur, règles de bascule cohérentes sur tous les fichiers. ✔

---

### ⬜ Phase 10 — Ouverture

**Concept** : sortir le framework du contexte personnel pour le rendre
utilisable par d'autres.

**Étapes possibles** :

1. Test interne avec l'équipe
2. Documentation publique (README, guide démarrage, exemples)
3. Repo GitHub public
4. Site/blog de référence ("how-to construire un framework agentique")
5. Communication communautaire

## Principes directeurs (boussole)

À chaque décision future, on se réfère à ces principes :

1. **Pour qui ?** Analystes techniques + équipes DevOps/CI-CD avant tout.
2. **Configuration ?** En markdown, lisible et modifiable par non-devs.
3. **Outils ?** VSCode + Copilot natif, rien d'autre à installer.
4. **Complexité ?** Si un dev senior est nécessaire pour configurer, on a échoué.
5. **Drift ?** Anti-drift par design, fiabilité avant fonctionnalités.
6. **Livrables ?** Markdown structurés dans `docs/`, prêts à committer.

## Parking lot (idées en attente)

Voir `IDEAS.md` pour la liste complète des idées notées au fil des sessions.
