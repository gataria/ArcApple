# ArcApple!!
A project for coloring an ArcGIS feature layer based on a raster layer.
## My journey in creating the Bad Apple!! video
1. Created a copy of the Block_Group TIGER shapefile (from the [*National Sub-State Geography Geodatabase* data product](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-geodatabase-file.2023.html), which only contains Census block groups for the contiguous United States.
   1. This entailed the removal of blocks outside the contiguous U.S. and the removal of blocks where `ALAND = 0` (i.e., blocks with only water bodies)
   2. My final census block group layer was then exported using the "Export Features" geoprocessing tool, which exported the layer into its own geodatabase.
2. Spatially reference [every frame of the Bad Apple!! music video](https://archive.org/details/bad_apple_is.7z) using [world files](https://gavinr.com/georeference-image-extent-arcgis-pro/).
   1. This entailed the calculation of geometry attributes for the most northwest, northeast, southwest, and southeast Census block groups in the contiguous U.S. -- specifically, the "Minimum" and "Maximum x/y-coordinate" attributes, specified in the Calculate Geometry Attributes geoprocessing tool.
   2. The min/max x/y coordinates in the contiguous U.S. were found to be the following, according to the Census block group boundaries:
         ```
         XMAX = -66.925986
         XMIN = -124.772692
         YMAX = 49.384479
         YMIN = 24.476981
         ```
   3. These coordinate values were then used for the following world file:
         ```
         0.04017132361
         0
         0
         -0.02306249815
         -124.772692
         49.384479
         ```
   4. This world file was then duplicated for the entire Bad Apple!! frame dataset (i.e., that text was written out to files with `bad_apple_(X)XXX.pngw` filenames).
      1. This was performed using the Python script `write_world_files.py`, found under `scripts/`.
3. Use a strategy such as creating a [tile index](https://gis.stackexchange.com/questions/229133/how-to-select-the-polygons-based-on-a-raster) to select and color specific polygons by location/overlap with the tiles.
   1. We could use the "Raster to Vector" geoprocessing tool -- however, we need to prepare the images first.