from PIL import Image

def inspect_top():
    img = Image.open(r'C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg')
    w, h = img.size
    print("--- TOP EDGE ---")
    for y in range(60):
        p = img.getpixel((w//2, y))
        print(f"y={y}: {p}")

if __name__ == "__main__":
    inspect_top()
