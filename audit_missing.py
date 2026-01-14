import os
import json
import glob

# Config
ASSETS_DIR = "assets"
METADATA_FILE = "metadata.json"

# Load Metadata
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Build map of existing files: { base_name_lower: full_path }
existing_files = {}
print("Scanning files...")
for root, dirs, files in os.walk(ASSETS_DIR):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            base = os.path.splitext(f)[0].lower()
            existing_files[base] = os.path.join(root, f)

print(f"Found {len(existing_files)} files on disk.")

# Check Metadata keys against files
missing = []
found_count = 0

print("\nChecking metadata keys...")
for key in data:
    if key == "_INSTRUCCIONES": continue
    
    # Logic: Metadata Key usually equals BaseName (e.g. "02cubesse_stilo_001")
    # But sometimes the user might have keys that don't match filenames exactly? 
    # Let's assume strict BaseName match for now as per previous logic.
    
    if key.lower() in existing_files:
        found_count += 1
    else:
        # Key is missing on disk
        # Try to guess folder from key name (e.g. "02cubesse_stilo_..." -> "02CUBESSE stilo")
        missing_entry = {
            "key": key,
            "title": data[key].get("title", "No Title"),
            "expected_match": key
        }
        missing.append(missing_entry)

print(f"Matched: {found_count}")
print(f"Missing (in metadata but not on disk): {len(missing)}")

print("\n--- POSSIBLY MOVED/RENAMED FILES (Top 20) ---")
for m in missing:
    # Filter for 02CUBESSE as users specific interest
    if "cubesse" in m["key"]:
        print(f"MISSING: {m['key']} | Title: {m['title']}")
