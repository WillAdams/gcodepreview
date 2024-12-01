#!/usr/bin/env python
#icon "C:\Program Files\PythonSCAD\bin\openscad.exe"  --trust-python
#Currently tested with 2024.09.23 and Python 3.11
#gcodepreview 0.7, for use with OpenPythonSCAD,
#if using from OpenPythonSCAD see gcodepreview.scad

import sys

# getting openscad functions into namespace
#https://github.com/gsohler/openscad/issues/39
try:
    from openscad import *
except ModuleNotFoundError as e:
    print("OpenSCAD module not loaded.")

# add math functions (using radians by default, convert to degrees where necessary)
import math

def gcpversion():
    return 0.71

class gcodepreview:

    def __init__(self, #basefilename = "export",
                 generatescad = False,
                 generategcode = False,
                 generatedxf = False,
#                 stockXwidth = 25,
#                 stockYheight = 25,
#                 stockZthickness = 1,
#                 zeroheight = "Top",
#                 stockzero = "Lower-left" ,
#                 retractheight = 6,
#                 currenttoolnum = 102,
#                 toolradius = 3.175,
#                 plunge = 100,
#                 feed = 400,
#                 speed = 10000
                  ):
#        self.basefilename = basefilename
        self.generatescad = generatescad
        self.generategcode = generategcode
        self.generatedxf = generatedxf
#        self.stockXwidth = stockXwidth
#        self.stockYheight = stockYheight
#        self.stockZthickness = stockZthickness
#        self.zeroheight = zeroheight
#        self.stockzero = stockzero
#        self.retractheight = retractheight
#        self.currenttoolnum = currenttoolnum
#        self.toolradius = toolradius
#        self.plunge = plunge
#        self.feed = feed
#        self.speed = speed
#        global toolpaths
#        self.toolpaths = cylinder(1.5875, 12.7)
#        global generatedxfs
#        if (self.generatescad == True):
        self.generatedxfs = False

    def opengcodefile(self, basefilename = "export",
                      currenttoolnum = 102,
                      toolradius = 3.175,
                      plunge = 400,
                      feed = 1600,
                      speed = 10000
                      ):
        self.currenttoolnum = currenttoolnum
        self.toolradius = toolradius
        self.plunge = plunge
        self.feed = feed
        self.speed = speed
        if self.generategcode == True:
            self.gcodefilename = basefilename + ".nc"
            self.gc = open(self.gcodefilename, "w")

    def opendxffile(self, basefilename = "export"):
        self.basefilename = basefilename
#        global generatedxfs
#        global dxfclosed
        self.dxfclosed = False
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
#        global generatedxfs
        self.basefilename = basefilename
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
#                print("Opening ", str(self.dxflgsqfilename))
                self.dxflgsq = open(self.dxflgsqfilename, "w")
            if (small_square_tool_num > 0):
#                print("Opening small square")
                self.dxfsmsqfilename = basefilename + str(small_square_tool_num) + ".dxf"
                self.dxfsmsq = open(self.dxfsmsqfilename, "w")
            if (large_ball_tool_num > 0):
#                print("Opening large ball")
                self.dxflgblfilename = basefilename + str(large_ball_tool_num) + ".dxf"
                self.dxflgbl = open(self.dxflgblfilename, "w")
            if (small_ball_tool_num > 0):
#                print("Opening small ball")
                self.dxfsmblfilename = basefilename + str(small_ball_tool_num) + ".dxf"
                self.dxfsmbl = open(self.dxfsmblfilename, "w")
            if (large_V_tool_num > 0):
#                print("Opening large V")
                self.dxflgVfilename = basefilename + str(large_V_tool_num) + ".dxf"
                self.dxflgV = open(self.dxflgVfilename, "w")
            if (small_V_tool_num > 0):
#                print("Opening small V")
                self.dxfsmVfilename = basefilename + str(small_V_tool_num) + ".dxf"
                self.dxfsmV = open(self.dxfsmVfilename, "w")
            if (DT_tool_num > 0):
#                print("Opening DT")
                self.dxfDTfilename = basefilename + str(DT_tool_num) + ".dxf"
                self.dxfDT = open(self.dxfDTfilename, "w")
            if (KH_tool_num > 0):
#                print("Opening KH")
                self.dxfKHfilename = basefilename + str(KH_tool_num) + ".dxf"
                self.dxfKH = open(self.dxfKHfilename, "w")
            if (Roundover_tool_num > 0):
#                print("Opening Rt")
                self.dxfRtfilename = basefilename + str(Roundover_tool_num) + ".dxf"
                self.dxfRt = open(self.dxfRtfilename, "w")
            if (MISC_tool_num > 0):
#                print("Opening Mt")
                self.dxfMtfilename = basefilename + str(MISC_tool_num) + ".dxf"
                self.dxfMt = open(self.dxfMtfilename, "w")
            if (large_square_tool_num > 0):
                self.dxfpreamble(large_square_tool_num)
            if (small_square_tool_num > 0):
                self.dxfpreamble(small_square_tool_num)
            if (large_ball_tool_num > 0):
                self.dxfpreamble(large_ball_tool_num)
            if (small_ball_tool_num > 0):
                self.dxfpreamble(small_ball_tool_num)
            if (large_V_tool_num > 0):
                self.dxfpreamble(large_V_tool_num)
            if (small_V_tool_num > 0):
                self.dxfpreamble(small_V_tool_num)
            if (DT_tool_num > 0):
                self.dxfpreamble(DT_tool_num)
            if (KH_tool_num > 0):
                self.dxfpreamble(KH_tool_num)
            if (Roundover_tool_num > 0):
                self.dxfpreamble(Roundover_tool_num)
            if (MISC_tool_num > 0):
                self.dxfpreamble(MISC_tool_num)

    def writegc(self, *arguments):
        line_to_write = ""
        for element in arguments:
            line_to_write += element
        self.gc.write(line_to_write)
        self.gc.write("\n")

    def writedxf(self, toolnumber, *arguments):
#        global dxfclosed
        line_to_write = ""
        for element in arguments:
            line_to_write += element
        if self.generatedxf == True:
            if self.dxfclosed == False:
                self.dxf.write(line_to_write)
                self.dxf.write("\n")
        if self.generatedxfs == True:
            self.writedxfs(toolnumber, line_to_write)

    def writedxfs(self, toolnumber, line_to_write):
#        print("Processing writing toolnumber", toolnumber)
#        line_to_write = ""
#        for element in arguments:
#            line_to_write += element
        if (toolnumber == 0):
            return
        elif self.generatedxfs == True:
            if (self.large_square_tool_num == toolnumber):
                self.dxflgsq.write(line_to_write)
                self.dxflgsq.write("\n")
            if (self.small_square_tool_num == toolnumber):
                self.dxfsmsq.write(line_to_write)
                self.dxfsmsq.write("\n")
            if (self.large_ball_tool_num == toolnumber):
                self.dxflgbl.write(line_to_write)
                self.dxflgbl.write("\n")
            if (self.small_ball_tool_num == toolnumber):
                self.dxfsmbl.write(line_to_write)
                self.dxfsmbl.write("\n")
            if (self.large_V_tool_num == toolnumber):
                self.dxflgV.write(line_to_write)
                self.dxflgV.write("\n")
            if (self.small_V_tool_num == toolnumber):
                self.dxfsmV.write(line_to_write)
                self.dxfsmV.write("\n")
            if (self.DT_tool_num == toolnumber):
                self.dxfDT.write(line_to_write)
                self.dxfDT.write("\n")
            if (self.KH_tool_num == toolnumber):
                self.dxfKH.write(line_to_write)
                self.dxfKH.write("\n")
            if (self.Roundover_tool_num == toolnumber):
                self.dxfRt.write(line_to_write)
                self.dxfRt.write("\n")
            if (self.MISC_tool_num == toolnumber):
                self.dxfMt.write(line_to_write)
                self.dxfMt.write("\n")

    def setupstock(self, stockXwidth,
                 stockYheight,
                 stockZthickness,
                 zeroheight,
                 stockzero,
                 retractheight):
        self.stockXwidth = stockXwidth
        self.stockYheight = stockYheight
        self.stockZthickness = stockZthickness
        self.zeroheight = zeroheight
        self.stockzero = stockzero
        self.retractheight = retractheight
#        global mpx
        self.mpx = float(0)
#        global mpy
        self.mpy = float(0)
#        global mpz
        self.mpz = float(0)
#        global tpz
        self.tpz = float(0)
#        global currenttoolnum
        self.currenttoolnum = 102
#        global currenttoolshape
        self.currenttoolshape = cylinder(12.7, 1.5875)
#        global stock
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
#        global mpx
        return self.mpx

    def ypos(self):
#        global mpy
        return self.mpy

    def zpos(self):
#        global mpz
        return self.mpz

    def tzpos(self):
#        global tpz
        return self.tpz

    def setxpos(self, newxpos):
#        global mpx
        self.mpx = newxpos

    def setypos(self, newypos):
#        global mpy
        self.mpy = newypos

    def setzpos(self, newzpos):
#        global mpz
        self.mpz = newzpos

    def settzpos(self, newtzpos):
#        global tpz
        self.tpz = newtzpos

    def settool(self,tn):
#        global currenttoolnum
        self.currenttoolnum = tn

    def currenttoolnumber(self):
#        global currenttoolnum
        return self.currenttoolnum

    def currentroundovertoolnumber(self):
#        global Roundover_tool_num
        return self.Roundover_tool_num

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
        return cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=False)

    def gcp_keyhole_shaft(self, es_diameter, es_flute_length):
        return cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=False)

    def gcp_dovetail(self, dt_bottomdiameter, dt_topdiameter, dt_height, dt_angle):
        return cylinder(r1=(dt_bottomdiameter / 2), r2=(dt_topdiameter / 2), h= dt_height, center=False)

    def currenttool(self):
#        global currenttoolshape
        return self.currenttoolshape

    def toolchange(self,tool_number,speed):
#        global currenttoolshape
        self.currenttoolshape = self.endmill_square(0.001, 0.001)

        self.settool(tool_number)
        if (self.generategcode == True):
            self.writegc("(Toolpath)")
            self.writegc("M05")
        if (tool_number == 201):
            self.writegc("(TOOL/MILL,6.35, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(6.35, 19.05)
        elif (tool_number == 102):
            self.writegc("(TOOL/MILL,3.175, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(3.175, 12.7)
        elif (tool_number == 112):
            self.writegc("(TOOL/MILL,1.5875, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(1.5875, 6.35)
        elif (tool_number == 122):
            self.writegc("(TOOL/MILL,0.79375, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(0.79375, 1.5875)
        elif (tool_number == 202):
            self.writegc("(TOOL/MILL,6.35, 3.175, 0.00, 0.00)")
            self.currenttoolshape = self.gcp_endmill_ball(6.35, 19.05)
        elif (tool_number == 101):
            self.writegc("(TOOL/MILL,3.175, 1.5875, 0.00, 0.00)")
            self.currenttoolshape = self.gcp_endmill_ball(3.175, 12.7)
        elif (tool_number == 111):
            self.writegc("(TOOL/MILL,1.5875, 0.79375, 0.00, 0.00)")
            self.currenttoolshape = self.gcp_endmill_ball(1.5875, 6.35)
        elif (tool_number == 121):
            self.writegc("(TOOL/MILL,3.175, 0.79375, 0.00, 0.00)")
            self.currenttoolshape = self.gcp_endmill_ball(0.79375, 1.5875)
        elif (tool_number == 327):
            self.writegc("(TOOL/MILL,0.03, 0.00, 13.4874, 30.00)")
            self.currenttoolshape = self.gcp_endmill_v(60, 26.9748)
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
            self.writegc("(TOOL/MILL,12.7, 6.367, 12.7, 0.00)")
            #dt_bottomdiameter, dt_topdiameter, dt_height, dt_angle)
            #https://www.leevalley.com/en-us/shop/tools/power-tool-accessories/router-bits/30172-dovetail-bits?item=18J1607
            self.currenttoolshape = self.gcp_dovetail(12.7, 6.367, 12.7, 14)
        elif (tool_number == 56125):#0.508/2, 1.531
            self.writegc("(TOOL/CRMILL, 0.508, 6.35, 3.175, 7.9375, 3.175)")
        elif (tool_number == 56142):#0.508/2, 2.921
            self.writegc("(TOOL/CRMILL, 0.508, 3.571875, 1.5875, 5.55625, 1.5875)")
#        elif (tool_number == 312):#1.524/2, 3.175
#            self.writegc("(TOOL/CRMILL, Diameter1, Diameter2,Radius, Height, Length)")
        elif (tool_number == 1570):#0.507/2, 4.509
            self.writegc("(TOOL/CRMILL, 0.17018, 9.525, 4.7625, 12.7, 4.7625)")
        self.writegc("M6T",str(tool_number))
        self.writegc("M03S",str(speed))

    def tool_diameter(self, ptd_tool, ptd_depth):
# Square 122,112,102,201
        if ptd_tool == 122:
            return 0.79375
        if ptd_tool == 112:
            return 1.5875
        if ptd_tool == 102:
            return 3.175
        if ptd_tool == 201:
            return 6.35
# Ball 121,111,101,202
        if ptd_tool == 122:
            if ptd_depth > 0.396875:
                return 0.79375
            else:
                return ptd_tool
        if ptd_tool == 112:
            if ptd_depth > 0.79375:
                return 1.5875
            else:
                return ptd_tool
        if ptd_tool == 101:
            if ptd_depth > 1.5875:
                return 3.175
            else:
                return ptd_tool
        if ptd_tool == 202:
            if ptd_depth > 3.175:
                return 6.35
            else:
                return ptd_tool
# V 301, 302, 390
        if ptd_tool == 301:
            return ptd_tool
        if ptd_tool == 302:
            return ptd_tool
        if ptd_tool == 390:
            return ptd_tool
# Keyhole
        if ptd_tool == 374:
            if ptd_depth < 3.175:
                return 9.525
            else:
                return 6.35
        if ptd_tool == 375:
            if ptd_depth < 3.175:
                return 9.525
            else:
                return 8
        if ptd_tool == 376:
            if ptd_depth < 4.7625:
                return 12.7
            else:
                return 6.35
        if ptd_tool == 378:
            if ptd_depth < 4.7625:
                return 12.7
            else:
                return 8
# Dovetail
        if ptd_tool == 814:
            if ptd_depth > 12.7:
                return 6.35
            else:
                return 12.7

    def tool_radius(self, ptd_tool, ptd_depth):
        tr = self.tool_diameter(ptd_tool, ptd_depth)/2
        return tr

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

    def dxfline(self, tn, xbegin,ybegin,xend,yend):
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
#            global dxfclosed
            self.dxfclosed = True
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

    def cutline(self,ex, ey, ez):
#        global toolpath
#        global toolpaths
#        print("cutline tool #", self.currenttoolnumber())
        if (self.currenttoolnumber() == 56142):
#                print("cutline tool internal #", self.currenttoolnumber())
            toolpath = self.cutroundovertool(self.xpos(), self.ypos(), self.zpos(), ex, ey, ez, 0.508/2, 1.531)
        elif (self.currenttoolnumber() == 56125):
            toolpath = self.cutroundovertool(self.xpos(), self.ypos(), self.zpos(), ex, ey, ez, 0.508/2, 2.921)
#        elif (self.currenttoolnumber() == 312):
#            toolpath = self.cutroundovertool(self.xpos(), self.ypos(), self.zpos(), ex, ey, ez, 1.524/2, 3.175)
        elif (self.currenttoolnumber() == 1570):
            toolpath = self.cutroundovertool(self.xpos(), self.ypos(), self.zpos(), ex, ey, ez, 0.507/2, 4.509)
        elif (self.currenttoolnumber() == 374):
#            self.writegc("(TOOL/MILL,9.53, 0.00, 3.17, 0.00)")
            shaft = cylinder(9.525, 6.35/2, 6.35/2)
            shaftend = shaft
            shaftbegin = shaft.translate([self.xpos(), self.ypos(), self.zpos()])
            shaftpath = hull(shaftbegin, shaftend.translate([ex,ey,ez]))
            start = cylinder(3.175, 9.525/2, 9.525/2)
            end = start
            start = start.translate([self.xpos(), self.ypos(), self.zpos()])
            cutpath = hull(start, end.translate([ex,ey,ez]))
            toolpath = union(shaftpath, cutpath)
        elif (self.currenttoolnumber() == 375):
#            self.writegc("(TOOL/MILL,9.53, 0.00, 3.17, 0.00)")
            shaft = cylinder(9.525, 8/2, 8/2)
            shaftend = shaft
            shaftbegin = shaft.translate([self.xpos(), self.ypos(), self.zpos()])
            shaftpath = hull(shaftbegin, shaftend.translate([ex,ey,ez]))
            start = cylinder(3.175, 9.525/2, 9.525/2)
            end = start
            start = start.translate([self.xpos(), self.ypos(), self.zpos()])
            cutpath = hull(start, end.translate([ex,ey,ez]))
            toolpath = union(shaftpath, cutpath)
        elif (self.currenttoolnumber() == 376):
#            self.writegc("(TOOL/MILL,12.7, 0.00, 4.77, 0.00)")
            shaft = cylinder(9.525, 6.35/2, 6.35/2)
            shaftend = shaft
            shaftbegin = shaft.translate([self.xpos(), self.ypos(), self.zpos()])
            shaftpath = hull(shaftbegin, shaftend.translate([ex,ey,ez]))
            start = cylinder(3.175, 12.7/2, 12.7/2)
            end = start
            start = start.translate([self.xpos(), self.ypos(), self.zpos()])
            cutpath = hull(start, end.translate([ex,ey,ez]))
            toolpath = union(shaftpath, cutpath)
        elif (self.currenttoolnumber() == 378):
#            self.writegc("(TOOL/MILL,12.7, 0.00, 4.77, 0.00)")
            shaft = cylinder(9.525, 8/2, 8/2)
            shaftend = shaft
            shaftbegin = shaft.translate([self.xpos(), self.ypos(), self.zpos()])
            shaftpath = hull(shaftbegin, shaftend.translate([ex,ey,ez]))
            start = cylinder(3.175, 12.7/2, 12.7/2)
            end = start
            start = start.translate([self.xpos(), self.ypos(), self.zpos()])
            cutpath = hull(start, end.translate([ex,ey,ez]))
            toolpath = union(shaftpath, cutpath)
        else:
            start = self.currenttool()
            start = start.translate([self.xpos(), self.ypos(), self.zpos()])
            end = self.currenttool()
            toolpath = hull(start, end.translate([ex,ey,ez]))
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
#        self.toolpaths = union([self.toolpaths, toolpath])
        return toolpath

    def cutZgcfeed(self, ez, feed):
        self.writegc("G01 Z", str(ez), "F",str(feed))
        return self.cutline(self.xpos(),self.ypos(),ez)

    def cutlinedxfgc(self,ex, ey, ez):
        self.dxfline(self.currenttoolnumber(), self.xpos(), self.ypos(), ex, ey)
        self.writegc("G01 X", str(ex), " Y", str(ey), " Z", str(ez))
        return self.cutline(ex, ey, ez)

    def cutlinedxfgcfeed(self,ex, ey, ez, feed):
        self.dxfline(self.currenttoolnumber(), self.xpos(), self.ypos(), ex, ey)
        self.writegc("G01 X", str(ex), " Y", str(ey), " Z", str(ez), " F", str(feed))
        return self.cutline(ex, ey, ez)

    def cutroundovertool(self, bx, by, bz, ex, ey, ez, tool_radius_tip, tool_radius_width):
#        n = 90 + fn*3
#        print("Tool dimensions", tool_radius_tip, tool_radius_width, "begin ",bx, by, bz,"end ", ex, ey, ez)
        step = 4 #360/n
        shaft = cylinder(step,tool_radius_tip,tool_radius_tip)
        toolpath = hull(shaft.translate([bx,by,bz]), shaft.translate([ex,ey,ez]))
        shaft = cylinder(tool_radius_width*2,tool_radius_tip+tool_radius_width,tool_radius_tip+tool_radius_width)
        toolpath = toolpath.union(hull(shaft.translate([bx,by,bz+tool_radius_width]), shaft.translate([ex,ey,ez+tool_radius_width])))
        for i in range(1, 90, 1):
            angle = i
            dx = tool_radius_width*math.cos(math.radians(angle))
            dxx = tool_radius_width*math.cos(math.radians(angle+1))
            dzz = tool_radius_width*math.sin(math.radians(angle))
            dz = tool_radius_width*math.sin(math.radians(angle+1))
            dh = abs(dzz-dz)+0.0001
            slice = cylinder(dh,tool_radius_tip+tool_radius_width-dx,tool_radius_tip+tool_radius_width-dxx)
            toolpath = toolpath.union(hull(slice.translate([bx,by,bz+dz]), slice.translate([ex,ey,ez+dz])))
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
#        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, barc, earc)
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
#            print(str(self.xpos()), str(self.ypos()))
            i += -1
#        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, barc, earc)
        return toolpath

    def dxfarc(self, tn, xcenter, ycenter, radius, anglebegin, endangle):
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
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,0,90)
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
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,90,180)
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
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,180,270)
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
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,270,360)
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
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,0,90)
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
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,270,360)
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
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,180,270)
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
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,90,180)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
        toolpath = self.narcloop(179,90, xcenter, ycenter, radius)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        return toolpath

    def arcCCgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.writegc("G03 X", str(ex), " Y", str(ey), " Z", str(ez), " R", str(radius))

    def arcCWgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.writegc("G02 X", str(ex), " Y", str(ey), " Z", str(ez), " R", str(radius))

    def cutarcNECCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        return self.cutarcNECCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcNWCCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        return self.cutarcNWCCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSWCCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        return self.cutarcSWCCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSECCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        return self.cutarcSECCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcNECWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        return self.cutarcNECWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSECWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        return self.cutarcSECWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSWCWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        return self.cutarcSWCWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcNWCWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        return self.cutarcNWCWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutkeyholegcdxf(self, kh_start_depth, kh_max_depth, kht_direction, kh_distance, kh_tool_num):
        if (kht_direction == "N"):
            toolpath = self.cutKHgcdxf(kh_start_depth, kh_max_depth, 90, kh_distance, kh_tool_num)
            return toolpath
        elif (kht_direction == "S"):
            toolpath = self.cutKHgcdxf(kh_start_depth, kh_max_depth, 270, kh_distance, kh_tool_num)
            return toolpath
        elif (kht_direction == "E"):
            toolpath = self.cutKHgcdxf(kh_start_depth, kh_max_depth, 0, kh_distance, kh_tool_num)
            return toolpath
        elif (kht_direction == "W"):
            toolpath = self.cutKHgcdxf(kh_start_depth, kh_max_depth, 180, kh_distance, kh_tool_num)
            return toolpath

    def cutKHgcdxf(self, kh_start_depth, kh_max_depth, kh_angle, kh_distance, kh_tool_num):
        oXpos = self.xpos()
        oYpos = self.ypos()
#Circle at entry hole
#    def dxfarc(self, xcenter, ycenter, radius, anglebegin, endangle, tn):
#        print(self.tool_radius(kh_tool_num, 7))
        self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 7),  0, 90)
        self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 7), 90,180)
        self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 7),180,270)
        self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 7),270,360)
        toolpath = self.cutline(self.xpos(), self.ypos(), -kh_max_depth)

#pre-calculate needed values
        r = self.tool_radius(kh_tool_num, 7)
#        print(r)
        rt = self.tool_radius(kh_tool_num, 1)
#        print(rt)
        ro = math.sqrt((self.tool_radius(kh_tool_num, 1))**2-(self.tool_radius(kh_tool_num, 7))**2)
#        print(ro)
        angle = math.degrees(math.acos(ro/rt))
#Outlines of entry hole and slot
        if (kh_angle == 0):
#Lower left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),180,270)
#Upper left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),90,180)
#Upper right of entry hole
#            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 41.810, 90)
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, angle, 90)
#Lower right of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 270, 360-angle)
#            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),270, 270+math.acos(math.radians(self.tool_diameter(kh_tool_num, 5)/self.tool_diameter(kh_tool_num, 1))))
#Actual line of cut
#            self.dxfline(kh_tool_num, self.xpos(),self.ypos(),self.xpos()+kh_distance,self.ypos())
#upper right of end of slot (kh_max_depth+4.36))/2
            self.dxfarc(kh_tool_num, self.xpos()+kh_distance,self.ypos(),self.tool_diameter(kh_tool_num, (kh_max_depth+4.36))/2,0,90)
#lower right of end of slot
            self.dxfarc(kh_tool_num, self.xpos()+kh_distance,self.ypos(),self.tool_diameter(kh_tool_num, (kh_max_depth+4.36))/2,270,360)
#upper right slot
            self.dxfline(kh_tool_num, self.xpos()+ro, self.ypos()-(self.tool_diameter(kh_tool_num,7)/2), self.xpos()+kh_distance, self.ypos()-(self.tool_diameter(kh_tool_num,7)/2))
#            self.dxfline(kh_tool_num, self.xpos()+(sqrt((self.tool_diameter(kh_tool_num,1)^2)-(self.tool_diameter(kh_tool_num,5)^2))/2), self.ypos()+self.tool_diameter(kh_tool_num, (kh_max_depth))/2, ( (kh_max_depth-6.34))/2)^2-(self.tool_diameter(kh_tool_num, (kh_max_depth-6.34))/2)^2, self.xpos()+kh_distance, self.ypos()+self.tool_diameter(kh_tool_num, (kh_max_depth))/2, kh_tool_num)
#end position at top of slot
#lower right slot
            self.dxfline(kh_tool_num, self.xpos()+ro, self.ypos()+(self.tool_diameter(kh_tool_num,7)/2), self.xpos()+kh_distance, self.ypos()+(self.tool_diameter(kh_tool_num,7)/2))
#        dxfline(kh_tool_num, self.xpos()+(sqrt((self.tool_diameter(kh_tool_num,1)^2)-(self.tool_diameter(kh_tool_num,5)^2))/2), self.ypos()-self.tool_diameter(kh_tool_num, (kh_max_depth))/2, ( (kh_max_depth-6.34))/2)^2-(self.tool_diameter(kh_tool_num, (kh_max_depth-6.34))/2)^2, self.xpos()+kh_distance, self.ypos()-self.tool_diameter(kh_tool_num, (kh_max_depth))/2, KH_tool_num)
#end position at top of slot
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos()+kh_distance, ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
#    cutwithfeed(getxpos()+kh_distance,getypos(),-kh_max_depth,feed);
#    setxpos(getxpos()-kh_distance);
#  } else if (kh_angle > 0 && kh_angle < 90) {
#//echo(kh_angle);
#  dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,90+kh_angle,180+kh_angle, KH_tool_num);
#  dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,180+kh_angle,270+kh_angle, KH_tool_num);
#dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)),90+kh_angle, KH_tool_num);
#dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,270+kh_angle,360+kh_angle-asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)), KH_tool_num);
#dxfarc(getxpos()+(kh_distance*cos(kh_angle)),
#  getypos()+(kh_distance*sin(kh_angle)),tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,0+kh_angle,90+kh_angle, KH_tool_num);
#dxfarc(getxpos()+(kh_distance*cos(kh_angle)),getypos()+(kh_distance*sin(kh_angle)),tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,270+kh_angle,360+kh_angle, KH_tool_num);
#dxfline( getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2*cos(kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2))),
# getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2*sin(kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2))),
# getxpos()+(kh_distance*cos(kh_angle))-((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)*sin(kh_angle)),
# getypos()+(kh_distance*sin(kh_angle))+((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)*cos(kh_angle)), KH_tool_num);
#//echo("a",tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2);
#//echo("c",tool_diameter(KH_tool_num, (kh_max_depth))/2);
#echo("Aangle",asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)));
#//echo(kh_angle);
# cutwithfeed(getxpos()+(kh_distance*cos(kh_angle)),getypos()+(kh_distance*sin(kh_angle)),-kh_max_depth,feed);
            toolpath = toolpath.union(self.cutline(self.xpos()+kh_distance, self.ypos(), -kh_max_depth))
        elif (kh_angle == 90):
#Lower left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),180,270)
#Lower right of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),270,360)
#left slot
            self.dxfline(kh_tool_num, self.xpos()-r, self.ypos()+ro, self.xpos()-r, self.ypos()+kh_distance)
#right slot
            self.dxfline(kh_tool_num, self.xpos()+r, self.ypos()+ro, self.xpos()+r, self.ypos()+kh_distance)
#upper left of end of slot
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos()+kh_distance,r,90,180)
#upper right of end of slot
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos()+kh_distance,r,0,90)
#Upper right of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 0, 90-angle)
#Upper left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 90+angle, 180)
            toolpath = toolpath.union(self.cutline(self.xpos(), self.ypos()+kh_distance, -kh_max_depth))
        elif (kh_angle == 180):
#Lower right of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),270,360)
#Upper right of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),0,90)
#Upper left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 90, 180-angle)
#Lower left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 180+angle, 270)
#upper slot
            self.dxfline(kh_tool_num, self.xpos()-ro, self.ypos()-r, self.xpos()-kh_distance, self.ypos()-r)
#lower slot
            self.dxfline(kh_tool_num, self.xpos()-ro, self.ypos()+r, self.xpos()-kh_distance, self.ypos()+r)
#upper left of end of slot
            self.dxfarc(kh_tool_num, self.xpos()-kh_distance,self.ypos(),r,90,180)
#lower left of end of slot
            self.dxfarc(kh_tool_num, self.xpos()-kh_distance,self.ypos(),r,180,270)
            toolpath = toolpath.union(self.cutline(self.xpos()-kh_distance, self.ypos(), -kh_max_depth))
        elif (kh_angle == 270):
#Upper left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),90,180)
#Upper right of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),0,90)
#left slot
            self.dxfline(kh_tool_num, self.xpos()-r, self.ypos()-ro, self.xpos()-r, self.ypos()-kh_distance)
#right slot
            self.dxfline(kh_tool_num, self.xpos()+r, self.ypos()-ro, self.xpos()+r, self.ypos()-kh_distance)
#lower left of end of slot
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos()-kh_distance,r,180,270)
#lower right of end of slot
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos()-kh_distance,r,270,360)
#lower right of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 180, 270-angle)
#lower left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 270+angle, 360)
            toolpath = toolpath.union(self.cutline(self.xpos(), self.ypos()-kh_distance, -kh_max_depth))
#        print(self.zpos())
        self.setxpos(oXpos)
        self.setypos(oYpos)
        return toolpath

#  } else if (kh_angle == 90) {
#    //Lower left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,180,270, KH_tool_num);
#    //Lower right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,270,360, KH_tool_num);
#    //Upper right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,0,acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
#    //Upper left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,180-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 180,KH_tool_num);
#    //Actual line of cut
#    dxfline(getxpos(),getypos(),getxpos(),getypos()+kh_distance);
#    //upper right of slot
#    dxfarc(getxpos(),getypos()+kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,0,90, KH_tool_num);
#    //upper left of slot
#    dxfarc(getxpos(),getypos()+kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,90,180, KH_tool_num);
#    //right of slot
#    dxfline(
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        getypos()+(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#    //end position at top of slot
#        getypos()+kh_distance,
#        KH_tool_num);
#    dxfline(getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2, getypos()+(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2), getxpos()-tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,getypos()+kh_distance, KH_tool_num);
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos()+kh_distance, zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
#    cutwithfeed(getxpos(),getypos()+kh_distance,-kh_max_depth,feed);
#    setypos(getypos()-kh_distance);
#  } else if (kh_angle == 180) {
#    //Lower right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,270,360, KH_tool_num);
#    //Upper right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,0,90, KH_tool_num);
#    //Upper left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,90, 90+acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
#    //Lower left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2, 270-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 270, KH_tool_num);
#    //upper left of slot
#    dxfarc(getxpos()-kh_distance,getypos(),tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,90,180, KH_tool_num);
#    //lower left of slot
#    dxfarc(getxpos()-kh_distance,getypos(),tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,180,270, KH_tool_num);
#    //Actual line of cut
#    dxfline(getxpos(),getypos(),getxpos()-kh_distance,getypos());
#    //upper left slot
#    dxfline(
#        getxpos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),
#        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()-kh_distance,
#    //end position at top of slot
#        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        KH_tool_num);
#    //lower right slot
#    dxfline(
#        getxpos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),
#        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()-kh_distance,
#    //end position at top of slot
#        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        KH_tool_num);
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos()-kh_distance, ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
#    cutwithfeed(getxpos()-kh_distance,getypos(),-kh_max_depth,feed);
#    setxpos(getxpos()+kh_distance);
#  } else if (kh_angle == 270) {
#    //Upper right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,0,90, KH_tool_num);
#    //Upper left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,90,180, KH_tool_num);
#    //lower right of slot
#    dxfarc(getxpos(),getypos()-kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,270,360, KH_tool_num);
#    //lower left of slot
#    dxfarc(getxpos(),getypos()-kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,180,270, KH_tool_num);
#    //Actual line of cut
#    dxfline(getxpos(),getypos(),getxpos(),getypos()-kh_distance);
#    //right of slot
#    dxfline(
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        getypos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#    //end position at top of slot
#        getypos()-kh_distance,
#        KH_tool_num);
#    //left of slot
#    dxfline(
#        getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        getypos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
#    //end position at top of slot
#        getypos()-kh_distance,
#        KH_tool_num);
#    //Lower right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,360-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 360, KH_tool_num);
#    //Lower left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,180, 180+acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos()-kh_distance, zpos()-kh_max_depth]){
#        gcp_keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
#    cutwithfeed(getxpos(),getypos()-kh_distance,-kh_max_depth,feed);
#    setypos(getypos()+kh_distance);
#  }
#}

from gcodepreview import *

