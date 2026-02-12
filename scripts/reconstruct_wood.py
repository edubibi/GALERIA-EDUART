from PIL import Image
import os

def create_pure_wood_frame():
    src_path = r'C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg'
    output_path = r'c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\wood_frame_pure.png'
    
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size
    
    # Extract a 50x30 patch of pure wood from the top edge (middle)
    # y=10 to y=30 is definitely wood (Top wood ends at 42)
    wood_sample = img.crop((w//2 - 25, 10, w//2 + 25, 40)) # 50x30 piece
    
    # We'll create a 120x120 sprite (40px per slice)
    slice_size = 40
    sprite = Image.new("RGBA", (slice_size * 3, slice_size * 3), (255, 255, 255, 0))
    
    # Prepare a 40x40 tile from the wood sample
    tile = wood_sample.resize((slice_size, slice_size), Image.Resampling.LANCZOS)
    
    # Fill the 9-slice area with wood (excluding the 1,1 center hole)
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue # The hole for the content
            
            # Rotate or flip for corners to look more natural? 
            # Let's keep it simple first just to get the color right
            sprite.paste(tile, (i * slice_size, j * slice_size))
            
    sprite.save(output_path, "PNG")
    print(f"✅ Symmetric pure wood sprite saved to: {output_path}")

if __name__ == "__main__":
    create_pure_wood_frame()
