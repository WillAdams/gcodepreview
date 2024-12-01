from gcodepreview import *

gcp = gcodepreview(False, #generatescad
                   False, #generategcode
                   True #generatedxf
                   )

Base_filename = "export"
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
gcp.opendxffiles(Base_filename,
                 large_square_tool_num,
                 small_square_tool_num,
                 large_ball_tool_num,
                 small_ball_tool_num,
                 large_V_tool_num,
                 small_V_tool_num,
                 DT_tool_num,
                 KH_tool_num,
                 Roundover_tool_num,
                 MISC_tool_num)

gcp.dxfrectangle(large_square_tool_num, 0, 0, 100, 50)
gcp.dxfrectangleround(large_square_tool_num, 1, 1, 98, 48, 11)

gcp.dxfcircle(large_square_tool_num, 50, 25, 12)

gcp.closedxffiles()
gcp.closedxffile()

