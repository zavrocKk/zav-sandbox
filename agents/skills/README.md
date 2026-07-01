# Skills techniques — Registre

Les skills sont des **modules de connaissance invocables** par un persona pendant
l'EXECUTE. Elles complètent les workflows sans les dupliquer.

**Règle d'invocation** : une skill n'est chargée que si sa `description` matche la
demande ET que le persona en a besoin maintenant. Jamais de chargement en bloc.

Règles complètes : [`.github/agents/modules/skills.md`](../../.github/agents/modules/skills.md).

---

## Skills disponibles

| Skill | Description | Quand l'invoquer | Auteur | Date |
|---|---|---|---|---|
| 🔍 [root-cause-analysis](root-cause-analysis/SKILL.md) | Remonter d'un symptôme à sa cause systémique via 5 Pourquoi / Ishikawa | Phase « Cause racine » d'un incident ou problème opérationnel récurrent | Zav | 2026-05-30 |
| 🎉 [party-mode](party-mode/SKILL.md) | Index des modes multi-personas (Panel/Débat/Party Real) + cheat-sheet anti-patterns | Session multi-personas, rappel des règles Panel/Débat/Party-Real | Zav | 2026-06-08 |

---

## Ajouter une skill

1. Crée `agents/skills/<slug>/SKILL.md` avec le frontmatter Agent Skills
   (`name`, `description`).
2. Corps : méthodologie, étapes, exemples, anti-patterns. **≤ 200 lignes** pour le
   corps principal.
3. (Optionnel) Ajoute des fichiers `reference/*.md` pour les détails avancés
   (un seul niveau de profondeur max).
4. Ajoute une ligne dans le tableau ci-dessus.
5. Mets à jour le tableau dans
   [`.github/agents/modules/skills.md`](../../.github/agents/modules/skills.md).

**Critères de qualité :**

- La `description` doit tenir en **une phrase** — c'est ce que l'orchestrator lit
  pour décider de charger ou non la skill.
- Une skill = un savoir spécialisé, pas un workflow. Si ça orchestre des personas,
  c'est un workflow.
- Tester sur 2–3 scénarios réels avant de fusionner.
