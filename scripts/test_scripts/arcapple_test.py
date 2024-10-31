import arcpy
import multiprocessing as mp
from pathlib import Path

# load in project to aprx
aprx = arcpy.mp.ArcGISProject(r"C:\Users\rodri\OneDrive\Development\ArcApple\arcgis\arcgis.aprx")

# process a list of images, and use the aprx project's layout to create output images
def process_image(image_file):
    print("Processing", str(image_file), flush=True)
    # retrieve map to place image on
    map = aprx.listMaps()[0]
    # retrieve layout
    layout = aprx.listLayouts()[0]
    # create layer object from image path
    raster_layer_result = arcpy.management.MakeRasterLayer(image_file)
    # add the layer to the map
    map_layer_result = map.addLayer(raster_layer_result[0])
    # style the layer
    # sym = map_layer.symbology
    # sym.renderer.symbol.color = {"RGB": [0, 0, 0, 255]}
    # map_layer.symbology = sym
    # export the layout to given output path
    output_path = Path(r"C:\Users\rodri\OneDrive\Development\ArcApple\files\bad_apple_is\image_sequence\test_frames\output") / Path(image_file).name
    print(str(output_path))
    layout.exportToPNG(str(output_path), resolution=72)
    # remove layer before returning
    map.removeLayer(map_layer_result[0])


if __name__ == '__main__':
    # get folder of images/world files; define file extension
    images_folder = Path(r"C:\Users\rodri\OneDrive\Development\ArcApple\files\bad_apple_is\image_sequence\test_frames")
    file_ext = "png"
    # construct images list
    images_file_list = [str(image_path) for image_path in images_folder.glob("*." + file_ext)]
    # start workers, equal to the number of CPU cores
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Map to run all processes
        pool.map(process_image, images_file_list)
    # for image in images_file_list:
    #     process_image(image)