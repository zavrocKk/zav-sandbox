---
type: architecture-note
date: 2026-05-10
status: draft
tags: [orchestrator, performance, stress-test, context-window, drift, phase-5-7]
references:
  - docs/decisions/0004-field-report-analysis-phase-5-7.md
  - .github/agents/orchestrator.agent.md
  - agents/protocols/preflight.md
---

# Analyse Théorique — Worst-Case Scenario Orchestrateur v5.7.A

> **Périmètre** : modélisation mathématique et logique des limites structurelles de l'orchestrateur
> en version 5.7.A. Ce document ne fabrique pas de données empiriques : il projette des comportements
> à partir des propriétés formelles du framework et de l'architecture transformer sous-jacente.
> Objectif : anticiper les points de rupture, calibrer les correctifs Phase 5.7.B.

---

## 1. Inventaire du budget contexte — Ligne de base

Avant la première interaction utilisateur, l'orchestrateur a déjà consommé un volume fixe
de contexte que l'on appelle **overhead statique**.

### 1.1 Composition du contexte statique

| Fichier chargé | Lignes estimées | Tokens estimés |
|---|---|---|
| `copilot-instructions.md` (instructions globales) | ~220 | ~2 800 |
| `orchestrator.agent.md` (contrat + flux + personas) | ~200+ | ~3 200 |
| `preflight.md` | ~55 | ~750 |
| `git-workflow.md` (repo memory) | ~30 | ~400 |
| Persona files × 9 (architect, devops, dev, qa, security, scribe…) | ~60 × 9 | ~7 200 |
| Métadonnées VS Code Copilot (editor context, workspace info) | variable | ~1 500 |
| **Total overhead statique** | | **~15 850 tokens** |

> **Note** : VS Code Copilot Chat (Sonnet 4.6) opère avec une fenêtre effective de 64K–200K tokens
> selon le mode. En mode agent, la fenêtre est typiquement **64 000 tokens** après sérialisation de
> l'historique. L'overhead statique représente donc **~25 % de la fenêtre** *avant* la première
> frappe clavier.

---

## 2. Calcul de la Densité de Bruit (Noise Density Ratio)

### 2.1 Définitions

- **Token Signal (S)** : token qui contribue directement au livrable technique (code, diagnostic,
  analyse fonctionnelle, décision, documentation utile).
- **Token Bruit (N)** : token de gestion de protocole sans valeur sémantique pour la tâche
  (en-têtes ANALYSE/PLAN/CONFIRM/EXECUTE/SYNTHESIS, handoffs entre personas, confirmations
  binaires, reformulations obligatoires).

### 2.2 Décomposition d'un cycle complet type

Pour une interaction de complexité moyenne (ex. : analyse d'une friction, production d'un
correctif dans un fichier `.md`) :

```
Phase ANALYSE         : 150 – 300  tokens   (reformulation + classification)
Phase PLAN (table)    : 200 – 450  tokens   (table markdown + déclaration livrable)
Phase CONFIRM         :  60 – 120  tokens   (question de validation + attente)
Phase EXECUTE
  └─ En-tête persona  :  40 – 80   tokens   (header visuel + contexte)
  └─ Handoff          :  60 – 100  tokens   (transition entre 2 personas)
  └─ Contenu technique: 500 – 1500 tokens   ← signal
Phase SYNTHESIS/Scribe: 300 – 600  tokens   (bilan, localisation artefact)
────────────────────────────────────────────
Bruit total (N)       : 810 – 1650 tokens
Signal total (S)      : 500 – 1500 tokens
```

### 2.3 Ratio Signal/Bruit (SNR)

$$SNR = \frac{S}{S + N}$$

| Scénario | S (tokens) | N (tokens) | SNR |
|---|---|---|---|
| Interaction simple (correctif court) | 500 | 1 650 | **23 %** |
| Interaction moyenne (analyse + fichier) | 1 000 | 1 200 | **45 %** |
| Interaction complexe (multi-personas) | 1 500 | 810 | **65 %** |
| **Moyenne pondérée (usage réel)** | **~900** | **~1 200** | **~43 %** |

**Lecture critique** : dans un usage quotidien, **57 % des tokens générés sont du protocole pur**,
sans contribution directe au livrable. Sur 5 sessions de 8h avec 15 interactions complexes chacune,
c'est ~56 000 tokens/session brûlés en overhead, contre ~42 000 tokens de contenu réel.

---

## 3. Projection de Saturation — Fenêtre à 64 000 tokens

### 3.1 Modèle de consommation

Soit $C_n$ la consommation cumulée au tour $n$ :

$$C_n = C_{static} + \sum_{i=1}^{n} (S_i + N_i + U_i)$$

Où :
- $C_{static}$ = 15 850 tokens (overhead statique, Section 1)
- $S_i + N_i$ = output du cycle $i$ ≈ 2 100 tokens (moyenne Section 2.2)
- $U_i$ = input utilisateur au tour $i$ ≈ 400 tokens (estimation conservative)

Budget résiduel initial : $64 000 - 15 850 = \mathbf{48 150\ tokens}$

Consommation par interaction : $2 100 + 400 = \mathbf{2 500\ tokens/tour}$

**Point de saturation théorique** :

$$n_{sat} = \frac{48 150}{2 500} \approx \mathbf{19\ interactions}$$

### 3.2 Mais ce calcul est optimiste — facteur de pensée étendue

En mode agent avec pensée étendue (extended thinking, non visible dans l'interface), les tokens
de raisonnement interne s'ajoutent au compteur de contexte sans apparaître dans la réponse :

- Multiplicateur empirique thinking : **× 2,5 à × 5** sur les tokens visibles
- Consommation réelle par interaction : **6 250 – 12 500 tokens/tour**

$$n_{sat,thinking} = \frac{48 150}{9 375} \approx \mathbf{5 \ interactions}$$

**Conclusion** : avec la pensée étendue active, **la fenêtre de contexte s'effondre entre la
5e et la 8e interaction complexe**. Pour une session de bureau de 8h avec une interaction toutes
les 25 minutes, la saturation est atteinte entre **2h05 et 3h20 après ouverture de la session**.

### 3.3 Seuil critique à 70 % — zone de dégradation graduelle

L'effondrement n'est pas binaire. La dégradation commence à **70 % de remplissage** :

| Seuil contexte | Interactions (sans thinking) | Interactions (avec thinking) |
|---|---|---|
| 50 % (dégradation précoce) | 9–10 | 2–3 |
| 70 % (dégradation active) | 13–14 | 4–5 |
| 90 % (effondrement imminent) | 17–18 | 6–7 |
| 100 % (truncation) | 19 | 7–8 |

---

## 4. Mécanisme de Dérive (Algorithmic Drift)

### 4.1 Fondement mathématique — Attention diluée

Dans l'architecture Transformer, chaque token génère une représentation contextualisée via
l'attention multi-têtes. Le poids d'attention entre la position courante $i$ et une position
historique $j$ suit :

$$a_{ij} = \frac{\exp\!\left(\frac{q_i \cdot k_j}{\sqrt{d_k}}\right)}{\displaystyle\sum_{l=1}^{n} \exp\!\left(\frac{q_i \cdot k_l}{\sqrt{d_k}}\right)}$$

Quand $n$ (longueur du contexte) augmente, le dénominateur croît, **diluant mécaniquement**
le poids de chaque token historique. Les règles du système prompt (positions 0–15 850) reçoivent
une attention relative décroissante :

| Longueur contexte $n$ | Poids relatif du système prompt |
|---|---|
| 15 850 (début) | **100 %** (seul contexte présent) |
| 32 000 (mi-session) | **≈ 50 %** |
| 48 000 (fin de session) | **≈ 33 %** |
| 64 000 (saturation) | **≈ 25 %** |

### 4.2 Biais de récence RoPE — accélérateur de dérive

Les LLMs modernes (dont Claude) utilisent RoPE (Rotary Positional Encoding), qui encode la
**distance relative** entre tokens plutôt que leur position absolue. Conséquence directe :
les tokens récents reçoivent un biais d'attention naturellement plus élevé que les tokens
anciens, **quelle que soit leur importance sémantique**.

Une règle binaire courte comme :
```
Tu NE DOIS JAMAIS répondre directement au fond d'une question technique.
```
est encodée en ~20 tokens à la position ~3 800 du contexte. Au tour 6 d'une session longue,
cette règle est à distance $d \approx 45 000$ tokens du point de génération courant.
Son poids d'attention effectif est inférieur à celui d'un en-tête de persona généré
5 interactions plus tôt.

**L'orchestrateur ne "désobéit" pas — il subit une dégradation probabiliste du signal
de contrainte.**

### 4.3 Renforcement contre-productif des patterns protocole

Paradoxe structurel : plus l'orchestrateur respecte son protocole (ANALYSE, PLAN, CONFIRM,
SYNTHESIS), plus il génère de tokens bruit. Ces tokens bruit deviennent eux-mêmes des
exemples en contexte (in-context learning) qui biaisent les prédictions suivantes vers
la reproduction de patterns protocole au détriment du contenu substantiel.

Le modèle apprend en-session que "le comportement attendu ici = produire des tables markdown
structurées avec en-têtes" → les réponses techniques deviennent progressivement plus
**formelles et moins denses** en contenu utile.

---

## 5. Modélisation des 3 Cas d'École

### Cas A — La Boucle Infinie de Réflexion

**Condition de déclenchement** : demande utilisateur ambiguë + règle
`default-to-clarification` active.

**Déroulement algorithmique** :

```
Tour 1 : Utilisateur envoie demande ambiguë (ex. "améliore la section 3")
         → PRE-FLIGHT : "premier message technique" = OUI
         → ANALYSE génère 3 ambiguïtés
         → CONFIRM demande clarification (Q1 + Q2 + Q3)

Tour 2 : Utilisateur répond à Q1 et Q2, ignore Q3
         → Nouvelle information → nouveau ANALYSE
         → ANALYSE génère 2 nouvelles ambiguïtés + Q3 toujours non résolue
         → CONFIRM redemande clarification (Q3 + Q4 + Q5)

Tour 3 : Utilisateur répond partiellement, introduit un nouveau terme
         → Nouveau terme = nouveau signal d'ambiguïté
         → ANALYSE génère 1 ambiguïté + Q3 toujours ouverte
         ...
```

**Coût par cycle de clarification** : ~600–900 tokens (ANALYSE + CONFIRM).
**Seuil de blocage** : après 8–10 cycles de clarification, le budget contexte
disponible pour l'exécution réelle est réduit de ~22 000 tokens.

**Invariant brisé** : la règle `default-to-clarification` est logiquement contradictoire
avec l'objectif de convergence. Une demande réelle contient toujours des ambiguïtés
résiduelles ; un agent maximiseur de clarification ne peut pas sortir de la boucle
de manière autonome sans seuil d'entropie explicite.

**Critère de sortie absent dans v5.7.A** : aucun compteur de clarifications,
aucun seuil `max_clarification_turns`, aucun mécanisme `proceed-with-assumptions-after-N`.

---

### Cas B — L'Amnésie du Prompt Système

**Condition de déclenchement** : session > 5 interactions complexes (avec thinking étendu)
ou > 12 interactions simples (sans thinking).

**Progression de l'amnésie** :

```
Interaction 1–3   : Règles binaires actives à ~85–100 % (faible dilution)
                    Délégation correcte, en-têtes personas présents.

Interaction 4–6   : Poids des règles ~50–65 %
                    Premier signe : SYNTHESIS du Scribe parfois omise.
                    Orchestrateur commence à répondre "brièvement" sans persona.

Interaction 7–10  : Poids des règles ~35–45 %
                    Orchestrateur répond au fond technique directement (F2 observé).
                    PLAN produit mais non suivi fidèlement (personas sautés).

Interaction 11+   : Poids des règles ~20–30 %
                    Comportement dominant = assistant généraliste (pretrained behavior).
                    Protocole respecté en surface (structure visible) mais vide de substance.
```

**Corrélation avec l'observation de terrain ADR-0004** : F2 ("Orchestrator ne délègue pas")
a été observé principalement en sessions longues, jamais sur la première interaction. C'est
la signature exacte d'une amnésie graduelle, pas d'un bug de parsing d'instruction.

**Implication pour Phase 5.7.A** : les correctifs textuels (renforcement des règles dans
les fichiers) ne résolvent pas ce problème. Ils retardent l'amnésie en augmentant le
signal initial, mais la dynamique de dilution reste inchangée. Seul un mécanisme de
**réinjection périodique** des contraintes critiques (re-grounding) peut y résister.

---

### Cas C — La Dégradation du Rapport Signal/Bruit (SNR)

**Condition de déclenchement** : progressive, démarre dès l'interaction 2.

**Mécanisme détaillé** :

Au fur et à mesure que la fenêtre de contexte se remplit de cycles protocole (ANALYSE,
PLAN, CONFIRM, EXECUTE, SYNTHESIS), le distribution statistique des tokens en contexte
bascule vers les patterns protocole :

```
Contexte début de session :
  [Système prompt 25%] [Tâche utilisateur 5%] [Espace libre 70%]
  → Signal élevé, bruit faible

Contexte milieu de session (8 interactions) :
  [Système prompt 15%] [Historique protocole 55%] [Tâche récente 5%] [Espace 25%]
  → Le modèle est conditionné par 55% de patterns protocole
  → Les nouvelles réponses reproduisent statistiquement le style protocole

Contexte fin de session (15+ interactions) :
  [Système prompt 10%] [Historique protocole 75%] [Tâche récente 3%] [Espace 12%]
  → Réponses : formellement correctes (structure visible), substantiellement vides
```

**Indicateurs observables de dégradation SNR** :

| Indicateur | Interaction 1 | Interaction 10 |
|---|---|---|
| Longueur des tables PLAN | 4–5 lignes (pertinentes) | 8–12 lignes (redondantes) |
| Ratio contenu/formatage dans EXECUTE | 70 / 30 | 35 / 65 |
| Nombre de reformulations inutiles | 0–1 | 3–5 |
| Densité de recommendations actionables | ~4/page | ~1.5/page |

**Paradoxe de la verbosité compensatoire** : en réponse à la dilution du signal,
le modèle produit davantage de tokens pour "atteindre" la même qualité perçue.
Résultat : le bruit augmente encore plus vite que le signal, accélérant la dégradation.

---

## 6. Synthèse — Matrice de Rupture

| Cas | Condition déclencheur | Interaction critique | Impact primaire | Correctif v5.7.A suffisant ? |
|---|---|---|---|---|
| A — Boucle réflexion | Demande ambiguë + clarification sans seuil | Dès interaction 1 | Paralysie de session | ❌ Non — manque seuil max_clarification |
| B — Amnésie prompt | Session > 5 interactions complexes | Interaction 4–6 | Non-délégation (F2) | ⚠️ Partiel — retarde sans résoudre |
| C — Dégradation SNR | Progressive dès interaction 2 | Interaction 8–10 | Livrables creux | ❌ Non — nécessite re-grounding |

### Points de résilience à intégrer (non couverts par v5.7.A)

1. **Seuil de clarification** : `max_clarification_turns = 2`. Au-delà, proceed-with-stated-assumptions.
2. **Re-grounding périodique** : réinjecter les 5 règles binaires critiques tous les 4–5 tours.
3. **Session kill-switch** : détecter automatiquement SNR < 30 % et proposer ouverture nouvelle session.
4. **Budget tracking explicite** : afficher le nombre d'interactions restantes avant seuil de dégradation.

---

## 7. Conclusion

L'orchestrateur v5.7.A est structurellement fragile sur les sessions de plus de **4–5 interactions complexes** avec pensée étendue active. Cette fragilité n'est pas un défaut de configuration — c'est une **propriété émergente de l'architecture transformer** : attention diluée + biais de récence RoPE + accumulation de patterns protocole.

Les correctifs Phase 5.7.A (règles textuelles, contrôles binaires) améliorent la robustesse des premières interactions mais n'adressent pas le mécanisme d'amnésie graduelle ni la boucle de réflexion infinie.

**Recommandation principale** : caps de session à **30 minutes / 5 interactions complexes max** comme mesure de mitigation immédiate (déjà identifié en ADR-0004 F4), en attendant les mécanismes de re-grounding prévus Phase 7.

> Ce document sert de base analytique au Field Report Phase 5.7.A. Les seuils numériques
> sont des projections théoriques calibrées sur l'architecture connue, non des mesures
> empiriques. Ils doivent être validés par observation sur la période d'usage réel suivante.
