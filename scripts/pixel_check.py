from PIL import Image

def manual_check():
    img = Image.open(r'C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg')
    print(f"Size: {img.size}")
    
    # Check a 50x50 block at the top left
    for y in range(50):
        row_colors = []
        for x in range(50):
            p = img.getpixel((x, y))
            # Rough wood colors: R~210, G~180, B~140
            # Rough white colors: R>240, G>240, B>240
            if p[0] > 240 and p[1] > 240 and p[2] > 240:
                row_colors.append(".") # White
            elif p[0] > 180 and p[1] > 150:
                row_colors.append("W") # Wood?
            else:
                row_colors.append("?") # Other
        print(f"{y:02d}: {''.join(row_colors)}")

if __name__ == "__main__":
    manual_check()
