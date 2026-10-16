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
