import arcpy
from pathlib import Path

# Load results geodatabase; this should already have ContinuousUnitedStates in it
workspace = r"C:\Users\rodri\OneDrive\Development\ArcApple\files\polygon_frames.gdb"
arcpy.env.workspace = workspace

# process a list of images, and use the aprx project's layout to create output images
def process_image(image_file_path):
    print("Processing", image_file_path, flush=True)
    # Define output name
    out_polygon = image_file_path.stem
    # Use the RasterToPolygon arcpy conversion to convert each image to a polygon; named w/o png file extension
    arcpy.conversion.RasterToPolygon(
        in_raster=str(image_file_path),
        out_polygon_features=out_polygon,
        simplify="SIMPLIFY",
        raster_field="Value",
        create_multipart_features="SINGLE_OUTER_PART",
        max_vertices_per_feature=None
    )


if __name__ == '__main__':
    # get folder of images/world files; define file extension
    images_folder = Path(r"C:\Users\rodri\OneDrive\Development\ArcApple\files\bad_apple_is\image_sequence\binary")
    images_file_ext = "png"
    # construct images list w/ reference to US layer
    images_file_list = images_folder.glob("*." + images_file_ext)
    # go through each image -- writing to a fGDB with multiple processes is messy
    for image in images_file_list:
        process_image(image)