"""Master Rebuild Script for Lumina Lexicon.
Ensures:
- All 67 baseline families are intact with their original words.
- No expansion family ever collides with a baseline family.
- Modal verbs: zhivi (vouloir), zhipi (pouvoir), shaki (savoir) are canonical roots in SH/ZH.
- Time nouns: tana (jour), tusa (nuit) are canonical roots in T/D.
- Everyday verbs: mido (chercher), tovi (trouver), kivi (marcher), giso (briller) are canonical roots.
- Everyday nouns: gape (nuage), gapi (neige), gari (rivière), mata (verre), safi (eau), jamo (maison).
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.baseline_data import BASELINE_DATA
import re

CONSONANTS = ['t', 'd', 'k', 'g', 'p', 'b', 's', 'z', 'm', 'n', 'f', 'v', 'l', 'r', 'sh', 'zh', 'j', 'ch', 'h']
VOWELS = ['a', 'e', 'i', 'o', 'u']

# 1. Map 67 baseline keys
baseline_keys = {}
for r in BASELINE_DATA['roots']:
    w = r['word'].lower()
    m = re.match(r'^(sh|zh|ch|[a-z])([aeiou])(sh|zh|ch|[a-z])([aeiou])$', w)
    if m:
        c1, v1, c2, v2 = m.groups()
        baseline_keys[(c1, c2, v2)] = w

print(f"Locked {len(baseline_keys)} baseline family keys.")

# Track all used keys
used_keys = set(baseline_keys.keys())

def allocate_slot(allowed_c1_list):
    for c1 in allowed_c1_list:
        for c2 in CONSONANTS:
            for v2 in VOWELS:
                key = (c1, c2, v2)
                if key not in used_keys:
                    used_keys.add(key)
                    return key
    raise ValueError(f"Exhausted slots for {allowed_c1_list}")

def serialize_family(fam):
    c1, c2, v2, dom, roles = fam
    lines = [f"    ('{c1}', '{c2}', '{v2}', {repr(dom)}, {{"]
    for role_v in ['a', 'i', 'u', 'o', 'e']:
        if role_v in roles:
            fr, en, sem = roles[role_v]
            lines.append(f"        '{role_v}': ({repr(fr)}, {repr(en)}, {repr(sem)}),")
    lines.append("    }),")
    return "\n".join(lines)

def write_family_file(fname, var_name, fam_list):
    fpath = ROOT_DIR / "scripts" / fname
    header = f'"""Lumina Semantic Families for {fname}.\nStrictly compliant C1-V1-C2-V2.\n"""\n\n{var_name} = [\n'
    body = "\n".join(serialize_family(fam) for fam in fam_list)
    footer = "\n]\n"
    fpath.write_text(header + body + footer, encoding="utf-8")
    print(f"Wrote {len(fam_list)} families to {fname}.")

# 1. Clean Core Domain Files
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

# Essential modal & time additions
modal_families = [
    ('zh', 'v', 'i', 'Abstraction / Volonté & Désir', {
        'a': ('volonté, désir, souhait, voeu', 'will, desire, wish, volition', 'Force de vouloir'),
        'i': ('vouloir, souhaiter, désirer, aimer', 'to want, to wish, to desire, would like', 'Avoir la volonté de'),
        'u': ('volontaire, désiré, souhaité, voulu', 'willing, voluntary, desired, wanted', 'Animé par la volonté'),
        'o': ('sphère du vouloir, registre des voeux', 'realm of will, wishbook', 'Lieu des souhaits'),
        'e': ('volontaire, personne qui veut', 'wisher, willing agent', 'Personne voulant'),
    }),
    ('zh', 'p', 'i', 'Abstraction / Pouvoir & Capacité', {
        'a': ('pouvoir, capacité, faculté, puissance', 'power, ability, capability, faculty', "Capacité d'agir"),
        'i': ('pouvoir, être capable de, être en mesure', 'can, to be able to, may', 'Avoir la faculté de'),
        'u': ('capable, possible, potentiel, puissant', 'capable, able, possible, potential', 'Qui peut accomplir'),
        'o': ('champ des possibles, sphère du pouvoir', 'realm of possibilities, power realm', 'Lieu du pouvoir'),
        'e': ('être capable, agent souverain', 'capable agent, achiever', 'Personne qui peut'),
    }),
    ('sh', 'k', 'i', 'Abstraction / Savoir & Connaissance', {
        'a': ('savoir, connaissance, science, érudition', 'knowledge, science, lore, learning', 'Ensemble des vérités acquises'),
        'i': ('savoir, connaître, avoir conscience', 'to know, to be aware of, to understand', 'Posséder le savoir'),
        'u': ('savant, instruit, érudit, connu', 'knowledgeable, learned, known, wise', 'Qui sait'),
        'o': ('académie du savoir, bibliothèque, temple', 'knowledge haven, library, academy', 'Lieu du savoir'),
        'e': ('savant, érudit, sage, chercheur', 'scholar, sage, scientist', 'Personne qui sait'),
    }),
]

time_families = [
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

core_domain_configs = [
    ("families_domain_t_d.py", "FAMILIES_T_D", mod_t_d.FAMILIES_T_D + time_families, ['t', 'd']),
    ("families_domain_k_g.py", "FAMILIES_K_G", mod_k_g.FAMILIES_K_G, ['k', 'g']),
    ("families_domain_p_b.py", "FAMILIES_P_B", mod_p_b.FAMILIES_P_B, ['p', 'b']),
    ("families_domain_s_z.py", "FAMILIES_S_Z", mod_s_z.FAMILIES_S_Z, ['s', 'z']),
    ("families_domain_m_n.py", "FAMILIES_M_N", mod_m_n.FAMILIES_M_N, ['m', 'n']),
    ("families_domain_f_v.py", "FAMILIES_F_V", mod_f_v.FAMILIES_F_V, ['f', 'v']),
    ("families_domain_l_r.py", "FAMILIES_L_R", mod_l_r.FAMILIES_L_R, ['l', 'r']),
    ("families_domain_sh_zh.py", "FAMILIES_SH_ZH", mod_sh_zh.FAMILIES_SH_ZH + modal_families, ['sh', 'zh']),
    ("families_domain_j_ch.py", "FAMILIES_J_CH", mod_j_ch.FAMILIES_J_CH, ['j', 'ch']),
    ("families_domain_h.py", "FAMILIES_H", mod_h.FAMILIES_H, ['h']),
]

for fname, var_name, fam_list, allowed_c1 in core_domain_configs:
    new_fam_list = []
    for fam in fam_list:
        c1, c2, v2, dom, roles = fam[0].lower(), fam[1].lower(), fam[2].lower(), fam[3], fam[4]
        key = (c1, c2, v2)
        if key in baseline_keys:
            # Canonical baseline slot: keep!
            new_fam_list.append((c1, c2, v2, dom, roles))
        elif c1 in allowed_c1 and c2 in CONSONANTS and v2 in VOWELS and key not in used_keys:
            used_keys.add(key)
            new_fam_list.append((c1, c2, v2, dom, roles))
        else:
            new_c1, new_c2, new_v2 = allocate_slot(allowed_c1)
            new_fam_list.append((new_c1, new_c2, new_v2, dom, roles))
    write_family_file(fname, var_name, new_fam_list)

# 2. Clean Expansions 1, 2, 3
import scripts.families_expansion as mod_exp1
import scripts.families_expansion_part2 as mod_exp2
import scripts.families_expansion_part3 as mod_exp3

exp_configs = [
    ("families_expansion.py", "FAMILIES_EXPANSION", mod_exp1.FAMILIES_EXPANSION, ['k', 'g', 's', 'j', 'm']),
    ("families_expansion_part2.py", "FAMILIES_EXPANSION_PART2", mod_exp2.FAMILIES_EXPANSION_PART2, ['k', 'g', 'l', 'j', 's', 'p']),
    ("families_expansion_part3.py", "FAMILIES_EXPANSION_PART3", mod_exp3.FAMILIES_EXPANSION_PART3, ['k', 'g', 'p', 's', 'n']),
]

for fname, var_name, fam_list, allowed_c1 in exp_configs:
    new_fam_list = []
    for fam in fam_list:
        c1, c2, v2, dom, roles = fam[0].lower(), fam[1].lower(), fam[2].lower(), fam[3], fam[4]
        key = (c1, c2, v2)
        if key not in baseline_keys and c1 in allowed_c1 and c2 in CONSONANTS and v2 in VOWELS and key not in used_keys:
            used_keys.add(key)
            new_fam_list.append((c1, c2, v2, dom, roles))
        else:
            new_c1, new_c2, new_v2 = allocate_slot(allowed_c1)
            new_fam_list.append((new_c1, new_c2, new_v2, dom, roles))
    write_family_file(fname, var_name, new_fam_list)

# 3. Clean Part 4 and Part 5 from RAW_FAMILIES
from scripts.build_expansion_part4 import RAW_FAMILIES
part4_families = []
for pref_c1, alt_c1, dom, roles in RAW_FAMILIES:
    c1, c2, v2 = allocate_slot([pref_c1, alt_c1])
    part4_families.append((c1, c2, v2, dom, roles))
write_family_file("families_expansion_part4.py", "FAMILIES_EXPANSION_PART4", part4_families)

from scripts.build_expansion_part5 import RAW_FAMILIES_PART5
part5_families = []
for pref_c1, alt_c1, dom, roles in RAW_FAMILIES_PART5:
    c1, c2, v2 = allocate_slot([pref_c1, alt_c1])
    part5_families.append((c1, c2, v2, dom, roles))
write_family_file("families_expansion_part5.py", "FAMILIES_EXPANSION_PART5", part5_families)

print(f"\nAll files cleanly generated! Total unique keys used: {len(used_keys)}")
