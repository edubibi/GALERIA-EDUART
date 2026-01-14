import os
import json
import shutil

# Config
ASSETS_DIR = "assets"
METADATA_FILE = "metadata.json"
BACKUP_FILE = "metadata.backup.json"

# 1. Load Metadata
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Backup first
shutil.copy(METADATA_FILE, BACKUP_FILE)
print(f"Backup created at {BACKUP_FILE}")

# 2. Scan files
existing_files_map = {}
for root, dirs, files in os.walk(ASSETS_DIR):
    if "PORTADILLAS_ESTILOS" in root: continue
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            base = os.path.splitext(f)[0].lower()
            existing_files_map[base] = f # Store original filename case if needed, or just existence

# 3. Identifiy Unindexed
added_count = 0
for base in existing_files_map:
    if base not in data:
        # Generate readable title from basename
        # e.g. "my_new_photo_01" -> "My New Photo 01"
        raw_title = base.replace("_", " ").replace("-", " ")
        # Heuristic: Remove common prefixes if they exist (optional, but requested by user before)
        # For now, just Capitalize First Letters
        title = raw_title.title()
        
        data[base] = {
            "title": title,
            "description": "Nueva obra añadida recientemente.",
            "price": "19,99",
            "size": "Consultar"
        }
        added_count += 1
        print(f"Auto-adding: {base} -> '{title}'")

# 4. Save
if added_count > 0:
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\nSUCCESS: Added {added_count} new entries to metadata.json")
else:
    print("\nNo unindexed files found. Metadata is up to date.")
