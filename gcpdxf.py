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

gcp.dxfrectangle(0, 0, stockXwidth, stockYheight)

gcp.setdxfcolor("Red")
gcp.setdxflayer("Red")

gcp.dxfarc(inset, inset, radius,  0, 90)
gcp.dxfarc(stockXwidth - inset, inset, radius, 90, 180)
gcp.dxfarc(stockXwidth - inset, stockYheight - inset, radius, 180, 270)
gcp.dxfarc(inset, stockYheight - inset, radius, 270, 360)

gcp.dxfline(inset, inset + radius, inset, stockYheight - (inset + radius))
gcp.dxfline(inset + radius, inset, stockXwidth - (inset + radius), inset)
gcp.dxfline(stockXwidth - inset, inset + radius, stockXwidth - inset, stockYheight - (inset + radius))
gcp.dxfline(inset + radius, stockYheight-inset, stockXwidth - (inset + radius), stockYheight - inset)

gcp.setdxfcolor("Blue")
gcp.setdxflayer("Blue")

gcp.dxfrectangle(radius +inset, radius, stockXwidth/2 - (radius * 4), stockYheight - (radius * 2), cornerstyle, radius)
gcp.dxfrectangle(stockXwidth/2 + (radius * 2) + inset, radius, stockXwidth/2 - (radius * 4), stockYheight - (radius * 2), cornerstyle, radius)

gcp.setdxfcolor("Black")
gcp.setdxflayer("DEFAULT")

gcp.beginpolyline(stockXwidth*0.75+radius*1.5,stockYheight/4-radius/2)
gcp.addvertex(stockXwidth*0.75+radius,stockYheight/4-radius/2)
gcp.addvertex(stockXwidth*0.75+radius,stockYheight*0.75+radius/2)
gcp.addvertex(stockXwidth*0.75+radius*1.5,stockYheight*0.75+radius/2)
gcp.closepolyline()

gcp.dxfarc(stockXwidth*0.75+radius*1.5, stockYheight*0.75, radius/2,  0, 90)

gcp.beginpolyline(stockXwidth*0.75+radius*2,stockYheight*0.75)
gcp.addvertex(stockXwidth*0.75+radius*2,stockYheight/4)
gcp.closepolyline()

gcp.dxfarc(stockXwidth*0.75+radius*1.5, stockYheight/4, radius/2,  270, 360)

gcp.setdxfcolor("Light Gray")
gcp.setdxflayer("Light Gray")

gcp.beginpolyline(stockXwidth*0.25-radius*1.5,stockYheight/4-radius/2)
gcp.addvertex(stockXwidth*0.25-radius,stockYheight/4-radius/2)
gcp.addvertex(stockXwidth*0.25-radius,stockYheight*0.75+radius/2)
gcp.addvertex(stockXwidth*0.25-radius*1.5,stockYheight*0.75+radius/2)
gcp.closepolyline()

gcp.dxfarc(stockXwidth*0.25-radius*1.5, stockYheight*0.75, radius/2,  90, 180)

gcp.beginpolyline(stockXwidth*0.25-radius*2,stockYheight*0.75)
gcp.addvertex(stockXwidth*0.25-radius*2,stockYheight/4)
gcp.closepolyline()

gcp.dxfarc(stockXwidth*0.25-radius*1.5, stockYheight/4, radius/2,  180, 270)

gcp.setdxfcolor("Yellow")
gcp.setdxflayer("Yellow")
gcp.dxfcircle(stockXwidth/4+1+radius/2, stockYheight/4, radius/2)

gcp.setdxfcolor("Green")
gcp.setdxflayer("Green")
gcp.dxfcircle(stockXwidth*0.75-(1+radius/2), stockYheight*0.75, radius/2)

gcp.setdxfcolor("Cyan")
gcp.setdxflayer("Cyan")
gcp.dxfcircle(stockXwidth/4+1+radius/2, stockYheight*0.75, radius/2)

gcp.setdxfcolor("Magenta")
gcp.setdxflayer("Magenta")
gcp.dxfcircle(stockXwidth*0.75-(1+radius/2), stockYheight/4, radius/2)

gcp.setdxfcolor("Dark Gray")
gcp.setdxflayer("Dark Gray")
gcp.dxfcircle(stockXwidth/2, stockYheight/2, radius * 2)

gcp.setdxfcolor("Light Gray")
gcp.setdxflayer("Light Gray")

gcp.toolchange(374)

gcp.dxfKH(stockXwidth/2, stockYheight/5*3, 0, -7, 270, 11.5875)

gcp.closedxffile()

