
import os
import json

path = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\js\data.js"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Strip JS assignment
json_content = content.replace("const categoryCovers = ", "").split("const artworkData = ")[1].replace(";", "").strip()

# Clean garbage if any exists after the last bracket (handled by split but ensuring)
# Actually the file has TWO objects. "const categoryCovers = {...}" and "const artworkData = [...]"
# My previous truncation might have messed up if I didn't account for both.
# Let's just extract the artworkData part.

try:
    start_idx = content.find("const artworkData =")
    if start_idx == -1:
         raise Exception("Could not find artworkData start")
    
    # Simple extraction: from [ to the last ]
    list_start = content.find("[", start_idx)
    list_end = content.rfind("]")
    
    json_str = content[list_start : list_end+1]
    
    # Try parse
    data = json.loads(json_str) 
    print(f"VALID JSON. Items: {len(data)}")
    
except Exception as e:
    print(f"INVALID JSON: {e}")
    # Print the end of the string to see what's wrong
    if 'json_str' in locals():
        print(f"Tail: {json_str[-50:]}")

