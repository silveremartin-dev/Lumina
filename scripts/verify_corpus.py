"""Verification and linting script for the Lumina lexicon and bilingual corpus."""

import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from source.analyzer import LuminaAnalyzer

def verify():
    print("--- Auditing Lumina Lexicon and Corpus ---")
    analyzer = LuminaAnalyzer()
    lex_file = ROOT_DIR / "data" / "lexique.json"
    prince_file = ROOT_DIR / "data" / "petit_prince.json"

    with open(lex_file, "r", encoding="utf-8") as f:
        lex_data = json.load(f)

    roots = lex_data.get("roots", [])
    print(f"Total canonical roots in lexicon: {len(roots)}")

    seen_words = set()
    errors = 0

    for r in roots:
        w = r["word"].lower()
        if w in seen_words:
            print(f"[ERROR] Duplicate word found: {w}")
            errors += 1
        seen_words.add(w)

        # Check canonical C1V1C2V2 format
        if not re.match(r'^(sh|zh|ch|ng|[a-z])([aeiou])(sh|zh|ch|ng|[a-z])([aeiou])$', w):
            print(f"[WARN] Non-canonical length/shape: {w} (POS: {r.get('pos')})")

    # Verify Petit Prince corpus
    with open(prince_file, "r", encoding="utf-8") as f:
        prince_data = json.load(f)

    sentences = prince_data.get("sentences", [])
    print(f"Total Petit Prince sentences: {len(sentences)}")

    for s in sentences:
        tokens = analyzer.analyze_sentence(s["lumina"])
        for tok in tokens:
            if tok["type"] == "unknown":
                print(f"[NOTE] Unregistered token in sentence #{s['id']}: '{tok['raw']}'")

    if errors == 0:
        print("\n✅ Corpus and lexicon audit passed successfully (0 fatal errors)!")
    else:
        print(f"\n❌ Audit completed with {errors} errors.")
        sys.exit(1)

if __name__ == "__main__":
    verify()
