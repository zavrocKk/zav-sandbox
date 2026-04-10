"""test_notes_service.py — Suite de tests du module notes.
Cas CRUD et persistance locale couverts.
"""
import pytest
from src import notes_service as ns


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path, monkeypatch):
    """Chaque test travaille dans un fichier JSON isolé."""
    monkeypatch.setattr(ns, "STORAGE_FILE", tmp_path / "notes.json")


# ── CREATE ────────────────────────────────────────────────────────────────────

class TestCreate:
    def test_creates_note_with_correct_fields(self):
        note = ns.create_note("Titre", "Contenu")
        assert note["title"] == "Titre"
        assert note["content"] == "Contenu"
        assert len(note["id"]) == 8
        assert note["created_at"] is not None
        assert note["updated_at"] is None

    def test_strips_whitespace_from_title(self):
        note = ns.create_note("  Titre  ", "")
        assert note["title"] == "Titre"

    def test_empty_title_raises(self):
        with pytest.raises(ValueError, match="obligatoire"):
            ns.create_note("", "Contenu")

    def test_whitespace_only_title_raises(self):
        with pytest.raises(ValueError):
            ns.create_note("   ", "Contenu")

    def test_empty_content_allowed(self):
        note = ns.create_note("Titre", "")
        assert note["content"] == ""

    def test_persisted_to_disk(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ns, "STORAGE_FILE", tmp_path / "notes.json")
        note = ns.create_note("A", "B")
        assert (tmp_path / "notes.json").exists()
        data = __import__("json").loads((tmp_path / "notes.json").read_text())
        assert note["id"] in data


# ── READ ──────────────────────────────────────────────────────────────────────

class TestRead:
    def test_get_existing_note(self):
        note = ns.create_note("A", "B")
        found = ns.get_note(note["id"])
        assert found["title"] == "A"

    def test_get_missing_returns_none(self):
        assert ns.get_note("unknown") is None

    def test_list_empty_when_no_notes(self):
        assert ns.list_notes() == []

    def test_list_returns_all(self):
        ns.create_note("A", "")
        ns.create_note("B", "")
        assert len(ns.list_notes()) == 2

    def test_list_sorted_by_creation(self):
        n1 = ns.create_note("Premier", "")
        n2 = ns.create_note("Second", "")
        listing = ns.list_notes()
        assert listing[0]["id"] == n1["id"]
        assert listing[1]["id"] == n2["id"]


# ── UPDATE ────────────────────────────────────────────────────────────────────

class TestUpdate:
    def test_update_title(self):
        note = ns.create_note("Ancien", "Corps")
        updated = ns.update_note(note["id"], title="Nouveau")
        assert updated["title"] == "Nouveau"
        assert updated["updated_at"] is not None

    def test_update_content(self):
        note = ns.create_note("T", "Vieux contenu")
        updated = ns.update_note(note["id"], content="Nouveau contenu")
        assert updated["content"] == "Nouveau contenu"

    def test_update_missing_returns_none(self):
        assert ns.update_note("ghost") is None

    def test_update_with_empty_title_raises(self):
        note = ns.create_note("T", "C")
        with pytest.raises(ValueError):
            ns.update_note(note["id"], title="")

    def test_update_no_fields_still_updates_timestamp(self):
        note = ns.create_note("T", "C")
        updated = ns.update_note(note["id"])
        assert updated["updated_at"] is not None


# ── DELETE ────────────────────────────────────────────────────────────────────

class TestDelete:
    def test_delete_existing(self):
        note = ns.create_note("Del", "Me")
        assert ns.delete_note(note["id"]) is True
        assert ns.get_note(note["id"]) is None

    def test_delete_missing_returns_false(self):
        assert ns.delete_note("absent") is False

    def test_delete_removes_only_target(self):
        n1 = ns.create_note("Garder", "")
        n2 = ns.create_note("Effacer", "")
        ns.delete_note(n2["id"])
        assert ns.get_note(n1["id"]) is not None
        assert ns.get_note(n2["id"]) is None
