import os
import json
import csv
import re

# Load existing metadata to preserve manual titles
metadata = {}
if os.path.exists("metadata.json"):
    with open("metadata.json", "r", encoding="utf-8") as f:
        try:
            metadata = json.load(f)
        except:
            pass

def clean_title(filename):
    # Remove extension
    name = os.path.splitext(filename)[0]
    
    # Remove common prefixes like "1_-_", "01_", "12_-_12", dates
    # Regex for "Digits_-_" or "Digits_"
    name = re.sub(r'^\d+[_-]+', '', name)
    # Regex for repeated digits at start "10HOLLYWOOD" -> "HOLLYWOOD" if following _-_
    name = re.sub(r'^\d+(?=[A-Za-z])', '', name) 
    
    # Replace underscores and dashes with spaces
    name = name.replace("_", " ").replace("-", " ")
    
    # Remove specific junk words if needed or user mentions
    name = re.sub(r'\b(PLUS|stilo|NEOINK|APLICC)\b', '', name, flags=re.IGNORECASE)
    
    # Clean whitespace
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Title Case
    return name.title()

assets_dir = "assets"
preview_rows = []

# Exclude these folders from "Artwork" renaming logic
EXCLUDED_DIRS = ["js", "css", "bg", "icons", "PORTADILLAS_ESTILOS", "_SUBIR_ESTO"]

print("Generating Preview...")

for root, dirs, files in os.walk(assets_dir):
    # Filter dirs
    dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
    
    folder_name = os.path.basename(root)
    if root == assets_dir: continue # Skip root assets folder files for now or handle separately
    
    # Sort files to maintain some order (optional)
    files.sort()
    
    counter = 1
    for filename in files:
        if not filename.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            continue
            
        old_path = os.path.join(root, filename)
        basename = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1].lower()
        
        # New Name Construction
        # clean_folder = folder_name.lower().replace(" ", "_")
        # Let's use a simpler prefix if folder name is like "01EXP_NEOCIRC" -> "01exp_neocirc"
        clean_folder = re.sub(r'^\d+', '', folder_name).lower().strip("_") # remove leading numbers for file prefix? 
        # Actually user example: "carpeta_001.jpg". 
        # Let's keep the folder prefix to allow flat listing context
        safe_folder = re.sub(r'[^a-zA-Z0-9]', '_', folder_name).lower()
        new_filename = f"{safe_folder}_{counter:03d}{ext}"
        
        # Title Logic
        current_title = ""
        source = "Extraction"
        
        # 1. Existing Metadata
        if basename in metadata and "title" in metadata[basename]:
            current_title = metadata[basename]["title"]
            source = "Metadata"
        else:
            # 2. Extract
            current_title = clean_title(filename)
            if not current_title or current_title.isdigit():
                current_title = "SIN TITULO"
                source = "MISSING"
        
        preview_rows.append({
            "Folder": folder_name,
            "OldFilename": filename,
            "NewFilename": new_filename,
            "ProposedTitle": current_title,
            "Source": source
        })
        counter += 1

# Save Preview
with open("RENAME_PREVIEW.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Folder", "OldFilename", "NewFilename", "ProposedTitle", "Source"])
    writer.writeheader()
    writer.writerows(preview_rows)

print(f"Preview generated with {len(preview_rows)} entries.")
