import json
import sys

METADATA_FILE = "metadata.json"

def cleanup():
    print(f"Loading {METADATA_FILE}...")
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("metadata.json not found.")
        return

    keys_to_remove = []
    
    print("Scanning for items to remove...")
    for key, item in data.items():
        if not isinstance(item, dict):
            continue
            
        category = item.get("category", "")
        
        # 1. Remove "General" category
        if category == "General":
            print(f"Marking for removal (General): {key}")
            keys_to_remove.append(key)
            continue
            
        # 2. Remove "bg" category
        if category == "bg":
            print(f"Marking for removal (bg): {key}")
            keys_to_remove.append(key)
            continue
            
        # 3. Remove "cover_book" from "SELLOS_MAGICOS"
        # We check by ID "cover_book" or filename if it ended up with a different ID
        if "cover_book" in key and "SELLOS_MAGICOS" in item.get("src", ""):
             print(f"Marking for removal (cover_book): {key}")
             keys_to_remove.append(key)
             continue
             
    if not keys_to_remove:
        print("Nothing to remove.")
        return

    print(f"Removing {len(keys_to_remove)} items...")
    for key in keys_to_remove:
        del data[key]
        
    print(f"Saving updated {METADATA_FILE}...")
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print("Cleanup complete.")

if __name__ == "__main__":
    cleanup()
