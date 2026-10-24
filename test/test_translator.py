"""Unit tests for Lumina bidirectional translator."""

import pytest
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from source.translator import LuminaTranslator

@pytest.fixture
def translator():
    return LuminaTranslator()

def test_lumina_to_fr_simple(translator):
    res = translator.translate_lumina_to_fr("Mina sifi la kafa")
    assert "Je" in res["target"]
    assert "voir" in res["target"]
    assert "animal" in res["target"]
    assert len(res["glosses"]) == 4

def test_lumina_to_fr_past(translator):
    res = translator.translate_lumina_to_fr("Mina na kidi la kafa kabo")
    assert "J'ai mangé" in res["target"] or "a manger" in res["target"]
    assert "éléphant" in res["target"]

def test_fr_to_lumina_simple(translator):
    res = translator.translate_fr_to_lumina("Je vois l'animal")
    assert "Mina" in res["target"]
    assert "sifi" in res["target"]
    assert "la" in res["target"]
    assert "kafa" in res["target"]

def test_fr_to_lumina_past(translator):
    res = translator.translate_fr_to_lumina("J'ai vu l'éléphant")
    assert "Mina" in res["target"]
    assert "na" in res["target"]
    assert "sifi" in res["target"]
    assert "kabo" in res["target"]

def test_fr_to_lumina_question(translator):
    res = translator.translate_fr_to_lumina("Est-ce que tu vois l'animal ?")
    assert res["target"].startswith("Ma")
    assert "tina" in res["target"].lower()
    assert "sifi" in res["target"]
    assert res["target"].endswith("?")

def test_fr_to_lumina_conversational_phrase(translator):
    res = translator.translate_fr_to_lumina("Bonjour, je m'appelle Silver, comment ça va ?")
    target = res["target"]
    assert "Fali" in target
    assert "Mina" in target
    assert "nomi" in target
    assert "Silver" in target
    assert "Tina" in target
    assert "zelu" in target

def test_lumina_to_fr_conversational_phrase(translator):
    res = translator.translate_lumina_to_fr("Fali, Mina nomi Silver, Ma Tina shili zelu?")
    target = res["target"]
    assert "Bonjour" in target
    assert "Silver" in target
    assert "m'appelle" in target.lower()
    assert "bien" in target.lower()

def test_lexicon_scale_multi_thousand(translator):
    assert len(translator.fr_to_lumina) >= 3000

def test_petit_prince_full_restoration():
    import json
    data_path = Path(__file__).resolve().parent.parent / "data" / "petit_prince.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["sentences"]) == 22
    assert "Arizona" in data["sentences"][14]["fr"]
    assert "cravates" in data["sentences"][20]["fr"]

def test_en_to_lumina_conversational_phrase(translator):
    res = translator.translate_en_to_lumina("Hello, my name is Silver, how are you?")
    target = res["target"]
    assert "Fali" in target
    assert "Mina" in target
    assert "nomi" in target
    assert "Silver" in target
    assert "Tina" in target
    assert "zelu" in target

def test_lumina_to_en_conversational_phrase(translator):
    res = translator.translate_lumina_to_en("Fali, Mina nomi Silver, Ma Tina shili zelu?")
    target = res["target"]
    assert "Hello" in target
    assert "Silver" in target
    assert "name is" in target.lower()
    assert "well" in target.lower()

def test_fr_everyday_sentences_clean(translator):
    sentences = [
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
    for s in sentences:
        res = translator.translate_fr_to_lumina(s)
        assert "[" not in res["target"], f"Bracket failure on '{s}': {res['target']}"

def test_en_everyday_sentences_clean(translator):
    sentences = [
        "Hello, my name is Silver, how are you?",
        "I am looking for my way.",
        "We walk along the river.",
        "How much does this watch cost?",
        "The sun shines through the clouds.",
        "I would like a glass of water please.",
        "The house is big and beautiful."
    ]
    for s in sentences:
        res = translator.translate_en_to_lumina(s)
        assert "[" not in res["target"], f"Bracket failure on '{s}': {res['target']}"
