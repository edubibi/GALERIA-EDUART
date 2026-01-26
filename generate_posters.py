import os
import argparse
from PIL import Image, ImageOps
import sys

def add_passepartout(input_dir, output_dir, border_percent=0.035):
    """
    Reads images from input_dir, adds a white border, and saves them to output_dir.
    Appends _POSTER to the filename.
    """
    print(f"🚀 Processing: {input_dir} -> {output_dir}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    count = 0
    errors = 0
    skipped = 0

    # Walk through input directory
    for root, dirs, files in os.walk(input_dir):
        # Determine relative path to maintain structure if needed in future
        # For now, we flatten or just process the specific folder asked
        
        for file in files:
            if file.lower().endswith(image_extensions):
                # Skip if it's already a poster (just in case)
                if("_POSTER" in file):
                    continue

                full_path = os.path.join(root, file)
                
                try:
                    img = Image.open(full_path)
                    
                    # Calculate border
                    short_side = min(img.size)
                    if short_side < 200:
                        skipped += 1
                        continue

                    border_px = int(short_side * border_percent)
                    
                    # Add border
                    poster_img = ImageOps.expand(img, border=border_px, fill='white')
                    
                    # Construct output filename
                    filename_base, ext = os.path.splitext(file)
                    output_filename = f"{filename_base}_POSTER{ext}"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    # Save
                    save_args = {'quality': 95}
                    icc = img.info.get('icc_profile')
                    if icc:
                        save_args['icc_profile'] = icc
                    
                    poster_img.save(output_path, **save_args)
                    print(f"✅ Created: {output_filename}")
                    count += 1
                    
                except Exception as e:
                    print(f"❌ FAILED: {file} - {e}")
                    errors += 1

    print(f"\n✨ Completed for {os.path.basename(input_dir)}")
    print(f"   Created: {count}")
    print(f"   Skipped: {skipped}")
    print(f"   Errors:  {errors}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add white passepartout to images.")
    parser.add_argument("--input", required=True, help="Input directory containing images")
    parser.add_argument("--output", required=True, help="Output directory for poster images")
    
    args = parser.parse_args()
    
    add_passepartout(args.input, args.output)
