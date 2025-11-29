from openscad import *
	# nimport("https://raw.githubusercontent.com/WillAdams/gcodepreview/refs/heads/main/gcodepreview.py")
from gcodepreview import *

gcp = gcodepreview("no_preview", # "cut" or "print"
                   False, # generategcode
                   True   # generatedxf
                   )

# [Stock] */
stockXwidth = 100
# [Stock] */
stockYheight = 50

# [Export] */
Base_filename = "gcpdxf"


# [CAM] */
large_square_tool_num = 102
# [CAM] */
small_square_tool_num = 0
# [CAM] */
large_ball_tool_num = 0
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

gcp.dxfrectangle(large_square_tool_num, 0, 0, stockXwidth, stockYheight)

gcp.setdxfcolor("Red")

gcp.dxfarc(large_square_tool_num, inset, inset, radius,  0, 90)
gcp.dxfarc(large_square_tool_num, stockXwidth - inset, inset, radius, 90, 180)
gcp.dxfarc(large_square_tool_num, stockXwidth - inset, stockYheight - inset, radius, 180, 270)
gcp.dxfarc(large_square_tool_num, inset, stockYheight - inset, radius, 270, 360)

gcp.dxfline(large_square_tool_num, inset, inset + radius, inset, stockYheight - (inset + radius))
gcp.dxfline(large_square_tool_num, inset + radius, inset, stockXwidth - (inset + radius), inset)
gcp.dxfline(large_square_tool_num, stockXwidth - inset, inset + radius, stockXwidth - inset, stockYheight - (inset + radius))
gcp.dxfline(large_square_tool_num, inset + radius, stockYheight-inset, stockXwidth - (inset + radius), stockYheight - inset)

gcp.setdxfcolor("Blue")

gcp.dxfrectangle(large_square_tool_num, radius +inset, radius, stockXwidth/2 - (radius * 4), stockYheight - (radius * 2), cornerstyle, radius)
gcp.dxfrectangle(large_square_tool_num, stockXwidth/2 + (radius * 2) + inset, radius, stockXwidth/2 - (radius * 4), stockYheight - (radius * 2), cornerstyle, radius)

gcp.setdxfcolor("Black")

gcp.beginpolyline(large_square_tool_num)
gcp.addvertex(large_square_tool_num, stockXwidth*0.75+radius*1.5,stockYheight/4-radius/2)
gcp.addvertex(large_square_tool_num, stockXwidth*0.75+radius,stockYheight/4-radius/2)
gcp.addvertex(large_square_tool_num, stockXwidth*0.75+radius,stockYheight*0.75+radius/2)
gcp.addvertex(large_square_tool_num, stockXwidth*0.75+radius*1.5,stockYheight*0.75+radius/2)
gcp.closepolyline(large_square_tool_num)

gcp.dxfarc(large_square_tool_num, stockXwidth*0.75+radius*1.5, stockYheight*0.75, radius/2,  0, 90)

gcp.beginpolyline(large_square_tool_num)
gcp.addvertex(large_square_tool_num, stockXwidth*0.75+radius*2,stockYheight*0.75)
gcp.addvertex(large_square_tool_num, stockXwidth*0.75+radius*2,stockYheight/4)
gcp.closepolyline(large_square_tool_num)

gcp.dxfarc(large_square_tool_num, stockXwidth*0.75+radius*1.5, stockYheight/4, radius/2,  270, 360)

gcp.setdxfcolor("White")

gcp.beginpolyline(large_square_tool_num)
gcp.addvertex(large_square_tool_num, stockXwidth*0.25-radius*1.5,stockYheight/4-radius/2)
gcp.addvertex(large_square_tool_num, stockXwidth*0.25-radius,stockYheight/4-radius/2)
gcp.addvertex(large_square_tool_num, stockXwidth*0.25-radius,stockYheight*0.75+radius/2)
gcp.addvertex(large_square_tool_num, stockXwidth*0.25-radius*1.5,stockYheight*0.75+radius/2)
gcp.closepolyline(large_square_tool_num)

gcp.dxfarc(large_square_tool_num, stockXwidth*0.25-radius*1.5, stockYheight*0.75, radius/2,  90, 180)

gcp.beginpolyline(large_square_tool_num)
gcp.addvertex(large_square_tool_num, stockXwidth*0.25-radius*2,stockYheight*0.75)
gcp.addvertex(large_square_tool_num, stockXwidth*0.25-radius*2,stockYheight/4)
gcp.closepolyline(large_square_tool_num)

gcp.dxfarc(large_square_tool_num, stockXwidth*0.25-radius*1.5, stockYheight/4, radius/2,  180, 270)

gcp.setdxfcolor("Yellow")
gcp.dxfcircle(large_square_tool_num, stockXwidth/4+1+radius/2, stockYheight/4, radius/2)

gcp.setdxfcolor("Green")
gcp.dxfcircle(large_square_tool_num, stockXwidth*0.75-(1+radius/2), stockYheight*0.75, radius/2)

gcp.setdxfcolor("Cyan")
gcp.dxfcircle(large_square_tool_num, stockXwidth/4+1+radius/2, stockYheight*0.75, radius/2)

gcp.setdxfcolor("Magenta")
gcp.dxfcircle(large_square_tool_num, stockXwidth*0.75-(1+radius/2), stockYheight/4, radius/2)

gcp.setdxfcolor("Dark Gray")

gcp.dxfcircle(large_square_tool_num, stockXwidth/2, stockYheight/2, radius * 2)

gcp.setdxfcolor("Light Gray")

gcp.dxfKH(374, stockXwidth/2, stockYheight/5*3, 0, -7, 270, 11.5875)

gcp.closedxffile()

