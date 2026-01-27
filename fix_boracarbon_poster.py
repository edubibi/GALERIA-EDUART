import os
from PIL import Image, ImageOps

def fix_poster():
    input_path = os.path.join("assets", "08BORACARBON", "08boracarbon_004.png")
    output_dir = os.path.join("assets_poster", "08BORACARBON")
    output_path = os.path.join(output_dir, "08boracarbon_004_POSTER.png")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Reading: {input_path}")
    img = Image.open(input_path)
    
    # Force convert to RGB to drop weird modes or profiles
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    # Calculate border
    border_percent = 0.035
    short_side = min(img.size)
    border_px = int(short_side * border_percent)
    
    print(f"Adding border: {border_px}px")
    poster_img = ImageOps.expand(img, border=border_px, fill='white')
    
    # Save without ICC profile to be safe for mobile
    print(f"Saving to: {output_path}")
    poster_img.save(output_path, format="PNG", optimize=True)
    print("Done.")

if __name__ == "__main__":
    fix_poster()
