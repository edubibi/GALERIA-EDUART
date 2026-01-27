import json
import re

def remove_leading_numbers():
    with open('metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    updates = []
    
    # regex for leading digits followed by optional whitespace
    pattern = re.compile(r'^(\d+)\s*(.*)')
    
    for key, item in data.items():
        if not isinstance(item, dict) or 'title' not in item:
            continue
            
        title = item.get('title', '')
        match = pattern.match(title)
        
        if match:
            # Check if it's the specific case or general
            # group(1) is number, group(2) is rest
            number = match.group(1)
            rest = match.group(2)
            
            # If rest is empty, we probably shouldn't remove the number as title would be empty
            if not rest:
                continue
                
            new_title = rest
            
            # Specific logic check
            # User mentioned "05 Bahia..." -> "Bahia..."
            # User said "principio de frase con números, los quitas"
            
            updates.append((key, title, new_title))
            
    print(f"Found {len(updates)} titles starting with numbers.")
    for key, old, new in updates:
        print(f"[{key}] '{old}' -> '{new}'")
        data[key]['title'] = new

    if updates:
        with open('metadata.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Metadata updated.")

if __name__ == "__main__":
    remove_leading_numbers()
