import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import json
import shutil

# Config
ASSETS_DIR = "assets"
METADATA_FILE = "metadata.json"
BACKUP_FILE = "metadata.backup.json"

# 1. Load Metadata
print(f"Loading {METADATA_FILE}...")
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Backup first
shutil.copy(METADATA_FILE, BACKUP_FILE)
print(f"Backup created at {BACKUP_FILE}")

# 2. Scan files
print(f"Scanning {ASSETS_DIR}...")
existing_files_map = {}
for root, dirs, files in os.walk(ASSETS_DIR):
    if "PORTADILLAS_ESTILOS" in root: continue
    if "bg" in root: continue
    
    # Infer Category from folder name
    rel_path = os.path.relpath(root, ASSETS_DIR)
    print(f"DEBUG: Scanning root='{root}', rel_path='{rel_path}'")
    
    if rel_path == ".":
        # Skip root directory (General)
        continue
    else:
        # Use the top-level folder inside assets as category
        category = rel_path.split(os.sep)[0]
    
    # print(f"DEBUG: Files in {rel_path}: {files}") # Commented out to reduce noise/errors

    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            if "_POSTER" in f: 
                # print(f"DEBUG: Skipping poster {f}")
                continue 
            
            if "cover_book" in f.lower() and "SELLOS_MAGICOS" in category:
                print(f"DEBUG: Skipping cover_book in {category}")
                continue

            
            base = os.path.splitext(f)[0].lower()
            # Store tuple of (filename, category)
            existing_files_map[base] = (f, category)
            # print(f"DEBUG: Found {f} (Category: {category})")

# 3. Identifiy Unindexed
added_count = 0
for base, (filename, category) in existing_files_map.items():
    if base not in data:
        print(f"DEBUG: Adding new item {base}")
        # Generate readable title from basename
        raw_title = base.replace("_", " ").replace("-", " ")
        title = raw_title.title()
        
        if category == "General":
            src_path = f"assets/{filename}"
        else:
            # We must use forward slashes for web usage
            src_path = f"assets/{category}/{filename}"

        data[base] = {
            "id": base,
            "title": title,
            "category": category,
            "src": src_path,
            "description": "Nueva obra añadida recientemente.",
            "price": "19,99",
            "size": "Consultar"
        }
        added_count += 1
        print(f"Auto-adding: {base} -> '{title}'")
    else:
        # Check if we need to update provided info (e.g. category was missing)
        current_data = data[base]
        
        # If category is missing or different, or src is wrong, update it.
        # But be careful not to overwrite custom titles?
        # Let's focused on patching Category and Src if they look default/wrong.
        
        needs_update = False
        
        if "category" not in current_data or current_data["category"] != category:
            print(f"DEBUG: Updating category for {base}: {current_data.get('category')} -> {category}")
            current_data["category"] = category
            needs_update = True
            
        if "id" not in current_data:
             current_data["id"] = base
             needs_update = True
             
        # Optional: Update src if it doesn't match new standard?
        # If src is missing, definitely add it.
        if "src" not in current_data:
            current_data["src"] = src_path
            needs_update = True
            
        if needs_update:
            data[base] = current_data
            added_count += 1 # Count as change
            print(f"Updated metadata for: {base}")
        else:
            if "00edusse" in base or "caballo" in base:
                print(f"DEBUG: Skipping {base}, up to date.")

# 4. Save
if added_count > 0:
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\nSUCCESS: Added {added_count} new entries to metadata.json")
else:
    print("\nNo new unindexed files found.")
