import json
import os

# Configuration
OUTPUT_FILE = "behance_generator.html"
METADATA_FILE = "metadata.json"

# The selection of artworks (Partial filenames or IDs to match)
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

HTML_TEMPLATE_START = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Portfolio Behance - Eduardo Ramírez</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400&display=swap');

        :root {
            --bg-color: #111;
            --text-color: #e0e0e0;
            --accent: #D4AF37;
            --width: 1400px;
        }

        body {
            background-color: #000;
            margin: 0;
            padding: 0;
            font-family: 'Lato', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .slide {
            width: var(--width);
            min-height: 1000px; /* Base height, can grow */
            background-color: var(--bg-color);
            color: var(--text-color);
            position: relative;
            display: flex;
            flex-direction: column;
            margin-bottom: 0px; /* Behance stitches images, but for preview we might want gap. 0 for continuity */
            padding-bottom: 80px;
            box-sizing: border-box;
            border-bottom: 1px solid #222;
        }

        .cover {
            height: 1200px;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(to bottom, #0a0a0a, #1a1a1a);
        }

        .cover h1 {
            font-family: 'Playfair Display', serif;
            font-size: 5rem;
            color: var(--accent);
            margin: 0;
            letter-spacing: -2px;
        }

        .cover h2 {
            font-family: 'Lato', sans-serif;
            font-size: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 8px;
            margin-top: 20px;
            color: #888;
        }

        .artwork-slide {
            padding: 80px;
            align-items: center;
        }

        .artwork-container {
            width: 100%;
            display: flex;
            justify-content: center;
            margin-bottom: 40px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }

        .artwork-img {
            max-width: 100%;
            max-height: 1200px;
            display: block;
        }

        .info-panel {
            text-align: center;
            max-width: 800px;
        }

        .title {
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            margin: 0 0 10px 0;
            color: #fff;
        }

        .meta {
            color: var(--accent);
            text-transform: uppercase;
            font-size: 0.9rem;
            letter-spacing: 2px;
            margin-bottom: 30px;
            display: inline-block;
            border-bottom: 1px solid var(--accent);
            padding-bottom: 5px;
        }

        .description {
            font-size: 1.1rem;
            line-height: 1.6;
            color: #aaa;
        }
        
        .footer-slide {
             height: 800px;
             justify-content: center;
             align-items: center;
             text-align: center;
             background: #0a0a0a;
        }

        .btn {
            display: inline-block;
            margin-top: 40px;
            padding: 15px 40px;
            border: 1px solid var(--accent);
            color: var(--accent);
            text-decoration: none;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s ease;
        }

        .btn:hover {
            background: var(--accent);
            color: #000;
        }

    </style>
</head>
<body>

    <div class="slide cover">
        <div>
            <h1>UNIVERSO EDUSSE</h1>
            <h2>Digital Art Selection 2026</h2>
            <div style="width: 2px; height: 100px; background: #333; margin: 40px auto;"></div>
            <p style="color: #666;">Eduardo Ramírez</p>
        </div>
    </div>
"""

HTML_TEMPLATE_END = """
    <div class="slide footer-slide">
        <div>
            <h2 style="color: #fff; font-family: 'Playfair Display', serif; font-size: 3rem;">Gracias por ver</h2>
            <p style="color: #666; font-size: 1.2rem;">Descubre la colección completa</p>
            <a href="https://dudeduart.es" class="btn">dudeduart.es</a>
        </div>
    </div>

</body>
</html>
"""

def find_artwork_in_metadata(metadata, key_part):
    """Finds an artwork in metadata that matches the key_part (filename or id)."""
    # Try exact match on ID first (if key_part includes extension or full name)
    if key_part in metadata:
        return metadata[key_part]
    
    # Search by inclusion in key or filename
    for filename, data in metadata.items():
        if key_part.lower() in filename.lower():
            # Special check for "aldea china" to avoid partial matches on other china items if any
            if key_part == "aldea china" and "aldea china" not in filename.lower():
                continue
            return data
    return None

def normalize_path(path):
    return path.replace("\\", "/")

def generate():
    print(f"Loading metadata from {METADATA_FILE}...")
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    html_content = HTML_TEMPLATE_START

    print("Processing artworks...")
    for item_key in SELECTION:
        data = find_artwork_in_metadata(metadata, item_key)
        if not data:
            print(f"WARNING: Could not find metadata for {item_key}")
            continue
        
        # Extract info
        title = data.get('title', 'Sin Título')
        desc = data.get('description', '')
        # Fallback description if empty
        if not desc:
            desc = "Una exploración visual de la estética y la técnica digital."

        # Construct image path. Metadata keys usually are usually filenames like "file.jpg"
        # We need to find where they are.
        # Assuming metadata keys ARE the filenames, we need to prefix with 'assets/PARENT_FOLDER/'
        # But wait, the metadata usually stores only the entry. 
        # Let's check locally found paths for the new ones.
        
        # Helper to find file path on disk since metadata might not have full relative path
        filename = os.path.basename(data.get('id', item_key + ".png")) # tentative
        
        # We'll do a quick walk to find the file path relative to script
        image_path = ""
        for root, dirs, files in os.walk("assets"):
            for file in files:
                if file.lower() == filename.lower() or file.lower().startswith(item_key.lower()):
                     image_path = os.path.join(root, file)
                     break
            if image_path: break
        
        if not image_path:
            # Fallback for "aldrea china" type keys that might be just names in my list
            # We already did find_by_name in planning.
            # Let's try to match loosely again
             for root, dirs, files in os.walk("assets"):
                for file in files:
                    if item_key.lower() in file.lower():
                         image_path = os.path.join(root, file)
                         break
                if image_path: break

        if image_path:
            image_path = normalize_path(image_path)
        else:
            image_path = "assets/placeholder.png"
            print(f"  -> Image not found on disk for {item_key}")

        # Get collection from parent folder
        collection = image_path.split('/')[1] if '/' in image_path else "Unknown"
        
        print(f"  -> Adding {title} ({collection})")

        html_content += f"""
    <div class="slide artwork-slide">
        <div class="artwork-container">
            <img src="{image_path}" class="artwork-img" alt="{title}">
        </div>
        <div class="info-panel">
            <h3 class="title">{title}</h3>
            <div class="meta">{collection}</div>
            <p class="description">{desc}</p>
        </div>
    </div>
"""

    html_content += HTML_TEMPLATE_END

    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Done!")

if __name__ == "__main__":
    generate()
