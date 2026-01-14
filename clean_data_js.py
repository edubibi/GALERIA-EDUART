
import os

path = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\js\data.js"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the last occurrence of ];
# We expect the file to end with ];
# If there is junk after, we want to cut it.

end_marker = "];"
last_idx = content.rfind(end_marker)

if last_idx != -1:
    # Keep content up to ];
    new_content = content[:last_idx + len(end_marker)]
    
    # Write back
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Truncated data.js at index {last_idx + len(end_marker)}. Removed {len(content) - (last_idx + len(end_marker))} bytes.")
else:
    print("Could not find ending '];' in data.js")
