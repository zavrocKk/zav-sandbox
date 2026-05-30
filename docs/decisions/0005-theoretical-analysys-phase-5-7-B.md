## 📌 AMENDEMENT 2026-05-10 — Mesure empirique contredisant la base théorique

> Cet amendement est ajouté le jour même de la création de l'ADR, suite à une
> investigation empirique de l'overhead de contexte. Il **invalide partiellement
> la base analytique théorique** de cet ADR. Il est conservé en tête de document
> car il change la façon dont les chiffres ci-dessous doivent être lus.

**Ce qui était supposé (théorique, note `field_report_2.md`)** :
- Overhead statique ~15 850 tokens (~25 % de 64K)
- Dont ~7 200 tokens (45 %) attribués au chargement des 9 personas

**Ce qui a été mesuré (empirique, 2026-05-10)** :

| Source | Tokens théoriques (note) | Tokens mesurés (réel) |
|---|---|---|
| Personas (9 fichiers) | ~7 200 | **~0 — non chargées** |
| `orchestrator.agent.md` | ~3 200 | ~2 100–3 400 |
| `copilot-instructions.md` | ~2 800 | ~650–970 |
| **Total overhead framework** | **~15 850** | **~2 750–4 370 (~6 %)** |

**Constat empirique vérifié** : l'orchestrator interrogé directement confirme ne
charger que `copilot-instructions.md`, `orchestrator.agent.md`, et une référence
mémoire non-lue. Les personas, workflows, checklists et templates ne sont PAS
injectés au démarrage — chargés à la demande uniquement. **Le framework fait déjà
du lazy-loading natif.**

**Conséquences sur cet ADR** :

1. La projection d'overhead de la note théorique était **surestimée d'un facteur ~4**.
   La répartition attribuant 45 % de l'overhead aux personas est **fausse** : les
   personas ne pèsent rien au démarrage.

2. Le Cas C (dégradation SNR) reste plausible, mais le mécanisme "verbosité
   compensatoire par accumulation de patterns" doit être mesuré séparément de
   l'overhead initial. La dégradation observée empiriquement à ~30K tokens provient
   de l'**accumulation par interaction** (thinking étendu ~9K/tour en tête, puis
   verbosité protocole), PAS de l'overhead de démarrage.

3. Les correctifs structurels du Lot 2 (re-grounding, budget tracking) gardent leur
   pertinence théorique, mais leur **priorité chute** : l'overhead qu'ils visaient
   à réduire est déjà faible. Le vrai levier de performance est le réglage du
   thinking et la réduction de verbosité par tour (mode `/light`), pas la structure
   de chargement.

**Statut de l'ADR inchangé** : reste `proposed-conditional`. Mais la condition
d'activation se précise : les correctifs structurels ne se justifient QUE si, après
optimisation du thinking et test d'un mode allégé, la dégradation persis