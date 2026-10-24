"""Analyze used keys and find available slots for clean remapping."""
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.baseline_data import BASELINE_DATA

CONSONANTS = ['t', 'd', 'k', 'g', 'p', 'b', 's', 'z', 'm', 'n', 'f', 'v', 'l', 'r', 'sh', 'zh', 'j', 'ch', 'h']
VOWELS = ['a', 'e', 'i', 'o', 'u']

# 1. Baseline root keys (MUST NOT CHANGE)
baseline_keys = set()
for r in BASELINE_DATA['roots']:
    w = r['word'].lower()
    # parse C1 V1 C2 V2
    import re
    m = re.match(r'^(sh|zh|ch|[a-z])([aeiou])(sh|zh|ch|[a-z])([aeiou])$', w)
    if m:
        c1, v1, c2, v2 = m.groups()
        baseline_keys.add((c1, c2, v2))

print(f"Baseline families reserved: {len(baseline_keys)}")

def get_free_keys_for_c1(c1, used_set):
    free = []
    for c2 in CONSONANTS:
        for v2 in VOWELS:
            key = (c1, c2, v2)
            if key not in used_set and key not in baseline_keys:
                free.append(key)
    return free

# Check how many keys are available for each C1
for c1 in CONSONANTS:
    free = get_free_keys_for_c1(c1, set())
    print(f"C1 '{c1}': {len(free)} free slots available out of {len(CONSONANTS)*len(VOWELS)} total")
