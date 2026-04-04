# Notes Service

Micro-service Python de gestion de notes (CRUD) avec stockage JSON local.

## Installation

```bash
pip install -e .
```

## Usage

```python
from notes_service import create_note, get_note, list_notes, update_note, delete_note

# Créer
note = create_note("Ma réunion", "Action items : ...")

# Lire
note = get_note("a1b2c3d4")          # par ID
all_notes = list_notes()             # toutes les notes

# Modifier
note = update_note("a1b2c3d4", title="Nouveau titre")

# Supprimer
deleted = delete_note("a1b2c3d4")    # True / False
```

## CLI (proposé par Sally / UX Designer)

| Commande | Résultat attendu | Erreur lisible |
|---|---|---|
| `notes add "Titre" "Corps"` | `✅ Note créée [id: a1b2c3d4]` | `❌ Le titre est obligatoire.` |
| `notes list` | Tableau formaté id / titre / date | `(vide) Aucune note trouvée.` |
| `notes get <id>` | Fiche détaillée | `❌ Note introuvable : <id>` |
| `notes update <id> --title "Nouveau"` | `✅ Note mise à jour` | `❌ Note introuvable : <id>` |
| `notes delete <id>` | `✅ Note supprimée` | `❌ Note introuvable : <id>` |

## Schéma JSON (Winston / Architect)

```json
{
  "a1b2c3d4": {
    "id": "a1b2c3d4",
    "title": "Titre de la note",
    "content": "Corps du texte",
    "created_at": "2026-04-04T13:00:00+00:00",
    "updated_at": null
  }
}
```

## Lancer les tests

```bash
pytest test_notes_service.py -v
```

## Idée V2 (Carson / Brainstorming)

**Semantic Snapshot** : À la fermeture de la session, générer automatiquement un résumé vectoriel léger de chaque note modifiée dans la journée (via un hash sémantique local), permettant une recherche fulltext offline sans dépendance réseau.
