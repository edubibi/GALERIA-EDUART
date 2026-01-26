import re
import json
import os
import datetime

DATA_FILE = "js/data.js"
TEMPLATE_FILE = "dossier_portfolio.html"
OUTPUT_FILE = "catalogo_completo.html"

def parse_js_data(filepath):
    """
    Parses the artworkData array from js/data.js manually or via regex, 
    returning a list of dictionaries.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return []

    # Regex to find the array content: const artworkData = [ ... ];
    # We find the start of the array and the end.
    start_match = re.search(r'const\s+artworkData\s*=\s*\[', content)
    if not start_match:
        print("Could not find artworkData array start.")
        return []

    # Extract the list part
    start_index = start_match.end()
    # Assume the array ends at the last bracket before the semicolon or EOF
    # A bit naive but usually works for this generated file. 
    # Let's clean up the JS specific syntax to make it valid JSON
    
    # Strategy: 
    # 1. Grab everything from [ ... ]
    # 2. Add quotes to keys
    # 3. Remove trailing commas
    
    # Actually, since we control the file format and it is pretty standard:
    # We can use a simpler line-by-line parser as used in previous scripts to be safe against JSON syntax issues
    
    artworks = []
    current_art = {}
    
    lines = content[start_index:].split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('];'): 
            break
        
        # Key-Value extraction
        # Matches: "key": "value", OR key: "value",
        # We need to handle multi-line strings if description is long? 
        # The previous scripts treated description as single line strings mostly.
        # Let's assume strict format preservation from our build tools.
        
        # Match: "key": "value"
        # We need to be careful with escaped quotes inside value.
        
        # Simple regex for  "key": "value" or key: "value"
        # Capture group 1: key, Capture group 2: value
        match = re.match(r'"?(\w+)"?\s*:\s*"(.*)",?$', line)
        if match:
            key, val = match.groups()
            # Unescape quotes if needed
            val = val.replace('\\"', '"')
            current_art[key] = val
            continue
            
        # Match boolean/numbers: "key": value
        match_bool = re.match(r'"?(\w+)"?\s*:\s*(true|false|[\d\.]+),?$', line)
        if match_bool:
            key, val = match_bool.groups()
            if val == 'true': val = True
            elif val == 'false': val = False
            else: val = float(val)
            current_art[key] = val
            continue
            
        if line == '{':
            current_art = {}
        elif line == '},' or line == '}':
            if current_art:
                artworks.append(current_art)
                current_art = {}
                
    return artworks

def generate_html(artworks):
    # Load Template parts
    # We will hardcode the css and structure based on dossier_portfolio.html
    # but generating pages dynamically.
    
    # CSS from dossier_portfolio.html (simplified/inline)
    css = """
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400&display=swap');
        :root { --primary: #1a1a1a; --accent: #D4AF37; --font-serif: 'Playfair Display', serif; --font-sans: 'Lato', sans-serif; }
        body { font-family: var(--font-sans); color: var(--primary); margin: 0; padding: 0; background: #fff; }
        @page { size: A4; margin: 0; }
        .page { width: 210mm; height: 297mm; padding: 20mm; box-sizing: border-box; position: relative; page-break-after: always; display: flex; flex-direction: column; justify-content: center; }
        .cover-page { text-align: center; justify-content: center; background: #111; color: #fff; }
        .cover-page h1 { font-family: var(--font-serif); font-size: 3rem; color: var(--accent); margin-bottom: 1rem; }
        .cover-page p { font-size: 1.2rem; letter-spacing: 2px; text-transform: uppercase; }
        .intro-page { justify-content: flex-start; padding-top: 40mm; }
        .intro-page h2 { font-family: var(--font-serif); font-size: 2rem; border-bottom: 2px solid var(--accent); padding-bottom: 10px; margin-bottom: 20px; }
        .artwork-page { align-items: center; }
        .artwork-image-container { width: 100%; height: 60%; display: flex; align-items: center; justify-content: center; margin-bottom: 2rem; }
        .artwork-image { max-width: 100%; max-height: 100%; object-fit: contain; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15); }
        .artwork-info { text-align: left; width: 100%; padding: 0 10%; box-sizing: border-box; }
        .artwork-title { font-family: var(--font-serif); font-size: 1.8rem; margin: 0 0 0.5rem 0; color: var(--primary); }
        .artwork-meta { color: #666; font-size: 0.9rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px; border-left: 3px solid var(--accent); padding-left: 10px; }
        .artwork-desc { font-size: 1rem; line-height: 1.6; color: #333; }
        .tech-info { margin-top: 1rem; font-size: 0.85rem; color: #777; font-style: italic; }
        footer { position: absolute; bottom: 10mm; left: 0; width: 100%; text-align: center; font-size: 0.8rem; color: #999; }
    """

    html_start = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Catálogo Completo - Eduardo Ramírez (EDUSSE)</title>
    <style>{css}</style>
</head>
<body>
    <!-- PORTADA -->
    <div class="page cover-page">
        <h1>CATÁLOGO DE OBRAS</h1>
        <p>Universo EDUSSE</p>
        <div style="margin-top: 2rem; width: 100px; height: 2px; background: #D4AF37; margin-left: auto; margin-right: auto;"></div>
        <p style="margin-top: 2rem; font-size: 1rem; text-transform: none;">Eduardo Ramírez de Cartagena</p>
        <p style="font-size: 0.8rem; opacity: 0.7;">Generado el {datetime.date.today().strftime('%d/%m/%Y')}</p>
    </div>
"""

    html_pages = ""
    # Filter only artworks, not bg or sellos? User said "catálogo de todas las fotos".
    # Let's skip 'bg' category if it exists as it seems to be background assets.
    # Keep SELLOS_MAGICOS as they are artworks.
    
    total_artworks = 0
    # Filter strictly for Styles. 
    # User requested ONLY "fotos de los estilos".
    # Exclude: 'General', 'bg', 'contact_header', and potentially others not fitting the style pattern.
    
    excluded_categories = ['General', 'bg', 'contact_header']
    
    # Optional: If we want to be very strict, we could whitelist 00-99 styles and named collections like SELLOS.
    # But for now, excluding the known "junk" categories is safest.
    
    valid_artworks = [a for a in artworks if a.get('category') not in excluded_categories]
    
    # Further filter: Remove specific IDs if they snuck in?
    # User mentioned "logos como cuadro". If "Logo Banner" is in a valid category, remove it.
    # But "Logo Banner" was in "General", so it should be gone.
    
    count = len(valid_artworks)

    for i, art in enumerate(valid_artworks):
        index = i + 1
        
        # Use Poster image if available? 
        # The user generated posters in 'assets_poster' but the web catalog links to 'assets/...'
        # The poster has the white border (passepartout).
        # It usually looks better for printing/catalog.
        # Check if poster exists.
        
        basename = os.path.basename(art.get('src', ''))
        poster_name = os.path.splitext(basename)[0] + "_POSTER" + os.path.splitext(basename)[1]
        poster_path = f"assets_poster/{art.get('category')}/{poster_name}"
        
        # If poster file exists locally, we can link it.
        # BUT html usually needs relative path.
        # Let's check if the file exists using os.path.exists (relative to CWD)
        # Note: categories in assets_poster might generally match assets structure.
        
        # Simple fallback: Use the original src if poster logic is too complex or file missing.
        img_src = art.get('src', '')
        
        # Attempt to use poster path if reasonable
        potential_poster = f"assets_poster/{art.get('category')}/{poster_name}"
        if os.path.exists(potential_poster):
            img_src = potential_poster
            
        title = art.get('title', 'Sin Título')
        category = art.get('category', 'General')
        desc = art.get('description', '')
        tech = art.get('tech_info', '')
        
        page_html = f"""
    <div class="page artwork-page">
        <div class="artwork-image-container">
            <img src="{img_src}" class="artwork-image" alt="{title}">
        </div>
        <div class="artwork-info">
            <h3 class="artwork-title">{title}</h3>
            <div class="artwork-meta">Colección: {category}</div>
            <p class="artwork-desc">{desc}</p>
            {f'<p class="tech-info">Tecnología: {tech}</p>' if tech else ''}
        </div>
        <footer>{index} / {count}</footer>
    </div>
"""
        html_pages += page_html

    html_end = """
</body>
</html>
"""
    return html_start + html_pages + html_end

def main():
    print("Reading data...")
    artworks = parse_js_data(DATA_FILE)
    print(f"Found {len(artworks)} items.")
    
    print("Generating HTML...")
    full_html = generate_html(artworks)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    print(f"Done! Catalog saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
