import os
import sys
from pathlib import Path

# check the number of parameters
if len(sys.argv) < 3:
    sys.exit("Wrong number of parameters. Usage: write_world_files.py <path to your folder of images> <file extension of your images>")

# specify the output to write to the world files
file_output = """0.04017132361
0
0
-0.02306249815
-124.772692
49.384479
"""

# get path to the given folder
filename = Path(sys.argv[1])

# get desired extension
file_ext = sys.argv[2]

# check if path exists
if not filename.exists():
    sys.exit("Nonexistent folder. Check the path and try again.")

# check if path is a folder
if not filename.is_dir():
    sys.exit("You gave a file, not a folder. Use a folder as your argument and try again.")

# get list of image files in the folder
file_list = list(filename.glob("*." + file_ext))

# iterate through all files
for file in file_list:
    world_file_path = str(file) + "w"

    # write contents of file_output to current world_file with the path world_file_path
    # this uses exclusive mode to prevent overwriting to existing files
    try:
        with open(world_file_path, mode="x") as world_file:
            world_file.write(file_output)
    except FileExistsError:
        print(world_file_path + " already exists. Moving onto the next file.")
        continue
