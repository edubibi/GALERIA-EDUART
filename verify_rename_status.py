
import os
import csv

ASSETS_DIR = "assets"
PREVIEW_FILE = "RENAME_PREVIEW.csv"

def verify():
    if not os.path.exists(PREVIEW_FILE):
        print("No preview file found.")
        return

    with open(PREVIEW_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    missing = []
    
    for row in rows:
        folder = row["Folder"]
        new_name = row["NewFilename"]
        old_name = row["OldFilename"]
        
        path = os.path.join(ASSETS_DIR, folder, new_name)
        
        if not os.path.exists(path):
            missing.append(f"{folder}/{old_name} -> {new_name}")

    if missing:
        print(f"Found {len(missing)} missing files (failed renames):")
        for m in missing:
            print(m)
    else:
        print("All files present. No missing renames detected.")

if __name__ == "__main__":
    verify()
