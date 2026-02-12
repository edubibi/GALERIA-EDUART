import json
import os

# Configuration
TARGET_FILE = "dossier_portfolio.html"
METADATA_FILE = "metadata.json"

SELECTION = [
    "00edusse_003",       # El Guardián
    "01exp_neocirc_017",  # Catedral
    "02cubesse_stilo_001",# Colibrí
    "08boracarbon_001",   # Abuelo
    "08boracarbon_004",   # Señora
    "23tridim_burst_004", # Nueva
    "03expneoplus_038",   # Nueva
    "09fracneo_001",      # Nueva
    "17fuzztess_001",     # Nueva
    "aldea china"         # Nueva
]

ITEM_TEMPLATE = """    <!-- {index}. {short_title} -->
    <div class="page artwork-page">
        <div class="artwork-image-container">
            <img src="{image_path}" class="artwork-image" alt="{title}">
        </div>
        <div class="artwork-info">
            <h3 class="artwork-title">{title}</h3>
            <div class="artwork-meta">Colección: {collection} | Digital Art</div>
            <p class="artwork-desc">
                {description}
            </p>
        </div>
        <footer>{index} / 10</footer>
    </div>
"""

def find_artwork_in_metadata(metadata, key_part):
    if key_part in metadata:
        return metadata[key_part]
    for filename, data in metadata.items():
        if key_part.lower() in filename.lower():
            if key_part == "aldea china" and "aldea china" not in filename.lower():
                continue
            return data
    return None

def normalize_path(path):
    return path.replace("\\", "/")

def get_image_path(key_part):
     # Helper to find file path on disk
    filename = key_part + ".png" # Assume png default, but check loosely
    
    image_path = ""
    for root, dirs, files in os.walk("assets"):
        for file in files:
            if file.lower() == filename.lower() or key_part.lower() in file.lower():
                # Avoid false positives for short keys, but our keys are specific enough usually
                # For "aldea china", it matches "aldea china.png"
                image_path = os.path.join(root, file)
                break
        if image_path: break
    
    if image_path:
        return normalize_path(image_path)
    return "assets/placeholder.png"

def update_dossier():
    print(f"Reading {TARGET_FILE}...")
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content to preserve header and maybe footer if it exists outside the loop?
    # actually dossier_portfolio.html ends with the items.
    # We look for <!-- OBRAS --> marker
    
    start_marker = "<!-- OBRAS -->"
    end_marker = "</body>"
    
    if start_marker not in content:
        print("Error: Could not find start marker <!-- OBRAS -->")
        return

    pre_content = content.split(start_marker)[0] + start_marker + "\n"
    
    # Generate new content
    print(f"Loading metadata from {METADATA_FILE}...")
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    new_items_html = ""
    
    for i, item_key in enumerate(SELECTION, 1):
        data = find_artwork_in_metadata(metadata, item_key)
        if not data:
            print(f"Warning: No metadata for {item_key}")
            data = {"title": "Sin Título", "description": "Descripción no disponible."}
        
        title = data.get('title', 'Sin Título')
        description = data.get('description', 'Descripción no disponible.')
        if not description: description = "Una obra maestra del Universo EDUSSE."
        
        image_path = get_image_path(item_key)
        collection = image_path.split('/')[1] if '/' in image_path else "Unknown"
        short_title = title.split(' ')[0]

        item_html = ITEM_TEMPLATE.format(
            index=i,
            short_title=short_title,
            image_path=image_path,
            title=title,
            collection=collection,
            description=description
        )
        new_items_html += item_html + "\n"

    # Assemble
    final_content = pre_content + new_items_html + "\n" + end_marker + "\n\n</html>"
    
    print(f"Writing updated content to {TARGET_FILE}...")
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("Done.")

if __name__ == "__main__":
    update_dossier()
