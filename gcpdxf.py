from openscad import *
#nimport("https://raw.githubusercontent.com/WillAdams/gcodepreview/refs/heads/main/gcodepreview.py")
from gcodepreview import *

gcp = gcodepreview(False, #generatepaths
                   False, #generategcode
                   True #generatedxf
                   )

Base_filename = "dxfexport"
large_square_tool_num = 102
small_square_tool_num = 0
large_ball_tool_num = 0
small_ball_tool_num = 0
large_V_tool_num = 0
small_V_tool_num = 0
DT_tool_num = 0
KH_tool_num = 0
Roundover_tool_num = 0
MISC_tool_num = 0

gcp.opendxffile(Base_filename)
#gcp.opendxffiles(Base_filename,
#                 large_square_tool_num,
#                 small_square_tool_num,
#                 large_ball_tool_num,
#                 small_ball_tool_num,
#                 large_V_tool_num,
#                 small_V_tool_num,
#                 DT_tool_num,
#                 KH_tool_num,
#                 Roundover_tool_num,
#                 MISC_tool_num)

gcp.dxfrectangle(large_square_tool_num, 0, 0, 100, 50)

gcp.dxfarc(large_square_tool_num,  3,  3, 6,   0,  90)
gcp.dxfarc(large_square_tool_num, 97,  3, 6,  90, 180)
gcp.dxfarc(large_square_tool_num, 97, 47, 6, 180, 270)
gcp.dxfarc(large_square_tool_num,  3, 47, 6, 270, 360)

gcp.dxfline(large_square_tool_num,  3, 9, 3,41)
gcp.dxfline(large_square_tool_num,  9, 3,91, 3)
gcp.dxfline(large_square_tool_num, 97, 9,97,41)
gcp.dxfline(large_square_tool_num,  9,47,91,47)

gcp.dxfrectangleround(large_square_tool_num, 12, 6, 24, 36, 6)
gcp.dxfrectangleround(large_square_tool_num, 64, 6, 24, 36, 6)

gcp.dxfcircle(large_square_tool_num, 50, 25, 12)

#gcp.closedxffiles()
gcp.closedxffile()

