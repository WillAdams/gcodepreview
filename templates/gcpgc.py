import sys

fn = 180

from openscad import *
#nimport("https://raw.githubusercontent.com/WillAdams/gcodepreview/refs/heads/main/gcodepreview.py")

try:
    if 'gcodepreview' in sys.modules:
        del sys.modules['gcodepreview']
except AttributeError:
    pass

from gcodepreview import *

gc_file = "C:\\Users\\willa\\OneDrive\\Desktop\\19mm_1_32_depth.nc"

gcp = gcodepreview(False, False)

gcp.previewgcodefile(gc_file)

#print(sys.getsizeof(gcp.toolpaths))

