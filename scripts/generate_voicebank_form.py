#!/usr/bin/env python3
import json
import pathlib
from datetime import datetime

# -----------------------------------------
# CONFIG
# -----------------------------------------
INDEX_PATH = "characters/index.json"
TEMPLATE_PATH = ".github/ISSUE_TEMPLATE/create_voicebank_template.yml"
OUTPUT_PATH = ".github/ISSUE_TEMPLATE/create_voicebank.yml"

# -----------------------------------------
# LOAD CHARACTER DATA
# -----------------------------------------
def load_characters():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Esperado: lista de objetos con `id`, `name`, `avatar`
    characters = []
    for c in data:
        characters.append({
            "id": c.get("id"),
            "name": c.get("name", c.get("id")),
            "avatar": c.get("avatar", None)
        })
    return characters


# -----------------------------------------
# GENERATE PREVIEW MARKDOWN
# -----------------------------------------
def generate_preview(characters):
    out = ["### Personajes disponibles:\n"]

    for c in characters:
        out.append(f"**{c['id']}** — {c['name']}")
        if c["avatar"]:
            out.append(f"![{c['id']}]({c['avatar']})")
        out.append("")  # newline

    return "\n".join(out)


# -----------------------------------------
# GENERATE DROPDOWN OPTIONS
# -----------------------------------------
def generate_options(characters):
    out = []
    for c in characters:
        out.append(f"  - {c['id']}  # {c['name']}")
    return "\n".join(out)


# -----------------------------------------
# APPLY TEMPLATE
# -----------------------------------------
def build_form():
    chars = load_characters()
    preview = generate_preview(chars)
    options = generate_options(chars)

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    output = (
        template
        .replace("{{CHARACTER_LIST_PREVIEW}}", preview)
        .replace("{{CHARACTER_ID_OPTIONS}}", options)
    )

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"[OK] Formulario generado en {OUTPUT_PATH}")


# -----------------------------------------
# ENTRYPOINT
# -----------------------------------------
if __name__ == "__main__":
    print("[INFO] Generando formulario dinámico para voicebanks...")
    build_form()
