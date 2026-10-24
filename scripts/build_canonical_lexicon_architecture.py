"""Master script to enforce Lumina ontological architecture across all family files.
Rules:
1. All baseline 71 roots, 24 particles, 6 pronouns, 11 numbers are 100% preserved.
2. Every family has c1 belonging to its domain:
   - families_domain_t_d.py: c1 in ['t', 'd']
   - families_domain_k_g.py: c1 in ['k', 'g']
   - families_domain_p_b.py: c1 in ['p', 'b']
   - families_domain_s_z.py: c1 in ['s', 'z']
   - families_domain_m_n.py: c1 in ['m', 'n']
   - families_domain_f_v.py: c1 in ['f', 'v']
   - families_domain_l_r.py: c1 in ['l', 'r']
   - families_domain_sh_zh.py: c1 in ['sh', 'zh']
   - families_domain_j_ch.py: c1 in ['j', 'ch']
   - families_domain_h.py: c1 in ['h']
   - families_expansion*.py: c1 chosen matching semantic domain
3. Every family key (c1, c2, v2) is 100% UNIQUE.
4. Total roots > 2,000, adverbs > 400.
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.baseline_data import BASELINE_DATA
import re

CONSONANTS = ['t', 'd', 'k', 'g', 'p', 'b', 's', 'z', 'm', 'n', 'f', 'v', 'l', 'r', 'sh', 'zh', 'j', 'ch', 'h']
VOWELS = ['a', 'e', 'i', 'o', 'u']

# 1. Collect baseline root keys
baseline_keys = {}
for r in BASELINE_DATA['roots']:
    w = r['word'].lower()
    m = re.match(r'^(sh|zh|ch|[a-z])([aeiou])(sh|zh|ch|[a-z])([aeiou])$', w)
    if m:
        c1, v1, c2, v2 = m.groups()
        baseline_keys[(c1, c2, v2)] = w

print(f"Total baseline family slots reserved: {len(baseline_keys)}")

used_keys = set(baseline_keys.keys())

def allocate_slot_for_domain(allowed_c1_list):
    for c1 in allowed_c1_list:
        for c2 in CONSONANTS:
            for v2 in VOWELS:
                key = (c1, c2, v2)
                if key not in used_keys:
                    used_keys.add(key)
                    return key
    raise ValueError(f"Exhausted slots for {allowed_c1_list}")

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

# Add crucial modal families to SH_ZH if not present
modal_families_sh_zh = [
    # Volition / Vouloir
    ('zh', 'v', 'i', 'Abstraction / Volonté & Désir', {
        'a': ('volonté, désir, souhait, voeu', 'will, desire, wish, volition', 'Force de vouloir'),
        'i': ('vouloir, souhaiter, désirer, aimer', 'to want, to wish, to desire, would like', 'Avoir la volonté de'),
        'u': ('volontaire, désiré, souhaité, voulu', 'willing, voluntary, desired, wanted', 'Animé par la volonté'),
        'o': ('sphère du vouloir, registre des voeux', 'realm of will, wishbook', 'Lieu des souhaits'),
        'e': ('volontaire, personne qui veut', 'wisher, willing agent', 'Personne voulant'),
    }),
    # Capability / Pouvoir
    ('zh', 'p', 'i', 'Abstraction / Pouvoir & Capacité', {
        'a': ('pouvoir, capacité, faculté, puissance', 'power, ability, capability, faculty', "Capacité d'agir"),
        'i': ('pouvoir, être capable de, être en mesure', 'can, to be able to, may', 'Avoir la faculté de'),
        'u': ('capable, possible, potentiel, puissant', 'capable, able, possible, potential', 'Qui peut accomplir'),
        'o': ('champ des possibles, sphère du pouvoir', 'realm of possibilities, power realm', 'Lieu du pouvoir'),
        'e': ('être capable, agent souverain', 'capable agent, achiever', 'Personne qui peut'),
    }),
    # Knowledge / Savoir
    ('sh', 'k', 'i', 'Abstraction / Savoir & Connaissance', {
        'a': ('savoir, connaissance, science, érudition', 'knowledge, science, lore, learning', 'Ensemble des vérités acquises'),
        'i': ('savoir, connaître, avoir conscience', 'to know, to be aware of, to understand', 'Posséder le savoir'),
        'u': ('savant, instruit, érudit, connu', 'knowledgeable, learned, known, wise', 'Qui sait'),
        'o': ('académie du savoir, bibliothèque, temple', 'knowledge haven, library, academy', 'Lieu du savoir'),
        'e': ('savant, érudit, sage, chercheur', 'scholar, sage, scientist', 'Personne qui sait'),
    }),
]

# Ensure Day / Night in T_D
time_families_t_d = [
    ('t', 'n', 'a', 'Temps / Chronologie & Jour', {
        'a': ('jour, journée, clarté diurne', 'day, daytime, daylight', 'Période de clarté entre deux nuits'),
        'i': ('faire jour, poindre (jour)', 'to dawn, to become day', 'Faire jour'),
        'u': ('diurne, de jour, quotidien', 'diurnal, daytime, daily', 'Relatif au jour'),
        'o': ('hémisphère de jour, cadran solaire', 'day side, sunlit hemisphere', 'Lieu éclairé de jour'),
        'e': ('être diurne, veilleur de jour', 'day creature, day watcher', 'Actif le jour'),
    }),
    ('t', 's', 'a', 'Temps / Chronologie & Nuit', {
        'a': ('nuit, obscurité nocturne, ombre', 'night, nighttime, darkness', 'Période nocturne sans soleil'),
        'i': ('faire nuit, tomber (nuit)', 'to become night, to fall (night)', 'Faire nuit'),
        'u': ('nocturne, de nuit, sombre', 'nocturnal, nightly, dark', 'Relatif à la nuit'),
        'o': ('nuit profonde, voûte obscure', 'dead of night, night sky', 'Royaume de la nuit'),
        'e': ('être nocturne, veilleur de nuit', 'night creature, night watcher', 'Actif la nuit'),
    }),
]

domain_configs = [
    ("families_domain_t_d.py", mod_t_d.FAMILIES_T_D + time_families_t_d, "FAMILIES_T_D", ['t', 'd']),
    ("families_domain_k_g.py", mod_k_g.FAMILIES_K_G, "FAMILIES_K_G", ['k', 'g']),
    ("families_domain_p_b.py", mod_p_b.FAMILIES_P_B, "FAMILIES_P_B", ['p', 'b']),
    ("families_domain_s_z.py", mod_s_z.FAMILIES_S_Z, "FAMILIES_S_Z", ['s', 'z']),
    ("families_domain_m_n.py", mod_m_n.FAMILIES_M_N, "FAMILIES_M_N", ['m', 'n']),
    ("families_domain_f_v.py", mod_f_v.FAMILIES_F_V, "FAMILIES_F_V", ['f', 'v']),
    ("families_domain_l_r.py", mod_l_r.FAMILIES_L_R, "FAMILIES_L_R", ['l', 'r']),
    ("families_domain_sh_zh.py", mod_sh_zh.FAMILIES_SH_ZH + modal_families_sh_zh, "FAMILIES_SH_ZH", ['sh', 'zh']),
    ("families_domain_j_ch.py", mod_j_ch.FAMILIES_J_CH, "FAMILIES_J_CH", ['j', 'ch']),
    ("families_domain_h.py", mod_h.FAMILIES_H, "FAMILIES_H", ['h']),
    ("families_expansion.py", mod_exp1.FAMILIES_EXPANSION, "FAMILIES_EXPANSION", ['k', 'g', 's', 'j']),
    ("families_expansion_part2.py", mod_exp2.FAMILIES_EXPANSION_PART2, "FAMILIES_EXPANSION_PART2", ['k', 'g', 'l', 'j', 's', 'p']),
    ("families_expansion_part3.py", mod_exp3.FAMILIES_EXPANSION_PART3, "FAMILIES_EXPANSION_PART3", ['k', 'g', 'p', 's', 'n']),
    ("families_expansion_part4.py", mod_exp4.FAMILIES_EXPANSION_PART4, "FAMILIES_EXPANSION_PART4", ['m', 's', 'l', 'p', 'j', 't', 'sh', 'k', 'g']),
    ("families_expansion_part5.py", mod_exp5.FAMILIES_EXPANSION_PART5, "FAMILIES_EXPANSION_PART5", ['f', 's', 'n', 'm', 'l', 'g', 'p']),
]

# We want each family to have a valid (c1, c2, v2) where c1 is in allowed_c1_list
cleaned_modules = {}

for fname, fam_list, var_name, allowed_c1 in domain_configs:
    new_fam_list = []
    for fam in fam_list:
        c1, c2, v2, dom, roles = fam[0].lower(), fam[1].lower(), fam[2].lower(), fam[3], fam[4]
        
        # Check if already baseline key
        is_baseline_key = (c1, c2, v2) in baseline_keys
        
        # Check if key is valid for this domain and unused
        key = (c1, c2, v2)
        if c1 in allowed_c1 and c2 in CONSONANTS and v2 in VOWELS and key not in used_keys:
            used_keys.add(key)
            new_fam_list.append((c1, c2, v2, dom, roles))
        elif is_baseline_key:
            # Baseline family slot: preserve!
            new_fam_list.append((c1, c2, v2, dom, roles))
        else:
            # Reassign to guaranteed free slot in allowed_c1
            new_c1, new_c2, new_v2 = allocate_slot_for_domain(allowed_c1)
            new_fam_list.append((new_c1, new_c2, new_v2, dom, roles))
            print(f"[{fname}] Reassigned ({c1}, {c2}, {v2}) -> ({new_c1}, {new_c2}, {new_v2}) [{dom}]")

    cleaned_modules[fname] = (var_name, new_fam_list)

print(f"\nTotal active families in use: {sum(len(f[1]) for f in cleaned_modules.values())}")
print(f"Total used keys: {len(used_keys)}")

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
    header = f'"""Lumina Semantic Families for {fname}.\nStrictly compliant C1-V1-C2-V2.\n"""\n\n{var_name} = [\n'
    body = "\n".join(serialize_family(fam) for fam in fam_list)
    footer = "\n]\n"
    fpath.write_text(header + body + footer, encoding="utf-8")
    print(f"Updated {fname} with {len(fam_list)} families.")

print("Canonical architecture enforcement completed!")
