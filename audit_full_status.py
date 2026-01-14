import os
import json

# Config
ASSETS_DIR = "assets"
METADATA_FILE = "metadata.json"

# Load Metadata
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Build map of existing files: { base_name_lower: full_path }
existing_files_map = {}
existing_files_list = []

print("Scanning files on disk...")
for root, dirs, files in os.walk(ASSETS_DIR):
    if "PORTADILLAS_ESTILOS" in root: continue
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            base = os.path.splitext(f)[0].lower()
            full_path = os.path.join(root, f)
            existing_files_map[base] = full_path
            existing_files_list.append(base)

print(f"Found {len(existing_files_list)} valid image files.")

# 1. Missing Metadata (Files on disk but not in JSON)
unindexed = []
for base in existing_files_list:
    if base not in data:
        unindexed.append(base)

# 2. Orphaned Metadata (Keys in JSON but not on disk)
orphans = []
for key in data:
    if key == "_INSTRUCCIONES": continue
    if key.lower() not in existing_files_map:
        orphans.append(key)

print(f"\nSTATUS REPORT:")
print(f"-------------")
print(f"Total Files: {len(existing_files_list)}")
print(f"Indexed: {len(existing_files_list) - len(unindexed)}")
print(f"Unindexed (New files?): {len(unindexed)}")
print(f"Orphaned Metadata (Deleted/Renamed?): {len(orphans)}")

if unindexed:
    print(f"\n[UNINDEXED FILES] (First 10):")
    for u in unindexed[:10]:
        print(f" - {u} (Path: {existing_files_map[u]})")

if orphans:
    print(f"\n[ORPHANED METADATA] (First 10):")
    for o in orphans[:10]:
        print(f" - {o}")
