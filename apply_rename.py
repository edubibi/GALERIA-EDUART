
import os
import csv
import json
import shutil

# Configuration
PREVIEW_FILE = "RENAME_PREVIEW.csv"
METADATA_FILE = "metadata.json"
ASSETS_DIR = "assets"

def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_metadata(data):
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def apply_rename():
    print("Starting renaming process...")
    
    if not os.path.exists(PREVIEW_FILE):
        print(f"Error: {PREVIEW_FILE} not found.")
        return

    # Load existing metadata
    old_metadata = load_metadata()
    new_metadata = {"_INSTRUCCIONES": old_metadata.get("_INSTRUCCIONES", "")}
    
    # Read CSV
    rows = []
    with open(PREVIEW_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    files_renamed = 0
    errors = 0

    for row in rows:
        folder = row["Folder"]
        old_name = row["OldFilename"]
        new_name = row["NewFilename"]
        title = row["ProposedTitle"]
        
        old_path = os.path.join(ASSETS_DIR, folder, old_name)
        new_path = os.path.join(ASSETS_DIR, folder, new_name)
        
        # 1. Rename File
        try:
            if os.path.exists(old_path):
                # Handle case where new name exists (very unlikely with our naming scheme unless re-run)
                if os.path.exists(new_path) and old_name != new_name:
                    print(f"Warning: Destination {new_name} already exists. Skipping file rename.")
                else:
                    os.rename(old_path, new_path)
                    files_renamed += 1
            else:
                # File might have been renamed already or missing
                if not os.path.exists(new_path):
                    print(f"Error: Source file {old_path} not found.")
                    errors += 1
                    continue
        except Exception as e:
            print(f"Exception renaming {old_name}: {e}")
            errors += 1
            continue

        # 2. Update Metadata
        # Old key is filename without extension
        old_key = os.path.splitext(old_name)[0]
        new_key = os.path.splitext(new_name)[0]
        
        # Get existing data for this artwork if any
        artwork_data = old_metadata.get(old_key, {})
        
        # Update/Set Title
        artwork_data["title"] = title
        
        # Note: We are preserving other fields like price, description, etc.
        new_metadata[new_key] = artwork_data

    # Save new metadata
    save_metadata(new_metadata)
    
    print(f"Process complete.")
    print(f"Files renamed: {files_renamed}")
    print(f"Metadata entries updated: {len(new_metadata)}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    apply_rename()
