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
    # # SelectLayerByLocation to fetch block groups by their proximity to the boundaries in the bad apple polygon
    # selected_block_groups = arcpy.management.SelectLayerByLocation(
    #     in_layer="ContiguousUnitedStates",
    #     overlap_type="WITHIN",
    #     select_features=out_polygon,
    #     search_distance=None,
    #     selection_type="NEW_SELECTION",
    #     invert_spatial_relationship="NOT_INVERT"
    # )
    # # Make a feature layer out of these block groups inside the resulting geodatabase
    # out_layer = out_polygon + "_selection"
    # obj_ids = arcpy.Describe(selected_block_groups).FIDSet
    # obj_ids_sql = "OBJECTID IN ({})".format(obj_ids.replace("; ", ","))
    # arcpy.management.MakeFeatureLayer(
    #     in_features=selected_block_groups,
    #     out_layer=out_layer,
    #     where_clause=obj_ids_sql
    # )

    # == WHAT I USED IN TESTING ==
    # arcpy.management.SelectLayerByAttribute(
    #     in_layer_or_view="bad_apple_100",
    #     selection_type="NEW_SELECTION",
    #     where_clause="gridcode = 0",
    #     invert_where_clause=None
    # )
    # selected_block_groups = arcpy.management.SelectLayerByLocation(
    #     in_layer="ContiguousUnitedStates",
    #     overlap_type="HAVE_THEIR_CENTER_IN",
    #     select_features="bad_apple_100",
    #     search_distance=None,
    #     selection_type="NEW_SELECTION",
    #     invert_spatial_relationship="NOT_INVERT"
    # )
    # out_layer = "bad_apple_100" + "_selection"
    # obj_ids = arcpy.Describe(selected_block_groups).FIDSet
    # obj_ids_sql = "OBJECTID IN ({})".format(obj_ids.replace("; ", ","))
    # arcpy.management.MakeFeatureLayer(
    #     in_features=selected_block_groups,
    #     out_layer=out_layer,
    #     where_clause=obj_ids_sql
    # )


if __name__ == '__main__':
    # get folder of images/world files; define file extension
    images_folder = Path(r"C:\Users\rodri\OneDrive\Development\ArcApple\files\bad_apple_is\image_sequence\binary")
    images_file_ext = "png"
    # construct images list w/ reference to US layer
    images_file_list = images_folder.glob("*." + images_file_ext)
    # go through each image -- writing to a fGDB with multiple processes is messy
    for image in images_file_list:
        process_image(image)