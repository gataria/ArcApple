# A quick script for converting a folder of greyscale images to binary images, using the simple binary threshold method found in the OpenCV python library.
import cv2 as cv
import sys
from pathlib import Path

# check the number of parameters
if len(sys.argv) < 4:
    sys.exit("Wrong number of parameters. Usage: threshold_images.py <path to your source folder of images> <path to your destination image folder> <file extension of your images>")

# get path to the input folder
input_folder = Path(sys.argv[1])

# get path to the output folder
output_folder = Path(sys.argv[2])

# get desired extension
file_ext = sys.argv[3]

# check if path exists
if not input_folder.exists():
    sys.exit("Nonexistent input folder. Check the path and try again.")

# check if path exists
if not output_folder.exists():
    sys.exit("Nonexistent output folder. Check the path and try again.")

# check if i/o paths are folders
if not input_folder.is_dir():
    sys.exit("You gave an input file, not an input folder. Use a folder as your argument and try again.")

if not output_folder.is_dir():
    sys.exit("You gave an output file, not an output folder. Use a folder as your argument and try again.")

# get list of image files in the folder
input_file_list = list(input_folder.glob("*." + file_ext))

# iterate through all files
for in_file in input_file_list:
    img = cv.imread(in_file.__str__(), cv.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    cv.imwrite(output_folder.__str__() + r"\\" + in_file.name, thresh1)

