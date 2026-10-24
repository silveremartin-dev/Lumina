"""Script to export and synchronize the Lumina lexicon across JSON and Markdown formats."""

import json
import sys
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
LEXIQUE_PATH = ROOT_DIR / "data" / "lexique.json"
DOC_DIR = ROOT_DIR / "docs"

def export_all():
    print("--- Exporting Lumina Dictionary ---")
    with open(LEXIQUE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Export docs/dictionary.json
    out_json = DOC_DIR / "dictionary.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Exported JSON: {out_json}")

    # 2. Export docs/DICTIONARY.MD
    out_md = DOC_DIR / "DICTIONARY.MD"
    lines = [
        "# Lumina — Standardized Bilingual Dictionary",
        "",
        "This dictionary is generated automatically from `data/lexique.json`.",
        "",
        "## 1. Functional Particles & Grammatical Markers",
        "",
        "| Word | Type | French | English | Operational Description |",
        "|---|---|---|---|---|"
    ]

    for p in data.get("particles", []):
        lines.append(f"| `{p['word']}` | {p.get('type', '')} | {p.get('fr', '')} | {p.get('en', '')} | {p.get('desc', '')} |")

    lines.extend([
        "",
        "## 2. Personal Pronouns",
        "",
        "| Word | Person | French | English |",
        "|---|---|---|---|"
    ])
    for pr in data.get("pronouns", []):
        lines.append(f"| `{pr['word']}` | {pr.get('desc', '')} | {pr.get('fr', '')} | {pr.get('en', '')} |")

    lines.extend([
        "",
        "## 3. Decimal Numbers (Domain P-)",
        "",
        "| Word | Value | French | English |",
        "|---|---|---|---|"
    ])
    for nb in data.get("numbers", []):
        lines.append(f"| `{nb['word']}` | {nb.get('value', '')} | {nb.get('fr', '')} | {nb.get('en', '')} |")

    lines.extend([
        "",
        "## 4. Canonical Roots (C1V1C2V2)",
        "",
        "| Word | Part of Speech | Domain | Semantic Vector | French | English |",
        "|---|---|---|---|---|---|"
    ])
    for r in sorted(data.get("roots", []), key=lambda x: x["word"]):
        lines.append(f"| `{r['word']}` | {r.get('pos', '')} | {r.get('domain', '')} | {r.get('semantic', '')} | {r.get('fr', '')} | {r.get('en', '')} |")

    lines.append("")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Exported Markdown: {out_md}")
    print("✅ Dictionary export completed successfully!")

if __name__ == "__main__":
    export_all()
