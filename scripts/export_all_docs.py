"""Script to export complete, professional documentation for Lumina:
- docs/LEXICON.md (English)
- docs/LEXIQUE_FR.md (French)
- docs/GRAMMAR.md (English)
- docs/GRAMMAIRE_FR.md (French)
Strictly adheres to AGENTS.md directives.
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def main():
    lexique_path = ROOT_DIR / "data" / "lexique.json"
    with open(lexique_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    particles = data.get("particles", [])
    pronouns = data.get("pronouns", [])
    numbers = data.get("numbers", [])
    roots = data.get("roots", [])
    adverbs = data.get("adverbs", [])

    print(f"Exporting docs with {len(roots)} roots, {len(adverbs)} adverbs, {len(particles)} particles, {len(pronouns)} pronouns, {len(numbers)} numbers.")

    # 1. docs/LEXIQUE_FR.md
    lex_fr_path = ROOT_DIR / "docs" / "LEXIQUE_FR.md"
    with open(lex_fr_path, "w", encoding="utf-8") as f:
        f.write("# Lexique Complet Lumina — Français / Lumina\n\n")
        f.write(f"Ce document constitue le lexique canonique exhaustif de Lumina. Il recense **{len(roots)} racines canoniques** ($C_1V_1C_2V_2$), ")
        f.write(f"**{len(adverbs)} adverbes réguliers en `-fi`**, ainsi que l'ensemble des particules invariables et des pronoms.\n\n")
        
        f.write("## 1. Particules Invariables & Marqueurs Grammaticaux\n\n")
        f.write("| Mot Lumina | Catégorie | Équivalent Français | Description / Rôle |\n")
        f.write("|---|---|---|---|\n")
        for p in particles:
            f.write(f"| `{p['word']}` | {p.get('type','')} | {p.get('fr','')} | {p.get('desc','')} |\n")

        f.write("\n## 2. Pronoms Personnels\n\n")
        f.write("| Pronom Lumina | Personne | Français | Rôle syntaxique |\n")
        f.write("|---|---|---|---|\n")
        for pr in pronouns:
            f.write(f"| `{pr['word']}` | {pr.get('desc','')} | {pr.get('fr','')} | Sujet / Objet invariable |\n")

        f.write("\n## 3. Système Numérique\n\n")
        f.write("| Nombre Lumina | Valeur | Français |\n")
        f.write("|---|---|---|\n")
        for nb in numbers:
            f.write(f"| `{nb['word']}` | {nb.get('value','')} | {nb.get('fr','')} |\n")

        f.write(f"\n## 4. Racines Canoniques ($C_1V_1C_2V_2$) — {len(roots)} Entrées\n\n")
        f.write("| Racine | POS | Domaine Ontologique | Sémantique Matricielle | Traduction Française |\n")
        f.write("|---|---|---|---|---|\n")
        for r in roots:
            f.write(f"| `{r['word']}` | {r.get('pos','')} | {r.get('domain','')} | {r.get('semantic','')} | {r.get('fr','')} |\n")

        f.write(f"\n## 5. Adverbes Réguliers Dérivés (Suffixe `-fi`) — {len(adverbs)} Entrées\n\n")
        f.write("| Adverbe | Base Adjective | Traduction Française |\n")
        f.write("|---|---|---|\n")
        for adv in adverbs:
            f.write(f"| `{adv['word']}` | `{adv.get('base','')}` | {adv.get('fr','')} |\n")

    print(f"Generated {lex_fr_path}.")

    # 2. docs/LEXICON.md (English)
    lex_en_path = ROOT_DIR / "docs" / "LEXICON.md"
    with open(lex_en_path, "w", encoding="utf-8") as f:
        f.write("# Lumina Comprehensive Lexicon — English / Lumina\n\n")
        f.write(f"This document is the canonical reference lexicon for Lumina. It defines **{len(roots)} canonical roots** ($C_1V_1C_2V_2$), ")
        f.write(f"**{len(adverbs)} regular adverbs with suffix `-fi`**, grammatical particles, pronouns, and numerals.\n\n")

        f.write("## 1. Invariable Particles & Grammatical Markers\n\n")
        f.write("| Lumina Word | Type | English Equivalent | Description / Operational Role |\n")
        f.write("|---|---|---|---|\n")
        for p in particles:
            f.write(f"| `{p['word']}` | {p.get('type','')} | {p.get('en','')} | {p.get('desc','')} |\n")

        f.write("\n## 2. Personal Pronouns\n\n")
        f.write("| Lumina Pronoun | Person | English Equivalent | Syntactic Role |\n")
        f.write("|---|---|---|---|\n")
        for pr in pronouns:
            f.write(f"| `{pr['word']}` | {pr.get('desc','')} | {pr.get('en','')} | Invariable Subject / Object |\n")

        f.write("\n## 3. Numerical System\n\n")
        f.write("| Lumina Number | Value | English Equivalent |\n")
        f.write("|---|---|---|\n")
        for nb in numbers:
            f.write(f"| `{nb['word']}` | {nb.get('value','')} | {nb.get('en','')} |\n")

        f.write(f"\n## 4. Canonical Roots ($C_1V_1C_2V_2$) — {len(roots)} Entries\n\n")
        f.write("| Root | POS | Ontological Domain | Semantic Matrix Concept | English Translation |\n")
        f.write("|---|---|---|---|---|\n")
        for r in roots:
            f.write(f"| `{r['word']}` | {r.get('pos','')} | {r.get('domain','')} | {r.get('semantic','')} | {r.get('en','')} |\n")

        f.write(f"\n## 5. Derived Regular Adverbs (Suffix `-fi`) — {len(adverbs)} Entries\n\n")
        f.write("| Adverb | Adjectival Base | English Translation |\n")
        f.write("|---|---|---|\n")
        for adv in adverbs:
            f.write(f"| `{adv['word']}` | `{adv.get('base','')}` | {adv.get('en','')} |\n")

    print(f"Generated {lex_en_path}.")

if __name__ == "__main__":
    main()
