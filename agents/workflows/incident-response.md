# Workflow — Incident Response

Réponse à un incident en production : panne, alerte, dégradation, comportement anormal.

## Diagramme des phases

```mermaid
flowchart LR
  T[1. Triage<br/>🛠️ DevOps] --> D[2. Diagnostic<br/>🛠️ DevOps + 💻 Dev]
  D --> M{3. Mitigation<br/>⚠️ confirm user}
  M -->|refusée ou échec| D
  M -->|appliquée| R{4. Cause racine<br/>routage par hypothèse}
  R -->|applicative| DEV[💻 Developer]
  R -->|infra / plateforme| OPS[🛠️ DevOps]
  R -->|sécurité ⚠️ escalade| SEC[🔒 Security]
  R -->|multi-domaines| PAN[Panel divergent]
  DEV --> H[5. Durcissement<br/>🏗️ Architect ± autres]
  OPS --> H
  SEC --> H
  PAN --> H
  H --> P[6. Post-mortem<br/>📝 Scribe]
```

## Personas par étape

| # | Phase           | Persona principal     | Personas secondaires      | Sortie attendue                                          |
| - | --------------- | --------------------- | ------------------------- | -------------------------------------------------------- |
| 1 | Triage          | 🛠️ DevOps             | —                         | Sévérité, périmètre impacté, timeline initiale           |
| 2 | Diagnostic      | 🛠️ DevOps             | 💻 Developer              | Hypothèses classées, signal/preuve associé(e)            |
| 3 | Mitigation      | 🛠️ DevOps             | 💻 Developer              | Action(s) appliquée(s) **après confirmation utilisateur**|
| 4 | Cause racine    | variable (voir ci-dessous) | autres au besoin    | Explication causale (pas seulement symptôme)             |
| 5 | Durcissement    | 🏗️ Architect          | 🔒 Security, 🛠️ DevOps     | Contre-mesures durables, ADR si décision structurante    |
| 6 | Post-mortem     | 📝 Scribe             | —                         | `docs/incidents/YYYY-MM-DD-slug.md` (blameless)          |

## Règles spécifiques

- **Phase 1 (Triage) — utiliser la checklist** `agents/checklists/incident-triage.md` dès le déclenchement. Couvrir les 2 premières minutes avant tout diagnostic.

- **Phase 3 (Mitigation) bloque sur confirmation utilisateur** dès que l'action est destructive ou irréversible (rollback, restart de service en prod, purge de cache, modification de config live).
- **Mitigation refusée ou inefficace → retour phase 2 (Diagnostic)** avec une nouvelle hypothèse. Jamais de passage en force ni de ré-application de la même action.
- Le DevOps ouvre toujours, le Scribe ferme toujours.
- **Phase 4 (Cause racine) — choix du persona** selon la nature des hypothèses qualifiées en phase 2 :
  - Hypothèses applicatives (logique, memory leak, query) → 💻 Developer
  - Hypothèses infra/plateforme (config, ressources, réseau) → 🛠️ DevOps
  - Hypothèses sécurité (intrusion, exfiltration, IAM anormal) → 🔒 Security + **escalade utilisateur immédiate**
  - **Hypothèses qui chevauchent plusieurs domaines → Panel** (Party Mode) : chaque
    persona concerné émet une carte d'angle (Position / Risque clé / Reco), une
    seule passe, puis le Scribe synthétise. Voir [`agents/protocols/light-panel.md`](../protocols/light-panel.md).
    Si les personas doivent se répondre entre eux → `/debate`.
- **Phase 4 (Cause racine) — invoquer la skill** [`root-cause-analysis`](../skills/root-cause-analysis/SKILL.md)
  pour structurer l'analyse (5 Pourquoi / Ishikawa) : remonter au défaut systémique,
  étayer chaque cause par une preuve, définir une contre-mesure durable (≠ mitigation).
- Si la cause racine est applicative → handoff explicite vers Developer.
- Si la cause est sécurité (intrusion, exfiltration suspecte) → handoff vers Security et **escalade utilisateur immédiate**.

## Anti-patterns

- ❌ Sauter le triage et plonger directement dans le code.
- ❌ Appliquer une mitigation destructive sans confirmation.
- ❌ Confondre mitigation (arrêter le saignement) et cause racine (comprendre pourquoi).
- ❌ Conclure sans post-mortem (« on verra plus tard »).
- ❌ Post-mortem accusatoire (nommer une personne plutôt qu'un défaut systémique).
- ❌ Action items sans owner ni échéance.

## Livrable final

`docs/incidents/YYYY-MM-DD-<slug-court>.md` produit avec le template `agents/templates/incident-report.md`.

**Cycle de vie du statut :** `draft` → `in-review` → `closed`.

**Inputs bruts associés :**
- Fixtures synthétiques de test → `docs/_scratch/mvp-inputs/<source>-<topic>.md` (versionnées, référencées depuis le rapport)
- Données réelles (logs, exports) → `docs/_scratch/inputs/` (git-ignoré, jamais committé)

**Si l'incident révèle une décision structurante** (ex. : refonte d'architecture, changement de stratégie de pool) → l'Architect ouvre un ADR dans `docs/decisions/NNNN-slug.md` en complément.

> ❌ Les plans de correctifs et action items vont dans `docs/_scratch/YYYY-MM-DD-plan-<slug>.md` — jamais dans `docs/decisions/`.
