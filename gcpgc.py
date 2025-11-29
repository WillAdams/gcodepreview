#Requires OpenPythonSCAD, so load support for 3D modeling in that tool:
from openscad import *

#The gcodepreview library must be loaded, either from github (first line below) or from a local library (second line below), uncomment one and comment out the other, depending on where one wishes to load from
#nimport("https://raw.githubusercontent.com/WillAdams/gcodepreview/refs/heads/main/gcodepreview.py")
from gcodepreview import *

#The file to be loaded must be specified:
#gc_file = "filename_of_G-code_file_to_process.nc"
#
#if using windows the full filepath should be provided with backslashes replaced with double backslashes and wrapped in quotes since it is provided as a string:
gc_file = "C:\\Users\\willa\\OneDrive\\Desktop\\19mm_1_32_depth.nc"

#Create the gcodepreview object:
gcp = gcodepreview("cut", False, False)

#Process the file
gcp.previewgcodefile(gc_file)

