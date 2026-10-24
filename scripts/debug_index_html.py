with open('index.html', encoding='utf-8') as f:
    text = f.read()
import re
scripts = re.findall(r'<script>(.*?)</script>', text, re.DOTALL)
s1 = scripts[1]

# Let's inspect where functions and initialization are
# Let's find all function names
functions = re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', s1)
print(f"Functions defined in Script 1 ({len(functions)}):", functions)

# Look for window.onload, DOMContentLoaded, or addEventListener
listeners = re.findall(r'(addEventListener\([^)]+\)|window\.[a-zA-Z0-9_$]+\s*=)', s1)
print(f"Event listeners / onload ({len(listeners)}):", listeners)

# Check all buttons in HTML and their onclick or id
buttons = re.findall(r'<button[^>]*>', text)
print(f"Total <button> elements in index.html: {len(buttons)}")
for b in buttons:
    print("  *", b)
