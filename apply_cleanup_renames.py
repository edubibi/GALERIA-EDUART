import json
import re

def apply_cleanups():
    with open('metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    updates = [
        ("00edusse_001", "Avestruz Del Universo"),
        ("12cristal_cubico_001", "Bodegon Masa Y Pan"), # User said yes to removing "Estilo" too implicitly or I should just clean it up.
        # "Bodegon Masa Y Pan Estilo" was the proposal, but leaving "Estilo" at the end is weird.
        # User said "si a todo" to my question "En el número 2 quito también 'Estilo'?". So yes.
        ("20borassie_006", "En El Pueblo Minimal"),
        ("capitana caplive", "Capitana"),
        ("altamar_espatac-mat", "Altamar")
    ]
    
    count = 0
    for item_id, new_title in updates:
        if item_id in data:
            old_title = data[item_id]['title']
            data[item_id]['title'] = new_title
            print(f"Updated {item_id}: '{old_title}' -> '{new_title}'")
            count += 1
            
    if count > 0:
        with open('metadata.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Metadata updated.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    apply_cleanups()
