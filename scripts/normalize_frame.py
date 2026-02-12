from PIL import Image

def normalize_frame(input_path, output_path):
    print(f"🛠️  Normalizing frame texture from: {input_path}")
    img = Image.open(input_path).convert("RGBA")
    
    # We'll create a 100x100 sprite for CSS border-image
    # Slice size will be 30px.
    slice_size = 30
    sprite = Image.new("RGBA", (slice_size * 3, slice_size * 3), (255, 255, 255, 0))
    
    # The top edge of the photo has the best wood (y=0 to y=42)
    # Let's take samples from there to ensure beige color.
    
    # Corner Top-Left: crop from top edge (using x=0 to x=30, y=0 to y=30)
    # But wait, left wood is only 22px. So if x > 22 it might be white.
    # We should take a piece from the TOP-MIDDLE to avoid corner shadows/irregularities.
    wood_sample = img.crop((100, 5, 200, 35)) # 100x30 strip of "pure wood"
    
    # Reconstruct a generic wood sprite
    # Corners (we can repeat the same texture or rotate it)
    corner = wood_sample.crop((0, 0, slice_size, slice_size))
    sprite.paste(corner, (0, 0))
    sprite.paste(corner.transpose(Image.FLIP_LEFT_RIGHT), (slice_size * 2, 0))
    sprite.paste(corner.transpose(Image.FLIP_TOP_BOTTOM), (0, slice_size * 2))
    sprite.paste(corner.transpose(Image.ROTATE_180), (slice_size * 2, slice_size * 2))
    
    # Edges
    edge_h = wood_sample.crop((0, 0, slice_size * 3, slice_size)) # This is only 100 wide, slice*3=90. OK.
    sprite.paste(edge_h.crop((0, 0, slice_size, slice_size)), (slice_size, 0)) # Top
    sprite.paste(edge_h.crop((0, 0, slice_size, slice_size)).transpose(Image.FLIP_TOP_BOTTOM), (slice_size, slice_size * 2)) # Bottom
    
    edge_v = edge_h.transpose(Image.ROTATE_90)
    sprite.paste(edge_v.crop((0, 0, slice_size, slice_size)), (0, slice_size)) # Left
    sprite.paste(edge_v.crop((0, 0, slice_size, slice_size)).transpose(Image.FLIP_LEFT_RIGHT), (slice_size * 2, slice_size)) # Right

    # Center (empty/transparent for border-image to work well)
    
    # Save as PNG
    sprite.save(output_path, "PNG")
    print(f"✅ Symmetric wood sprite saved to: {output_path}")

if __name__ == "__main__":
    SRC = r"C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg"
    DEST = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\frame_texture_symmetric.png"
    normalize_frame(SRC, DEST)
