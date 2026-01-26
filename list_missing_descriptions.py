import re

DATA_FILE = "js/data.js"
PLACEHOLDER = "Nueva obra añadida recientemente."

def list_missing():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: data.js not found.")
        return

    # Use regex to find blocks or simple line scanning
    # Regex is risky if format varies, but line scanning is robust for this file structure
    
    current_id = "Unknown"
    current_title = "Unknown"
    current_category = "Unknown"
    
    missing_list = []

    for line in content.split('\n'):
        line = line.strip()
        
        if line.startswith('"id":'):
            current_id = line.split(':')[1].strip().strip('",')
        
        if line.startswith('"title":'):
            current_title = line.split(':')[1].strip().strip('",')
            
        if line.startswith('"category":'):
            current_category = line.split(':')[1].strip().strip('",')
            
        if PLACEHOLDER in line:
            missing_list.append(f"- **{current_title}** ({current_category})\n  - ID: `{current_id}`")

    if missing_list:
        print(f"Found {len(missing_list)} artworks needing descriptions:\n")
        print('\n'.join(missing_list))
    else:
        print("All artworks seem to have descriptions!")

if __name__ == "__main__":
    list_missing()
