from PIL import Image
import os

def extract_samples():
    img = Image.open(r'C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg')
    w, h = img.size
    
    # Let's extract specific parts to show the user
    # 1. Top left corner (wood)
    corner = img.crop((0, 0, 100, 100))
    corner.save(r'c:\Users\Usuario\AppData\Local\Temp\corner_test.png')
    
    # 2. A strip of "pure wood" from the top edge
    # Based on previous analysis, wood ends around y=22
    wood_strip = img.crop((w//2 - 50, 0, w//2 + 50, 22))
    wood_strip.save(r'c:\Users\Usuario\AppData\Local\Temp\wood_strip.png')
    
    print(f"Top-Left corner wood pixels (y=10):")
    for x in range(30):
        print(f"x={x}: {img.getpixel((x, 10))}")

if __name__ == "__main__":
    extract_samples()
