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
generatepaths = False
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

gcp = gcodepreview(generatepaths,
                   generategcode,
                   generatedxf,
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

#print(pygcpversion())

#print(gcp.myfunc(4))

#print(gcp.getvv())

#ts = cylinder(12.7, 1.5875, 1.5875)
#toolpaths = gcp.cutshape(stockXwidth/2,stockYheight/2,-stockZthickness)

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

#toolpaths = gcp.cutline(stockXwidth/2,stockYheight/2,-stockZthickness)
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

rapids = gcp.rapid(gcp.xpos(),gcp.ypos(),retractheight)
gcp.toolchange(102,10000)

rapids = gcp.rapid(-stockXwidth/4+stockYheight/16, +stockYheight/4,0)

toolpaths = toolpaths.union(gcp.cutarcCC(0,90, gcp.xpos()-stockYheight/16, gcp.ypos(), stockYheight/16, -stockZthickness/4))
toolpaths = toolpaths.union(gcp.cutarcCC(90,180, gcp.xpos(), gcp.ypos()-stockYheight/16, stockYheight/16, -stockZthickness/4))
toolpaths = toolpaths.union(gcp.cutarcCC(180,270, gcp.xpos()+stockYheight/16, gcp.ypos(), stockYheight/16, -stockZthickness/4))
toolpaths = toolpaths.union(gcp.cutarcCC(270,360, gcp.xpos(), gcp.ypos()+stockYheight/16, stockYheight/16, -stockZthickness/4))

rapids = gcp.movetosafeZ()
rapids = gcp.rapidXY(stockXwidth/4-stockYheight/16, -stockYheight/4)
rapids = gcp.rapidZ(0)

toolpaths = toolpaths.union(gcp.cutarcCW(180,90, gcp.xpos()+stockYheight/16, gcp.ypos(), stockYheight/16, -stockZthickness/4))
toolpaths = toolpaths.union(gcp.cutarcCW(90,0, gcp.xpos(), gcp.ypos()-stockYheight/16, stockYheight/16, -stockZthickness/4))
toolpaths = toolpaths.union(gcp.cutarcCW(360,270, gcp.xpos()-stockYheight/16, gcp.ypos(), stockYheight/16, -stockZthickness/4))
toolpaths = toolpaths.union(gcp.cutarcCW(270,180, gcp.xpos(), gcp.ypos()+stockYheight/16, stockYheight/16, -stockZthickness/4))

rapids = gcp.movetosafeZ()
gcp.toolchange(201,10000)
rapids = gcp.rapidXY(stockXwidth/2, -stockYheight/2)
rapids = gcp.rapidZ(0)

toolpaths = toolpaths.union(gcp.cutlinedxfgc(gcp.xpos(), gcp.ypos(), -stockZthickness))
#test = gcp.cutlinedxfgc(gcp.xpos(), gcp.ypos(), -stockZthickness)

rapids = gcp.movetosafeZ()
rapids = gcp.rapidXY(stockXwidth/2-6.34, -stockYheight/2)
rapids = gcp.rapidZ(0)

toolpaths = toolpaths.union(gcp.cutarcCW(180,90, stockXwidth/2, -stockYheight/2, 6.34, -stockZthickness))

rapids = gcp.movetosafeZ()
gcp.toolchange(814,10000)
rapids = gcp.rapidXY(0, -(stockYheight/2+12.7))
rapids = gcp.rapidZ(0)

toolpaths = toolpaths.union(gcp.cutlinedxfgc(gcp.xpos(), gcp.ypos(), -stockZthickness))
toolpaths = toolpaths.union(gcp.cutlinedxfgc(gcp.xpos(), -12.7, -stockZthickness))

rapids = gcp.rapidXY(0, -(stockYheight/2+12.7))
rapids = gcp.movetosafeZ()
gcp.toolchange(374,10000)
rapids = gcp.rapidXY(stockXwidth/4-stockXwidth/16, -(stockYheight/4+stockYheight/16))
rapids = gcp.rapidZ(0)

gcp.rapidZ(retractheight)
gcp.toolchange(374,10000)
gcp.rapidXY(-stockXwidth/4-stockXwidth/16, -(stockYheight/4+stockYheight/16))
gcp.rapidZ(0)

toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), -stockZthickness/2))
toolpaths = toolpaths.union(gcp.cutlinedxfgc(gcp.xpos()+stockYheight/9, gcp.ypos(), gcp.zpos()))
#below should probably be cutlinegc
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos()-stockYheight/9, gcp.ypos(), gcp.zpos()))
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), 0))

#key = gcp.cutkeyholegcdxf(KH_tool_num, 0, stockZthickness*0.75, "E", stockYheight/9)
#key = gcp.cutKHgcdxf(374, 0, stockZthickness*0.75, 90, stockYheight/9)
#toolpaths = toolpaths.union(key)

gcp.rapidZ(retractheight)
gcp.rapidXY(-stockXwidth/4+stockXwidth/16, -(stockYheight/4+stockYheight/16))
gcp.rapidZ(0)
#toolpaths = toolpaths.union(gcp.cutkeyholegcdxf(KH_tool_num, 0, stockZthickness*0.75, "N", stockYheight/9))
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), -stockZthickness/2))
toolpaths = toolpaths.union(gcp.cutlinedxfgc(gcp.xpos(), gcp.ypos()+stockYheight/9, gcp.zpos()))
#below should probably be cutlinegc
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos()-stockYheight/9, gcp.zpos()))
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), 0))

gcp.rapidZ(retractheight)
gcp.rapidXY(-stockXwidth/4+stockXwidth/16, -(stockYheight/4-stockYheight/8))
gcp.rapidZ(0)
#toolpaths = toolpaths.union(gcp.cutkeyholegcdxf(KH_tool_num, 0, stockZthickness*0.75, "W", stockYheight/9))
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), -stockZthickness/2))
toolpaths = toolpaths.union(gcp.cutlinedxfgc(gcp.xpos()-stockYheight/9, gcp.ypos(), gcp.zpos()))
#below should probably be cutlinegc
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos()+stockYheight/9, gcp.ypos(), gcp.zpos()))
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), 0))

gcp.rapidZ(retractheight)
gcp.rapidXY(-stockXwidth/4-stockXwidth/16, -(stockYheight/4-stockYheight/8))
gcp.rapidZ(0)
#toolpaths = toolpaths.union(gcp.cutkeyholegcdxf(KH_tool_num, 0, stockZthickness*0.75, "S", stockYheight/9))
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), -stockZthickness/2))
toolpaths = toolpaths.union(gcp.cutlinedxfgc(gcp.xpos(), gcp.ypos()-stockYheight/9, gcp.zpos()))
#below should probably be cutlinegc
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos()+stockYheight/9, gcp.zpos()))
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), 0))

gcp.rapidZ(retractheight)
gcp.toolchange(56142,10000)
gcp.rapidXY(-stockXwidth/2, -(stockYheight/2+0.508/2))
#gcp.cutZgcfeed(-1.531,plunge)
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), -1.531))
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/2+0.508/2, -(stockYheight/2+0.508/2), -1.531))

gcp.rapidZ(retractheight)
#gcp.toolchange(56125,10000)
#gcp.cutZgcfeed(-1.531,plunge)
toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), -1.531))
toolpaths = toolpaths.union(gcp.cutlinedxfgc(stockXwidth/2+0.508/2, (stockYheight/2+0.508/2), -1.531))


part = gcp.stock.difference(toolpaths)

output (part)
#output(test)
#output (key)
#output(dt)
#gcp.stockandtoolpaths()
#gcp.stockandtoolpaths("stock")
#output (gcp.stock)
#output (gcp.toolpaths)
#output (toolpaths)

#gcp.makecube(3, 2, 1)
#
#gcp.placecube()
#
#c = gcp.instantiatecube()
#
#output(c)

gcp.closegcodefile()
gcp.closedxffiles()
gcp.closedxffile()
