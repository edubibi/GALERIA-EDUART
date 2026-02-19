import re
import json
import os

data_path = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\js\data.js"
assets_path = r"c:\Users\Usuario\.gemini\antigravity\scratch\photo_catalog_portable\assets"

with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

styles = {}

# Regex to find artwork objects
artwork_pattern = re.compile(r"\{[^{}]*?\"category\":\s*\"([^\"]+)\"[^{}]*?\"description\":\s*\"([^\"]+)\"[^{}]*?\}", re.DOTALL)

matches = artwork_pattern.findall(content)

for category, description in matches:
    # Clean up category name (remove ' stilo' etc if needed, but keeping exact for now to match)
    if category not in styles:
        styles[category] = description
    else:
        # Keep the longest description as it might be more detailed
        if len(description) > len(styles[category]):
            styles[category] = description

# Also check directories in assets to find any missing ones
missing_styles = []
for item in os.listdir(assets_path):
    if os.path.isdir(os.path.join(assets_path, item)):
        # Check if it looks like a style (starts with digits)
        if re.match(r"^\d{2}", item):
            # Check if this exact directory name is in styles keys
            # or if it matches a key with suffix
            found = False
            for key in styles.keys():
                if key.startswith(item) or item.startswith(key.split(" ")[0]):
                    found = True
                    break
            if not found:
                missing_styles.append(item)

print("FOUND STYLES IN DATA:")
for style in sorted(styles.keys()):
    print(f"{style}|{styles[style][:100]}...") # Print first 100 chars

print("\nSTYLES IN ASSETS BUT NOT IN DATA:")
for style in missing_styles:
    print(style)
