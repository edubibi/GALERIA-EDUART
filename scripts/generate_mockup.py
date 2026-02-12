import os
from PIL import Image, ImageOps, ImageFilter

def create_mockup(frame_path, painting_path, output_path, margin_cm=3):
    print(f"🖼️  Creating mockup: {painting_path} in {frame_path}")
    
    # Load images
    frame = Image.open(frame_path).convert("RGBA")
    painting = Image.open(painting_path).convert("RGBA")
    
    frame_w, frame_h = frame.size
    
    # Based on analysis: Wooden border is from ~21px to ~694px (width)
    # The A4 hole is centered.
    a4_ratio = 210 / 297
    
    # We'll make the A4 hole take about 65% of the total frame height to leave room for the passepartout
    target_h = int(frame_h * 0.65)
    target_w = int(target_h * a4_ratio)
    
    hole_box = (
        (frame_w - target_w) // 2,
        (frame_h - target_h) // 2,
        (frame_w + target_w) // 2,
        (frame_h + target_h) // 2
    )
    
    hole_w = hole_box[2] - hole_box[0]
    hole_h = hole_box[3] - hole_box[1]
    
    # 3cm margin calculation:
    # If frame_h (1024) is roughly 50cm in real life: 1cm ~ 20.5px.
    # 3cm ~ 62px.
    margin_px = 62 
    
    # Available area for painting inside the A4 window
    # The painting occupies the inner part, leaving the 3cm white margin of the passepartout inside the A4?
    # No, usually the 3cm margin IS the passepartout.
    # User said: "dejar el margen de 3 cm del paspartú blanco".
    # This means the painting should be smaller than the hole by 3cm on each side.
    
    available_w = hole_w - (2 * margin_px)
    available_h = hole_h - (2 * margin_px)
    
    # Resize painting to fit
    painting.thumbnail((available_w, available_h), Image.Resampling.LANCZOS)
    
    # Create white area for the hole
    draw_area = Image.new("RGBA", (hole_w, hole_h), (255, 255, 255, 255))
    
    # Center painting in the hole
    paste_x = (hole_w - painting.width) // 2
    paste_y = (hole_h - painting.height) // 2
    
    # Subtle shadow for the painting
    shadow = Image.new("RGBA", painting.size, (0, 0, 0, 80))
    shadow = ImageOps.expand(shadow, border=6, fill=(0,0,0,0))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
    
    draw_area.paste(shadow, (paste_x - 6, paste_y - 6), shadow)
    draw_area.paste(painting, (paste_x, paste_y), painting)
    
    # Optional: Draw a very subtle inner shadow on the hole edges for realism
    # But let's keep it simple for now.
    
    # Composite onto frame
    frame.paste(draw_area, (hole_box[0], hole_box[1]), draw_area)
    
    # Save result
    frame.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Mockup saved to: {output_path}")

if __name__ == "__main__":
    FRAME_IMG = r"C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg"
    # Testing with ESPATAC series as requested
    PAINTING_IMG = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\28ESPATAC\arando con bueyes.png"
    OUTPUT_FILE = r"C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\mockup_test.jpg"
    
    create_mockup(FRAME_IMG, PAINTING_IMG, OUTPUT_FILE)
