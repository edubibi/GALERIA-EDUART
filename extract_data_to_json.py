import json
import os
import re

DATA_JS_PATH = os.path.join("js", "data.js")
METADATA_JSON_PATH = "metadata.json"

def extract_data():
    if not os.path.exists(DATA_JS_PATH):
        print(f"Error: {DATA_JS_PATH} not found.")
        return

    print(f"Reading {DATA_JS_PATH}...")
    with open(DATA_JS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract the array content similar to how we did in generate_full_catalog
    start_marker = "const artworkData = ["
    start = content.find(start_marker)
    if start == -1:
        print("Error: Could not find artworkData array.")
        return

    # Extract everything after the marker
    array_content = content[start + len("const artworkData ="):]
    array_content = array_content.strip()
    if array_content.endswith(";"):
        array_content = array_content[:-1]

    # Quick fix for JS object to JSON conversion (quoting keys)
    # This regex looks for word characters followed by a colon and wraps them in quotes
    # It avoids already quoted keys
    # limitation: might break if keys are unusual, but 'id', 'title' etc are simple.
    fixed_json = re.sub(r'([{,]\s*)(\w+):', r'\1"\2":', array_content)
    
    # Remove trailing commas
    fixed_json = re.sub(r',\s*]', ']', fixed_json)
    fixed_json = re.sub(r',\s*}', '}', fixed_json)

    try:
        data = json.loads(fixed_json)
        print(f"Successfully parsed {len(data)} items from JS.")
    except Exception as e:
        print(f"Error parsing JS data to JSON: {e}")
        # Debug: write to file
        with open("debug_extracted.json", "w", encoding="utf-8") as f:
            f.write(fixed_json)
        return

    # Load existing metadata to preserve any extra fields if they exist?
    # Actually, the goal is to make metadata.json the source of truth based on current web data.
    # But we should preserve structure if metadata.json has non-artwork keys (like _INSTRUCCIONES)
    
    current_metadata = {}
    if os.path.exists(METADATA_JSON_PATH):
        try:
            with open(METADATA_JSON_PATH, "r", encoding="utf-8") as f:
                current_metadata = json.load(f)
        except:
            pass
    
    # We want to format metadata.json as a dict keyed by ID for easier editing
    # or keep it as a list? The user's current metadata.json is keyed by ID.
    # Let's maintain that structure: { "id1": { "title": ... }, "id2": ... }
    
    new_metadata = {}
    if "_INSTRUCCIONES" in current_metadata:
        new_metadata["_INSTRUCCIONES"] = current_metadata["_INSTRUCCIONES"]
    else:
        new_metadata["_INSTRUCCIONES"] = "Base de datos maestra. Edita aquí y ejecuta build_data.py."

    for item in data:
        item_id = item.get("id")
        if not item_id: continue
        
        # We store the whole object
        new_metadata[item_id] = item

    print(f"Writing {len(new_metadata)} items to {METADATA_JSON_PATH}...")
    with open(METADATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(new_metadata, f, indent=4, ensure_ascii=False)
    
    print("Done.")

if __name__ == "__main__":
    extract_data()
