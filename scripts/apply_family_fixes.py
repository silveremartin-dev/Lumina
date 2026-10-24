"""Script to apply clean, collision-free family fixes to:
- scripts/families_domain_k_g.py
- scripts/families_domain_l_r.py
- scripts/families_expansion.py
- scripts/families_expansion_part2.py
- scripts/families_expansion_part3.py
"""

from pathlib import Path
import re

ROOT_DIR = Path(__file__).resolve().parent.parent

def fix_k_g():
    path = ROOT_DIR / "scripts" / "families_domain_k_g.py"
    content = path.read_text(encoding="utf-8")
    
    # 1. Replace second ('k', 'p', 'a', ...) at index 31: hat duplicate -> foot/step ('k', 'p', 'e')
    old_31 = """    ('k', 'p', 'a', "Espace / Matière & Forme", {
        'a': ("chapeau, couvre-chef", "hat, cap", "Protection de tête"),"""
    new_31 = """    ('k', 'p', 'e', "Espace / Corps & Pied", {
        'a': ("pied, patte, pas", "foot, paw, step", "Organe de locomotion au sol"),"""
    if old_31 in content:
        content = content.replace(old_31, new_31, 1)

    # 2. Fix index 32: ('k', 'o', 'p', ...) -> ('k', 'n', 'a', ...)
    old_32 = """    ('k', 'o', 'p', "Espace / Matière & Corps", {
        'a': ("nez, trompe, appendice nasal", "nose, trunk, muzzle", "Organe de l'odorat et de respiration"),"""
    new_32 = """    ('k', 'n', 'a', "Espace / Matière & Corps", {
        'a': ("nez, trompe, appendice nasal", "nose, trunk, muzzle", "Organe de l'odorat et de respiration"),"""
    if old_32 in content:
        content = content.replace(old_32, new_32, 1)

    # 3. Fix index 47: boite/coffre ('k', 'b', 'o', ...) -> ('k', 'b', 'e', ...)
    old_47 = """    ('k', 'b', 'o', "Espace / Matière & Forme", {
        'a': ("boîte, coffre, réceptacle fermé", "box, chest, crate, container\""""
    new_47 = """    ('k', 'b', 'e', "Espace / Matière & Forme", {
        'a': ("boîte, coffre, réceptacle fermé", "box, chest, crate, container\""""
    if old_47 in content:
        content = content.replace(old_47, new_47, 1)

    # 4. Fix index 52: réseau ('g', 'f', 'o', ...) -> ('g', 'f', 'e', ...)
    old_52 = """    ('g', 'f', 'o', "Espace / Lien & Système", {
        'a': ("réseau, toile, matrice maillée", "network, web, mesh, internet\""""
    new_52 = """    ('g', 'f', 'e', "Espace / Lien & Système", {
        'a': ("réseau, toile, matrice maillée", "network, web, mesh, internet\""""
    if old_52 in content:
        content = content.replace(old_52, new_52, 1)

    path.write_text(content, encoding="utf-8")
    print("Fixed families_domain_k_g.py successfully.")

def fix_l_r():
    path = ROOT_DIR / "scripts" / "families_domain_l_r.py"
    content = path.read_text(encoding="utf-8")

    # index 3: voyage ('l', 's', 'o') -> ('l', 's', 'u')
    old_3 = "('l', 's', 'o', \"Mouvement / Voyage & Aventure\","
    new_3 = "('l', 's', 'u', \"Mouvement / Voyage & Aventure\","
    assert old_3 in content, "old_3 not found"
    content = content.replace(old_3, new_3, 1)

    # index 12: voiture ('l', 'k', 'o') -> ('l', 'k', 'u')
    old_12 = "('l', 'k', 'o', \"Mouvement / Voiture & Automobile\","
    new_12 = "('l', 'k', 'u', \"Mouvement / Voiture & Automobile\","
    assert old_12 in content, "old_12 not found"
    content = content.replace(old_12, new_12, 1)

    path.write_text(content, encoding="utf-8")
    print("Fixed families_domain_l_r.py successfully.")

def fix_expansion():
    path = ROOT_DIR / "scripts" / "families_expansion.py"
    content = path.read_text(encoding="utf-8")

    # Faim: ('k', 't', 'u') -> ('k', 'f', 'i')
    content = content.replace("('k', 't', 'u', \"Espace / Matière & Faim\"", "('k', 'f', 'i', \"Espace / Matière & Faim\"", 1)
    # Pain: ('k', 'm', 'u') -> ('k', 'm', 'a')
    content = content.replace("('k', 'm', 'u', \"Espace / Matière & Pain\"", "('k', 'm', 'a', \"Espace / Matière & Pain\"", 1)
    # Lait: ('k', 'l', 'a') -> ('k', 'l', 'u')
    content = content.replace("('k', 'l', 'a', \"Espace / Matière & Lait\"", "('k', 'l', 'u', \"Espace / Matière & Lait\"", 1)
    # Raisin: ('k', 's', 'i') -> ('k', 's', 'e')
    content = content.replace("('k', 's', 'i', \"Espace / Matière & Raisin/Vigne\"", "('k', 's', 'e', \"Espace / Matière & Raisin/Vigne\"", 1)
    # Visage: ('k', 'b', 'i') -> ('k', 'v', 'a')
    content = content.replace("('k', 'b', 'i', \"Espace / Corps & Visage\"", "('k', 'v', 'a', \"Espace / Corps & Visage\"", 1)
    # Bouche: ('k', 'b', 'u') -> ('k', 'b', 'a')
    content = content.replace("('k', 'b', 'u', \"Espace / Corps & Bouche\"", "('k', 'b', 'a', \"Espace / Corps & Bouche\"", 1)
    # Bras: ('k', 't', 'o') -> ('k', 'r', 'a')
    content = content.replace("('k', 't', 'o', \"Espace / Corps & Bras\"", "('k', 'r', 'a', \"Espace / Corps & Bras\"", 1)
    # Os: ('k', 's', 'o') -> ('k', 's', 'u')
    content = content.replace("('k', 's', 'o', \"Espace / Corps & Os\"", "('k', 's', 'u', \"Espace / Corps & Os\"", 1)
    # Volcan: ('k', 'v', 'l') -> ('k', 'v', 'o')
    content = content.replace("('k', 'v', 'l', \"Espace / Objet & Volcan\"", "('k', 'v', 'o', \"Espace / Objet & Volcan\"", 1)
    # Globe: ('j', 'g', 'l') -> ('j', 'g', 'u')
    content = content.replace("('j', 'g', 'l', \"Outil / Objet & Globe de verre\"", "('j', 'g', 'u', \"Outil / Objet & Globe de verre\"", 1)

    path.write_text(content, encoding="utf-8")
    print("Fixed families_expansion.py successfully.")

def fix_expansion_part2():
    path = ROOT_DIR / "scripts" / "families_expansion_part2.py"
    content = path.read_text(encoding="utf-8")

    # Prise: ('k', 't', 'i') -> ('k', 't', 'e')
    content = content.replace("('k', 't', 'i', \"Espace / Action & Prise\"", "('k', 't', 'e', \"Espace / Action & Prise\"", 1)
    # Cloche: ('j', 'k', 'l') -> ('j', 'k', 'e')
    content = content.replace("('j', 'k', 'l', \"Outil / Objet & Cloche/Dôme\"", "('j', 'k', 'e', \"Outil / Objet & Cloche/Dôme\"", 1)
    # Jeux salon: ('j', 'g', 'o') -> ('j', 'g', 'a')
    content = content.replace("('j', 'g', 'o', \"Outil / Loisir & Jeux de salon (Bridge, Golf)\"", "('j', 'g', 'a', \"Outil / Loisir & Jeux de salon (Bridge, Golf)\"", 1)
    # Carré/Angle: ('p', 'k', 'o') -> ('p', 'k', 'u')
    content = content.replace("('p', 'k', 'o', \"Quantité / Forme & Carré/Angle\"", "('p', 'k', 'u', \"Quantité / Forme & Carré/Angle\"", 1)

    path.write_text(content, encoding="utf-8")
    print("Fixed families_expansion_part2.py successfully.")

def fix_expansion_part3():
    path = ROOT_DIR / "scripts" / "families_expansion_part3.py"
    content = path.read_text(encoding="utf-8")

    # Faune & Loup: ('k', 'v', 'i') -> ('k', 'v', 'e')
    content = content.replace("('k', 'v', 'i', \"Espace / Faune & Loup\"", "('k', 'v', 'e', \"Espace / Faune & Loup\"", 1)
    # Faune & Ours: ('k', 'b', 'r') -> ('k', 'g', 'a')
    content = content.replace("('k', 'b', 'r', \"Espace / Faune & Ours\"", "('k', 'g', 'a', \"Espace / Faune & Ours\"", 1)
    # Faune & Cerf: ('k', 'r', 'b') -> ('k', 'r', 'e')
    content = content.replace("('k', 'r', 'b', \"Espace / Faune & Cerf/Biche\"", "('k', 'r', 'e', \"Espace / Faune & Cerf/Biche\"", 1)
    # Faune & Lapin: ('k', 'l', 'p') -> ('k', 'l', 'e')
    content = content.replace("('k', 'l', 'p', \"Espace / Faune & Lapin/Lièvre\"", "('k', 'l', 'e', \"Espace / Faune & Lapin/Lièvre\"", 1)
    # Faune & Aigle: ('k', 'g', 'l') -> ('k', 'g', 'e')
    content = content.replace("('k', 'g', 'l', \"Espace / Faune & Aigle/Oiseau de proie\"", "('k', 'g', 'e', \"Espace / Faune & Aigle/Oiseau de proie\"", 1)
    # Faune & Tortue: ('k', 'd', 'k') -> ('k', 'd', 'u')
    content = content.replace("('k', 'd', 'k', \"Espace / Faune & Tortue\"", "('k', 'd', 'u', \"Espace / Faune & Tortue\"", 1)
    # Faune & Abeille: ('k', 's', 'm') -> ('k', 'z', 'a')
    content = content.replace("('k', 's', 'm', \"Espace / Faune & Abeille\"", "('k', 'z', 'a', \"Espace / Faune & Abeille\"", 1)
    # Végétal & Chêne: ('k', 'd', 'r') -> ('k', 'd', 'e')
    content = content.replace("('k', 'd', 'r', \"Espace / Végétal & Chêne\"", "('k', 'd', 'e', \"Espace / Végétal & Chêne\"", 1)
    # Végétal & Palmier: ('k', 'p', 'l') -> ('k', 'p', 'i')
    content = content.replace("('k', 'p', 'l', \"Espace / Végétal & Palmier\"", "('k', 'p', 'i', \"Espace / Végétal & Palmier\"", 1)
    # Végétal & Menthe: ('k', 'm', 'n') -> ('k', 'm', 'e')
    content = content.replace("('k', 'm', 'n', \"Espace / Végétal & Menthe/Herbe aromatique\"", "('k', 'm', 'e', \"Espace / Végétal & Menthe/Herbe aromatique\"", 1)
    # Atome: ('p', 't', 'm') -> ('p', 't', 'a')
    content = content.replace("('p', 't', 'm', \"Quantité / Physique & Atome\"", "('p', 't', 'a', \"Quantité / Physique & Atome\"", 1)
    # Gravité: ('p', 'g', 'r') -> ('p', 'g', 'a')
    content = content.replace("('p', 'g', 'r', \"Quantité / Physique & Gravité\"", "('p', 'g', 'a', \"Quantité / Physique & Gravité\"", 1)
    # Vitesse lumière: ('p', 'v', 'l') -> ('p', 'v', 'a')
    content = content.replace("('p', 'v', 'l', \"Quantité / Physique & Vitesse de la lumière\"", "('p', 'v', 'a', \"Quantité / Physique & Vitesse de la lumière\"", 1)
    # Énergie: ('p', 'z', 'm') -> ('p', 'z', 'a')
    content = content.replace("('p', 'z', 'm', \"Quantité / Énergie & Puissance\"", "('p', 'z', 'a', \"Quantité / Énergie & Puissance\"", 1)
    # Tribunal: ('n', 't', 'r') -> ('n', 't', 'a')
    content = content.replace("('n', 't', 'r', \"Humain / Société & Tribunal\"", "('n', 't', 'a', \"Humain / Société & Tribunal\"", 1)
    # Théâtre: ('s', 't', 'r') -> ('s', 't', 'a')
    content = content.replace("('s', 't', 'r', \"Sensation / Art & Théâtre\"", "('s', 't', 'a', \"Sensation / Art & Théâtre\"", 1)
    # Sculpture: ('s', 'k', 'l') -> ('s', 'k', 'e')
    content = content.replace("('s', 'k', 'l', \"Sensation / Art & Sculpture\"", "('s', 'k', 'e', \"Sensation / Art & Sculpture\"", 1)
    # Photo: ('s', 'f', 't') -> ('s', 'f', 'e')
    content = content.replace("('s', 'f', 't', \"Sensation / Art & Photographie\"", "('s', 'f', 'e', \"Sensation / Art & Photographie\"", 1)
    # Violon: ('s', 'v', 'l') -> ('s', 'v', 'a')
    content = content.replace("('s', 'v', 'l', \"Sensation / Musique & Violon/Cordes\"", "('s', 'v', 'a', \"Sensation / Musique & Violon/Cordes\"", 1)
    # Flûte: ('s', 'f', 'l') -> ('s', 'f', 'u')
    content = content.replace("('s', 'f', 'l', \"Sensation / Musique & Flûte/Vent\"", "('s', 'f', 'u', \"Sensation / Musique & Flûte/Vent\"", 1)

    path.write_text(content, encoding="utf-8")
    print("Fixed families_expansion_part3.py successfully.")

if __name__ == "__main__":
    fix_k_g()
    fix_l_r()
    fix_expansion()
    fix_expansion_part2()
    fix_expansion_part3()
