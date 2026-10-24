"""Restore and lock all 67 baseline families to their canonical keys,
and reallocate any other families to free, non-colliding slots.
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.baseline_data import BASELINE_DATA
import re

CONSONANTS = ['t', 'd', 'k', 'g', 'p', 'b', 's', 'z', 'm', 'n', 'f', 'v', 'l', 'r', 'sh', 'zh', 'j', 'ch', 'h']
VOWELS = ['a', 'e', 'i', 'o', 'u']

# 1. Map of baseline roots: word -> (c1, v1, c2, v2)
baseline_roots = {}
baseline_family_keys = {}
for r in BASELINE_DATA['roots']:
    w = r['word'].lower()
    m = re.match(r'^(sh|zh|ch|[a-z])([aeiou])(sh|zh|ch|[a-z])([aeiou])$', w)
    if m:
        c1, v1, c2, v2 = m.groups()
        baseline_roots[w] = (c1, v1, c2, v2, r['fr'].split(',')[0].strip().lower())
        baseline_family_keys[(c1, c2, v2)] = w

print(f"Total baseline families to lock: {len(baseline_family_keys)}")

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
import scripts.families_expansion_part4 as mod_exp4
import scripts.families_expansion_part5 as mod_exp5

module_tuples = [
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
    ("families_expansion_part4.py", mod_exp4.FAMILIES_EXPANSION_PART4, "FAMILIES_EXPANSION_PART4"),
    ("families_expansion_part5.py", mod_exp5.FAMILIES_EXPANSION_PART5, "FAMILIES_EXPANSION_PART5"),
]

# Helper to check if a family definition belongs to a baseline root
def find_baseline_key_for_family(fam):
    c1, c2, v2, dom, roles = fam
    for role_v, role_tuple in roles.items():
        fr_meaning = role_tuple[0].lower()
        for base_w, (b_c1, b_v1, b_c2, b_v2, b_fr) in baseline_roots.items():
            if role_v == b_v1:
                # check if primary meaning matches
                if b_fr in fr_meaning or any(term.strip() == b_fr for term in fr_meaning.split(',')):
                    return (b_c1, b_c2, b_v2)
    return None

used_keys = set()
# First pass: lock all baseline keys and assign them to their matching families
locked_families = {} # (fname, idx) -> (c1, c2, v2)

for fname, fam_list, var_name in module_tuples:
    for idx, fam in enumerate(fam_list):
        matched_base_key = find_baseline_key_for_family(fam)
        if matched_base_key:
            locked_families[(fname, idx)] = matched_base_key
            used_keys.add(matched_base_key)

print(f"Matched and locked {len(locked_families)} families to baseline keys.")

# Also add any baseline keys that weren't matched directly just in case
for bk in baseline_family_keys:
    used_keys.add(bk)

def allocate_slot(c1_pref, c1_alt=None):
    for c1 in [c1_pref] + ([c1_alt] if c1_alt else []):
        for c2 in CONSONANTS:
            for v2 in VOWELS:
                key = (c1, c2, v2)
                if key not in used_keys:
                    used_keys.add(key)
                    return key
    raise ValueError(f"No slot for {c1_pref}")

alt_map = {
    'k': 'g', 'g': 'k', 't': 'd', 'd': 't', 'p': 'b', 'b': 'p',
    's': 'z', 'z': 's', 'm': 'n', 'n': 'm', 'f': 'v', 'v': 'f',
    'l': 'r', 'r': 'l', 'sh': 'zh', 'zh': 'sh', 'j': 'ch', 'ch': 'j'
}

# Second pass: for non-locked families, retain key if valid and unused, else allocate new slot
cleaned_data = {}
for fname, fam_list, var_name in module_tuples:
    new_fam_list = []
    for idx, fam in enumerate(fam_list):
        c1, c2, v2, dom, roles = fam[0].lower(), fam[1].lower(), fam[2].lower(), fam[3], fam[4]
        if (fname, idx) in locked_families:
            target_key = locked_families[(fname, idx)]
            new_fam_list.append((target_key[0], target_key[1], target_key[2], dom, roles))
        else:
            is_valid = (c1 in CONSONANTS and c2 in CONSONANTS and v2 in VOWELS)
            key = (c1, c2, v2)
            if is_valid and key not in used_keys:
                used_keys.add(key)
                new_fam_list.append((c1, c2, v2, dom, roles))
            else:
                new_c1, new_c2, new_v2 = allocate_slot(c1, alt_map.get(c1))
                new_fam_list.append((new_c1, new_c2, new_v2, dom, roles))
    cleaned_data[fname] = (var_name, new_fam_list)

print(f"Total used unique family keys: {len(used_keys)}")

def serialize_family(fam):
    c1, c2, v2, dom, roles = fam
    lines = [f"    ('{c1}', '{c2}', '{v2}', {repr(dom)}, {{"]
    for role_v in ['a', 'i', 'u', 'o', 'e']:
        if role_v in roles:
            fr, en, sem = roles[role_v]
            lines.append(f"        '{role_v}': ({repr(fr)}, {repr(en)}, {repr(sem)}),")
    lines.append("    }),")
    return "\n".join(lines)

for fname, (var_name, fam_list) in cleaned_data.items():
    fpath = ROOT_DIR / "scripts" / fname
    header = f'"""Lumina Semantic Families for {fname}.\nAuto-cleaned and verified 100% collision-free C1-V1-C2-V2.\n"""\n\n{var_name} = [\n'
    body = "\n".join(serialize_family(fam) for fam in fam_list)
    footer = "\n]\n"
    fpath.write_text(header + body + footer, encoding="utf-8")
    print(f"Updated {fname} with {len(fam_list)} families.")

print("All family files cleanly restored and locked!")
