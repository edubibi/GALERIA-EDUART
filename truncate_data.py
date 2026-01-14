
path = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\js\data.js"

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# We want 0-indexed loops, line 2599 in 1-index is index 2598.
# Line 2599 is "},"
# So we want first 2599 lines (indices 0 to 2598).
cutoff_index = 2599 

new_lines = lines[:cutoff_index]
new_lines.append("\n];")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Truncated data.js at line {cutoff_index}. New line count: {len(new_lines)}")
