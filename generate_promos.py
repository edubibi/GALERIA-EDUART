import os
import random
from moviepy import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# Config
OUTPUT_DIR = "promos"
ASSETS_DIR = "assets"
AUDIO_FILE = os.path.join(ASSETS_DIR, "music.mp3") 
DURATION = 15 # Increased duration
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 24
IMAGES_PER_VIDEO = 5 # Number of images to show in the slideshow

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Styles to exclude
EXCLUDE_DIRS = ["bg", "icons", "css", "js", "img", ".git", "PORTADILLAS_ESTILOS", "recovered_wix"]

def create_text_image(text, width, height):
    """Creates a transparent PNG with text using Pillow."""
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Fonts
    try:
        font_name = "arial.ttf"
        font = ImageFont.truetype(font_name, 100)
        h_font = ImageFont.truetype(font_name, 60)
        sub_font = ImageFont.truetype(font_name, 40)
    except:
        font = ImageFont.load_default()
        h_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    # 1. Main Title (Bottom Center)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    x = (width - text_w) // 2
    y = height - 400
    
    # Shadow & Text
    draw.text((x+4, y+4), text, font=font, fill=(0, 0, 0, 180))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    # 2. Header (Top Center)
    header = "De mi nueva colección"
    h_bbox = draw.textbbox((0, 0), header, font=h_font)
    h_x = (width - (h_bbox[2] - h_bbox[0])) // 2
    h_y = 150
    
    draw.text((h_x+3, h_y+3), header, font=h_font, fill=(0, 0, 0, 180))
    draw.text((h_x, h_y), header, font=h_font, fill=(255, 255, 255, 255))
    
    # 3. Footer (Url)
    sub = "dudeduart.es"
    sub_bbox = draw.textbbox((0, 0), sub, font=sub_font)
    sub_x = (width - (sub_bbox[2] - sub_bbox[0])) // 2
    draw.text((sub_x, y + 140), sub, font=sub_font, fill=(200, 200, 200, 255))

    return np.array(img)

def process_image_for_video(img_path):
    """Loads image, creates blurred bg and centered fg, returns composite numpy array."""
    try:
        pil_img = Image.open(img_path).convert('RGB')
        
        # Background (Blur)
        bg = pil_img.resize((int(VIDEO_HEIGHT * pil_img.width / pil_img.height), VIDEO_HEIGHT))
        bg = bg.crop(((bg.width - VIDEO_WIDTH)//2, 0, (bg.width + VIDEO_WIDTH)//2, VIDEO_HEIGHT))
        bg = bg.filter(ImageFilter.GaussianBlur(radius=20))
        
        # Foreground (Fit Width)
        target_width = int(VIDEO_WIDTH * 0.95)
        ratio = target_width / pil_img.width
        target_height = int(pil_img.height * ratio)
        fg = pil_img.resize((target_width, target_height))
        
        # Composite on black canvas to avoid size mismatch if fg is weird
        final_frame = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), (0,0,0))
        final_frame.paste(bg, (0,0))
        
        fg_x = (VIDEO_WIDTH - target_width) // 2
        fg_y = (VIDEO_HEIGHT - target_height) // 2
        final_frame.paste(fg, (fg_x, fg_y))
        
        return np.array(final_frame)
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return None

def make_promo(style_name, image_paths):
    print(f"🎬 Creating SLIDESHOW for: {style_name} ({len(image_paths)} images)")
    
    clips = []
    # Calculate duration per slide logic
    # Crossfade takes time from both clips, so we need overlap.
    # Total time = (ClipDuration * N) - (TransitionTime * (N-1))
    # Let's target approx DURATION.
    
    transition_time = 1.0
    slide_duration = (DURATION / len(image_paths)) + transition_time
    
    for img_path in image_paths:
        img_array = process_image_for_video(img_path)
        if img_array is not None:
            # Zoom effect
            clip = ImageClip(img_array).with_duration(slide_duration)
            
            # Simple Zoom (using reliable resize method for moviepy 2.0 / or fallback)
            # vfx.Resize is tricky in some versions, sticking to static zoom or simple pan if possible.
            # Let's do a simple center crop zoom simulation or just static for stability first, then zoom.
            # Using scroll is safer:
            # clip = clip.with_effects([vfx.Scroll(x_speed=0, y_speed=10)])
            # Let's keep it static but with crossfade for now to ensure stability.
            
            clips.append(clip)
            
    if not clips:
        return

    # Concatenate with Crossfade
    # moviepy 1.x vs 2.x discrepancies. 
    # Using simple concatenate_videoclips first.
    # To do crossfade, we need CompositeVideoClip logic or use transition=
    
    # Manual Crossfade Composition
    final_clips = [clips[0]]
    for i in range(1, len(clips)):
        # Overlap previous
        final_clips.append(clips[i].with_start(final_clips[-1].end - transition_time).with_effects([vfx.CrossFadeIn(transition_time)]))
        
    # Ideally standard concat with padding
    video = CompositeVideoClip(final_clips)
    
    # Trim to exact duration requested
    video = video.subclipped(0, DURATION)

    # 4. Text Overlay (Static on top of slideshow)
    txt_array = create_text_image(style_name.replace("_", " "), VIDEO_WIDTH, VIDEO_HEIGHT)
    txt_clip = ImageClip(txt_array).with_duration(DURATION)
    
    final = CompositeVideoClip([video, txt_clip])

    # 6. Audio
    if os.path.exists(AUDIO_FILE):
        try:
            audio = AudioFileClip(AUDIO_FILE)
            # Loop audio manually to avoid version issues
            if audio.duration < DURATION:
                n_loops = int(DURATION / audio.duration) + 2
                audio = concatenate_audioclips([audio] * n_loops)
            
            # Trim to duration
            audio = audio.subclipped(0, DURATION)
            
            # Fade out audio
            audio = audio.with_effects([afx.AudioFadeOut(1.0)])
            final = final.with_audio(audio)
        except Exception as e:
            print(f"⚠️ Audio error: {e}")

    # 7. Export
    output_path = os.path.join(OUTPUT_DIR, f"{style_name}.mp4")
    final.write_videofile(output_path, fps=FPS, codec='libx264', audio=True, preset='ultrafast')
    print(f"✅ Saved: {output_path}")

# Main execution
if __name__ == "__main__":
    count = 0
    dirs = [d for d in os.listdir(ASSETS_DIR) if os.path.isdir(os.path.join(ASSETS_DIR, d)) and d not in EXCLUDE_DIRS]
    dirs.sort()

    for style in dirs:
        style_path = os.path.join(ASSETS_DIR, style)
        
        # Gather all images
        images = []
        for f in os.listdir(style_path):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                images.append(os.path.join(style_path, f))
        
        if images:
            # Shuffle and pick N
            random.shuffle(images)
            selected = images[:IMAGES_PER_VIDEO]
            make_promo(style, selected)
            count += 1
    
    if count == 0:
        print("⚠️ No styles processed.")
