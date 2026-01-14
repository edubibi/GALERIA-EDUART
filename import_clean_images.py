
import os
import shutil

# Mapping ID -> Title Keywords to search for
# keys correspond to the 1-10 numbering
# Keywords are what we expect the user might name their clean files
mapping = {
    1: ["pamplona"],
    2: ["huesca"],
    3: ["zaragoza"],
    4: ["girona"],
    5: ["lleida"],
    6: ["anfiteatro", "tarragona"], 
    7: ["castellon", "castellón"],
    8: ["valencia"],
    9: ["caceres", "cáceres"],
    10: ["sevilla"]
}

folder = r"C:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\24BORACARBON MONUMENTOS"
prefix = "boracarbon_mon"

print(f"Scanning {folder} for clean images...")

files = os.listdir(folder)
files_lower = {f.lower(): f for f in files}

count = 0

for i, keywords in mapping.items():
    target_base = f"{prefix}_{i:03d}"
    
    # Check if we find a file matching the keyword (and not already the target name)
    found_file = None
    
    # Naive search: check if any file in the folder contains the main keyword
    # We prefer exact matches or unambiguous ones.
    # Let's iterate all files and check if *any* search keyword is in the filename
    # AND the filename doesn't start with the prefix (to avoid re-renaming processed ones if run twice)
    
    candidate = None
    for f in files:
        if f.startswith(prefix):
            continue
            
        f_lower = f.lower()
        # specific logic: if 'anfiteatro' or 'tarragona' in name
        match = False
        for k in keywords:
            if k in f_lower:
                match = True
                break
        
        if match:
            candidate = f
            break
            
    if candidate:
        ext = os.path.splitext(candidate)[1]
        new_name = f"{target_base}{ext}"
        
        src = os.path.join(folder, candidate)
        dst = os.path.join(folder, new_name)
        
        # Check for existing watermarked file to remove/overwrite
        # Existing matches: `boracarbon_mon_00X.*`
        # We need to find them to delete them if the extension is different
        # If extension is same, os.rename/shutil.move might fail or overwrite depending on OS. Windows replace?
        # Safe bet: find any existing file with that base name and delete it?
        # Or just let rename fail and handle it?
        
        # Let's clean up ANY existing file with that ID to prepare for the new one
        for existing in files:
            if existing.startswith(target_base) and existing != new_name:
                print(f"   Removing old version {existing}...")
                os.remove(os.path.join(folder, existing))
                
        if os.path.exists(dst):
             print(f"   Overwriting {dst}...")
             os.remove(dst)
             
        print(f"[MATCH] Found '{candidate}' -> Renaming to '{new_name}'")
        os.rename(src, dst)
        count += 1
    else:
        # Optional: Checking if the target already exists (maybe satisfied)
        # print(f"Waiting for image for {keywords[0]}...")
        pass

if count == 0:
    print("\nNo matching clean files found yet.")
    print("Please ensure your clean files contain the city name (e.g. 'Pamplona.jpg') and are in the folder.")
else:
    print(f"\nSuccessfully swapped {count} images.")
    print("Old watermarked versions have been replaced.")
