from PIL import Image

def find_wood_edges():
    img = Image.open(r'C:\Users\Usuario\.gemini\antigravity\brain\9d38d049-e5ca-4fcd-b253-599a2b2b6dac\uploaded_media_1770399800013.jpg')
    w, h = img.size
    
    def is_white(p):
        return p[0] > 230 and p[1] > 230 and p[2] > 230

    # Scan Top
    top_edge = 0
    for y in range(h):
        if is_white(img.getpixel((w//2, y))):
            top_edge = y
            break
    
    # Scan Bottom
    bottom_edge = 0
    for y in range(h):
        if is_white(img.getpixel((w//2, h-1-y))):
            bottom_edge = y
            break
            
    # Scan Left
    left_edge = 0
    for x in range(w):
        if is_white(img.getpixel((x, h//2))):
            left_edge = x
            break
            
    # Scan Right
    right_edge = 0
    for x in range(w):
        if is_white(img.getpixel((w-1-x, h//2))):
            right_edge = x
            break
            
    print(f"WOOD_EDGES: T={top_edge}, B={bottom_edge}, L={left_edge}, R={right_edge}")

if __name__ == "__main__":
    find_wood_edges()
