import os
import subprocess

folders = [
    "00EDUSSE", "15CUBESSEPLUS", "16EXPNEO", "18ABSTRACTO_CONFLUENCIA", 
    "19FUZZLINE_ABS", "23TRIDIM-BURST", "25CAPLIVE", "26CARL_LINE", 
    "27LINEVORT", "28ESPATAC", "29ESPATAC-MAT", "30OLONATUR-COLOR", 
    "31OLENATUR", "33MINIGESTPOETIC", "34EXPTERICO", "35PAPERCHIN"
]

for folder in folders:
    input_dir = f"assets/{folder}"
    output_dir = f"assets_poster/{folder}"
    print(f"--- Processing {folder} ---")
    if os.path.exists(input_dir):
        # Call generate_posters.py as a script
        subprocess.run(["py", "generate_posters.py", "--input", input_dir, "--output", output_dir])
    else:
        print(f"Directory {input_dir} not found, skipping.")

print("All poster generation tasks completed.")
