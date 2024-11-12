#!/usr/bin/env python

# getting openscad functions into namespace
#https://github.com/gsohler/openscad/issues/39
from openscad import *

import sys
try:
    if 'gcodepreview' in sys.modules:
        del sys.modules['gcodepreview']
except AttributeError:
    pass

#Below command only needed if using withing OpenPythonSCAD
from gcodepreview import *

#fa = 2
#fs = 0.125

# [Export] */
Base_filename = "export"
# [Export] */
generatedxf = True
# [Export] */
generategcode = True

# [Stock] */
stockXwidth = 219
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
large_square_tool_num = 0 # [0:0,112:112,102:102,201:201]
# [CAM] */
small_square_tool_num = 102 # [0:0,122:122,112:112,102:102]
# [CAM] */
large_ball_tool_num = 0 # [0:0,111:111,101:101,202:202]
# [CAM] */
small_ball_tool_num = 0 # [0:0,121:121,111:111,101:101]
# [CAM] */
large_V_tool_num = 0 # [0:0,301:301,690:690]
# [CAM] */
small_V_tool_num = 0 # [0:0,390:390,301:301]
# [CAM] */
DT_tool_num = 0 # [0:0,814:814]
# [CAM] */
KH_tool_num = 0 # [0:0,374:374,375:375,376:376,378]
# [CAM] */
Roundover_tool_num = 0 # [56125:56125, 56142:56142,312:312, 1570:1570]
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

gcp = gcodepreview(Base_filename, #"export", basefilename
                   True, #generategcode
                   True, #generatedxf
                   stockXwidth,
                   stockYheight,
                   stockZthickness,
                   zeroheight,
                   stockzero,
                   retractheight,
                   large_square_tool_num,
                   toolradius,
                   plunge,
                   feed,
                   speed)

gcp.opengcodefile(Base_filename)
gcp.opendxffiles(Base_filename)

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

gcp.setzpos(retractheight)
gcp.toolchange(202,10000)
gcp.rapidXY(0, stockYheight/8)
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/16*6, stockYheight/2, -stockZthickness))

gcp.setzpos(retractheight)
gcp.toolchange(101,10000)
gcp.rapidXY(0, stockYheight/16*3)
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/16*5, stockYheight/2, -stockZthickness))

gcp.setzpos(retractheight)
gcp.toolchange(390,10000)
gcp.rapidXY(0, stockYheight/16*4)
gcp.rapidZ(0)
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/16*4, stockYheight/2, -stockZthickness))
gcp.setzpos(retractheight)

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

gcp.setzpos(retractheight)
gcp.toolchange(102,10000)
gcp.rapidXY(stockXwidth/4+stockYheight/8+stockYheight/16, +stockYheight/8)
gcp.rapidZ(0)
#gcp.settzpos(stockZthickness/90)
#toolpaths = toolpaths.union(gcp.arcloop(0, 90, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))
toolpaths = toolpaths.union(gcp.cutarcNECCdxf(stockXwidth/4+stockYheight/8, stockYheight/8+stockYheight/16, -stockZthickness, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))
toolpaths = toolpaths.union(gcp.cutarcNWCCdxf(stockXwidth/4+stockYheight/8-stockYheight/16, stockYheight/8, -stockZthickness, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))
toolpaths = toolpaths.union(gcp.cutarcSWCCdxf(stockXwidth/4+stockYheight/8, stockYheight/8-stockYheight/16, -stockZthickness, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))
toolpaths = toolpaths.union(gcp.cutarcSECCdxf(stockXwidth/4+stockYheight/8+stockYheight/16, stockYheight/8, -stockZthickness, stockXwidth/4+stockYheight/8, stockYheight/8, stockYheight/16))

#a = gcp.currenttool()
#arcbegin = a.translate([64.37357214209116, -37.33638368965047,-stockZthickness])
#arcend = a.translate([55.16361631034953, -28.12642785790883,-stockZthickness])
#toolpaths = toolpaths.union(arcbegin)
#toolpaths = toolpaths.union(arcend)

#cu = cube([10,20,30])
#c = cu.translate([0,0,gcp.zpos()])

part = gcp.stock.difference(toolpaths)

#output(gcp.stock)
#output(gcp.currenttool())
#output(test)
output(part)
#output(toolpaths)
#output (arc)

gcp.setzpos(retractheight)

gcp.closegcodefile()
gcp.closedxffile()
#gcp.closedxffiles()

