"""Diagnose and clean all family definitions.
Checks:
1. c1 in valid consonants
2. c2 in valid consonants
3. v2 in valid vowels ('a', 'e', 'i', 'o', 'u')
4. No duplicate (c1, c2, v2)
"""

import sys
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

CONSONANTS = {'t', 'd', 'k', 'g', 'p', 'b', 's', 'z', 'm', 'n', 'f', 'v', 'l', 'r', 'sh', 'zh', 'j', 'ch', 'h'}
VOWELS = {'a', 'e', 'i', 'o', 'u'}

all_family_groups = [
    ('families_domain_t_d.py', FAMILIES_T_D),
    ('families_domain_k_g.py', FAMILIES_K_G),
    ('families_domain_p_b.py', FAMILIES_P_B),
    ('families_domain_s_z.py', FAMILIES_S_Z),
    ('families_domain_m_n.py', FAMILIES_M_N),
    ('families_domain_f_v.py', FAMILIES_F_V),
    ('families_domain_l_r.py', FAMILIES_L_R),
    ('families_domain_sh_zh.py', FAMILIES_SH_ZH),
    ('families_domain_j_ch.py', FAMILIES_J_CH),
    ('families_domain_h.py', FAMILIES_H),
    ('families_expansion.py', FAMILIES_EXPANSION),
    ('families_expansion_part2.py', FAMILIES_EXPANSION_PART2),
    ('families_expansion_part3.py', FAMILIES_EXPANSION_PART3),
]

seen_keys = {}
issues = []

for file_name, fam_list in all_family_groups:
    for idx, fam in enumerate(fam_list):
        c1 = fam[0].lower()
        c2 = fam[1].lower()
        v2 = fam[2].lower()
        dom = fam[3]
        
        # Check c1
        if c1 not in CONSONANTS:
            issues.append(f"[{file_name} #{idx}] Invalid c1: '{c1}' in {dom}")
        # Check c2
        if c2 not in CONSONANTS:
            issues.append(f"[{file_name} #{idx}] Invalid c2: '{c2}' in {dom}")
        # Check v2
        if v2 not in VOWELS:
            issues.append(f"[{file_name} #{idx}] Invalid v2: '{v2}' in {dom} (c1={c1}, c2={c2})")
            
        key = (c1, c2, v2)
        if key in seen_keys:
            prev_file, prev_idx, prev_dom = seen_keys[key]
            issues.append(f"Duplicate key {key}: [{prev_file} #{prev_idx} ({prev_dom})] vs [{file_name} #{idx} ({dom})]")
        else:
            seen_keys[key] = (file_name, idx, dom)

print(f"Total families inspected: {sum(len(f) for _, f in all_family_groups)}")
print(f"Total issues found: {len(issues)}")
for iss in issues:
    print("  *", iss)
