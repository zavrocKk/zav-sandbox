---
type: adr
number: 0019
status: accepted
date: 2026-07-14
deciders: [Zav]
supersedes_partial: 0015
tags: [skills, observability, terrain, fork-job, source-de-verite, phase-10]
---

# ADR-0019 — Skill dédiée pour un outil à usages multiples ; le repo canonique reste la source de vérité

> Format : Michael Nygard. Une décision = un fichier, immuable une fois
> `accepted`. Si on change d'avis, on crée un nouvel ADR qui `supersedes` celui-ci.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-14
**Décideurs** : Zav
**Supersedes (partiel)** : [ADR-0015](0015-analyst-skills-family.md) — la règle
« ajouter un outil = ajouter une annexe, pas une skill » est restreinte au cas
où l'usage de l'outil est contenu dans la méthode. Le reste de 0015 (famille de
4 skills, règles de conformité binaires, hors-périmètre connexions) tient.

## Contexte

Premier retour terrain (2026-07-13) : le framework est installé dans
l'environnement de travail réel de l'utilisateur, et son fork a **divergé** —
`observability-triage` y a été éclatée en une skill générale (la méthode) plus
des **skills dédiées par outil** (AWS, Datadog, Splunk). Deux raisons
rapportées :

1. **Usages plus larges que le triage** : construire des dashboards, gérer des
   alertes, lire des logs au quotidien — l'annexe de 0015 ne couvrait que la
   syntaxe au service du triage.
2. **Volume** : le savoir utile par outil est trop gros pour une annexe — une
   skill dédiée permet d'être complet.

C'est une **falsification partielle de l'ADR-0015 par l'usage** : sa prémisse
« le savoir-faire d'évidence est unique, seule la syntaxe varie » ne tenait que
tant que l'usage de l'outil restait un sous-ensemble de la méthode. Dès qu'un
outil sert plusieurs usages, l'annexe déborde. C'est le premier ADR provoqué
par le terrain plutôt que par le design — le protocole de test fonctionne.

Limite d'évidence, déclarée : la source est le rapport de l'utilisateur et ses
notes personnelles (contenu job, confidentiel) — pas encore un artefact
reproductible dans ce repo. Le rétroportage (ci-dessous) la matérialisera.

La divergence pose une seconde question, structurelle : **qui est la source de
vérité** quand le fork job et le repo canonique ne disent plus la même chose ?

## Décision

1. **Règle skills amendée** : un outil reste une **annexe** de la skill-méthode
   tant que son usage est contenu dans la méthode ; un outil à **usages
   multiples** (dépassant la méthode) devient une **skill dédiée**. Dans tous
   les cas la skill-méthode reste **unique** : la méthode n'est jamais recopiée
   dans les skills outil (garde TOK-01) — une skill outil porte le savoir outil
   (syntaxe, navigation, dashboards, alertes) et **pointe** vers la méthode.
2. **Le repo canonique est la source de vérité ; le fork job est le terrain.**
   Le fork expérimente et remonte ; toute divergence est soit **rétroportée**
   (anonymisée, par PR — plus un ADR si elle change une règle), soit consignée
   comme spécifique à l'instance job. Une divergence silencieuse est non
   conforme.
3. **Rétroportage des skills par outil : différé.** Il attend les versions
   anonymisées fournies par l'utilisateur — pas de reconstruction de tête ici,
   le canonique ne doit pas inventer ce que le terrain a déjà écrit.

## Alternatives considérées

### Option B — Le fork job devient la source de vérité

- Description : le terrain a raison, le canonique suit.
- Avantages : zéro délai entre découverte et référence.
- **Pourquoi rejetée** : le contenu job est confidentiel (non publiable) ; le
  fork n'a ni historique ADR, ni CI, ni falsifiabilité outillée ; et la
  division des rôles actée le 2026-07-13 place l'amélioration du framework ici
  — le terrain teste et rapporte.

### Option C — Maintenir 0015 tel quel et traiter le fork comme une erreur

- Description : l'annexe reste la règle ; le fork devrait re-fusionner.
- Avantages : zéro amendement, cohérence du registre de skills.
- **Pourquoi rejetée** : le gel exigeait des données avant d'amender — les
  voici. Volume constaté et usages hors-méthode sont exactement l'évidence que
  la règle « annexe » ne pouvait pas anticiper ; nier le terrain inverserait la
  raison d'être du protocole de test.

## Conséquences

### Positives

- La règle skills reflète l'usage réel, pas l'esthétique du design.
- La divergence fork/canonique a désormais un protocole (rétroporter ou
  consigner) — plus jamais silencieuse.
- Précédent sain : première décision du registre déclenchée par une
  falsification terrain.

### Négatives

- Le risque qui avait fait rejeter « une skill par outil » dans 0015 revient
  partiellement : la sélection de skill se fait par matching de `description` —
  plusieurs skills outil mal différenciées peuvent dégrader la sélection. Garde :
  chaque description de skill outil nomme l'outil **et** ses usages propres,
  jamais la méthode.
- Le canonique est temporairement en retard sur le terrain (annexes vs skills
  dédiées) jusqu'au rétroportage — assumé, préférable à une reconstruction non
  fidèle.

### Neutres / À surveiller

- Signal journal terrain : erreurs de sélection entre skill-méthode et skills
  outil → affiner les descriptions.
- Signal TOK-01 : toute recopie de la méthode dans une skill outil = drift à
  corriger immédiatement.

## Implémentation

Cet ADR seul — il grave la règle et la gouvernance de divergence. Le
rétroportage des skills AWS/Datadog/Splunk (et la conversion des annexes
`observability-triage/reference/*.md`) fera l'objet d'une PR dédiée, gated sur
les versions anonymisées remontées du terrain. Les registres
(`agents/skills/README.md`, `.github/agents/modules/skills.md`) seront mis à
jour dans cette PR-là, pas avant.

## Références

- [ADR-0015](0015-analyst-skills-family.md) — règle initiale « outil = annexe »
  (Option B alors rejetée : ce contexte-là supposait usage ⊂ méthode).
- Retour terrain du 2026-07-13 (notes personnelles de l'utilisateur, fork job).
- [ADR-0009](0009-abaisser-seuil-panel-inline.md) /
  [ADR-0013](0013-format-mechanism-model.md) — précédents `supersedes_partial`.
