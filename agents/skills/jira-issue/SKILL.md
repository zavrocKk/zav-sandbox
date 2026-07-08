---
name: jira-issue
version: "1.0.0"
description: Rédige un billet JIRA bug/defect prêt à coller, au format Atlassian standard (Summary « Quoi-Où-Quand », Steps to Reproduce, Expected vs Actual, Environment, évidence, acceptance criteria). À utiliser quand l'utilisateur demande de préparer un billet de bug, ou pour transformer un finding de bilan en ticket actionnable. Ne crée rien dans JIRA — sortie markdown copiable uniquement.
---

# JIRA Issue — bug / defect prêt à coller

Produit un ticket **complet et actionnable** qu'un développeur peut prendre sans
poser de question. Skill de **format** : aucune connexion, aucun appel API — la
sortie est un bloc markdown que l'utilisateur colle dans JIRA. La connexion
éventuelle (MCP) est un choix séparé, hors de cette skill.

## Format de sortie

```text
Summary     : <Quoi est cassé> — <Où (service/module)> — <Quand/condition>   [≤ 255 chars]
Issue Type  : Bug
Environment : <prod | staging | dev> — <versions app/OS/navigateur pertinentes> — <région/compte si cloud>

Steps to Reproduce :
1. <depuis l'état initial — chaque input, chaque clic>
2. <…>
3. <…>

Expected Result : <ce qui devrait se produire>
Actual Result   : <ce qui se produit — message d'erreur exact si disponible>

Evidence :
- <pointeur log/capture + timestamp UTC — jamais le dump brut, jamais de secret>
- <requête d'observabilité re-exécutable si disponible (voir skill observability-triage)>

Severity proposée : <S1-S4> — <justification en une ligne>
Acceptance criteria (fix) :
- [ ] <critère binaire observable — comment on saura que c'est corrigé>
```

## Règles (binaires)

- **Conformité** : les 7 blocs ci-dessus présents, sinon le ticket est **non conforme**
  — on complète avant de livrer, on ne livre pas un ticket troué.
- **Summary** : structure « Quoi – Où – Quand », ≤ 255 caractères. « Ne marche pas »
  est interdit — dire ce qui ne marche pas, où, sous quelle condition.
- **Steps** : numérotées **depuis l'état initial** (pas depuis le milieu du parcours).
- **Severity ≠ Priority** : la severity (impact technique) est **proposée** par
  l'analyste ; la priority (ordre de traitement) est une **décision humaine** —
  la skill ne la remplit jamais.
- **Evidence** : pointeurs + timestamps, contenu anonymisé. Aucun secret, aucun PII
  (règles sécurité du workspace).

## Pont bilan → ticket

Si le ticket naît d'un finding de [`bilan-remediation`](../../workflows/bilan-remediation.md) :

| Champ du bilan | Champ du ticket |
|---|---|
| Conclusion + Action recommandée | Description / Summary |
| Signal + Preuve | Evidence |
| Critère de vérification | Acceptance criteria |

Le ticket **pointe** vers le bilan (chemin repo), il ne recopie pas l'analyse complète.

## Adaptation à ton instance

Chaque JIRA d'entreprise a ses champs custom (components, labels, epic link,
équipe…). Cette section est à compléter avec 1-2 tickets réels **anonymisés**
déposés dans `docs/_scratch/mvp-inputs/` :

```text
<!-- À remplir après fixtures :
Champs custom obligatoires : <…>
Issue types disponibles    : <Bug | Defect | …>
Convention de labels       : <…>
-->
```

## Anti-patterns

- ❌ « L'application ne marche pas » en summary.
- ❌ Steps qui supposent un état intermédiaire non décrit.
- ❌ Severity et priority confondues, ou priority remplie par l'IA.
- ❌ Coller l'analyse complète du bilan dans le ticket (pointer, pas recopier).
- ❌ Logs bruts avec PII/secrets en pièce jointe.
