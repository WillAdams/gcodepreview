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

gcp.dxfarc(large_square_tool_num, 88, 38, 12,   0,  90)
gcp.dxfarc(large_square_tool_num, 12, 38, 12,  90, 180)
gcp.dxfarc(large_square_tool_num, 12, 12, 12, 180, 270)
gcp.dxfarc(large_square_tool_num, 88, 12, 12, 270, 360)

gcp.dxfline(large_square_tool_num, 12, 0, 88, 0)
gcp.dxfline(large_square_tool_num, 100, 12, 100, 38)
gcp.dxfline(large_square_tool_num, 88, 50, 12, 50)
gcp.dxfline(large_square_tool_num, 0, 38, 0, 12)

gcp.dxfarc(large_square_tool_num, 50, 25, 12,   0,  90)
gcp.dxfarc(large_square_tool_num, 50, 25, 12,  90, 180)
gcp.dxfarc(large_square_tool_num, 50, 25, 12, 180, 270)
gcp.dxfarc(large_square_tool_num, 50, 25, 12, 270, 360)

gcp.closedxffiles()
gcp.closedxffile()

