import json
import os

def count_artworks():
    try:
        with open('metadata.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return

    stats = {}
    total_items = 0
    total_artworks = 0

    excluded_categories = ['bg', 'General', 'contact_header']

    for key, item in data.items():
        if not isinstance(item, dict):
            continue
            
        total_items += 1
        cat = item.get('category', 'Unknown')
        
        stats[cat] = stats.get(cat, 0) + 1
        
        if cat not in excluded_categories:
            total_artworks += 1

    print("\n--- Summary ---")
    print(f"Total entries in DB: {total_items}")
    print(f"Total ARTWORKS (excluding bg/General): {total_artworks}")

    print(f"--- Breakdown ---")
    for cat, count in sorted(stats.items()):
        print(f"{cat}: {count}")

if __name__ == "__main__":
    count_artworks()
