"""Unit tests for Lumina morphological analyzer and phonetic transcriber."""

import pytest
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from source.analyzer import LuminaAnalyzer

@pytest.fixture
def analyzer():
    return LuminaAnalyzer()

def test_canonical_root_breakdown(analyzer):
    res = analyzer.analyze_word("kafa")
    assert res["clean"] == "kafa"
    assert res["type"] == "noun"
    assert res["breakdown"]["c1"] == "K"
    assert res["breakdown"]["v1"] == "a"
    assert res["breakdown"]["role"] == "Nom"
    assert "animal" in res["meaning_fr"]

def test_verb_root_breakdown(analyzer):
    res = analyzer.analyze_word("sifi")
    assert res["type"] == "verb"
    assert res["breakdown"]["c1"] == "S"
    assert res["breakdown"]["v1"] == "i"
    assert res["breakdown"]["role"] == "Verbe"
    assert "voir" in res["meaning_fr"]

def test_particle_identification(analyzer):
    res = analyzer.analyze_word("la")
    assert "particle" in res["type"]
    assert "le, la, les" in res["meaning_fr"]

    res_na = analyzer.analyze_word("na")
    assert "particle" in res_na["type"]
    assert "[passé]" in res_na["meaning_fr"]

def test_pronouns(analyzer):
    mina = analyzer.analyze_word("mina")
    assert mina["type"] == "pronoun"
    assert "je" in mina["meaning_fr"]

    miro = analyzer.analyze_word("miro")
    assert miro["type"] == "pronoun"
    assert "nous" in miro["meaning_fr"]

def test_number_sequence(analyzer):
    pano = analyzer.analyze_word("pano")
    assert pano["type"] == "number"
    assert "0" in pano["meaning_fr"]

    pani = analyzer.analyze_word("pani")
    assert pani["type"] == "number"
    assert "2" in pani["meaning_fr"]

    panu = analyzer.analyze_word("panu")
    assert panu["type"] == "number"
    assert "3" in panu["meaning_fr"]

def test_adverb_derivation(analyzer):
    res = analyzer.analyze_word("purufi")
    assert res["type"] == "adverb"
    assert "-fi" in res["breakdown"].get("suffix", "")

def test_ipa_stress_rule(analyzer):
    # Penultimate stress rule on 2-syllable word
    ipa_kafa = analyzer.to_ipa("kafa")
    assert ipa_kafa == "/ˈkafa/"

    # Digraph substitution
    ipa_chapo = analyzer.to_ipa("chapo")
    assert "t͡ʃ" in ipa_chapo
