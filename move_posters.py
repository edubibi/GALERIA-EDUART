import os
import shutil

def move_posters(source_root, target_root):
    """
    Moves files with '_POSTER' in their name from source_root to target_root,
    preserving the directory structure.
    """
    if not os.path.exists(source_root):
        print(f"Error: Source directory '{source_root}' does not exist.")
        return

    print(f"Starting migration from '{source_root}' to '{target_root}'...")
    
    moved_count = 0
    errors = 0

    for root, dirs, files in os.walk(source_root):
        for file in files:
            if "_POSTER" in file:
                source_path = os.path.join(root, file)
                
                # Calculate relative path to maintain structure
                rel_path = os.path.relpath(root, source_root)
                target_dir = os.path.join(target_root, rel_path)
                
                target_path = os.path.join(target_dir, file)
                
                try:
                    # Create target directory if it doesn't exist
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # Move the file
                    shutil.move(source_path, target_path)
                    print(f"Moved: {file} -> {target_dir}")
                    moved_count += 1
                except Exception as e:
                    print(f"FAILED to move {file}: {e}")
                    errors += 1

    print(f"\nMigration Complete.")
    print(f"Total files moved: {moved_count}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    base_dir = os.getcwd()
    assets_dir = os.path.join(base_dir, "assets")
    assets_poster_dir = os.path.join(base_dir, "assets_poster")
    
    move_posters(assets_dir, assets_poster_dir)
