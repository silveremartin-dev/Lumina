"""Script to build the comprehensive Lumina Lexicon (multi-thousand words).
Strictly adheres to AGENTS.md and formal specifications:
- Zero exceptions
- Pure orthogonal matrix C1-V1-C2-V2
- 100% preservation of the initial 71 roots
- Complete French and English mappings
- Regular adverb derivation with -fi
"""

import sys
import re
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.families_domain_t_d import FAMILIES_T_D
from scripts.families_domain_k_g import FAMILIES_K_G
from scripts.families_domain_p_b import FAMILIES_P_B
from scripts.families_domain_s_z import FAMILIES_S_Z
from scripts.families_domain_m_n import FAMILIES_M_N
from scripts.families_domain_f_v import FAMILIES_F_V
from scripts.families_domain_l_r import FAMILIES_L_R
from scripts.families_domain_sh_zh import FAMILIES_SH_ZH
from scripts.families_domain_j_ch import FAMILIES_J_CH
from scripts.families_domain_h import FAMILIES_H
from scripts.families_expansion import FAMILIES_EXPANSION
from scripts.families_expansion_part2 import FAMILIES_EXPANSION_PART2
from scripts.families_expansion_part3 import FAMILIES_EXPANSION_PART3
from scripts.families_expansion_part4 import FAMILIES_EXPANSION_PART4
from scripts.families_expansion_part5 import FAMILIES_EXPANSION_PART5
from scripts.baseline_data import BASELINE_DATA

def main():
    lexique_path = ROOT_DIR / "data" / "lexique.json"
    original_data = BASELINE_DATA

    # Preserve existing items
    existing_particles = original_data.get("particles", [])
    existing_pronouns = original_data.get("pronouns", [])
    existing_numbers = original_data.get("numbers", [])
    existing_roots = original_data.get("roots", [])

    existing_root_dict = {r["word"].lower(): r for r in existing_roots}
    print(f"Loaded {len(existing_root_dict)} existing roots.")

    all_families = (
        FAMILIES_T_D + FAMILIES_K_G + FAMILIES_P_B + FAMILIES_S_Z +
        FAMILIES_M_N + FAMILIES_F_V + FAMILIES_L_R + FAMILIES_SH_ZH +
        FAMILIES_J_CH + FAMILIES_H + FAMILIES_EXPANSION + FAMILIES_EXPANSION_PART2 +
        FAMILIES_EXPANSION_PART3 + FAMILIES_EXPANSION_PART4 + FAMILIES_EXPANSION_PART5
    )
    print(f"Loaded {len(all_families)} semantic families.")

    final_roots_dict = {}

    # 1. Insert existing roots first
    for w, r in existing_root_dict.items():
        final_roots_dict[w] = r

    # 2. Derive all 5 canonical roles for each family
    pos_map = {
        'a': 'noun',
        'i': 'verb',
        'u': 'adj',
        'o': 'locus',
        'e': 'agent'
    }

    added_count = 0
    for fam in all_families:
        c1, c2, v2, domain, roles = fam
        # Check 5 vowels
        for v1 in ['a', 'i', 'u', 'o', 'e']:
            word = f"{c1}{v1}{c2}{v2}".lower()
            if word in final_roots_dict:
                # Existing word preserved!
                continue
            
            if v1 in roles:
                fr, en, sem = roles[v1]
                pos = pos_map[v1]
                final_roots_dict[word] = {
                    "word": word,
                    "pos": pos,
                    "domain": domain,
                    "semantic": sem,
                    "fr": fr,
                    "en": en
                }
                added_count += 1

    print(f"Generated {added_count} new canonical roots. Total roots: {len(final_roots_dict)}.")

    # 3. Derive adverbs with -fi from adjectives
    adverbs_list = []
    for w, item in list(final_roots_dict.items()):
        if item.get("pos") == "adj" and not w.endswith("fi"):
            adv_word = f"{w}fi"
            base_fr = item.get("fr", "").split(",")[0].strip()
            base_en = item.get("en", "").split(",")[0].strip()
            
            # French adverb formation helper
            fr_adv = f"{base_fr}ment"
            if base_fr.endswith("e"):
                fr_adv = f"{base_fr}ment"
            elif base_fr in ["bon", "beau"]:
                fr_adv = "bien, bellement"
            elif base_fr == "vrai":
                fr_adv = "vraiment, en vérité"
            elif base_fr == "grand":
                fr_adv = "grandement, beaucoup"
            elif base_fr == "petit":
                fr_adv = "peu, modérément"
            elif base_fr == "heureux":
                fr_adv = "heureusement, avec joie"
            else:
                fr_adv = f"de façon {base_fr}, {base_fr}ment"

            en_adv = f"{base_en}ly"
            if base_en == "good":
                en_adv = "well, finely"
            elif base_en == "fast":
                en_adv = "fast, quickly"

            adverbs_list.append({
                "word": adv_word,
                "pos": "adverb",
                "domain": item.get("domain", "Modificateur / Adverbe"),
                "semantic": f"Manière dérivée de {item.get('semantic', base_fr)}",
                "fr": fr_adv,
                "en": en_adv,
                "base": w
            })

    print(f"Generated {len(adverbs_list)} derived adverbs with -fi.")

    # Sort all canonical roots alphabetically
    sorted_roots = sorted(final_roots_dict.values(), key=lambda x: x["word"])

    # Build updated JSON payload
    updated_data = {
        "particles": existing_particles,
        "pronouns": existing_pronouns,
        "numbers": existing_numbers,
        "roots": sorted_roots,
        "adverbs": adverbs_list
    }

    # Save to data/lexique.json
    with open(lexique_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {lexique_path} with {len(sorted_roots)} roots and {len(adverbs_list)} adverbs.")

    # Save to docs/dictionary.json
    docs_dict_path = ROOT_DIR / "docs" / "dictionary.json"
    with open(docs_dict_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {docs_dict_path}.")

    # Generate Markdown documentation in docs/dictionary.md
    docs_md_path = ROOT_DIR / "docs" / "dictionary.md"
    with open(docs_md_path, "w", encoding="utf-8") as f:
        f.write("# Lumina — Dictionnaire Lexical Exhaustif & Matrice Sémantique\n\n")
        f.write(f"Ce document recense les **{len(sorted_roots)} racines canoniques** ($C_1V_1C_2V_2$) ")
        f.write(f"et les **{len(adverbs_list)} adverbes réguliers** (suffixe `-fi`) de la langue logique Lumina.\n\n")
        f.write("## 1. Particules & Marqueurs Grammaticaux\n\n")
        f.write("| Mot | Rôle | Français | English | Description |\n")
        f.write("|---|---|---|---|---|\n")
        for p in existing_particles:
            f.write(f"| `{p['word']}` | {p.get('type','')} | {p.get('fr','')} | {p.get('en','')} | {p.get('desc','')} |\n")

        f.write("\n## 2. Pronoms Personnels\n\n")
        f.write("| Pronom | Personne | Français | English |\n")
        f.write("|---|---|---|---|\n")
        for pr in existing_pronouns:
            f.write(f"| `{pr['word']}` | {pr.get('desc','')} | {pr.get('fr','')} | {pr.get('en','')} |\n")

        f.write("\n## 3. Nombres\n\n")
        f.write("| Mot | Valeur | Français | English |\n")
        f.write("|---|---|---|---|\n")
        for nb in existing_numbers:
            f.write(f"| `{nb['word']}` | {nb.get('value','')} | {nb.get('fr','')} | {nb.get('en','')} |\n")

        f.write(f"\n## 4. Racines Canoniques ($C_1V_1C_2V_2$) — {len(sorted_roots)} Entrées\n\n")
        f.write("| Racine | POS | Domaine | Sémantique | Français | English |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in sorted_roots:
            f.write(f"| `{r['word']}` | {r.get('pos','')} | {r.get('domain','')} | {r.get('semantic','')} | {r.get('fr','')} | {r.get('en','')} |\n")

        f.write(f"\n## 5. Adverbes Dérivés (Suffixe `-fi`) — {len(adverbs_list)} Entrées\n\n")
        f.write("| Adverbe | Base Adj | Français | English |\n")
        f.write("|---|---|---|---|\n")
        for adv in adverbs_list:
            f.write(f"| `{adv['word']}` | `{adv.get('base','')}` | {adv.get('fr','')} | {adv.get('en','')} |\n")

    print(f"Generated {docs_md_path}.")

if __name__ == "__main__":
    main()
