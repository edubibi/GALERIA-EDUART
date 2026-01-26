import re

with open('js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

cats = set(re.findall(r'category:\s*"([^"]+)"', content))
print("Categories found:")
for c in sorted(cats):
    print(f"- {c}")
