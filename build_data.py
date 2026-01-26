import json
import os

METADATA_FILE = "metadata.json"
DATA_JS_FILE = os.path.join("js", "data.js")

def build_data():
    if not os.path.exists(METADATA_FILE):
        print(f"Error: {METADATA_FILE} not found.")
        return

    print(f"Reading {METADATA_FILE}...")
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata_map = json.load(f)

    # Convert map back to list
    artwork_list = []
    
    # We simply iterate over the values that are dicts and have an 'id'
    # We ignore keys like '_INSTRUCCIONES'
    for key, item in metadata_map.items():
        if isinstance(item, dict) and "id" in item:
            artwork_list.append(item)
            
    # Sort by ID or Category? original data.js was roughly sorted.
    # Let's sort by Category then ID
    artwork_list.sort(key=lambda x: (x.get("category", ""), x.get("id", "")))

    print(f"Loaded {len(artwork_list)} artworks.")

    # We need to preserve the header (categoryCovers map) from the original data.js 
    # OR we should store that in metadata.json too?
    # For now, let's just hardcode the header or read it from the existing file if possible.
    # To be safe and self-contained, let's use a standard header. 
    # But wait, categoryCovers is important for the UI.
    
    # Strategy: Read existing data.js to get the header part (up to artworkData)
    # If not exists, use default.
    header = ""
    if os.path.exists(DATA_JS_FILE):
        with open(DATA_JS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            parts = content.split("const artworkData =")
            if len(parts) > 0:
                header = parts[0]
    
    if not header:
        print("Warning: Could not extract header from existing data.js. Using minimal default.")
        header = "const categoryCovers = {};\n\n"

    # Serialize list to JSON format
    json_str = json.dumps(artwork_list, indent=4, ensure_ascii=False)
    
    # Construct new file content
    # JS needs to assign it to variable.
    new_content = header + "const artworkData = " + json_str + ";"
    
    print(f"Writing to {DATA_JS_FILE}...")
    with open(DATA_JS_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("Build complete.")

if __name__ == "__main__":
    build_data()
