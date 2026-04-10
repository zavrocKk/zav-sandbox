#!/usr/bin/env python3
"""Delivery Contract Validator — GSANE"""
import io
import json
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows (cp1252 can't encode emojis)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "_config" / "dc-schema.json"


def parse_dc_markdown(filepath):
    """Parse un fichier DC Markdown et retourne un dict des champs."""
    text = Path(filepath).read_text(encoding="utf-8")

    # --- Extract YAML frontmatter ---
    fm_match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    frontmatter = {}
    if fm_match:
        for line in fm_match.group(1).splitlines():
            m = re.match(r'^(\w[\w_]*):\s*(.+)$', line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip().strip('"').strip("'")
                frontmatter[key] = val

    # --- Extract sections by ## heading ---
    sections = {}
    current_heading = None
    current_lines = []
    for line in text.splitlines():
        heading_match = re.match(r'^##\s+(.+)', line)
        if heading_match:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = heading_match.group(1).strip()
            current_lines = []
        elif current_heading is not None:
            current_lines.append(line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    # --- Build DC data dict ---
    dc_data = {}

    # id <- task_id from frontmatter
    dc_data["id"] = frontmatter.get("task_id", "")

    # task <- Mission Goal section
    for key in sections:
        if "mission goal" in key.lower():
            dc_data["task"] = sections[key]
            break
    else:
        dc_data["task"] = ""

    # constraints <- Architectural Constraints section
    constraints_text = ""
    for key in sections:
        if "architectural constraints" in key.lower() or "contraintes" in key.lower():
            constraints_text = sections[key]
            break
    dc_data["constraints"] = constraints_text

    # files <- backtick paths in constraints section
    files = re.findall(r'`([^`]+(?:\.[a-zA-Z]+|/))`', constraints_text)
    dc_data["files"] = files if files else []

    # acceptance_criteria <- lines starting with - [ ] or - [x] in Acceptance Criteria
    ac_text = ""
    for key in sections:
        if "acceptance criteria" in key.lower():
            ac_text = sections[key]
            break
    ac_items = []
    for line in ac_text.splitlines():
        m = re.match(r'^\s*-\s*\[[ x]\]\s*(AC-\d+\s*:.+)', line)
        if m:
            ac_items.append(m.group(1).strip())
    dc_data["acceptance_criteria"] = ac_items

    # agent_principal <- owner from frontmatter
    dc_data["agent_principal"] = frontmatter.get("owner", "")

    # validation_agent <- validation_agent from frontmatter
    dc_data["validation_agent"] = frontmatter.get("validation_agent", "")

    return dc_data


def validate_dc(dc_data, schema):
    """Valide un DC dict contre le schéma. Retourne (bool, list[str])."""
    errors = []
    required = schema.get("required", [])
    properties = schema.get("properties", {})

    for field in required:
        value = dc_data.get(field)
        if value is None or value == "" or value == []:
            errors.append(f"Champ requis manquant ou vide : '{field}'")
            continue

        prop = properties.get(field, {})
        expected_type = prop.get("type")

        if expected_type == "string" and not isinstance(value, str):
            errors.append(f"'{field}' doit être une chaîne de caractères")
        elif expected_type == "array":
            if not isinstance(value, list):
                errors.append(f"'{field}' doit être un tableau")
                continue
            min_items = prop.get("minItems", 0)
            if len(value) < min_items:
                errors.append(f"'{field}' doit contenir au moins {min_items} élément(s), trouvé {len(value)}")
            # Validate item patterns
            items_schema = prop.get("items", {})
            pattern = items_schema.get("pattern")
            if pattern:
                for i, item in enumerate(value):
                    if not re.match(pattern, item):
                        errors.append(f"'{field}[{i}]' ne matche pas le pattern '{pattern}' : '{item}'")

    return len(errors) == 0, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python dc-validator.py <dc-file.md>")
        sys.exit(1)

    dc_file = Path(sys.argv[1])
    if not dc_file.exists():
        print(f"❌ Fichier introuvable : {dc_file}")
        sys.exit(1)

    if not SCHEMA_PATH.exists():
        print(f"❌ Schéma introuvable : {SCHEMA_PATH}")
        sys.exit(1)

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    dc_data = parse_dc_markdown(dc_file)
    valid, errors = validate_dc(dc_data, schema)

    if valid:
        print(f"✅ PASS — {dc_file.name} est valide.")
        sys.exit(0)
    else:
        print(f"❌ FAIL — {dc_file.name} :")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
