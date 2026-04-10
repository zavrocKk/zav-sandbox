"""notes_service.py — Micro-service CRUD de gestion de notes avec stockage JSON local.

Architecture: module unique, stockage notes.json, ID court UUID-8, timestamps ISO.
Périmètre MVP: create / read-one / list-all / update / delete. Hors scope: auth, tags, search.
"""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

STORAGE_FILE = Path("notes.json")


# ── I/O ───────────────────────────────────────────────────────────────────────

def _load() -> dict:
    if not STORAGE_FILE.exists():
        return {}
    with STORAGE_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with STORAGE_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── CRUD ──────────────────────────────────────────────────────────────────────

def create_note(title: str, content: str) -> dict:
    """Crée une note et la persiste. Retourne la note créée."""
    if not title or not title.strip():
        raise ValueError("Le titre est obligatoire.")
    notes = _load()
    note_id = str(uuid.uuid4())[:8]
    note = {
        "id": note_id,
        "title": title.strip(),
        "content": content,
        "created_at": _now(),
        "updated_at": None,
    }
    notes[note_id] = note
    _save(notes)
    return note


def get_note(note_id: str) -> dict | None:
    """Retourne la note ou None si introuvable."""
    return _load().get(note_id)


def list_notes() -> list[dict]:
    """Retourne toutes les notes triées par date de création."""
    return sorted(_load().values(), key=lambda n: n["created_at"])


def update_note(note_id: str, title: str | None = None, content: str | None = None) -> dict | None:
    """Met à jour un ou plusieurs champs. Retourne la note mise à jour ou None."""
    notes = _load()
    if note_id not in notes:
        return None
    if title is not None:
        if not title.strip():
            raise ValueError("Le titre ne peut pas être vide.")
        notes[note_id]["title"] = title.strip()
    if content is not None:
        notes[note_id]["content"] = content
    notes[note_id]["updated_at"] = _now()
    _save(notes)
    return notes[note_id]


def delete_note(note_id: str) -> bool:
    """Supprime une note. Retourne True si supprimée, False si introuvable."""
    notes = _load()
    if note_id not in notes:
        return False
    del notes[note_id]
    _save(notes)
    return True
