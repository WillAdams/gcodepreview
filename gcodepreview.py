#!/usr/bin/env python
#icon "C:\Program Files\PythonSCAD\bin\openscad.exe"  --trust-python
#Currently tested with 2024.09.23 and Python 3.11
#gcodepreview 0.7, for use with OpenPythonSCAD,
#if using from OpenPythonSCAD see gcodepreview.scad

# getting openscad functions into namespace
#https://github.com/gsohler/openscad/issues/39
from openscad import *

# add math functions (using radians by default, convert to degrees where necessary)
import math

class gcodepreview:

    def __init__(self, basefilename = "export",
                 generategcode = False,
                 generatedxf = False,
                 stockXwidth = 25,
                 stockYheight = 25,
                 stockZthickness = 1,
                 zeroheight = "Top",
                 stockzero = "Lower-left" ,
                 retractheight = 6,
                 currenttoolnum = 102,
                 toolradius = 3.175,
                 plunge = 100,
                 feed = 400,
                 speed = 10000):
        self.basefilename = basefilename
        self.generategcode = generategcode
        self.generatedxf = generatedxf
        self.stockXwidth = stockXwidth
        self.stockYheight = stockYheight
        self.stockZthickness = stockZthickness
        self.zeroheight = zeroheight
        self.stockzero = stockzero
        self.retractheight = retractheight
        self.currenttoolnum = currenttoolnum
        self.toolradius = toolradius
        self.plunge = plunge
        self.feed = feed
        self.speed = speed
#        global toolpaths
#        self.toolpaths = cylinder(1.5875, 12.7)
        global generatedxfs
        self.generatedxfs = False

    def opengcodefile(self, basefilename = "export"):
        if self.generategcode == True:
            self.gcodefilename = basefilename + ".nc"
            self.gc = open(self.gcodefilename, "w")

    def opendxffile(self, basefilename = "export"):
        global generatedxfs
        if self.generatedxf == True:
            self.generatedxfs = False
            self.dxffilename = basefilename + ".dxf"
            self.dxf = open(self.dxffilename, "w")
            self.dxfpreamble(-1)

    def opendxffiles(self, basefilename = "export",
                     large_square_tool_num = 0,
                     small_square_tool_num = 0,
                     large_ball_tool_num = 0,
                     small_ball_tool_num = 0,
                     large_V_tool_num = 0,
                     small_V_tool_num = 0,
                     DT_tool_num = 0,
                     KH_tool_num = 0,
                     Roundover_tool_num = 0,
                     MISC_tool_num = 0):
        global generatedxfs
        self.generatedxfs = True
        self.large_square_tool_num = large_square_tool_num
        self.small_square_tool_num = small_square_tool_num
        self.large_ball_tool_num = large_ball_tool_num
        self.small_ball_tool_num = small_ball_tool_num
        self.large_V_tool_num = large_V_tool_num
        self.small_V_tool_num = small_V_tool_num
        self.DT_tool_num = DT_tool_num
        self.KH_tool_num = KH_tool_num
        self.Roundover_tool_num = Roundover_tool_num
        self.MISC_tool_num = MISC_tool_num
        if self.generatedxf == True:
            if (large_square_tool_num > 0):
                self.dxflgsqfilename = basefilename + str(large_square_tool_num) + ".dxf"
                print("Opening ", str(self.dxflgsqfilename))
                self.dxflgsq = open(self.dxflgsqfilename, "w")
                self.dxfpreamble(large_square_tool_num)
            if (small_square_tool_num > 0):
                print("Opening small square")
                self.dxfsmsqfilename = basefilename + str(small_square_tool_num) + ".dxf"
                self.dxfsmsq = open(self.dxfsmsqfilename, "w")
                self.dxfpreamble(small_square_tool_num)
            if (large_ball_tool_num > 0):
                print("Opening large ball")
                self.dxflgblfilename = basefilename + str(large_ball_tool_num) + ".dxf"
                self.dxflgbl = open(self.dxflgblfilename, "w")
                self.dxfpreamble(large_ball_tool_num)
            if (small_ball_tool_num > 0):
                print("Opening small ball")
                self.dxfsmblfilename = basefilename + str(small_ball_tool_num) + ".dxf"
                self.dxfsmbl = open(self.dxfsmblfilename, "w")
                self.dxfpreamble(small_ball_tool_num)
            if (large_V_tool_num > 0):
                print("Opening large V")
                self.dxflgVfilename = basefilename + str(large_V_tool_num) + ".dxf"
                self.dxflgV = open(self.dxflgVfilename, "w")
                self.dxfpreamble(large_V_tool_num)
            if (small_V_tool_num > 0):
                print("Opening small V")
                self.dxfsmVfilename = basefilename + str(small_V_tool_num) + ".dxf"
                self.dxfsmV = open(self.dxfsmVfilename, "w")
                self.dxfpreamble(small_V_tool_num)
            if (DT_tool_num > 0):
                print("Opening DT")
                self.dxfDTfilename = basefilename + str(DT_tool_num) + ".dxf"
                self.dxfDT = open(self.dxfDTfilename, "w")
                self.dxfpreamble(DT_tool_num)
            if (KH_tool_num > 0):
                print("Opening KH")
                self.dxfKHfilename = basefilename + str(KH_tool_num) + ".dxf"
                self.dxfKH = open(self.dxfKHfilename, "w")
                self.dxfpreamble(KH_tool_num)
            if (Roundover_tool_num > 0):
                print("Opening Rt")
                self.dxfRtfilename = basefilename + str(Roundover_tool_num) + ".dxf"
                self.dxfRt = open(self.dxfRtfilename, "w")
                self.dxfpreamble(Roundover_tool_num)
            if (MISC_tool_num > 0):
                print("Opening Mt")
                self.dxfMtfilename = basefilename + str(MISC_tool_num) + ".dxf"
                self.dxfMt = open(self.dxfMtfilename, "w")
                self.dxfpreamble(MISC_tool_num)

    def writegc(self, *arguments):
        line_to_write = ""
        for element in arguments:
            line_to_write += element
        self.gc.write(line_to_write)
        self.gc.write("\n")

    def writedxf(self, toolnumber, *arguments):
        line_to_write = ""
        for element in arguments:
            line_to_write += element
        if self.generatedxf == True:
            self.dxf.write(line_to_write)
            self.dxf.write("\n")
        if self.generatedxfs == True:
            self.writedxfs(toolnumber, arguments)

    def writedxfs(self, toolnumber, *arguments):
        print("Processing writing toolnumber", toolnumber)
        line_to_write = ""
        for element in arguments:
            line_to_write += element
        if (toolnumber == 0):
            return
        elif self.generatedxfs == True:
            if (self.large_square_tool_num > 0):
                self.dxflgsq.write(line_to_write)
                self.dxflgsq.write("\n")
            if (self.small_square_tool_num > 0):
                self.dxfsmsq.write(line_to_write)
                self.dxfsmsq.write("\n")
            if (self.large_ball_tool_num > 0):
                self.dxflgbl.write(line_to_write)
                self.dxflgbl.write("\n")
            if (self.small_ball_tool_num > 0):
                self.dxfsmbl.write(line_to_write)
                self.dxfsmbl.write("\n")
            if (self.large_V_tool_num > 0):
                self.dxflgV.write(line_to_write)
                self.dxflgV.write("\n")
            if (self.small_V_tool_num > 0):
                self.dxfsmV.write(line_to_write)
                self.dxfsmV.write("\n")
            if (self.DT_tool_num > 0):
                self.dxfDT.write(line_to_write)
                self.dxfDT.write("\n")
            if (self.KH_tool_num > 0):
                self.dxfKH.write(line_to_write)
                self.dxfKH.write("\n")
            if (self.Roundover_tool_num > 0):
                self.dxfRt.write(line_to_write)
                self.dxfRt.write("\n")
            if (self.MISC_tool_num > 0):
                self.dxfMt.write(line_to_write)
                self.dxfMt.write("\n")

    def setupstock(self, stockXwidth,
                 stockYheight,
                 stockZthickness,
                 zeroheight,
                 stockzero,
                 retractheight):
        global mpx
        mpx = float(0)
        global mpy
        mpy = float(0)
        global mpz
        mpz = float(0)
        global tpz
        tpz = float(0)
        global currenttoolnum
        currenttoolnum = 102
        global currenttoolshape
        currenttoolshape = cylinder(1.5875,12.7)
        global stock
        self.stock = cube([stockXwidth, stockYheight, stockZthickness])
        if self.generategcode == True:
            self.writegc("(Design File: " + self.basefilename + ")")
        if self.zeroheight == "Top":
            if self.stockzero == "Lower-Left":
                self.stock = stock.translate([0,0,-self.stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, 0.00mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, ",str(stockYheight),"mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, 0.00, ",str(self.stockZthickness),")")
            if self.stockzero == "Center-Left":
                self.stock = self.stock.translate([0,-stockYheight / 2,-stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -",str(self.stockYheight/2),"mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, ",str(self.stockYheight/2),"mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, ",str(self.stockYheight/2),", ",str(self.stockZthickness),")");
            if self.stockzero == "Top-Left":
                self.stock = self.stock.translate([0,-self.stockYheight,-self.stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -",str(self.stockYheight),"mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, 0.00mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, ",str(self.stockYheight),", ",str(self.stockZthickness),")")
            if self.stockzero == "Center":
                self.stock = self.stock.translate([-self.stockXwidth / 2,-self.stockYheight / 2,-self.stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin: -",str(self.stockXwidth/2),", -",str(self.stockYheight/2),"mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth/2),"mm, ",str(self.stockYheight/2),"mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", ",str(self.stockXwidth/2),", ", str(self.stockYheight/2),", ",str(self.stockZthickness),")")
        if self.zeroheight == "Bottom":
            if self.stockzero == "Lower-Left":
                 self.stock = self.stock.translate([0,0,0])
                 if self.generategcode == True:
                     self.writegc("(stockMin:0.00mm, 0.00mm, 0.00mm)")
                     self.writegc("(stockMax:",str(self.stockXwidth),"mm, ",str(self.stockYheight),"mm,  ",str(self.stockZthickness),"mm)")
                     self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, 0.00, 0.00)")
            if self.stockzero == "Center-Left":
                self.stock = self.stock.translate([0,-self.stockYheight / 2,0])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -",str(self.stockYheight/2),"mm, 0.00mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, ",str(self.stockYheight/2),"mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, ",str(self.stockYheight/2),", 0.00mm)");
            if self.stockzero == "Top-Left":
                self.stock = self.stock.translate([0,-self.stockYheight,0])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -",str(self.stockYheight),"mm, 0.00mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, 0.00mm, ",str(self.stockZthickness),"mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, ",str(self.stockYheight),", 0.00)")
            if self.stockzero == "Center":
                self.stock = self.stock.translate([-self.stockXwidth / 2,-self.stockYheight / 2,0])
                if self.generategcode == True:
                    self.writegc("(stockMin: -",str(self.stockXwidth/2),", -",str(self.stockYheight/2),"mm, 0.00mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth/2),"mm, ",str(self.stockYheight/2),"mm, ",str(self.stockZthickness),"mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", ",str(self.stockXwidth/2),", ", str(self.stockYheight/2),", 0.00)")
        if self.generategcode == True:
            self.writegc("G90");
            self.writegc("G21");

    def xpos(self):
        global mpx
        return mpx

    def ypos(self):
        global mpy
        return mpy

    def zpos(self):
        global mpz
        return mpz

    def tzpos(self):
        global tpz
        return tpz

    def setxpos(self, newxpos):
        global mpx
        mpx = newxpos

    def setypos(self, newypos):
        global mpy
        mpy = newypos

    def setzpos(self, newzpos):
        global mpz
        mpz = newzpos

    def settzpos(self, newtzpos):
        global tpz
        tpz = newtzpos

    def settool(self,tn):
        global currenttoolnum
        currenttoolnum = tn

    def currenttoolnumber(self):
        global currenttoolnum
        return currenttoolnum

    def endmill_square(self, es_diameter, es_flute_length):
        return cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center = False)

    def gcp_endmill_ball(self, es_diameter, es_flute_length):
        b = sphere(r=(es_diameter / 2))
        s = cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=False)
        p = union(b,s)
        return p.translate([0, 0, (es_diameter / 2)])

    def gcp_endmill_v(self, es_v_angle, es_diameter):
        es_v_angle = math.radians(es_v_angle)
        v = cylinder(r1=0, r2=(es_diameter / 2), h=((es_diameter / 2) / math.tan((es_v_angle / 2))), center=False)
        s = cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=((es_diameter * 8) ), center=False)
        sh = s.translate([0, 0, ((es_diameter / 2) / math.tan((es_v_angle / 2)))])
        return union(v,sh)

    def gcp_keyhole(self, es_diameter, es_flute_length):
        return cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=false)

    def gcp_keyhole_shaft(self, es_diameter, es_flute_length):
        return cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=false)

    def gcp_dovetail(self, dt_bottomdiameter, dt_topdiameter, dt_height, dt_angle):
        return cylinder(r1=(dt_bottomdiameter / 2), r2=(dt_topdiameter / 2), h= dt_height, center=false)

    def currenttool(self):
        global currenttoolshape
        return self.currenttoolshape

    def toolchange(self,tool_number,speed):
        global currenttoolshape

        self.settool(tool_number)
        if (self.generategcode == True):
            self.writegc("(Toolpath)")
            self.writegc("M05")
        if (tool_number == 201):
            self.writegc("(TOOL/MILL,6.35, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(6.35, 19.05)
        elif (tool_number == 202):
            self.writegc("(TOOL/MILL,6.35, 3.17, 0.00, 0.00)")
            self.currenttoolshape = self.gcp_endmill_ball(6.35, 19.05)
        elif (tool_number == 102):
            self.writegc("(TOOL/MILL,3.17, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(3.175, 12.7)
        elif (tool_number == 101):
            self.writegc("(TOOL/MILL,3.17, 1.58, 0.00, 0.00)")
            self.currenttoolshape = self.gcp_endmill_ball(3.175, 12.7)
        elif (tool_number == 301):
            self.writegc("(TOOL/MILL,0.03, 0.00, 6.35, 45.00)")
            self.currenttoolshape = self.gcp_endmill_v(90, 12.7)
        elif (tool_number == 302):
            self.writegc("(TOOL/MILL,0.03, 0.00, 10.998, 30.00)")
            self.currenttoolshape = self.gcp_endmill_v(60, 12.7)
        elif (tool_number == 390):
            self.writegc("(TOOL/MILL,0.03, 0.00, 1.5875, 45.00)")
            self.currenttoolshape = self.gcp_endmill_v(90, 3.175)
        elif (tool_number == 374):
            self.writegc("(TOOL/MILL,9.53, 0.00, 3.17, 0.00)")
        elif (tool_number == 375):
            self.writegc("(TOOL/MILL,9.53, 0.00, 3.17, 0.00)")
        elif (tool_number == 376):
            self.writegc("(TOOL/MILL,12.7, 0.00, 4.77, 0.00)")
        elif (tool_number == 378):
            self.writegc("(TOOL/MILL,12.7, 0.00, 4.77, 0.00)")
        elif (tool_number == 814):
            writegc("(TOOL/MILL,12.7, 6.367, 12.7, 0.00)")
        self.writegc("M6T",str(tool_number))
        self.writegc("M03S",str(speed))

#def ptool_diameter(ptd_tool, ptd_depth):
# Square 122,112,102,201
#    if ptd_tool == 122:
#        return 0.79375
#    if ptd_tool == 112:
#        return 1.5875
#    if ptd_tool == 102:
#        return 3.175
#    if ptd_tool == 201:
#        return 6.35
## Ball 121,111,101,202
#    if ptd_tool == 122:
#        return
#        if ptd_depth > 0.396875:
#            return 0.79375
#        else:
#            return 0
#    if ptd_tool == 112:
#        if ptd_depth > 0.79375:
#            return 1.5875
#        else:
#            return 0
#    if ptd_tool == 101:
#        if ptd_depth > 1.5875:
#            return 3.175
#        else:
#            return 0
#    if ptd_tool == 202:
#        if ptd_depth > 3.175:
#            return 6.35
#        else:
#            return 0
## V 301, 302, 390
#    if ptd_tool == 301:
#        return 0
#    if ptd_tool == 302:
#        return 0
#    if ptd_tool == 390:
#        return 0
## Keyhole
#    if ptd_tool == 374:
#        if ptd_depth < 3.175:
#            return 9.525
#        else:
#            return 6.35
#    if ptd_tool == 375:
#        if ptd_depth < 3.175:
#            return 9.525
#        else:
#            return 8
#    if ptd_tool == 376:
#        if ptd_depth < 4.7625:
#            return 12.7
#        else:
#            return 6.35
#    if ptd_tool == 378:
#        if ptd_depth < 4.7625:
#            return 12.7
#        else:
#            return 8
## Dovetail
#    if ptd_tool == 814:
#        if ptd_depth > 12.7:
#            return 6.35
#        else:
#            return 12.7
#
#def popengcodefile(fn):
#    global f
#    f = open(fn, "w")
#
#def popendxffile(fn):
#    global dxf
#    dxf = open(fn, "w")
#
#def popendxflgblfile(fn):
#    global dxflgbl
#    dxflgbl = open(fn, "w")
#
#def popendxflgsqfile(fn):
#    global dxflgsq
#    dxflgsq = open(fn, "w")
#
#def popendxflgVfile(fn):
#    global dxflgV
#    dxflgV = open(fn, "w")
#
#def popendxfsmblfile(fn):
#    global dxfsmbl
#    dxfsmbl = open(fn, "w")
#
#def popendxfsmsqfile(fn):
#    global dxfsmsq
#    dxfsmsq = open(fn, "w")
#
#def popendxfsmVfile(fn):
#    global dxfsmV
#    dxfsmV = open(fn, "w")
#
#def popendxfKHfile(fn):
#    global dxfKH
#    dxfKH = open(fn, "w")
#
#def popendxfDTfile(fn):
#    global dxfDT
#    dxfDT = open(fn, "w")
#
#def writedxflgbl(*arguments):
#    line_to_write = ""
#    for element in arguments:
#        line_to_write += element
#    dxflgbl.write(line_to_write)
#    print(line_to_write)
#    dxflgbl.write("\n")
#
#def writedxflgsq(*arguments):
#    line_to_write = ""
#    for element in arguments:
#        line_to_write += element
#    dxflgsq.write(line_to_write)
#    print(line_to_write)
#    dxflgsq.write("\n")
#
#def writedxflgV(*arguments):
#    line_to_write = ""
#    for element in arguments:
#        line_to_write += element
#    dxflgV.write(line_to_write)
#    print(line_to_write)
#    dxflgV.write("\n")
#
#def writedxfsmbl(*arguments):
#    line_to_write = ""
#    for element in arguments:
#        line_to_write += element
#    dxfsmbl.write(line_to_write)
#    print(line_to_write)
#    dxfsmbl.write("\n")
#
#def writedxfsmsq(*arguments):
#    line_to_write = ""
#    for element in arguments:
#        line_to_write += element
#    dxfsmsq.write(line_to_write)
#    print(line_to_write)
#    dxfsmsq.write("\n")
#
#def writedxfsmV(*arguments):
#    line_to_write = ""
#    for element in arguments:
#        line_to_write += element
#    dxfsmV.write(line_to_write)
#    print(line_to_write)
#    dxfsmV.write("\n")
#
#def writedxfKH(*arguments):
#    line_to_write = ""
#    for element in arguments:
#        line_to_write += element
#    dxfKH.write(line_to_write)
#    print(line_to_write)
#    dxfKH.write("\n")
#
#def writedxfDT(*arguments):
#    line_to_write = ""
#    for element in arguments:
#        line_to_write += element
#    dxfDT.write(line_to_write)
#    print(line_to_write)
#    dxfDT.write("\n")
#
    def dxfpreamble(self, tn):
#        self.writedxf(tn,str(tn))
        self.writedxf(tn,"0")
        self.writedxf(tn,"SECTION")
        self.writedxf(tn,"2")
        self.writedxf(tn,"ENTITIES")

    def dxfpolyline(self, tn, xbegin,ybegin,xend,yend):
        self.writedxf(tn,"0")
        self.writedxf(tn,"LWPOLYLINE")
        self.writedxf(tn,"90")
        self.writedxf(tn,"2")
        self.writedxf(tn,"70")
        self.writedxf(tn,"0")
        self.writedxf(tn,"43")
        self.writedxf(tn,"0")
        self.writedxf(tn,"10")
        self.writedxf(tn,str(xbegin))
        self.writedxf(tn,"20")
        self.writedxf(tn,str(ybegin))
        self.writedxf(tn,"10")
        self.writedxf(tn,str(xend))
        self.writedxf(tn,"20")
        self.writedxf(tn,str(yend))

    def dxfpostamble(self,tn):
#        self.writedxf(tn,str(tn))
        self.writedxf(tn,"0")
        self.writedxf(tn,"ENDSEC")
        self.writedxf(tn,"0")
        self.writedxf(tn,"EOF")

    def gcodepostamble(self):
        self.writegc("Z12.700")
        self.writegc("M05")
        self.writegc("M02")

    def closegcodefile(self):
        self.gcodepostamble()
        self.gc.close()

    def closedxffile(self):
        if self.generatedxf == True:
            self.dxfpostamble(-1)
            self.dxf.close()

    def closedxffiles(self):
        if self.generatedxfs == True:
            if (self.large_square_tool_num > 0):
                self.dxfpostamble(self.large_square_tool_num)
            if (self.small_square_tool_num > 0):
                self.dxfpostamble(self.small_square_tool_num)
            if (self.large_ball_tool_num > 0):
                self.dxfpostamble(self.large_ball_tool_num)
            if (self.small_ball_tool_num > 0):
                self.dxfpostamble(self.small_ball_tool_num)
            if (self.large_V_tool_num > 0):
                self.dxfpostamble(self.large_V_tool_num)
            if (self.small_V_tool_num > 0):
                self.dxfpostamble(self.small_V_tool_num)
            if (self.DT_tool_num > 0):
                self.dxfpostamble(self.DT_tool_num)
            if (self.KH_tool_num > 0):
                self.dxfpostamble(self.KH_tool_num)
            if (self.Roundover_tool_num > 0):
                self.dxfpostamble(self.Roundover_tool_num)
            if (self.MISC_tool_num > 0):
                self.dxfpostamble(self.MISC_tool_num)

            if (self.large_square_tool_num > 0):
                self.dxflgsq.close()
            if (self.small_square_tool_num > 0):
                self.dxfsmsq.close()
            if (self.large_ball_tool_num > 0):
                self.dxflgbl.close()
            if (self.small_ball_tool_num > 0):
                self.dxfsmbl.close()
            if (self.large_V_tool_num > 0):
                self.dxflgV.close()
            if (self.small_V_tool_num > 0):
                self.dxfsmV.close()
            if (self.DT_tool_num > 0):
                self.dxfDT.close()
            if (self.KH_tool_num > 0):
                self.dxfKH.close()
            if (self.Roundover_tool_num > 0):
                self.dxfRt.close()
            if (self.MISC_tool_num > 0):
                self.dxfMt.close()

    def movetosafeZ(self):
#        global toolpaths
        self.writegc("(Move to safe Z to avoid workholding)")
        self.writegc("G53G0Z-5.000")
        self.setzpos(self.retractheight)
        toolpath = cylinder(1.5875,12.7)
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
#        self.toolpaths = union([self.toolpaths, toolpath])
        return toolpath

    def rapid(self, ex, ey, ez):
#        global toolpath
#        global toolpaths
        self.writegc("G00 X", str(ex), " Y", str(ey), " Z", str(ez))
        start = self.currenttool()
        start = start.translate([self.xpos(), self.ypos(), self.zpos()])
        toolpath = hull(start, start.translate([ex,ey,ez]))
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
#        self.toolpaths = union([self.toolpaths, toolpath])
        return toolpath

    def rapidXY(self, ex, ey):
#        global toolpath
#        global toolpaths
        self.writegc("G00 X", str(ex), " Y", str(ey))
        start = self.currenttool()
        start = start.translate([self.xpos(), self.ypos(), self.zpos()])
        toolpath = hull(start, start.translate([ex,ey,self.zpos()]))
        self.setxpos(ex)
        self.setypos(ey)
#        self.toolpaths = union([self.toolpaths, toolpath])
        return toolpath

    def rapidZ(self, ez):
#        global toolpath
#        global toolpaths
        self.writegc("G00 Z", str(ez))
        start = self.currenttool()
        start = start.translate([self.xpos(), self.ypos(), self.zpos()])
        toolpath = hull(start, start.translate([self.xpos(),self.ypos(),ez]))
        self.setzpos(ez)
#        self.toolpaths = union([self.toolpaths, toolpath])
        return toolpath

    def cutlinedxfgc(self,ex, ey, ez):
#        global toolpath
#        global toolpaths
        self.dxfpolyline(self.currenttool(), self.xpos(), self.ypos(), ex, ey)
        self.writegc("G01 X", str(ex), " Y", str(ey), " Z", str(ez))
        start = self.currenttool()
        start = start.translate([self.xpos(), self.ypos(), self.zpos()])
        end = self.currenttool()
        toolpath = hull(start, end.translate([ex,ey,ez]))
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
#        self.toolpaths = union([self.toolpaths, toolpath])
        return toolpath

    def cutline(self,ex, ey, ez):
#        global toolpath
#        global toolpaths
        start = self.currenttool()
        start = start.translate([self.xpos(), self.ypos(), self.zpos()])
        end = self.currenttool()
        toolpath = hull(start, end.translate([ex,ey,ez]))
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
#        self.toolpaths = union([self.toolpaths, toolpath])
        return toolpath

    def arcloop(self, barc, earc, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        i = barc
        while i < earc:
            toolpath = toolpath.union(self.cutline(xcenter + radius * math.cos(math.radians(i)), ycenter + radius * math.sin(math.radians(i)), self.zpos()-(self.tzpos())))
            self.setxpos(xcenter + radius * math.cos(math.radians(i)))
            self.setypos(ycenter + radius * math.sin(math.radians(i)))
            i += 1
#        self.dxfarc(xcenter, ycenter, radius, barc, earc, self.currenttoolnumber())
        return toolpath

    def narcloop(barc,earc, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        i = barc
        while i > earc:
            toolpath = toolpath.union(self.cutline(xcenter + radius * math.cos(math.radians(i)), ycenter + radius * math.sin(math.radians(i)), self.zpos()-(self.tzpos())))
            self.setxpos(xcenter + radius * math.cos(math.radians(i)))
            self.setypos(ycenter + radius * math.sin(math.radians(i)))
            print(str(self.xpos()), str(self.ypos()))
            i += -1
#        self.dxfarc(xcenter, ycenter, radius, barc, earc, self.currenttoolnumber())
        return toolpath

    def dxfarc(self, xcenter, ycenter, radius, anglebegin, endangle, tn):
        if (self.generatedxf == True):
            self.writedxf(tn, "0")
            self.writedxf(tn, "ARC")
            self.writedxf(tn, "10")
            self.writedxf(tn, str(xcenter))
            self.writedxf(tn, "20")
            self.writedxf(tn, str(ycenter))
            self.writedxf(tn, "40")
            self.writedxf(tn, str(radius))
            self.writedxf(tn, "50")
            self.writedxf(tn, str(anglebegin))
            self.writedxf(tn, "51")
            self.writedxf(tn, str(endangle))

    def gcodearc(self, xcenter, ycenter, radius, anglebegin, endangle, tn):
        if (self.generategcode == True):
            self.writegc(tn, "(0)")

    def cutarcNECCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(xcenter,ycenter,radius,0,90, self.currenttoolnumber())
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
        toolpath = self.arcloop(1,90, xcenter, ycenter, radius)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        return toolpath

    def cutarcNWCCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(xcenter,ycenter,radius,90,180, self.currenttoolnumber())
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
        toolpath = self.arcloop(91,180, xcenter, ycenter, radius)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        return toolpath

    def cutarcSWCCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(xcenter,ycenter,radius,180,270, self.currenttoolnumber())
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
        toolpath = self.arcloop(181,270, xcenter, ycenter, radius)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        return toolpath

    def cutarcSECCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(xcenter,ycenter,radius,270,360, self.currenttoolnumber())
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
        toolpath = self.arcloop(271,360, xcenter, ycenter, radius)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        return toolpath

    def cutarcNECWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(xcenter,ycenter,radius,0,90, self.currenttoolnumber())
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
        toolpath = self.narcloop(89,0, xcenter, ycenter, radius)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        return toolpath

    def cutarcSECWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(xcenter,ycenter,radius,270,360, self.currenttoolnumber())
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
        toolpath = self.narcloop(359,270, xcenter, ycenter, radius)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        return toolpath

    def cutarcSWCWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(xcenter,ycenter,radius,180,270, self.currenttoolnumber())
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
        toolpath = self.narcloop(269,180, xcenter, ycenter, radius)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        return toolpath

    def cutarcNWCWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
        toolpath = self.currenttool()
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(xcenter,ycenter,radius,90,180, self.currenttoolnumber())
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
        toolpath = self.narcloop(179,90, xcenter, ycenter, radius)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        return toolpath

