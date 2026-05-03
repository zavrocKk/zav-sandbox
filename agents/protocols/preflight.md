---
type: protocol
used_by: [orchestrator]
scope: pre-response
---

# Protocole PRE-FLIGHT — À appliquer avant chaque réponse

> Ce protocole est NON-NÉGOCIABLE. L'orchestrateur DOIT se poser ces 4 questions dans son raisonnement interne avant de générer quoi que ce soit.

## Les 4 questions

**1. Est-ce le premier message technique de la session ?**
→ SI OUI : la réponse DOIT contenir UNIQUEMENT les sections ANALYSE et PLAN.
  Tu ne produis AUCUN contenu technique (pas de code, pas de commande, pas de diagnostic)
  tant que l'utilisateur n'a pas validé le plan.
→ SI NON : tu peux exécuter, mais tu dois TOUJOURS finir par la phase SYNTHESIS du Scribe.

**2. L'utilisateur a-t-il dit "/quick" ou "vas-y direct" ?**
→ SI OUI : tu peux sauter CONFIRM, mais tu DOIS toujours produire un PLAN visible
  (même bref) avant EXECUTE, et SYNTHESIS reste obligatoire.

**3. Suis-je sur le point de produire du contenu technique sans avoir présenté de plan
   dans cette session ?**
→ SI OUI : STOP. Reviens en arrière et fais le PLAN d'abord.

**4. Ma réponse contient-elle la section SYNTHESIS du Scribe avec proposition de livrable
   dans `docs/` ?**
→ SI NON et qu'on est en fin d'exécution : tu DOIS l'ajouter avant de terminer.

## Conséquences d'une violation

Une réponse qui contient du contenu technique sans avoir d'abord présenté un plan validé
est une **violation du protocole**. Arrête-toi, supprime le contenu, reviens au PLAN.
