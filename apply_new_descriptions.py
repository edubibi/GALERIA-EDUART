import json
import re

METADATA_FILE = "metadata.json"
INPUT_TEXT_FILE = "new_descriptions.txt"

def update_metadata():
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        
    with open(INPUT_TEXT_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    # Regex to find blocks of ID and content
    # Look for patterns like: "1. El Ave Cósmica (00edusse_001.jpg)"
    # or "•  Atenas / Acrópolis (01exp_neocirc_011.jpg):"
    
    # We will identify sections by finding the ID in parentheses (e.g. 00edusse_001.jpg)
    # Then take everything until the next ID search match as the "content".
    
    # Split text by lines
    lines = text.split('\n')
    
    current_id = None
    current_buffer = []
    
    # Helper to save buffer to previous ID
    def save_buffer(id_str, buffer):
        if not id_str or not buffer: return
        raw_desc = '\n'.join(buffer).strip()
        
        # Clean up the ID (remove extension)
        clean_id = id_str.lower().replace('.jpg', '').replace('.png', '').replace('.jpeg', '')
        
        if clean_id in metadata:
            print(f"Updating {clean_id}...")
            # We treat the whole block as the description for now, preserving line breaks?
            # Or should we format it? The user used "Técnica Visual:", "Narrativa:", etc.
            # Let's clean it up slightly but keep the structure.
            metadata[clean_id]['description'] = raw_desc
            metadata[clean_id]['tech_info'] = "Ver descripción detallada." # Optional: flag that it has deep info?
        else:
            print(f"Warning: ID {clean_id} from text not found in metadata.")

    # Regex to catch lines that START a new item
    # Matches: "1. Name (id.jpg)" or "• Name (id.jpg):"
    id_pattern = re.compile(r'\(([\w_]+\.(?:jpg|png|jpeg))\)')

    for line in lines:
        match = id_pattern.search(line)
        if match:
            # Found a new item line. Save previous.
            save_buffer(current_id, current_buffer)
            
            # Start new
            current_id = match.group(1)
            current_buffer = []
            
            # Does this line contain valuable info or just title?
            # It usually contains the title before the parens.
            # The description follows.
            # We can optionally extract the title if needed, but we might trust the existing titles?
            # The user's text: "1. El Ave Cósmica (00edusse_001.jpg)" -> Title is "El Ave Cósmica"
            # Let's skip adding this line to the description buffer to avoid duplicating the header.
        else:
            if current_id:
                # Add to buffer if not empty/useless
                if line.strip():
                    current_buffer.append(line.strip())

    # Save last one
    save_buffer(current_id, current_buffer)
    
    # Write back
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    
    print("Metadata updated successfully.")

if __name__ == "__main__":
    update_metadata()
