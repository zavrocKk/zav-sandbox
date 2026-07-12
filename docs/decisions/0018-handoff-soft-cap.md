---
type: adr
number: 0018
status: accepted
date: 2026-07-10
deciders: [Zav]
tags: [party-mode, handoffs, budget, gate, adr-0013, debat]
---

# ADR-0018 — Plafond souple déclaré pour les handoffs (la taille seule ne rejette jamais)

> Format : Michael Nygard. Une décision = un fichier, immuable une fois `accepted`.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-10
**Décideurs** : Zav — après débat contradictoire (avocat du diable en fenêtre
fraîche vs défense), stress-test « investigation de milliers de logs AWS », et
principe utilisateur explicite : « plus de tokens si le résultat le demande ».

## Contexte

Le budget handoff (cible ≤ 500 tokens, plafond 1000 — PR #139, Phase 9.3) était
une **estimation de design jamais validée** (journal terrain vide). Trois défauts
établis au débat :

1. **Incohérence temporelle** : la règle de preuve falsifiable par finding
   (PR #153) est postérieure au budget et consomme 15-40 tokens/finding — jusqu'à
   40 % d'une cible calibrée sans elle. Jamais recalibré.
2. **Le rejet-taille fabrique des tours** : rejeter un handoff dense force une
   re-invocation (un tour Copilot — la métrique n°1 du projet) ou le fallback
   (qui sacrifie la fenêtre fraîche). Punir l'excès de signal est absurde —
   démontré par le scénario « 15-20 findings prouvés d'un gros incident »,
   structurellement > 1000 avec une discipline parfaite.
3. La ligne §3 du protocole (« renforcer le gate ») aggravait le symptôme qu'elle
   mesurait.

Ce qui tient (concédé par l'avocat du diable) : **un garde-fou reste nécessaire**
— en régime convergent, un handoff est relu par tous les agents suivants + le
Scribe ; sans borne, la croissance quadratique que la Phase 9.1 a éliminée
(−80 %) revient. Et le désordre du vrai travail (scripts ratés, reprises,
révisions : ~25-80k tokens/investigation) vit dans la **fenêtre jetable** d'un
agent — le handoff n'en transporte que le distillat (~1-2 %).

## Décision

1. **La taille seule ne rejette jamais au gate.** Motifs de rejet : section
   manquante, preuve manquante, remplissage sans signal (même sous le seuil),
   dépassement **non déclaré**.
2. **Dépassement déclaré** : au-delà de 1000 tokens / 4000 chars, le handoff
   s'ouvre par « Budget dépassé : <raison> ». Dense et prouvé → il passe.
   Silencieux → non conforme. (Sortie de tunnel documentée, comme le fallback.)
3. **Les lignes de preuve sont hors cible** — correction de l'incohérence
   #139/#153.
4. **H6/H6bis pré-enregistrées** (protocole §3) : dépassements fréquents et
   utiles → relever la cible par ADR ; dépassements = remplissage → renforcer
   « pointeur > recopie », sans rétablir le rejet-taille.

## Alternatives considérées

### Option B — Garder le plafond dur (statu quo)

- **Pourquoi rejetée** : fabrique des tours (la vraie métrique) pour punir la
  rigueur ; incohérent avec la règle de preuve qu'il précède ; le cas réel de
  l'utilisateur (pentest/incident riche en findings) le casse par construction.

### Option C — Abolir tout budget

- **Pourquoi rejetée** : le lectorat multiplié du régime convergent ramène la
  croissance quadratique ; sans signal anti-verbosité, un agent recopie un diff
  « pour être sûr » et annule le bénéfice fenêtre-fraîche.

## Conséquences

### Positives

- Un agent rigoureux n'est plus puni ; zéro re-invocation pour cause de taille.
- Le budget redevient cohérent avec la règle de preuve.

### Négatives

- La « raison » d'un dépassement est déclarative — un agent peut sur-déclarer ;
  H6bis le mesure.
- Les 8 `.agent.md` mentionnent encore « plafond absolu 1000 » (guidance) — la
  sémantique exacte vit ici et dans le module ; **harmoniser les 8 mentions lors
  de TOK-01** (dé-duplication).

### Neutres / À surveiller

- H6/H6bis au §3 — le terrain juge la cible, pas le débat.

## Implémentation

Module `party-mode.md` (gate + budget), template `party-handoff.md`, protocole §3
(H6/H6bis remplacent la ligne « renforcer le gate »).

## Références

- [ADR-0013](0013-format-mechanism-model.md) (format × mécanisme), PR #139
  (budget initial), PR #153 (règle de preuve), PR #161 (matrice de capacités).
