"""Script to reassign duplicate or invalid family keys to guaranteed unique, valid slots.
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.baseline_data import BASELINE_DATA
import re

CONSONANTS = ['t', 'd', 'k', 'g', 'p', 'b', 's', 'z', 'm', 'n', 'f', 'v', 'l', 'r', 'sh', 'zh', 'j', 'ch', 'h']
VOWELS = ['a', 'e', 'i', 'o', 'u']

# 1. Collect baseline reserved root keys
baseline_keys = set()
for r in BASELINE_DATA['roots']:
    w = r['word'].lower()
    m = re.match(r'^(sh|zh|ch|[a-z])([aeiou])(sh|zh|ch|[a-z])([aeiou])$', w)
    if m:
        c1, v1, c2, v2 = m.groups()
        baseline_keys.add((c1, c2, v2))

# Also particles and pronouns
for p in BASELINE_DATA['particles']:
    w = p['word'].lower()
    m = re.match(r'^(sh|zh|ch|[a-z])([aeiou])(sh|zh|ch|[a-z])([aeiou])$', w)
    if m:
        c1, v1, c2, v2 = m.groups()
        baseline_keys.add((c1, c2, v2))

for pr in BASELINE_DATA['pronouns']:
    w = pr['word'].lower()
    m = re.match(r'^(sh|zh|ch|[a-z])([aeiou])(sh|zh|ch|[a-z])([aeiou])$', w)
    if m:
        c1, v1, c2, v2 = m.groups()
        baseline_keys.add((c1, c2, v2))

print(f"Total baseline reserved keys: {len(baseline_keys)}")

# Helper to find next free key
used_keys = set(baseline_keys)

def get_free_slot(c1_pref, alternative_c1=None):
    for c1 in [c1_pref] + ([alternative_c1] if alternative_c1 else []):
        for c2 in CONSONANTS:
            for v2 in VOWELS:
                key = (c1, c2, v2)
                if key not in used_keys:
                    used_keys.add(key)
                    return key
    raise ValueError(f"No free slot for {c1_pref}")

# Let's inspect each file and build a clean dictionary of families
# We want to keep all valid, non-duplicate families, and reassign only the duplicates/invalids.

import scripts.families_domain_t_d as mod_t_d
import scripts.families_domain_k_g as mod_k_g
import scripts.families_domain_p_b as mod_p_b
import scripts.families_domain_s_z as mod_s_z
import scripts.families_domain_m_n as mod_m_n
import scripts.families_domain_f_v as mod_f_v
import scripts.families_domain_l_r as mod_l_r
import scripts.families_domain_sh_zh as mod_sh_zh
import scripts.families_domain_j_ch as mod_j_ch
import scripts.families_domain_h as mod_h
import scripts.families_expansion as mod_exp1
import scripts.families_expansion_part2 as mod_exp2
import scripts.families_expansion_part3 as mod_exp3

modules = [
    ("families_domain_t_d.py", mod_t_d.FAMILIES_T_D, "FAMILIES_T_D"),
    ("families_domain_k_g.py", mod_k_g.FAMILIES_K_G, "FAMILIES_K_G"),
    ("families_domain_p_b.py", mod_p_b.FAMILIES_P_B, "FAMILIES_P_B"),
    ("families_domain_s_z.py", mod_s_z.FAMILIES_S_Z, "FAMILIES_S_Z"),
    ("families_domain_m_n.py", mod_m_n.FAMILIES_M_N, "FAMILIES_M_N"),
    ("families_domain_f_v.py", mod_f_v.FAMILIES_F_V, "FAMILIES_F_V"),
    ("families_domain_l_r.py", mod_l_r.FAMILIES_L_R, "FAMILIES_L_R"),
    ("families_domain_sh_zh.py", mod_sh_zh.FAMILIES_SH_ZH, "FAMILIES_SH_ZH"),
    ("families_domain_j_ch.py", mod_j_ch.FAMILIES_J_CH, "FAMILIES_J_CH"),
    ("families_domain_h.py", mod_h.FAMILIES_H, "FAMILIES_H"),
    ("families_expansion.py", mod_exp1.FAMILIES_EXPANSION, "FAMILIES_EXPANSION"),
    ("families_expansion_part2.py", mod_exp2.FAMILIES_EXPANSION_PART2, "FAMILIES_EXPANSION_PART2"),
    ("families_expansion_part3.py", mod_exp3.FAMILIES_EXPANSION_PART3, "FAMILIES_EXPANSION_PART3"),
]

reassigned_count = 0
cleaned_modules = {}

for fname, fam_list, var_name in modules:
    new_fam_list = []
    for fam in fam_list:
        c1, c2, v2, dom, roles = fam[0].lower(), fam[1].lower(), fam[2].lower(), fam[3], fam[4]
        # Check validity and uniqueness
        is_valid = (c1 in CONSONANTS and c2 in CONSONANTS and v2 in VOWELS)
        key = (c1, c2, v2)
        if not is_valid or key in used_keys:
            # Reassign!
            # Determine alternative domain consonant
            alt_map = {
                'k': 'g', 'g': 'k', 't': 'd', 'd': 't', 'p': 'b', 'b': 'p',
                's': 'z', 'z': 's', 'm': 'n', 'n': 'm', 'f': 'v', 'v': 'f',
                'l': 'r', 'r': 'l', 'sh': 'zh', 'zh': 'sh', 'j': 'ch', 'ch': 'j'
            }
            new_c1, new_c2, new_v2 = get_free_slot(c1, alt_map.get(c1))
            new_fam = (new_c1, new_c2, new_v2, dom, roles)
            new_fam_list.append(new_fam)
            reassigned_count += 1
            print(f"Reassigned in {fname}: {key} -> ({new_c1}, {new_c2}, {new_v2}) [{dom}]")
        else:
            used_keys.add(key)
            new_fam_list.append((c1, c2, v2, dom, roles))
    cleaned_modules[fname] = (var_name, new_fam_list)

print(f"\nTotal reassigned: {reassigned_count}")
print(f"Total active family keys in use: {len(used_keys)}")

# Now serialize each file back cleanly!
def serialize_family(fam):
    c1, c2, v2, dom, roles = fam
    lines = [f"    ('{c1}', '{c2}', '{v2}', {repr(dom)}, {{"]
    for role_v in ['a', 'i', 'u', 'o', 'e']:
        if role_v in roles:
            fr, en, sem = roles[role_v]
            lines.append(f"        '{role_v}': ({repr(fr)}, {repr(en)}, {repr(sem)}),")
    lines.append("    }),")
    return "\n".join(lines)

for fname, (var_name, fam_list) in cleaned_modules.items():
    fpath = ROOT_DIR / "scripts" / fname
    header = f'"""Lumina Semantic Families for {fname}.\nAuto-cleaned and verified 100% collision-free C1-V1-C2-V2.\n"""\n\n{var_name} = [\n'
    body = "\n".join(serialize_family(fam) for fam in fam_list)
    footer = "\n]\n"
    fpath.write_text(header + body + footer, encoding="utf-8")
    print(f"Wrote {len(fam_list)} families to {fname}.")

print("All family files successfully updated and collision-free!")
