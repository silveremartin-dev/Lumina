"""Test real-world French and English sentences bidirectionally."""
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from source.translator import LuminaTranslator

t = LuminaTranslator()

test_phrases_fr = [
    "Bonjour, je m'appelle Silver, comment ça va ?",
    "Je cherche mon chemin.",
    "Il fait beau aujourd'hui.",
    "Nous marchons le long de la rivière.",
    "Combien coûte cette montre ?",
    "Le soleil brille à travers les nuages.",
    "Je voudrais un verre d'eau s'il vous plaît.",
    "L'enfant mange du pain et boit de l'eau.",
    "La maison est grande et belle.",
    "Où est la gare ?"
]

print("=" * 60)
print("TESTS FRANÇAIS -> LUMINA -> FRANÇAIS")
print("=" * 60)

for fr in test_phrases_fr:
    res = t.translate_fr_to_lumina(fr)
    lum = res["target"]
    back = t.translate_lumina_to_fr(lum)
    has_bracket = "[" in lum
    status = "WARN BRACKETS" if has_bracket else "OK CLEAN"
    print(f"\n[FR]: {fr}")
    print(f"[{status} -> LUM]: {lum}")
    print(f"[BACK -> FR]: {back['target']}")

test_phrases_en = [
    "Hello, my name is Silver, how are you?",
    "I am looking for my way.",
    "We walk along the river.",
    "How much does this watch cost?",
    "The sun shines through the clouds.",
    "I would like a glass of water please.",
    "The house is big and beautiful."
]

print("\n" + "=" * 60)
print("TESTS ANGLAIS -> LUMINA -> ANGLAIS")
print("=" * 60)

for en in test_phrases_en:
    res = t.translate_en_to_lumina(en)
    lum = res["target"]
    back = t.translate_lumina_to_en(lum)
    has_bracket = "[" in lum
    status = "WARN BRACKETS" if has_bracket else "OK CLEAN"
    print(f"\n[EN]: {en}")
    print(f"[{status} -> LUM]: {lum}")
    print(f"[BACK -> EN]: {back['target']}")
