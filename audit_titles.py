import os
import json
import csv

# Load metadata
metadata = {}
if os.path.exists("metadata.json"):
    with open("metadata.json", "r", encoding="utf-8") as f:
        try:
            metadata = json.load(f)
        except:
            print("Error loading metadata.json")

# Walker
missing_files = []
assets_dir = "assets"

print("Scanning assets...")

for root, dirs, files in os.walk(assets_dir):
    for filename in files:
        if filename.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            basename = os.path.splitext(filename)[0]
            rel_path = os.path.relpath(os.path.join(root, filename), assets_dir)
            folder = os.path.dirname(rel_path)
            
            # Check metadata
            title = ""
            status = "MISSING_REC"
            
            # 1. Direct ID match
            if basename in metadata:
                entry = metadata[basename]
                if "title" in entry and entry["title"]:
                    title = entry["title"]
                    status = "OK"
                else:
                    status = "NO_TITLE_FIELD"
            
            # Simple heuristic for numeric titles 
            if status == "OK":
                if title.replace(" ", "").isdigit():
                    status = "NUMERIC_TITLE"
            
            # Add to list if not OK
            if status != "OK":
                missing_files.append({
                    "Folder": folder,
                    "Filename": filename,
                    "CurrentTitle": title,
                    "Status": status
                })

# Write Report
output_file = "MISSING_TITLES.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Folder", "Filename", "Status", "CurrentTitle"])
    writer.writeheader()
    for row in missing_files:
        writer.writerow(row)

print(f"Audit complete. Found {len(missing_files)} files needing attention.")
print(f"Report saved to {output_file}")
