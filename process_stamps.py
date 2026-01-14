
import os
import json
import re

directory = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\SELLOS_MAGICOS"
output_json_path = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\stamps_metadata_snippet.json"

# exclude cover_book.png
files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg')) and "cover_book" not in f]
files.sort()

metadata = {}
current_index = 1

print(f"Found {len(files)} stamp files.")

for filename in files:
    # Generate new ID
    new_id = f"sello_magico_{current_index:03d}"
    extension = os.path.splitext(filename)[1]
    new_filename = f"{new_id}{extension}"
    
    # Generate Title from old filename
    # Remove extension
    title_raw = os.path.splitext(filename)[0]
    # Replace capitalization (capitalize first letter of each word)
    title = title_raw.lower().title()
    
    # Construct paths
    old_path = os.path.join(directory, filename)
    new_path = os.path.join(directory, new_filename)
    
    # Rename file
    try:
        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")
    except Exception as e:
        print(f"Error renaming {filename}: {e}")
        continue
        
    # Add to metadata dict structure (using the format compatible with metadata.json)
    metadata[new_id] = {
        "title": title
    }
    
    current_index += 1

# Save metadata snippet to file so I can read it
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)

print(f"Metadata snippet saved to {output_json_path}")
