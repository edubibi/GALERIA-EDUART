from PIL import Image

def create_wood_texture():
    img = Image.open(r'C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg')
    # Let's take a patch of wood that is definitely NOT white.
    # From top edge: x=100-150, y=5-15
    wood_patch = img.crop((100, 5, 150, 15))
    
    # Let's average it or just use it as a pattern
    wood_patch = wood_patch.resize((50, 50), Image.Resampling.LANCZOS)
    wood_patch.save(r'c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\wood_test.png')
    
    # Create a simple 9-slice preview (150x150)
    canvas = Image.new("RGBA", (150, 150), (255, 255, 255, 255))
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1: continue # hole
            canvas.paste(wood_patch, (i*50, j*50))
    canvas.save(r'c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets\wood_preview.png')

if __name__ == "__main__":
    create_wood_texture()
