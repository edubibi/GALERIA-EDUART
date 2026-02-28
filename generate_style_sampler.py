import json
import os

def generate_sampler():
    metadata_path = 'metadata.json'
    output_html = 'muestrario_estilos.html'
    
    if not os.path.exists(metadata_path):
        print(f"Error: {metadata_path} not found.")
        return

    with open(metadata_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    categories = {}
    # Extract one sample per category
    for key, item in data.items():
        if 'category' in item:
            cat = item['category']
            if cat not in categories:
                categories[cat] = item

    # Sort categories to be organized
    sorted_cats = sorted(categories.keys())

    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Muestrario de Estilos - Galería</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #1a1a1a; 
            color: #e0e0e0; 
            padding: 40px; 
            margin: 0;
        }}
        h1 {{ 
            text-align: center; 
            color: #fff; 
            text-transform: uppercase; 
            letter-spacing: 2px;
            margin-bottom: 50px;
        }}
        .grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
            gap: 30px; 
            max-width: 1400px;
            margin: 0 auto;
        }}
        .card {{ 
            background: #2a2a2a; 
            border-radius: 12px; 
            overflow: hidden; 
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            transition: transform 0.3s ease;
            border: 1px solid #333;
        }}
        .card:hover {{
            transform: translateY(-5px);
            border-color: #555;
        }}
        .img-container {{
            width: 100%;
            height: 220px;
            overflow: hidden;
            background: #000;
        }}
        img {{ 
            width: 100%; 
            height: 100%; 
            object-fit: cover;
            opacity: 0.9;
            transition: opacity 0.3s;
        }}
        .card:hover img {{
            opacity: 1;
        }}
        .info {{ 
            padding: 15px; 
        }}
        .style-tag {{
            font-size: 0.75rem;
            color: #aaa;
            text-transform: uppercase;
            margin: 0;
            margin-bottom: 5px;
        }}
        .title {{ 
            font-size: 1.1rem; 
            font-weight: 600; 
            margin: 0;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
    </style>
</head>
<body>
    <h1>Muestrario de Estilos ({len(sorted_cats)} categorías)</h1>
    <div class="grid">
"""

    for cat in sorted_cats:
        item = categories[cat]
        src = item.get('src', '')
        title = item.get('title', 'Sin título')
        
        html_content += f"""
        <div class="card">
            <div class="img-container">
                <img src="{src}" alt="{title}">
            </div>
            <div class="info">
                <p class="style-tag">Estilo: {cat}</p>
                <p class="title">{title}</p>
            </div>
        </div>
"""

    html_content += """
    </div>
</body>
</html>
"""

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Archivo generado: {os.path.abspath(output_html)}")

if __name__ == "__main__":
    generate_sampler()
