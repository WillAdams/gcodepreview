#gcpthreedp.py --- Template for 3D printing
#                  Initial version.
#!/usr/bin/env python

import sys

try:
    if 'gcodepreview' in sys.modules:
        del sys.modules['gcodepreview']
except AttributeError:
    pass

from gcodepreview import *

fa = 2
fs = 0.125

# [Export] */
Base_filename = "aexport"
# [Export] */
generatedxf = False
# [Export] */
generategcode = True
# [3D Printing] */
printer_name = 'prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0
# [3D Printing] */
nozzlediameter = 0.4
# [3D Printing] */
filamentdiameter = 1.75
# [3D Printing] */
extrusionwidth = 0.6
# [3D Printing] */
layerheight = 0.2
# [3D Printing] */
extruder_temperature =200
# [3D Printing] */
bed_temperature = 60

gcp = gcodepreview("print", # "cut" or "no_preview"
                   generategcode,
                   generatedxf,
                   )

gcp.initializeforprinting(nozzlediameter,
                          filamentdiameter,
                          extrusionwidth,
                          layerheight,
                          "absolute",
                          extruder_temperature,
                          bed_temperature,
                          printer_name,
                          Base_filename)

gcp.extrude(9, 18, layerheight)

gcp.rapid(125, 125, layerheight)
gcp.extrude(150, 125, layerheight)
gcp.extrude(150, 150, layerheight)
gcp.extrude(125, 150, layerheight)
gcp.extrude(125, 125, layerheight)

gcp.stockandtoolpaths("toolpaths")

gcp.shutdownafterprinting()

