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
generatedxf = True
# [Export] */
generategcode = True

# [Stock] */
stockXwidth = 220
# [Stock] */
stockYheight = 150
# [Stock] */
stockZthickness = 8.35
# [Stock] */
zeroheight = "Top" # [Top, Bottom]
# [Stock] */
stockzero = "Center" # [Lower-Left, Center-Left, Top-Left, Center]
# [Stock] */
retractheight = 9

# [CAM] */
toolradius = 1.5875
# [CAM] */
large_square_tool_num = 201 # [0:0,112:112,102:102,201:201]
# [CAM] */
small_square_tool_num = 102 # [0:0,122:122,112:112,102:102]
# [CAM] */
large_ball_tool_num = 202 # [0:0,111:111,101:101,202:202]
# [CAM] */
small_ball_tool_num = 101 # [0:0,121:121,111:111,101:101]
# [CAM] */
large_V_tool_num = 301 # [0:0,301:301,690:690]
# [CAM] */
small_V_tool_num = 390 # [0:0,390:390,301:301]
# [CAM] */
DT_tool_num = 814 # [0:0,814:814]
# [CAM] */
KH_tool_num = 374 # [0:0,374:374,375:375,376:376,378]
# [CAM] */
Roundover_tool_num = 56142 # [56142:56142, 56125:56125, 1570:1570]
# [CAM] */
MISC_tool_num = 0 #

# [Feeds and Speeds] */
plunge = 100
# [Feeds and Speeds] */
feed = 400
# [Feeds and Speeds] */
speed = 16000
# [Feeds and Speeds] */
small_square_ratio = 0.75 # [0.25:2]
# [Feeds and Speeds] */
large_ball_ratio = 1.0 # [0.25:2]
# [Feeds and Speeds] */
small_ball_ratio = 0.75 # [0.25:2]
# [Feeds and Speeds] */
large_V_ratio = 0.875 # [0.25:2]
# [Feeds and Speeds] */
small_V_ratio = 0.625 # [0.25:2]
# [Feeds and Speeds] */
DT_ratio = 0.75 # [0.25:2]
# [Feeds and Speeds] */
KH_ratio = 0.75 # [0.25:2]
# [Feeds and Speeds] */
RO_ratio = 0.5 # [0.25:2]
# [Feeds and Speeds] */
MISC_ratio = 0.5 # [0.25:2]

gcp = gcodepreview(True, #generatescad
                   True, #generategcode
                   True, #generatedxf
                   )

gcp.opengcodefile(Base_filename)
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

gcp.setupstock(stockXwidth,stockYheight,stockZthickness,"Top","Center",retractheight)

gcp.movetosafeZ()

gcp.toolchange(102,10000)

#gcp.rapidXY(6,12)
gcp.rapidZ(0)

#print (gcp.xpos())
#print (gcp.ypos())
#psetzpos(7)
#gcp.setzpos(-12)
#print (gcp.zpos())

#print ("X", str(gcp.xpos()))
#print ("Y", str(gcp.ypos()))
#print ("Z", str(gcp.zpos()))

toolpaths = gcp.currenttool()

toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/2, stockYheight/2, -stockZthickness))

gcp.rapidZ(retractheight)
gcp.toolchange(201,10000)
gcp.rapidXY(0, stockYheight/16)
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/16*7, stockYheight/2, -stockZthickness))

gcp.rapidZ(retractheight)
gcp.toolchange(202,10000)
gcp.rapidXY(0, stockYheight/8)
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/16*6, stockYheight/2, -stockZthickness))

gcp.rapidZ(retractheight)
gcp.toolchange(101,10000)
gcp.rapidXY(0, stockYheight/16*3)
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/16*5, stockYheight/2, -stockZthickness))

gcp.setzpos(retractheight)
gcp.toolchange(390,10000)
gcp.rapidXY(0, stockYheight/16*4)
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/16*4, stockYheight/2, -stockZthickness))
gcp.rapidZ(retractheight)

gcp.toolchange(301,10000)
gcp.rapidXY(0, stockYheight/16*6)
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/16*2, stockYheight/2, -stockZthickness))

#gcp.setzpos(retractheight)
#gcp.toolchange(102,10000)
#gcp.rapidXY(stockXwidth/4+stockYheight/16, -(stockYheight/4))
#gcp.rapidZ(0)
##arcloop(barc, earc, xcenter, ycenter, radius)
#gcp.settzpos(stockZthickness/90)
#toolpaths = toolpaths.union(gcp.arcloop(0, 90, stockXwidth/4, -stockYheight/4, stockYheight/16))

gcp.rapidZ(retractheight)
gcp.toolchange(102,10000)
gcp.rapidXY(stockXwidth/4+stockYheight/8+stockYheight/16, +stockYheight/8)
gcp.rapidZ(0)
#gcp.settzpos(stockZthickness/90)
#toolpaths = toolpaths.union(gcp.arcloop(0, 90, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))
toolpaths = toolpaths.union(gcp.cutarcNECCdxfgc(stockXwidth/4+stockYheight/8, stockYheight/8+stockYheight/16, -stockZthickness, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))
toolpaths = toolpaths.union(gcp.cutarcNWCCdxfgc(stockXwidth/4+stockYheight/8-stockYheight/16, stockYheight/8, -stockZthickness, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))
toolpaths = toolpaths.union(gcp.cutarcSWCCdxfgc(stockXwidth/4+stockYheight/8, stockYheight/8-stockYheight/16, -stockZthickness, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))
toolpaths = toolpaths.union(gcp.cutarcSECCdxfgc(stockXwidth/4+stockYheight/8+stockYheight/16, stockYheight/8, -stockZthickness, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))

#a = gcp.currenttool()
#arcbegin = a.translate([64.37357214209116, -37.33638368965047,-stockZthickness])
#arcend = a.translate([55.16361631034953, -28.12642785790883,-stockZthickness])
#toolpaths = toolpaths.union(arcbegin)
#toolpaths = toolpaths.union(arcend)

#cu = cube([10,20,30])
#c = cu.translate([0,0,gcp.zpos()])

#def cutroundovertool(bx, by, bz, ex, ey, ez, tool_radius_tip, tool_radius_width):
#    n = 90 + fn*3
#    step = 360/n
#    shaft = cylinder(step,tool_radius_tip,tool_radius_tip)
#    toolpath = hull(shaft.translate([bx,by,bz]), shaft.translate([ex,ey,ez]))
#    shaft = cylinder(tool_radius_width*2,tool_radius_tip+tool_radius_width,tool_radius_tip+tool_radius_width)
#    toolpath = toolpath.union(hull(shaft.translate([bx,by,bz+tool_radius_width]), shaft.translate([ex,ey,ez+tool_radius_width])))
#    for i in range(1, 90, 1):
#        angle = i
#        dx = tool_radius_width*math.cos(math.radians(angle))
#        dxx = tool_radius_width*math.cos(math.radians(angle+1))
#        dzz = tool_radius_width*math.sin(math.radians(angle))
#        dz = tool_radius_width*math.sin(math.radians(angle+1))
#        dh = abs(dzz-dz)+0.0001
#        slice = cylinder(dh,tool_radius_tip+tool_radius_width-dx,tool_radius_tip+tool_radius_width-dxx)
#        toolpath = toolpath.union(hull(slice.translate([bx,by,bz+dz]), slice.translate([ex,ey,ez+dz])))
#    return toolpath

gcp.rapidZ(retractheight)
gcp.toolchange(814,10000)
gcp.rapidXY(0, -(stockYheight/2+12.7))
gcp.cutZgcfeed(-stockZthickness,plunge)
toolpaths = toolpaths.union(gcp.cutlinedxfgcfeed(0, -(stockYheight/16), -stockZthickness, feed))


gcp.rapidZ(0)

#print(gcp.currenttoolnumber())

gcp.rapidZ(retractheight)
gcp.toolchange(56142,10000)
gcp.rapidXY(-stockXwidth/2, -(stockYheight/2+0.508/2))
gcp.cutZgcfeed(-1.531,plunge)
toolpaths = toolpaths.union(gcp.cutlinedxfgcfeed(stockXwidth/2+0.508/2, -(stockYheight/2+0.508/2), -1.531, feed))

gcp.rapidZ(retractheight)
#gcp.toolchange(56125,10000)
gcp.cutZgcfeed(-1.531,plunge)
toolpaths = toolpaths.union(gcp.cutlinedxfgcfeed(stockXwidth/2+0.508/2, (stockYheight/2+0.508/2), -1.531, feed))

gcp.rapidZ(retractheight)
gcp.toolchange(374,10000)
gcp.rapidXY(stockXwidth/4-stockXwidth/16, -(stockYheight/4+stockYheight/16))
gcp.rapidZ(0)
#toolpaths = toolpaths.union(gcp.cutlinedxfgcfeed(gcp.xpos(), gcp.ypos(), -4, feed))
#toolpaths = toolpaths.union(gcp.cutZgcfeed(-4,plunge))
#toolpaths = toolpaths.union(gcp.cutlinedxfgcfeed(stockXwidth/4, -(stockYheight/4)+25.4, -4, feed))
#key = gcp.cutlinedxfgcfeed(stockXwidth/2+0.508/2, (stockYheight/2+0.508/2), -1.531, feed)

#cutkeyholegcdxf(stockZthickness/2, stockZthickness/2, "N", stockYheight/8, KH_tool_num)
#rapid(getxpos(),getypos(),stockZthickness);
#rapid(-stockXwidth/4,-stockYheight/4,0);
#cutkeyhole_toolpath((stockZthickness), (stockZthickness), "S", stockYheight/8, KH_tool_num);
#rapid(getxpos(),getypos(),stockZthickness);
#rapid(-stockXwidth/4,-stockYheight/8,0);
key = gcp.cutkeyholegcdxf(0, stockZthickness*0.75, "E", stockYheight/9, KH_tool_num)
toolpaths = toolpaths.union(key)
#rapid(getxpos(),getypos(),stockZthickness);
#rapid(-stockXwidth/8,-stockYheight/8*3,0);
#cutkeyhole_toolpath((stockZthickness), (stockZthickness), "W", stockYheight/8, KH_tool_num);

gcp.rapidZ(retractheight)
gcp.rapidXY(stockXwidth/4+stockXwidth/16, -(stockYheight/4+stockYheight/16))
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutkeyholegcdxf(0, stockZthickness*0.75, "N", stockYheight/9, KH_tool_num))

gcp.rapidZ(retractheight)
gcp.rapidXY(stockXwidth/4+stockXwidth/16, -(stockYheight/4-stockYheight/8))
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutkeyholegcdxf(0, stockZthickness*0.75, "W", stockYheight/9, KH_tool_num))

gcp.rapidZ(retractheight)
gcp.rapidXY(stockXwidth/4-stockXwidth/16, -(stockYheight/4-stockYheight/8))
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutkeyholegcdxf(0, stockZthickness*0.75, "S", stockYheight/9, KH_tool_num))

gcp.rapidZ(retractheight)

#Last dxf command not being written...
#empty = gcp.cutlinedxfgcfeed(stockXwidth/2, -(stockYheight/2+0.508/2), 1, feed)

part = gcp.stock.difference(toolpaths)
#part = gcp.stock.union(key)

output(part)
#output(toolpaths)
#output(key)

gcp.setzpos(retractheight)

gcp.closegcodefile()
gcp.closedxffiles()
gcp.closedxffile()

