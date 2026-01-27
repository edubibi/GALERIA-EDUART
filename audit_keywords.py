import json
import re

def audit_titles():
    with open('metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    style_map = {
        '00EDUSSE': ['Edusse'],
        '01EXP_NEOCIRC': ['Neocirc'],
        '02CUBESSE stilo': ['Cubesse', 'Stilo'],
        '03EXPNEOPLUS': ['Neoplus'],
        '04APLICC': ['Aplicc'],
        '05PLUMINK': ['Plumink'],
        '06IDE_CLASSIC': ['Ide Classic', 'Classic'],
        '07NEOINK stilo': ['Neoink', 'Stilo'],
        '08BORACARBON': ['Boracarbon'],
        '09FRACNEO': ['Fracneo'],
        '10OLEOCUBBO': ['Oleocubbo'],
        '11URBANSPHERIC': ['Urbanspheric'],
        '12CRISTAL_CUBICO': ['Cristal', 'Cubico'],
        '13RECTESSE': ['Rectesse'],
        '14TEREXSE': ['Terexse'],
        '15CUBESSEPLUS': ['Cubesseplus'],
        '16EXPNEO': ['Expneo'],
        '17FUZZTESS': ['Fuzztess'],
        '18ABSTRACTO_CONFLUENCIA': ['Abstracto', 'Confluencia'],
        '19FUZZLINE_ABS': ['Fuzzline', 'Abs'],
        '20BORASSIE': ['Borassie'],
        '21OCE-BURST': ['Oce-Burst', 'Oce Burst'],
        '22NEO-LUMINA': ['Neo-Lumina', 'Neo Lumina'],
        '23TRIDIM-BURST': ['Tridim-Burst', 'Tridim Burst'],
        '24BORACARBON MONUMENTOS': ['Boracarbon', 'Monumentos'],
        '25CAPLIVE': ['Caplive'],
        '26CARL_LINE': ['Carl Line'],
        '27LINEVORT': ['Linevort'],
        '28ESPATAC': ['Espatac'],
        '29ESPATAC-MAT': ['Espatac', 'Mat'],
        'SAGA CUBESSEPLUS': ['Cubesseplus']
    }
    
    candidates = []

    for key, item in data.items():
        if not isinstance(item, dict) or 'title' not in item:
            continue
            
        category = item.get('category', '')
        title = item.get('title', '')
        
        # Determine keywords for this category
        keywords = style_map.get(category, [])
        
        # If no strict mapping, try generic approach (last resort)
        if not keywords:
             continue

        new_title = title
        matched = False
        for kw in keywords:
            # check if keyword is in title (case insensitive)
            # Use \b to ensure word boundary, avoid partial matches if possible, 
            # though "Neocirc" inside "Neocircular" assumes they are different words.
            pattern = re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE)
            if pattern.search(new_title):
                # Remove it
                new_title = pattern.sub('', new_title)
                matched = True
        
        if matched:
            # Cleanup extra spaces
            new_title = re.sub(r'\s+', ' ', new_title).strip()
            # If title became empty or too short, warn/skip?
            if len(new_title) < 2:
                continue 
            
            if new_title.lower() != title.lower():
                candidates.append({
                    'id': key,
                    'category': category,
                    'current_title': title,
                    'proposed_title': new_title
                })

    print(f"Found {len(candidates)} candidates for renaming.")
    with open('rename_candidates.txt', 'w', encoding='utf-8') as f:
        for C in candidates:
            line = f"[{C['category']}] {C['id']} : {C['current_title']} -> {C['proposed_title']}"
            print(line)
            f.write(line + "\n")


if __name__ == "__main__":
    audit_titles()
