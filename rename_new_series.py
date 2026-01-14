import os

folder = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\24BORACARBON MONUMENTOS"
prefix = "boracarbon_mon"

files = [f for f in os.listdir(folder) if f.endswith('.png') or f.endswith('.jpg')]
files.sort() # Sort by name (timestamp essentially)

for i, filename in enumerate(files):
    ext = os.path.splitext(filename)[1]
    new_name = f"{prefix}_{i+1:03d}{ext}"
    src = os.path.join(folder, filename)
    dst = os.path.join(folder, new_name)
    
    print(f"Renaming {filename} -> {new_name}")
    os.rename(src, dst)
