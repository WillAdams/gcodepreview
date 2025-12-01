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
nozzlediameter = 0.4
filamentdiameter = 1.75
extrusionwidth = 0.6
layerheight = 0.2
temperature =200

gcp = gcodepreview("print", # "cut" or "no_preview"
                   generategcode,
                   generatedxf,
                   )

gcp.opengcodefile(Base_filename)

gcp.initializeforprinting(nozzlediameter,
                          filamentdiameter,
                          extrusionwidth,
                          layerheight)

gcp.setandwaitforextrudertemperature(temperature)
gcp.liftandprimenozzle()

gcp.moveatfeedrate(3.752, 3.756, layerheight, 20000)

gcp.extrude(253.37, 253.389, layerheight) # E should be 12.49134

gcp.stockandtoolpaths("toolpaths")

gcp.closegcodefile()

