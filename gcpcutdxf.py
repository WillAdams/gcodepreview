from openscad import *
# nimport("https://raw.githubusercontent.com/WillAdams/gcodepreview/refs/heads/main/gcodepreview.py")
from gcodepreview import *

fa = 2
fs = 0.125

gcp = gcodepreview("cut", # "print" or "no_preview"
                   False, # generategcode
                   True   # generatedxf
                   )

# [Stock] */
stockXwidth = 100
# [Stock] */
stockYheight = 50
# [Stock] */
stockZthickness = 3.175
# [Stock] */
zeroheight = "Top"  # [Top, Bottom]
# [Stock] */
stockzero = "Lower-Left"  # [Lower-Left, Center-Left, Top-Left, Center]
# [Stock] */
retractheight = 3.175

# [Export] */
Base_filename = "gcpdxf"


# [CAM] */
large_square_tool_num = 112
# [CAM] */
small_square_tool_num = 0
# [CAM] */
large_ball_tool_num = 111
# [CAM] */
small_ball_tool_num = 0
# [CAM] */
large_V_tool_num = 0
# [CAM] */
small_V_tool_num = 0
# [CAM] */
DT_tool_num = 374
# [CAM] */
KH_tool_num = 0
# [CAM] */
Roundover_tool_num = 0
# [CAM] */
MISC_tool_num = 0

# [Design] */
inset = 3
# [Design] */
radius = 6
# [Design] */
cornerstyle = "Fillet"  # "Chamfer", "Flipped Fillet"

gcp.opendxffile(Base_filename)

gcp.setupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero, retractheight)

gcp.toolchange(large_square_tool_num)

gcp.setdxfcolor("Red")

gcp.cutrectangledxf(large_square_tool_num, 0, 0, 0, stockXwidth, stockYheight, stockZthickness)

gcp.toolchange(large_ball_tool_num)

gcp.setdxfcolor("Gray")

gcp.rapid(inset + radius, inset, 0, "laser")

gcp.cutlinedxf(inset + radius, inset, -stockZthickness/2)
gcp.cutquarterCCNEdxf(inset, inset + radius, -stockZthickness/2, radius)

gcp.cutlinedxf(inset, stockYheight - (inset + radius), -stockZthickness/2)

gcp.cutquarterCCSEdxf(inset + radius, stockYheight - inset, -stockZthickness/2, radius)

gcp.cutlinedxf(stockXwidth - (inset + radius), stockYheight - inset, -stockZthickness/2)

gcp.cutquarterCCSWdxf(stockXwidth - inset, stockYheight - (inset + radius), -stockZthickness/2, radius)

gcp.cutlinedxf(stockXwidth - (inset), (inset + radius), -stockZthickness/2)

gcp.cutquarterCCNWdxf(stockXwidth - (inset + radius), inset, -stockZthickness/2, radius)

gcp.cutlinedxf((inset + radius), inset, -stockZthickness/2)

gcp.setdxfcolor("Blue")

gcp.rapid(radius + inset + radius, radius, 0, "laser")

gcp.cutrectanglerounddxf(large_square_tool_num, radius +inset, radius, 0, stockXwidth/2 - (radius * 4), stockYheight - (radius * 2), -stockZthickness/4, radius)

gcp.rapid(stockXwidth/2 + (radius * 2) + inset + radius, radius, 0, "laser")

gcp.cutrectanglerounddxf(large_square_tool_num, stockXwidth/2 + (radius * 2) + inset, radius, 0, stockXwidth/2 - (radius * 4), stockYheight - (radius * 2), -stockZthickness/4, radius)

gcp.setdxfcolor("Red")

gcp.rapid(stockXwidth/2 + radius, stockYheight/2, 0, "laser")

gcp.toolchange(large_square_tool_num)

gcp.cutcircleCC(stockXwidth/2, stockYheight/2, 0, -stockZthickness, radius)

gcp.cutcircleCC(stockXwidth/2, stockYheight/2, -stockZthickness, -stockZthickness, radius*1.5)

gcp.closedxffile()

gcp.stockandtoolpaths()

