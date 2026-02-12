import os
from PIL import Image

def extract_frame_texture(input_path, output_path):
    print(f"🪚 Extracting frame texture from: {input_path}")
    img = Image.open(input_path).convert("RGBA")
    
    # Based on analysis: Wood is at the edges (0-22px left, 0-42px top, etc.)
    # We must include the whole frame to get the wood texture.
    crop_box = (0, 0, 718, 1024)
    frame_texture = img.crop(crop_box)
    
    # Save as PNG
    frame_texture.save(output_path, "PNG")
    print(f"✅ Texture saved to: {output_path} ({frame_texture.width}x{frame_texture.height})")

if __name__ == "__main__":
    SRC = r"C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg"
    DEST = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\frame_texture.png"
    
    os_dir = os.path.dirname(DEST)
    if not os.path.exists(os_dir):
        os.makedirs(os_dir)
        
    extract_frame_texture(SRC, DEST)
