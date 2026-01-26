import json
import re
import os

# --- CONFIG ---
OUTPUT_FILE = "fichas_completo.html"
DATA_FILE = "js/data.js"

# --- HTML TEMPLATES ---
HTML_HEADER = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Fichas Técnicas Completas - Tu Arte</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

        :root {
            --primary: #000;
            --accent: #D4AF37;
            --font-serif: 'Playfair Display', serif;
            --font-sans: 'Lato', sans-serif;
        }

        body {
            font-family: var(--font-sans);
            margin: 0;
            padding: 0;
            background: #eee;
        }

        @page {
            size: A4;
            margin: 0;
        }

        .sheet {
            width: 210mm;
            height: 297mm;
            padding: 15mm;
            box-sizing: border-box;
            background: white;
            position: relative;
            page-break-after: always;
            display: flex;
            flex-direction: column;
        }

        .header {
            border-bottom: 2px solid var(--accent);
            padding-bottom: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }

        .header h1 {
            font-family: var(--font-serif);
            font-size: 1.8rem;
            margin: 0;
            color: var(--primary);
            max-width: 70%;
        }

        .subtitle {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #666;
        }

        .image-box {
            width: 100%;
            height: 50%; /* Mitad de página para la imagen */
            display: flex;
            justify-content: center;
            align-items: center;
            background: #fafafa;
            margin-bottom: 20px;
            border: 1px solid #eee;
        }

        .image-box img {
            max-width: 95%;
            max-height: 95%;
            object-fit: contain;
            box-shadow: 2px 5px 10px rgba(0,0,0,0.1);
        }

        .content {
            flex-grow: 1;
        }

        .section {
            margin-bottom: 20px;
        }

        .section h3 {
            font-family: var(--font-serif);
            font-size: 1.1rem;
            color: var(--accent);
            margin: 0 0 8px 0;
            text-transform: uppercase;
            border-left: 3px solid var(--accent);
            padding-left: 10px;
        }

        .section p {
            font-size: 1rem;
            line-height: 1.6;
            margin: 0;
            color: #333;
            text-align: justify;
        }

        .meta-table {
            width: 100%;
            background: #f9f9f9;
            padding: 10px;
            border-radius: 4px;
            margin-top: auto; /* Push to bottom */
            font-size: 0.8rem;
            color: #666;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
        }
        
        .meta-item strong { color: #000; }

        footer {
            text-align: right;
            font-size: 0.7rem;
            color: #bbb;
            margin-top: 10px;
        }

    </style>
</head>
<body>
"""

HTML_FOOTER = """
</body>
</html>
"""

def parse_data_js():
    # Same parsing logic as before
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    start = content.find("const artworkData = [")
    if start == -1: return []
    array_str = content[start + len("const artworkData ="):]
    array_str = array_str.strip()
    if array_str.endswith(";"): array_str = array_str[:-1]

    # Normalize JSON keys
    fixed_json = re.sub(r'(\w+):', r'"\1":', array_str)
    fixed_json = re.sub(r',\s*]', ']', fixed_json)
    fixed_json = re.sub(r',\s*}', '}', fixed_json)
    
    try:
        data = json.loads(fixed_json)
        return data
    except Exception as e:
        print(f"JSON Parsing Error: {e}")
        return []

def generate():
    artworks = parse_data_js()
    if not artworks:
        return

    # Sort by Category/Title
    artworks.sort(key=lambda x: (x.get('category', ''), x.get('title', '')))

    html = HTML_HEADER
    
    count = 1
    for art in artworks:
        # Resolve Poster Path
        base, ext = os.path.splitext(art['src'])
        poster_path = f"{base}_POSTER{ext}"
        final_src = poster_path if os.path.exists(poster_path) else art['src']

        # Formatting texts
        desc = art.get('description', '')
        tech = art.get('tech_info', '')
        
        # If description contains explicit period, we might split visually?
        # No, just output as block.

        html += f"""
        <div class="sheet">
            <div class="header">
                <div>
                    <div class="subtitle">Colección {art.get('category','')}</div>
                    <h1>{art.get('title','Sin Título')}</h1>
                    <div style="font-size: 0.8rem; color: #999;">ID: {art.get('id','')}</div>
                </div>
                <!-- Optional Logo if desired -->
                <!-- <img src="assets/logo_banner.png" style="height: 30px;"> -->
            </div>

            <div class="image-box">
                <img src="{final_src}" alt="{art.get('title','')}">
            </div>

            <div class="content">
                <div class="section">
                    <h3>Análisis Artístico</h3>
                    <p>{desc}</p>
                </div>
                
                <div class="section">
                     <h3>Especificaciones Técnicas</h3>
                     <p>{tech}</p>
                </div>
            </div>

            <div class="meta-table">
                <div class="meta-item"><strong>Dimensión:</strong> {art.get('size','Consultar')}</div>
                <div class="meta-item"><strong>Precio Ref:</strong> {art.get('price','Consultar')}€</div>
                <div class="meta-item"><strong>Estado:</strong> {'Vendido' if art.get('sold') else 'Disponible'}</div>
            </div>
            
            <footer>Ficha {count} | Universo EDUSSE</footer>
        </div>
        """
        count += 1

    html += HTML_FOOTER
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Fichas Completas Generated: {OUTPUT_FILE} ({count-1} sheets)")

if __name__ == "__main__":
    generate()
