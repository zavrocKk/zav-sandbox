# Vision — Agentic Team Framework

> Document de référence stratégique. Cette vision est la **boussole** du projet :
> à chaque décision future, on s'y réfère pour rester aligné.

## Pitch en une phrase

**"Agentic Team transforme tes idées techniques en livrables de qualité senior,
sans avoir à coder. Pour ceux qui pensent comme un architecte mais qui n'ont
pas le temps d'être développeur."**

## Pour qui

Les profils techniques qui ne sont pas développeurs à 100%, mais qui doivent
produire des livrables de niveau senior :

- **Analystes techniques** — comprennent les concepts, font de la configuration,
  ne codent pas mais ont la culture technique
- **Platform Engineers / SRE** — opérationnels, vivent dans les incidents et
  les configurations
- **Équipes CI/CD et DevOps** — produisent du YAML, des manifests, des pipelines,
  des runbooks au quotidien
- **Architectes solutions** — pensent design et trade-offs, doivent produire
  des ADRs et des diagrammes
- **Product Owners techniques** — font le pont entre business et tech, doivent
  cadrer des features

**Point commun** : ils ont la compréhension technique mais pas le temps (ou pas
l'envie) de coder des frameworks Python pour automatiser leurs workflows.

## Le problème qu'on résout

Les frameworks agentiques actuels (BMAD, AutoGen, CrewAI, LangGraph) sont
**conçus par des devs senior pour des devs senior**. Doc, exemples, concepts —
tout suppose qu'on sait déjà coder, déboguer, lire du Python, comprendre des
graphes d'agents.

**Résultat** : la moitié des effectifs IT en grande entreprise (analystes,
ops, PO techniques, architectes solutions junior) sont **sous-équipés**. Ils
dépendent des devs senior pour produire du livrable technique, ce qui ralentit
tout le monde.

## Ce qu'on propose

Un framework agentique qui peut être **adopté et configuré par des gens qui
ne sont pas développeurs à plein temps**, mais qui ont besoin de produire du
livrable technique de qualité.

### Différenciation

| Aspect | Frameworks actuels | Agentic Team |
|---|---|---|
| Configuration | Python, YAML complexe | **100% Markdown** |
| Installation | Serveur, Docker, deps | **Natif VSCode + Copilot** |
| Courbe d'apprentissage | Heures à jours | **30 minutes** |
| Templates DevOps | À construire | **Prêts à l'emploi** |
| Mémoire entre sessions | Non / DIY | **Persistante via artefacts** |
| Drift en session longue | Fréquent | **Anti-drift par design** |
| Ton des agents | Neutre / fonctionnel | **Personnalité contrôlée** |

### Ce qu'on fait

✅ **Tout est en Markdown** — pas de Python, pas de YAML complexe
✅ **Configuration déclarative** — personas, workflows, skills sont des `.md` lisibles
✅ **Intégration native VSCode** — pas de serveur, pas de docker-compose
✅ **Templates DevOps prêts** — incidents, runbooks, ADRs, deployment plans
✅ **Vocabulaire métier natif** — runbook, post-mortem, change request, IaC
✅ **Anti-drift par design** — le système ne dérive pas même sur sessions longues

### Ce qu'on NE fait PAS (et c'est OK)

❌ Un framework général-purpose qui fait tout
❌ Un système avec interface graphique sophistiquée
❌ Un produit SaaS avec backend
❌ Quelque chose pour les data scientists ou ML engineers
❌ Un clone de BMAD ou AutoGen

**Tu fais une chose, et tu la fais excellemment** : aider les profils techniques
non-devs à transformer leurs workflows manuels en sessions agentiques qui
produisent des livrables markdown structurés.

## Ambition

**Court terme** : framework officiel de mon équipe (DevOps/CI-CD/Plateforme).

**Moyen terme** : framework adopté par d'autres équipes de l'entreprise, avec
des skills métier spécifiques (Helm, K8s, Terraform, AWS, observabilité).

**Long terme** : ouverture publique, rivaliser avec BMAD/AutoGen/CrewAI/
LangGraph sur le segment "agentique pour les non-devs". Devenir la référence
sur cette niche.

## Boussole de décision

À chaque arbitrage futur, on se pose ces questions dans cet ordre :

1. **Pour qui ?** Est-ce que ça aide un analyste technique ou une équipe DevOps ?
2. **Configuration ?** Est-ce que c'est en markdown, lisible par un non-dev ?
3. **Outils ?** Est-ce que ça reste sur VSCode + Copilot natif ?
4. **Complexité ?** Est-ce qu'un dev senior est nécessaire pour configurer ?
   Si oui → on a échoué.
5. **Drift ?** Est-ce que ça tient sur une session longue ?
6. **Livrables ?** Est-ce que ça produit du markdown structuré dans `docs/` ?

Si une fonctionnalité ne passe pas ces 6 filtres, **elle n'entre pas dans
Agentic Team**.

## Position éthique

Je suis ambassadeur IA dans mon entreprise — j'ai donc de la latitude reconnue
pour expérimenter et innover. Pas de gouvernance IP en place actuellement.

**Principes de prudence quand même** :
- Reconstruction propre, pas copier-coller du système au bureau
- Le système au bureau (BMAD modifié) sert d'inspiration conceptuelle uniquement
- Si le projet décolle ou si la gouvernance change, communication transparente
  avec le management

## Décisions stratégiques majeures

### 2025-05-02 — Clarification de la vision (Phase 4.5)
- **Cible** : analystes techniques + équipes DevOps/CI-CD/Platform/SRE
- **Différenciation** : 100% markdown, natif VSCode + Copilot
- **Pitch** : transformation d'idées techniques en livrables senior sans coder
- **Ambition** : framework officiel d'équipe → ouverture publique
- **Position éthique** : ambassadeur IA, prudence par reconstruction propre
