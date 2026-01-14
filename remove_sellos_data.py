
import os
import json

path = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\js\data.js"

# Read file
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the text "const artworkData = " and the trailing ";"
json_str = content.replace("const artworkData = ", "").strip()
if json_str.endswith(";"):
    json_str = json_str[:-1]

try:
    data = json.loads(json_str)
    # Filter out SELLOS_MAGICOS
    new_data = [item for item in data if item.get('category') != "SELLOS_MAGICOS"]
    
    # Write back
    json_out = json.dumps(new_data, indent=4, ensure_ascii=False)
    final_content = "const artworkData = " + json_out + ";"
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Removed SELLOS_MAGICOS. Count: {len(data)} -> {len(new_data)}")
except Exception as e:
    print(f"Error parsing JSON: {e}")
