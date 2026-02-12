import os
from PIL import Image, ImageOps, ImageDraw

# Configurations
INPUT_DIR = "assets"
OUTPUT_DIR = "social_launch_pack"
MOCKUP_BASE_PATH = r"C:/Users/Usuario/.gemini/antigravity/brain/c084f937-408e-4a43-ae5b-7ba828675503/modern_living_room_wall_mockup_1769952181776.png"

# Assets to process
PROFILE_ART = "00edusse_003.png" # El Guardian
POST_ARTS = [
    "01exp_neocirc_017.jpg", # Catedral
    "23tridim_burst_004.png", # Trueno
    "28ESPATAC/aldea china.png" # Aldea China
]

# Create output dir
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def find_file(partial_path):
    # Walk to find exact path
    base_name = os.path.basename(partial_path)
    for root, dirs, files in os.walk(INPUT_DIR):
        if base_name in files:
            return os.path.join(root, base_name)
    return None

def create_profile_pic():
    print("Generating Profile Pic...")
    img_path = find_file(PROFILE_ART)
    if not img_path:
        print(f"Error: {PROFILE_ART} not found")
        return

    img = Image.open(img_path).convert("RGBA")
    
    # Square crop center
    width, height = img.size
    new_size = min(width, height)
    left = (width - new_size)/2
    top = (height - new_size)/2
    right = (width + new_size)/2
    bottom = (height + new_size)/2

    img = img.crop((left, top, right, bottom))
    img = img.resize((1080, 1080), Image.LANCZOS)

    # Circle mask
    mask = Image.new('L', (1080, 1080), 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0, 1080, 1080), fill=255)

    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    # Save as PNG
    output.save(f"{OUTPUT_DIR}/profile_pic_circle.png")
    
    # Save as JPG square (some platforms prefer square no transparency)
    bg = Image.new("RGB", output.size, (255, 255, 255))
    bg.paste(output, mask=output.split()[3])
    bg.save(f"{OUTPUT_DIR}/profile_pic_square.jpg", quality=95)
    print("Profile Pic Done.")

def create_insta_post(filename, name_suffix=""):
    print(f"Generating Post for {filename}...")
    img_path = find_file(filename)
    if not img_path:
        print(f"Error: {filename} not found")
        return

    img = Image.open(img_path).convert("RGB")
    
    # 1. Square Post (Fit with white padding or maximize?)
    # Let's do a "Fit in Square" with white border, very gallery style.
    
    base = Image.new("RGB", (1080, 1080), (255, 255, 255))
    
    # Resize img to fit in 900x900
    img.thumbnail((900, 900), Image.LANCZOS)
    
    # Center
    w, h = img.size
    x = (1080 - w) // 2
    y = (1080 - h) // 2
    
    base.paste(img, (x, y))
    
    out_name = os.path.basename(img_path).split('.')[0] + "_post.jpg"
    base.save(f"{OUTPUT_DIR}/{out_name}", quality=95)
    
    # 2. Detail Crop (Zoom) for carousel
    original_img = Image.open(img_path).convert("RGB")
    w, h = original_img.size
    min_dim = min(w, h)
    
    # Crop center-ish but zoomed
    crop_size = min_dim // 2
    left = (w - crop_size) // 2
    top = (h - crop_size) // 2
    
    detail = original_img.crop((left, top, left + crop_size, top + crop_size))
    detail = detail.resize((1080, 1080), Image.LANCZOS)
    
    out_name_detail = os.path.basename(img_path).split('.')[0] + "_detail.jpg"
    detail.save(f"{OUTPUT_DIR}/{out_name_detail}", quality=95)
    print("Posts Done.")
    return img_path

def create_mockup(artwork_filename):
    print(f"Generating Mockup for {artwork_filename}...")
    if not os.path.exists(MOCKUP_BASE_PATH):
        print("Error: Mockup base not found")
        return

    room = Image.open(MOCKUP_BASE_PATH).convert("RGBA")
    
    art_path = find_file(artwork_filename)
    if not art_path: return
    
    art = Image.open(art_path).convert("RGBA")
    
    # Calculate placement. 
    # Room is 1024x1024 (from generate_image default typically) or similar.
    # Let's assume wall center.
    rw, rh = room.size
    
    # Target size for art on wall (e.g. 40% of room width)
    target_width = int(rw * 0.45)
    
    # Resize art maintaining aspect ratio
    aw, ah = art.size
    ratio = ah / aw
    target_height = int(target_width * ratio)
    
    art_resized = art.resize((target_width, target_height), Image.LANCZOS)
    
    # Add shadow
    shadow_offset = 15
    from PIL import ImageFilter
    
    # Center position
    center_x = rw // 2
    center_y = int(rh * 0.45) # Slightly higher than center usually looks better for hanging art
    
    pos_x = center_x - (target_width // 2)
    pos_y = center_y - (target_height // 2)
    
    # Shadow layer
    shadow_layer = Image.new("RGBA", room.size, (0,0,0,0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_rect = [pos_x + 10, pos_y + 10, pos_x + target_width + 10, pos_y + target_height + 10]
    s_draw.rectangle(s_rect, fill=(0,0,0, 60))
    
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=15))
    
    room.alpha_composite(shadow_layer)
    room.paste(art_resized, (pos_x, pos_y), art_resized)
    
    out_name = os.path.basename(artwork_filename).split('.')[0] + "_mockup.png"
    room.save(f"{OUTPUT_DIR}/{out_name}")
    print("Mockup Done.")

if __name__ == "__main__":
    create_profile_pic()
    for art in POST_ARTS:
        create_insta_post(art)
        create_mockup(art)
    print("All tasks finished. Check 'social_launch_pack' folder.")
