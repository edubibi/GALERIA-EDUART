import os
import json
import sys

# Force UTF-8 for stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

METADATA_FILE = "metadata.json"
ASSETS_DIR = "assets"

def list_new_photos():
    if not os.path.exists(METADATA_FILE):
        print("Metadata file not found.")
        return

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    indexed_ids = set(data.keys())
    new_files = []

    for root, dirs, files in os.walk(ASSETS_DIR):
        if "PORTADILLAS_ESTILOS" in root: continue
        if "bg" in root: continue
        
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                if "_POSTER" in f: continue
                
                base = os.path.splitext(f)[0]
                if base not in indexed_ids:
                    rel_path = os.path.relpath(os.path.join(root, f), ASSETS_DIR)
                    new_files.append(rel_path)

    print(f"Found {len(new_files)} new files:")
    for nf in new_files:
        print(f"- {nf}")

if __name__ == "__main__":
    list_new_photos()
