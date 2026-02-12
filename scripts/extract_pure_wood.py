from PIL import Image

def extract_clean_wood():
    src_path = r'C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg'
    output_path = r'c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\pure_wood_texture.png'
    
    img = Image.open(src_path).convert("RGBA")
    
    # Extract a strip of wood from the top edge (where it's definitely beige)
    # Based on pixel scan, wood is roughly between y=0 and y=22
    # We take a piece from the middle of the top border to avoid corner shadows
    wood_strip = img.crop((100, 2, 200, 22)) # 100x20 area of "pure wood"
    
    # We will build a 60x60 9-slice sprite using this wood
    slice_size = 20
    sprite = Image.new("RGBA", (slice_size * 3, slice_size * 3), (255, 255, 255, 0))
    
    # Take a 20x20 piece for the pattern
    wood_tile = wood_strip.crop((0, 0, slice_size, slice_size))
    
    # Fill the 9-slice (except the center)
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1: continue # hole
            sprite.paste(wood_tile, (i * slice_size, j * slice_size))
            
    sprite.save(output_path, "PNG")
    print(f"✅ Pure wood texture saved to: {output_path}")

if __name__ == "__main__":
    extract_clean_wood()
