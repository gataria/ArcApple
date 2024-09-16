import arcpy
from pathlib import Path
import time
import multiprocessing as mp

# Define the polygon frame geodatabase as the workspace
arcpy.env.workspace = r"C:\Users\rodri\OneDrive\Development\ArcApple\files\polygon_frames.gdb"
# Load in project to aprx
aprx = arcpy.mp.ArcGISProject(r"C:\Users\rodri\OneDrive\Development\ArcApple\arcgis\arcgis.aprx")
# Get US map
ba_map = aprx.listMaps()[0]
# Get print/output layout
ba_layout = aprx.listLayouts()[0]
# Get the ContiguousUnitedStates layer from on the map for selections
cont_us_layer = ba_map.listLayers("ContiguousUnitedStates")[0]

def create_frame(frame):
    # Print
    print("Creating frame", frame)
    # Execute process_frame
    process_frame(frame)
    # Get the path to that gdb with the selection feature class
    gdb_path = Path(r"C:\Users\rodri\OneDrive\Development\ArcApple\files\frame_gdbs") / (frame + ".gdb")
    # Delete the gdb once function returns
    if gdb_path.exists():
        arcpy.management.Delete(str(gdb_path))

def process_frame(frame):
    # Define name of temp layers and feature classes
    frame_layer = frame + "_frame_layer"
    final_layer = frame + "_final_layer"
    out_fc = frame + "_selection"
    # Make temp layer using shaded areas (where gridcode = 0 [black])
    arcpy.management.MakeFeatureLayer(
        in_features=frame,
        out_layer=frame_layer,
        where_clause="gridcode = 0",
    )
    # From the shaded areas layer, make a selection on the ContiguousUnitedStates layer
    arcpy.management.SelectLayerByLocation(
        in_layer=cont_us_layer,
        # overlap_type="WITHIN",
        overlap_type="HAVE_THEIR_CENTER_IN",
        select_features=frame_layer,
        search_distance=None,
        selection_type="NEW_SELECTION",
        invert_spatial_relationship="NOT_INVERT"
    )
    # delete generated frame_layer since we're not using it again
    arcpy.management.Delete(frame_layer)
    # copy over selection
    # Create a path for the fGDB
    gdb_path = Path(r"C:\Users\rodri\OneDrive\Development\ArcApple\files\frame_gdbs") / (frame + ".gdb")
    # create the gdb
    arcpy.management.CreateFileGDB(
        str(gdb_path.parent),
        (frame + ".gdb")
    )
    # change workspace
    arcpy.env.workspace = str(gdb_path)
    # copy selected features as a feature class to gdb
    arcpy.management.CopyFeatures(cont_us_layer, out_fc)
    # remove selection from contiguous US layer
    arcpy.management.SelectLayerByAttribute(cont_us_layer, "CLEAR_SELECTION")
    # Make a feature layer out of the selected US block groups
    final_layer_result = arcpy.management.MakeFeatureLayer(
        in_features=out_fc,
        out_layer=final_layer,
    )
    # Add the final selection layer to the map
    map_layer_result = ba_map.addLayer(final_layer_result[0])
    # Style the layer
    sym = map_layer_result[0].symbology
    sym.renderer.symbol.color = {"RGB": [0, 0, 0, 255]}
    sym.renderer.symbol.outlineWidth = 0.0
    map_layer_result[0].symbology = sym
    # Define output path
    output_path = Path(r"C:\Users\rodri\OneDrive\Development\ArcApple\files\bad_apple_is\image_sequence\test_frames\output_frames") / (frame + ".png")
    # Export
    ba_layout.exportToPNG(str(output_path), resolution=72)
    # Remove layer, delete it
    ba_map.removeLayer(map_layer_result[0])
    arcpy.management.Delete(final_layer)
    # Delete selection fc and reference
    arcpy.management.Delete(out_fc)
    del out_fc
    # Change back to the original workspace
    arcpy.env.workspace = r"C:\Users\rodri\OneDrive\Development\ArcApple\files\polygon_frames.gdb"

if __name__ == '__main__':
    # # Get bad apple frames for testing
    # ba_frame_list = [
    #                 "bad_apple_100",
    #                 "bad_apple_101",
    #                 "bad_apple_102",
    #                 "bad_apple_103",
    #                 "bad_apple_104",
    #                 "bad_apple_105",
    #                 "bad_apple_106",
    #                 "bad_apple_107",
    #                 "bad_apple_108",
    #                 "bad_apple_109",
    #                 "bad_apple_110",
    #                 "bad_apple_111",
    #                 "bad_apple_112",
    #                 "bad_apple_113",
    #                 "bad_apple_114",
    #                 "bad_apple_115",
    #                 "bad_apple_116",
    #                 "bad_apple_117",
    #                 "bad_apple_118",
    #                 "bad_apple_119",
    #                 "bad_apple_120",
    #             ]
    # # Get all Bad Apple frames
    ba_frame_list = arcpy.ListFeatureClasses("bad_apple*")
    # Send each frame to process
    start = time.time()
    # for ba_frame in ba_frame_list:
    #     create_frame(ba_frame)
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(create_frame, ba_frame_list)

    end = time.time()
    print(str(end - start), "s")
    print("avg:", str((end - start) / len(ba_frame_list)), "s / frame")