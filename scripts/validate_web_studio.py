import re, sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Check replacement character
if '\ufffd' in content:
    print("ERROR: Replacement character found in index.html!")
    sys.exit(1)
else:
    print("PASS: Zero replacement characters (100% clean UTF-8).")

# 2. Extract scripts
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', content)
print(f"Total script tags: {len(scripts)}")
js = scripts[-1] # Main app script

# 3. Check duplicate top-level let/const declarations (4-space indent)
top_lets = re.findall(r'^    (?:let|const|var)\s+([a-zA-Z0-9_$]+)', js, re.MULTILINE)
import collections
counts = collections.Counter(top_lets)
dups = {k: v for k, v in counts.items() if v > 1}
if dups:
    print("ERROR: Duplicate top-level declarations found:", dups)
    sys.exit(1)
else:
    print("PASS: Zero duplicate top-level let/const declarations.")
    print("Top-level variables declared:", list(counts.keys()))

# 4. Check all onclick functions are defined
onclicks = set(re.findall(r'onclick=["\']([a-zA-Z0-9_$]+)\(', content))
print("\nChecking onclick functions used in HTML:")
missing = []
for fn in sorted(onclicks):
    if f"function {fn}" in js or f"window.{fn}" in js:
        print(f"  [OK] {fn}")
    else:
        print(f"  [MISSING] {fn}")
        missing.append(fn)

if missing:
    print("ERROR: Missing functions:", missing)
    sys.exit(1)

print("\nALL VALIDATION CHECKS PASSED SUCCESSFULLY!")
