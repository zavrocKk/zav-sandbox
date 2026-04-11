# Delivery Contract — Générer un DC

Générer un Delivery Contract formel pour la tâche demandée.

## Instructions

1. Lire le template : `_gsane/workflows/delivery-contract.tpl.md`
2. Analyser la demande : $ARGUMENTS
3. Identifier : fichiers cibles, contraintes, critères d'acceptance testables
4. Produire le DC avec tous les champs obligatoires :
   - TÂCHE (verbe d'action)
   - FICHIERS CIBLES (chemins exacts)
   - CONTRAINTES (règles non-négociables)
   - CRITÈRES D'ACCEPTANCE (commandes ou asserts vérifiables)
   - AGENT PRINCIPAL + VALIDATION
5. Écrire dans `_gsane-output/current-delivery-contract.md`

## Validation

Chaque AC doit être vérifiable par une commande CLI ou un assert pytest.
Un DC incomplet est rejeté — tous les champs sont obligatoires.
