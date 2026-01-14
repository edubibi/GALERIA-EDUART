
import json
import os

metadata_path = r"C:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\metadata.json"

titles = {
    1: "PAMPLONA",
    2: "HUESCA",
    3: "ZARAGOZA",
    4: "GIRONA",
    5: "LLEIDA",
    6: "ANFITEATRO DE TARRAGONA",
    7: "CASTELLÓN",
    8: "VALENCIA",
    9: "CACERES",
    10: "SEVILLA"
}

with open(metadata_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in range(1, 11):
    key = f"boracarbon_mon_{i:03d}"
    if key not in data:
        data[key] = {}
    
    # Update title
    # Title casing: The user gave CAPS. Usually we might want Title Case?
    # The previous titles were Title Case ("El Sendero...").
    # But some might be specific. "ANFITEATRO DE TARRAGONA".
    # I will stick to what the user gave but maybe Capitalize nicely?
    # User wrote "PAMPLONA", "ANFITEATRO DE TARRAGONA".
    # I'll use .title() but keep 'De' lowercase if I get fancy, but standard .title() is safer for now.
    # Actually, let's keep user input or just Title Case it manually?
    # "PAMPLONA" -> "Pamplona"
    # "ANFITEATRO DE TARRAGONA" -> "Anfiteatro De Tarragona"
    # User's other titles: "El Sendero De Los Globos..." (uses Title Case).
    
    raw_title = titles[i]
    # Simple title casing
    title_cased = raw_title.title() 
    # Fix 'De' if needed? "Anfiteatro De Tarragona" is fine.
    
    data[key]["title"] = title_cased
    data[key]["category"] = "24BORACARBON MONUMENTOS" # Assuming category based on folder name
    # Or should I leave category out? The other entries in the grep didn't show category in the snippets?
    # Wait, the 01exp_neocirc_012 snippet only showed "title".
    # I'll check if category is needed.

# Save
with open(metadata_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Metadata updated.")
