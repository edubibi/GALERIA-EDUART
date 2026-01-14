import re
import json

path = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\js\data.js"

try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"File read successfully. Length: {len(content)} bytes.")

    # Extract artworkData
    match = re.search(r'const artworkData = (\[.*?\]);', content, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            print(f"SUCCESS: artworkData parsed correctly. {len(data)} items found.")
            
            # Check for Sellos
            sellos = [x for x in data if x.get('category') == "SELLOS_MAGICOS"]
            print(f"Items with category 'SELLOS_MAGICOS': {len(sellos)}")
            
        except json.JSONDecodeError as e:
            print(f"ERROR: extracted string is not valid JSON. {e}")
            # Print context around error
            print(f"Error at char: {e.pos}")
            start = max(0, e.pos - 50)
            end = min(len(json_str), e.pos + 50)
            print(f"Context: ...{json_str[start:end]}...")
            
    else:
        print("ERROR: Could not find 'const artworkData = [...];' pattern.")

except Exception as e:
    print(f"CRITICAL ERROR reading file: {e}")
