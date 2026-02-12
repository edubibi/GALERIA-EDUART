import os
from PIL import Image, ImageOps, ImageFilter

def create_dynamic_mockup(frame_path, painting_path, output_path, margin_cm=3):
    print(f"🎬 Creating dynamic mockup for: {painting_path}")
    
    # Load images
    src_frame = Image.open(frame_path).convert("RGBA")
    painting = Image.open(painting_path).convert("RGBA")
    
    # Based on analysis of uploaded_media_1770398220983.jpg (718x1024)
    # Precise wood thickness from pixel analysis
    border_thickness = 22
    
    # Slicing the frame (9-slice)
    # Corners
    c_tl = src_frame.crop((0, 0, border_thickness, border_thickness))
    c_tr = src_frame.crop((src_frame.width - border_thickness, 0, src_frame.width, border_thickness))
    c_bl = src_frame.crop((0, src_frame.height - border_thickness, border_thickness, src_frame.height))
    c_br = src_frame.crop((src_frame.width - border_thickness, src_frame.height - border_thickness, src_frame.width, src_frame.height))
    
    # Edges (we take a slice that we will repeat or stretch)
    e_t = src_frame.crop((border_thickness, 0, src_frame.width - border_thickness, border_thickness))
    e_b = src_frame.crop((border_thickness, src_frame.height - border_thickness, src_frame.width - border_thickness, src_frame.height))
    e_l = src_frame.crop((0, border_thickness, border_thickness, src_frame.height - border_thickness))
    e_r = src_frame.crop((src_frame.width - border_thickness, border_thickness, src_frame.width, src_frame.height - border_thickness))

    # Painting dimensions and dynamic sizing
    # 1cm ~ 20.5px (Assuming frame height is ~50cm)
    margin_px = int(margin_cm * 20.5)
    
    # Inner hole size based on painting + margin
    inner_w = painting.width + (2 * margin_px)
    inner_h = painting.height + (2 * margin_px)
    
    # Total new frame size
    total_w = inner_w + (2 * border_thickness)
    total_h = inner_h + (2 * border_thickness)
    
    # Reconstruct new frame
    new_frame = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 0))
    
    # Corners
    new_frame.paste(c_tl, (0, 0))
    new_frame.paste(c_tr, (total_w - border_thickness, 0))
    new_frame.paste(c_bl, (0, total_h - border_thickness))
    new_frame.paste(c_br, (total_w - border_thickness, total_h - border_thickness))
    
    # Stretch Edges
    new_frame.paste(e_t.resize((total_w - 2 * border_thickness, border_thickness)), (border_thickness, 0))
    new_frame.paste(e_b.resize((total_w - 2 * border_thickness, border_thickness)), (border_thickness, total_h - border_thickness))
    new_frame.paste(e_l.resize((border_thickness, total_h - 2 * border_thickness)), (0, border_thickness))
    new_frame.paste(e_r.resize((border_thickness, total_h - 2 * border_thickness)), (total_w - border_thickness, border_thickness))
    
    # Create white passepartout
    passepartout = Image.new("RGBA", (inner_w, inner_h), (255, 255, 255, 255))
    
    # Center painting
    paste_x = margin_px
    paste_y = margin_px
    
    # Subtle shadow for the painting
    shadow = Image.new("RGBA", painting.size, (0, 0, 0, 80))
    shadow = ImageOps.expand(shadow, border=6, fill=(0,0,0,0))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
    
    passepartout.paste(shadow, (paste_x - 6, paste_y - 6), shadow)
    passepartout.paste(painting, (paste_x, paste_y), painting)
    
    # Add inner shadow to passepartout hole for realism
    # (Simplified inner shadow using border lines)
    # passepartout = ImageOps.expand(passepartout, border=1, fill=(200, 200, 200, 255))
    
    # Combine frame and passepartout
    new_frame.paste(passepartout, (border_thickness, border_thickness), passepartout)
    
    # Final cleanup (convert to RGB)
    final_img = new_frame.convert("RGB")
    final_img.save(output_path, "JPEG", quality=95)
    print(f"✅ Dynamic mockup saved to: {output_path} (Size: {total_w}x{total_h})")

if __name__ == "__main__":
    FRAME_IMG = r"C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg"
    # Testing with a different aspect ratio image if possible
    PAINTING_IMG = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\28ESPATAC\El Parque Nacional de Zhāngjiājiè.png"
    OUTPUT_FILE = r"C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\dynamic_mockup.jpg"
    
    create_dynamic_mockup(FRAME_IMG, PAINTING_IMG, OUTPUT_FILE)
