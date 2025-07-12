#!/usr/bin/env python
#icon "C:\Program Files\PythonSCAD\bin\openscad.exe" --trust-python
#Currently tested with https://www.pythonscad.org/downloads/PythonSCAD_nolibfive-2025.06.04-x86-64-Installer.exe and Python 3.11
#gcodepreview 0.9, for use with PythonSCAD,
#if using from PythonSCAD using OpenSCAD code, see gcodepreview.scad

import sys

# add math functions (sqrt)
import math

# getting openscad functions into namespace
#https://github.com/gsohler/openscad/issues/39
try:
    from openscad import *
except ModuleNotFoundError as e:
    print("OpenSCAD module not loaded.")

def pygcpversion():
    thegcpversion = 0.9
    return thegcpversion

class gcodepreview:

    def __init__(self,
                 generategcode = False,
                 generatedxf = False,
                 gcpfa = 2,
                 gcpfs = 0.125,
                 steps = 10
                 ):
        """
        Initialize gcodepreview object.

        Parameters
        ----------
        generategcode : boolean
                        Enables writing out G-code.
        generatedxf   : boolean
                        Enables writing out DXF file(s).

        Returns
        -------
        object
            The initialized gcodepreview object.
        """
        if generategcode == 1:
            self.generategcode = True
        elif generategcode == 0:
            self.generategcode = False
        else:
            self.generategcode = generategcode
        if generatedxf == 1:
            self.generatedxf = True
        elif generatedxf == 0:
            self.generatedxf = False
        else:
            self.generatedxf = generatedxf
# unless multiple dxfs are enabled, the check for them is of course False
        self.generatedxfs = False
# set up 3D previewing parameters
        fa = gcpfa
        fs = gcpfs
        self.steps = steps
# initialize the machine state
        self.mc = "Initialized"
        self.mpx = float(0)
        self.mpy = float(0)
        self.mpz = float(0)
        self.tpz = float(0)
# initialize the toolpath state
        self.retractheight = 5
# initialize the DEFAULT tool
        self.currenttoolnum = 102
        self.endmilltype = "square"
        self.diameter = 3.175
        self.flute = 12.7
        self.shaftdiameter = 3.175
        self.shaftheight = 12.7
        self.shaftlength = 19.5
        self.toolnumber = "100036"
        self.cutcolor = "green"
        self.rapidcolor = "orange"
        self.shaftcolor = "red"
# the variables for holding 3D models must be initialized as empty lists so as to ensure that only append or extend commands are used with them
        self.rapids = []
        self.toolpaths = []

#    def myfunc(self, var):
#        self.vv = var * var
#        return self.vv
#
#    def getvv(self):
#        return self.vv
#
#    def checkint(self):
#        return self.mc
#
#    def makecube(self, xdim, ydim, zdim):
#        self.c=cube([xdim, ydim, zdim])
#
#    def placecube(self):
#        show(self.c)
#
#    def instantiatecube(self):
#        return self.c

    def xpos(self):
        return self.mpx

    def ypos(self):
        return self.mpy

    def zpos(self):
        return self.mpz

    def setxpos(self, newxpos):
        self.mpx = newxpos

    def setypos(self, newypos):
        self.mpy = newypos

    def setzpos(self, newzpos):
        self.mpz = newzpos

    def setupstock(self, stockXwidth,
                 stockYheight,
                 stockZthickness,
                 zeroheight,
                 stockzero,
                 retractheight):
        """
        Set up blank/stock for material and position/zero.

        Parameters
        ----------
        stockXwidth :   float
                        X extent/dimension
        stockYheight :  float
                        Y extent/dimension
        stockZthickness : boolean
                        Z extent/dimension
        zeroheight :    string
                        Top or Bottom, determines if Z extent will be positive or negative
        stockzero :     string
                        Lower-Left, Center-Left, Top-Left, Center, determines XY position of stock
        retractheight : float
                        Distance which tool retracts above surface of stock.

        Returns
        -------
        none
        """
        self.stockXwidth = stockXwidth
        self.stockYheight = stockYheight
        self.stockZthickness = stockZthickness
        self.zeroheight = zeroheight
        self.stockzero = stockzero
        self.retractheight = retractheight
        self.stock = cube([stockXwidth, stockYheight, stockZthickness])

        if self.zeroheight == "Top":
            if self.stockzero == "Lower-Left":
                self.stock = self.stock.translate([0, 0, -self.stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, 0.00mm, -", str(self.stockZthickness), "mm)")
                    self.writegc("(stockMax:", str(self.stockXwidth), "mm, ", str(stockYheight), "mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ", str(self.stockXwidth), ", ", str(self.stockYheight), ", ", str(self.stockZthickness), ", 0.00, 0.00, ", str(self.stockZthickness), ")")
            if self.stockzero == "Center-Left":
                self.stock = self.stock.translate([0, -stockYheight / 2, -stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -", str(self.stockYheight/2), "mm, -", str(self.stockZthickness), "mm)")
                    self.writegc("(stockMax:", str(self.stockXwidth), "mm, ", str(self.stockYheight/2), "mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ", str(self.stockXwidth), ", ", str(self.stockYheight), ", ", str(self.stockZthickness), ", 0.00, ", str(self.stockYheight/2), ", ", str(self.stockZthickness), ")");
            if self.stockzero == "Top-Left":
                self.stock = self.stock.translate([0, -self.stockYheight, -self.stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -", str(self.stockYheight), "mm, -", str(self.stockZthickness), "mm)")
                    self.writegc("(stockMax:", str(self.stockXwidth), "mm, 0.00mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ", str(self.stockXwidth), ", ", str(self.stockYheight), ", ", str(self.stockZthickness), ", 0.00, ", str(self.stockYheight), ", ", str(self.stockZthickness), ")")
            if self.stockzero == "Center":
                self.stock = self.stock.translate([-self.stockXwidth / 2, -self.stockYheight / 2, -self.stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin: -", str(self.stockXwidth/2), ", -", str(self.stockYheight/2), "mm, -", str(self.stockZthickness), "mm)")
                    self.writegc("(stockMax:", str(self.stockXwidth/2), "mm, ", str(self.stockYheight/2), "mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ", str(self.stockXwidth), ", ", str(self.stockYheight), ", ", str(self.stockZthickness), ", ", str(self.stockXwidth/2), ", ", str(self.stockYheight/2), ", ", str(self.stockZthickness), ")")
        if self.zeroheight == "Bottom":
            if self.stockzero == "Lower-Left":
                 self.stock = self.stock.translate([0, 0, 0])
                 if self.generategcode == True:
                     self.writegc("(stockMin:0.00mm, 0.00mm, 0.00mm)")
                     self.writegc("(stockMax:", str(self.stockXwidth), "mm, ", str(self.stockYheight), "mm, ", str(self.stockZthickness), "mm)")
                     self.writegc("(STOCK/BLOCK, ", str(self.stockXwidth), ", ", str(self.stockYheight), ", ", str(self.stockZthickness), ", 0.00, 0.00, 0.00)")
            if self.stockzero == "Center-Left":
                self.stock = self.stock.translate([0, -self.stockYheight / 2, 0])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -", str(self.stockYheight/2), "mm, 0.00mm)")
                    self.writegc("(stockMax:", str(self.stockXwidth), "mm, ", str(self.stockYheight/2), "mm, -", str(self.stockZthickness), "mm)")
                    self.writegc("(STOCK/BLOCK, ", str(self.stockXwidth), ", ", str(self.stockYheight), ", ", str(self.stockZthickness), ", 0.00, ", str(self.stockYheight/2), ", 0.00mm)");
            if self.stockzero == "Top-Left":
                self.stock = self.stock.translate([0, -self.stockYheight, 0])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -", str(self.stockYheight), "mm, 0.00mm)")
                    self.writegc("(stockMax:", str(self.stockXwidth), "mm, 0.00mm, ", str(self.stockZthickness), "mm)")
                    self.writegc("(STOCK/BLOCK, ", str(self.stockXwidth), ", ", str(self.stockYheight), ", ", str(self.stockZthickness), ", 0.00, ", str(self.stockYheight), ", 0.00)")
            if self.stockzero == "Center":
                self.stock = self.stock.translate([-self.stockXwidth / 2, -self.stockYheight / 2, 0])
                if self.generategcode == True:
                    self.writegc("(stockMin: -", str(self.stockXwidth/2), ", -", str(self.stockYheight/2), "mm, 0.00mm)")
                    self.writegc("(stockMax:", str(self.stockXwidth/2), "mm, ", str(self.stockYheight/2), "mm, ", str(self.stockZthickness), "mm)")
                    self.writegc("(STOCK/BLOCK, ", str(self.stockXwidth), ", ", str(self.stockYheight), ", ", str(self.stockZthickness), ", ", str(self.stockXwidth/2), ", ", str(self.stockYheight/2), ", 0.00)")
        if self.generategcode == True:
            self.writegc("G90");
            self.writegc("G21");

    def setupcuttingarea(self, sizeX, sizeY, sizeZ, extentleft, extentfb, extentd):
#        self.initializemachinestate()
        c=cube([sizeX,sizeY,sizeZ])
        c = c.translate([extentleft,extentfb,extentd])
        self.stock = c
        self.toolpaths = []
        return c

    def shiftstock(self, shiftX, shiftY, shiftZ):
         self.stock = self.stock.translate([shiftX, shiftY, shiftZ])

    def addtostock(self, stockXwidth, stockYheight, stockZthickness,
                         shiftX = 0,
                         shiftY = 0,
                         shiftZ = 0):
         addedpart = cube([stockXwidth, stockYheight, stockZthickness])
         addedpart = addedpart.translate([shiftX, shiftY, shiftZ])
         self.stock = self.stock.union(addedpart)

    def currenttoolnumber(self):
        return(self.currenttoolnum)

    def toolchange(self, tool_number, speed = 10000):
        self.currenttoolnum = tool_number

        if (self.generategcode == True):
            self.writegc("(Toolpath)")
            self.writegc("M05")

        if (tool_number == 201): #201/251/322 (Amana 46202-K) == 100047
            self.writegc("(TOOL/MILL, 6.35, 0.00, 0.00, 0.00)")
            self.endmilltype = "square"
            self.diameter = 6.35
            self.flute = 19.05
            self.shaftdiameter = 6.35
            self.shaftheight = 19.05
            self.shaftlength = 20.0
            self.toolnumber = "100047"
        elif (tool_number == 102): #102/326 == 100036
            self.writegc("(TOOL/MILL, 3.175, 0.00, 0.00, 0.00)")
            self.endmilltype = "square"
            self.diameter = 3.175
            self.flute = 12.7
            self.shaftdiameter = 3.175
            self.shaftheight = 12.7
            self.shaftlength = 20.0
            self.toolnumber = 100036
        elif (tool_number == 112): #112 == 100024
            self.writegc("(TOOL/MILL, 1.5875, 0.00, 0.00, 0.00)")
            self.endmilltype = "square"
            self.diameter = 1.5875
            self.flute = 6.35
            self.shaftdiameter = 3.175
            self.shaftheight = 6.35
            self.shaftlength = 12.0
            self.toolnumber = "100024"
        elif (tool_number == 122): #122 == 100012
            self.writegc("(TOOL/MILL, 0.79375, 0.00, 0.00, 0.00)")
            self.endmilltype = "square"
            self.diameter = 0.79375
            self.flute = 1.5875
            self.shaftdiameter = 3.175
            self.shaftheight = 1.5875
            self.shaftlength = 12.0
            self.toolnumber = "100012"
        elif (tool_number == 324): #324 (Amana 46170-K) == 100048
            self.writegc("(TOOL/MILL, 6.35, 0.00, 0.00, 0.00)")
            self.endmilltype = "square"
            self.diameter = 6.35
            self.flute = 22.225
            self.shaftdiameter = 6.35
            self.shaftheight = 22.225
            self.shaftlength = 20.0
            self.toolnumber = "100048"
        elif (tool_number == 205): #205 == 100048
            self.writegc("(TOOL/MILL, 6.35, 0.00, 0.00, 0.00)")
            self.endmilltype = "square"
            self.diameter = 6.35
            self.flute = 25.4
            self.shaftdiameter = 6.35
            self.shaftheight = 25.4
            self.shaftlength = 20.0
            self.toolnumber = "100048"
#
        elif (tool_number == 282): #282 == 000204
            self.writegc("(TOOL/MILL, 2.0, 0.00, 0.00, 0.00)")
            self.endmilltype = "O-flute"
            self.diameter = 2.0
            self.flute = 6.35
            self.shaftdiameter = 6.35
            self.shaftheight = 6.35
            self.shaftlength = 12.0
            self.toolnumber = "000204"
        elif (tool_number == 274): #274 == 000036
            self.writegc("(TOOL/MILL, 3.175, 0.00, 0.00, 0.00)")
            self.endmilltype = "O-flute"
            self.diameter = 3.175
            self.flute = 12.7
            self.shaftdiameter = 3.175
            self.shaftheight = 12.7
            self.shaftlength = 20.0
            self.toolnumber = "000036"
        elif (tool_number == 278): #278 == 000047
            self.writegc("(TOOL/MILL, 6.35, 0.00, 0.00, 0.00)")
            self.endmilltype = "O-flute"
            self.diameter = 6.35
            self.flute = 19.05
            self.shaftdiameter = 3.175
            self.shaftheight = 19.05
            self.shaftlength = 20.0
            self.toolnumber = "000047"
#
        elif (tool_number == 202): #202 == 204047
            self.writegc("(TOOL/MILL, 6.35, 3.175, 0.00, 0.00)")
            self.endmilltype = "ball"
            self.diameter = 6.35
            self.flute = 19.05
            self.shaftdiameter = 6.35
            self.shaftheight = 19.05
            self.shaftlength = 20.0
            self.toolnumber = "204047"
        elif (tool_number == 101): #101 == 203036
            self.writegc("(TOOL/MILL, 3.175, 1.5875, 0.00, 0.00)")
            self.endmilltype = "ball"
            self.diameter = 3.175
            self.flute = 12.7
            self.shaftdiameter = 3.175
            self.shaftheight = 12.7
            self.shaftlength = 20.0
            self.toolnumber = "203036"
        elif (tool_number == 111): #111 == 202024
            self.writegc("(TOOL/MILL, 1.5875, 0.79375, 0.00, 0.00)")
            self.endmilltype = "ball"
            self.diameter = 1.5875
            self.flute = 6.35
            self.shaftdiameter = 3.175
            self.shaftheight = 6.35
            self.shaftlength = 20.0
            self.toolnumber = "202024"
        elif (tool_number == 121): #121 == 201012
            self.writegc("(TOOL/MILL, 3.175, 0.79375, 0.00, 0.00)")
            self.endmilltype = "ball"
            self.diameter = 0.79375
            self.flute = 1.5875
            self.shaftdiameter = 3.175
            self.shaftheight = 1.5875
            self.shaftlength = 20.0
            self.toolnumber = "201012"
        elif (tool_number == 325): #325 (Amana 46376-K) == 204048
            self.writegc("(TOOL/MILL, 6.35, 3.175, 0.00, 0.00)")
            self.endmilltype = "ball"
            self.diameter = 6.35
            self.flute = 25.4
            self.shaftdiameter = 6.35
            self.shaftheight = 25.4
            self.shaftlength = 20.0
            self.toolnumber = "204048"
#
        elif (tool_number == 301): #301 == 390074
            self.writegc("(TOOL/MILL, 0.10, 0.05, 6.35, 45.00)")
            self.endmilltype = "V"
            self.diameter = 12.7
            self.flute = 6.35
            self.angle = 90
            self.shaftdiameter = 6.35
            self.shaftheight = 6.35
            self.shaftlength = 20.0
            self.toolnumber = "390074"
        elif (tool_number == 302): #302 == 360071
            self.writegc("(TOOL/MILL, 0.10, 0.05, 6.35, 30.00)")
            self.endmilltype = "V"
            self.diameter = 12.7
            self.flute = 11.067
            self.angle = 60
            self.shaftdiameter = 6.35
            self.shaftheight = 11.067
            self.shaftlength = 20.0
            self.toolnumber = "360071"
        elif (tool_number == 390): #390 == 390032
            self.writegc("(TOOL/MILL, 0.03, 0.00, 1.5875, 45.00)")
            self.endmilltype = "V"
            self.diameter = 3.175
            self.flute = 1.5875
            self.angle = 90
            self.shaftdiameter = 3.175
            self.shaftheight = 1.5875
            self.shaftlength = 20.0
            self.toolnumber = "390032"
        elif (tool_number == 327): #327 (Amana RC-1148) == 360098
            self.writegc("(TOOL/MILL, 0.03, 0.00, 13.4874, 30.00)")
            self.endmilltype = "V"
            self.diameter = 25.4
            self.flute = 22.134
            self.angle = 60
            self.shaftdiameter = 6.35
            self.shaftheight = 22.134
            self.shaftlength = 20.0
            self.toolnumber = "360098"
        elif (tool_number == 323): #323 == 330041 30 degree V Amana, 45771-K
            self.writegc("(TOOL/MILL, 0.10, 0.05, 11.18, 15.00)")
            self.endmilltype = "V"
            self.diameter = 6.35
            self.flute = 11.849
            self.angle = 30
            self.shaftdiameter = 6.35
            self.shaftheight = 11.849
            self.shaftlength = 20.0
            self.toolnumber = "330041"
#
        elif (tool_number == 374): #374 == 906043
            self.writegc("(TOOL/MILL, 9.53, 0.00, 3.17, 0.00)")
            self.endmilltype = "keyhole"
            self.diameter = 9.525
            self.flute = 3.175
            self.radius = 6.35
            self.shaftdiameter = 6.35
            self.shaftheight = 3.175
            self.shaftlength = 20.0
            self.toolnumber = "906043"
        elif (tool_number == 375): #375 == 906053
            self.writegc("(TOOL/MILL, 9.53, 0.00, 3.17, 0.00)")
            self.endmilltype = "keyhole"
            self.diameter = 9.525
            self.flute = 3.175
            self.radius = 8
            self.shaftdiameter = 6.35
            self.shaftheight = 3.175
            self.shaftlength = 20.0
            self.toolnumber = "906053"
        elif (tool_number == 376): #376 == 907040
            self.writegc("(TOOL/MILL, 12.7, 0.00, 4.77, 0.00)")
            self.endmilltype = "keyhole"
            self.diameter = 12.7
            self.flute = 4.7625
            self.radius = 6.35
            self.shaftdiameter = 6.35
            self.shaftheight = 4.7625
            self.shaftlength = 20.0
            self.toolnumber = "907040"
        elif (tool_number == 378): #378 == 907050
            self.writegc("(TOOL/MILL, 12.7, 0.00, 4.77, 0.00)")
            self.endmilltype = "keyhole"
            self.diameter = 12.7
            self.flute = 4.7625
            self.radius = 8
            self.shaftdiameter = 6.35
            self.shaftheight = 4.7625
            self.shaftlength = 20.0
            self.toolnumber = "907050"
#
        elif (tool_number == 45981): #45981 == 445981
#Amana Carbide Tipped Bowl & Tray 1/8 Radius x 1/2 Dia x 1/2 x 1/4 Inch Shank
            self.writegc("(TOOL/MILL,0.03, 0.00, 10.00, 30.00)")
            self.writegc("(TOOL/MILL, 15.875, 6.35, 19.05, 0.00)")
            self.endmilltype = "bowl"
            self.diameter = 12.7
            self.flute = 12.7
            self.radius = 3.175
            self.shaftdiameter = 6.35
            self.shaftheight = 12.7
            self.shaftlength = 20.0
            self.toolnumber = "445981"
        elif (tool_number == 45982):#0.507/2, 4.509
            self.writegc("(TOOL/MILL, 15.875, 6.35, 19.05, 0.00)")
            self.endmilltype = "bowl"
            self.diameter = 19.05
            self.flute = 15.875
            self.radius = 6.35
            self.shaftdiameter = 6.35
            self.shaftheight = 15.875
            self.shaftlength = 20.0
            self.toolnumber = "445982"
#        elif (tool_number == 1370): #1370 == 401370
#Whiteside Bowl & Tray Bit 1/4"SH, 1/8"R, 7/16"CD (5/16" cutting flute length)
            self.writegc("(TOOL/MILL, 11.1125, 8, 3.175, 0.00)")
            self.endmilltype = "bowl"
            self.diameter = 11.1125
            self.flute = 8
            self.radius = 3.175
            self.shaftdiameter = 6.35
            self.shaftheight = 8
            self.shaftlength = 20.0
            self.toolnumber = "401370"
#        elif (tool_number == 1372): #1372/45982 == 401372
#Whiteside Bowl & Tray Bit 1/4"SH, 1/4"R, 3/4"CD (5/8" cutting flute length)
#Amana Carbide Tipped Bowl & Tray 1/4 Radius x 3/4 Dia x 5/8 x 1/4 Inch Shank
            self.writegc("(TOOL/MILL, 19.5, 15.875, 6.35, 0.00)")
            self.endmilltype = "bowl"
            self.diameter = 19.5
            self.flute = 15.875
            self.radius = 6.35
            self.shaftdiameter = 6.35
            self.shaftheight = 15.875
            self.shaftlength = 20.0
            self.toolnumber = "401372"
#
        elif (tool_number == 501): #501 == 530131
            self.writegc("(TOOL/MILL,0.03, 0.00, 10.00, 30.00)")
#            self.currenttoolshape = self.toolshapes("tapered ball", 3.175, 5.561, 30, 0.254)
            self.endmilltype = "tapered ball"
            self.diameter = 3.175
            self.flute = 5.561
            self.angle = 30
            self.tip = 0.254
            self.shaftdiameter = 3.175
            self.shaftheight = 5.561
            self.shaftlength = 10.0
            self.toolnumber = "530131"
        elif (tool_number == 502): #502 == 540131
            self.writegc("(TOOL/MILL,0.03, 0.00, 10.00, 20.00)")
#            self.currenttoolshape = self.toolshapes("tapered ball", 3.175, 4.117, 40, 0.254)
            self.endmilltype = "tapered ball"
            self.diameter = 3.175
            self.flute = 4.117
            self.angle = 40
            self.tip = 0.254
            self.shaftdiameter = 3.175
            self.shaftheight = 4.117
            self.shaftlength = 10.0
            self.toolnumber = "540131"
#        elif (tool_number == 204):#
#            self.writegc("()")
#            self.currenttoolshape = self.tapered_ball(1.5875, 6.35, 38.1, 3.6)
#        elif (tool_number == 304):#
#            self.writegc("()")
#            self.currenttoolshape = self.tapered_ball(3.175, 6.35, 38.1, 2.4)
#
        elif (tool_number == 56125):#0.508/2, 1.531 56125 == 603042
            self.writegc("(TOOL/CRMILL, 0.508, 6.35, 3.175, 7.9375, 3.175)")
            self.endmilltype = "roundover"
            self.tip = 0.508
            self.diameter = 6.35 - self.tip
            self.flute = 8 - self.tip
            self.radius = 3.175 - self.tip
            self.shaftdiameter = 6.35
            self.shaftheight = 8
            self.shaftlength = 10.0
            self.toolnumber = "603042"
        elif (tool_number == 56142):#0.508/2, 2.921 56142 == 602032
            self.writegc("(TOOL/CRMILL, 0.508, 3.571875, 1.5875, 5.55625, 1.5875)")
            self.endmilltype = "roundover"
            self.tip = 0.508
            self.diameter = 3.175 - self.tip
            self.flute = 4.7625 - self.tip
            self.radius = 1.5875 - self.tip
            self.shaftdiameter = 3.175
            self.shaftheight = 4.7625
            self.shaftlength = 10.0
            self.toolnumber = "602032"
#        elif (tool_number == 312):#1.524/2, 3.175
#            self.writegc("(TOOL/CRMILL, Diameter1, Diameter2, Radius, Height, Length)")
#        elif (tool_number == 1568):#0.507/2, 4.509 1568 == 603032
##FIX            self.writegc("(TOOL/CRMILL, 0.17018, 9.525, 4.7625, 12.7, 4.7625)")
##            self.currenttoolshape = self.toolshapes("roundover", 3.175, 6.35, 3.175, 0.396875)
#            self.endmilltype = "roundover"
#            self.diameter = 3.175
#            self.flute = 6.35
#            self.radius = 3.175
#            self.tip = 0.396875
#            self.toolnumber = "603032"
##https://www.amanatool.com/45982-carbide-tipped-bowl-tray-1-4-radius-x-3-4-dia-x-5-8-x-1-4-inch-shank.html
#        elif (tool_number == 1570):#0.507/2, 4.509 1570 == 600002 ?!?
#            self.writegc("(TOOL/CRMILL, 0.17018, 9.525, 4.7625, 12.7, 4.7625)")
##            self.currenttoolshape = self.toolshapes("roundover", 4.7625, 9.525, 4.7625, 0.396875)
#            self.endmilltype = "roundover"
#            self.diameter = 4.7625
#            self.flute = 9.525
#            self.radius = 4.7625
#            self.tip = 0.396875
#            self.toolnumber = "600002"
#        elif (tool_number == 1572): #1572 = 604042
##FIX            self.writegc("(TOOL/CRMILL, 0.17018, 9.525, 4.7625, 12.7, 4.7625)")
##            self.currenttoolshape = self.toolshapes("roundover", 6.35, 12.7, 6.35, 0.396875)
#            self.endmilltype = "roundover"
#            self.diameter = 6.35
#            self.flute = 12.7
#            self.radius = 6.35
#            self.tip = 0.396875
#            self.toolnumber = "604042"
#        elif (tool_number == 1574): #1574 == 600062
##FIX            self.writegc("(TOOL/CRMILL, 0.17018, 9.525, 4.7625, 12.7, 4.7625)")
##            self.currenttoolshape = self.toolshapes("roundover", 9.525, 19.5, 9.515, 0.396875)
#            self.endmilltype = "roundover"
#            self.diameter = 9.525
#            self.flute = 19.5
#            self.radius = 9.515
#            self.tip = 0.396875
#            self.toolnumber = "600062"
#
        elif (tool_number == 814): #814 == 814071
#Item 18J1607, 1/2" 14° Dovetail Bit, 8mm shank
            self.writegc("(TOOL/MILL, 12.7, 6.367, 12.7, 0.00)")
        #    dt_bottomdiameter, dt_topdiameter, dt_height, dt_angle)
        #    https://www.leevalley.com/en-us/shop/tools/power-tool-accessories/router-bits/30172-dovetail-bits?item=18J1607
#            self.currenttoolshape = self.toolshapes("dovetail", 12.7, 12.7, 14)
            self.endmilltype = "dovetail"
            self.diameter = 12.7
            self.flute = 12.7
            self.angle = 14
            self.toolnumber = "814071"
        elif (tool_number == 808079): #45828 == 808071
            self.writegc("(TOOL/MILL, 12.7, 6.816, 20.95, 0.00)")
        #    http://www.amanatool.com/45828-carbide-tipped-dovetail-8-deg-x-1-2-dia-x-825-x-1-4-inch-shank.html
#            self.currenttoolshape = self.toolshapes("dovetail", 12.7, 20.955, 8)
            self.endmilltype = "dovetail"
            self.diameter = 12.7
            self.flute = 20.955
            self.angle = 8
            self.toolnumber = "808071"
#
        self.writegc("M6T", str(tool_number))
        self.writegc("M03S", str(speed))

    def setcolor(self,
                  cutcolor = "green",
                  rapidcolor = "orange",
                  shaftcolor = "red"):
        self.cutcolor = cutcolor
        self.rapidcolor = rapidcolor
        self.shaftcolor = shaftcolor

    def toolmovement(self, bx, by, bz, ex, ey, ez, step = 0):
        tslist = []
        if step > 0:
            steps = step
        else:
            steps = self.steps

        if self.endmilltype == "square":
            ts = cylinder(r1=(self.diameter / 2), r2=(self.diameter / 2), h=self.flute, center = False)
            tslist.append(hull(ts.translate([bx, by, bz]), ts.translate([ex, ey, ez])))
            return tslist

        if self.endmilltype == "O-flute":
            ts = cylinder(r1=(self.diameter / 2), r2=(self.diameter / 2), h=self.flute, center = False)
            tslist.append(hull(ts.translate([bx, by, bz]), ts.translate([ex, ey, ez])))
            return tslist

        if self.endmilltype == "ball":
            b = sphere(r=(self.diameter / 2))
            s = cylinder(r1=(self.diameter / 2), r2=(self.diameter / 2), h=self.flute, center=False)
            bs = union(b, s)
            bs = bs.translate([0, 0, (self.diameter / 2)])
            tslist.append(hull(bs.translate([bx, by, bz]), bs.translate([ex, ey, ez])))
            return tslist
#
        if self.endmilltype == "bowl":
            inner = cylinder(r1 = self.diameter/2 - self.radius, r2 = self.diameter/2 - self.radius, h = self.flute)
            outer = cylinder(r1 = self.diameter/2, r2 = self.diameter/2, h = self.flute - self.radius)
            outer = outer.translate([0,0, self.radius])
            slices = hull(outer, inner)
#    slices = cylinder(r1 = 0.0001, r2 = 0.0001, h = 0.0001, center=False)
            for i in range(1, 90 - self.steps, self.steps):
                slice = cylinder(r1 = self.diameter / 2 - self.radius + self.radius * Sin(i), r2 = self.diameter / 2 - self.radius + self.radius * Sin(i+self.steps), h = self.radius/90, center=False)
                slices = hull(slices, slice.translate([0, 0, self.radius - self.radius * Cos(i+self.steps)]))
            tslist.append(hull(slices.translate([bx, by, bz]), slices.translate([ex, ey, ez])))
            return tslist
#
        if self.endmilltype == "V":
            v = cylinder(r1=0, r2=(self.diameter / 2), h=((self.diameter / 2) / Tan((self.angle / 2))), center=False)
#                s = cylinder(r1=(self.diameter / 2), r2=(self.diameter / 2), h=self.flute, center=False)
#                sh = s.translate([0, 0, ((self.diameter / 2) / Tan((self.angle / 2)))])
            tslist.append(hull(v.translate([bx, by, bz]), v.translate([ex, ey, ez])))
            return tslist

        if self.endmilltype == "keyhole":
            kh = cylinder(r1=(self.diameter / 2), r2=(self.diameter / 2), h=self.flute, center=False)
            sh = (cylinder(r1=(self.radius / 2), r2=(self.radius / 2), h=self.flute*2, center=False))
            tslist.append(hull(kh.translate([bx, by, bz]), kh.translate([ex, ey, ez])))
            tslist.append(hull(sh.translate([bx, by, bz]), sh.translate([ex, ey, ez])))
            return tslist

        if self.endmilltype == "tapered ball":
            b = sphere(r=(self.tip / 2))
            s = cylinder(r1=(self.tip / 2), r2=(self.diameter / 2), h=self.flute, center=False)
            bshape = union(b, s)
            tslist.append(hull(bshape.translate([bx, by, bz]), bshape.translate([ex, ey, ez])))
            return tslist

        if self.endmilltype == "dovetail":
            dt = cylinder(r1=(self.diameter / 2), r2=(self.diameter / 2) - self.flute * Tan(self.angle), h= self.flute, center=False)
            tslist.append(hull(dt.translate([bx, by, bz]), dt.translate([ex, ey, ez])))
            return tslist
        if self.endmilltype == "other":
            tslist = []
#    def dovetail(self, dt_bottomdiameter, dt_topdiameter, dt_height, dt_angle):
#        return cylinder(r1=(dt_bottomdiameter / 2), r2=(dt_topdiameter / 2), h= dt_height, center=False)

        if self.endmilltype == "roundover":
            shaft = cylinder(self.steps, self.tip/2, self.tip/2)
            toolpath = hull(shaft.translate([bx, by, bz]), shaft.translate([ex, ey, ez]))
            shaft = cylinder(self.flute, self.diameter/2 + self.tip/2, self.diameter/2 + self.tip/2)
            toolpath = toolpath.union(hull(shaft.translate([bx, by, bz + self.radius]), shaft.translate([ex, ey, ez + self.radius])))
            tslist = [toolpath]
            slice = cylinder(0.0001, 0.0001, 0.0001)
            slices = slice
            for i in range(1, 90 - self.steps, self.steps):
                dx = self.radius*Cos(i)
                dxx = self.radius*Cos(i + self.steps)
                dzz = self.radius*Sin(i)
                dz = self.radius*Sin(i + self.steps)
                dh = dz - dzz
                slice = cylinder(r1 = self.tip/2+self.radius-dx, r2 = self.tip/2+self.radius-dxx, h = dh)
                slices = slices.union(hull(slice.translate([bx, by, bz+dz]), slice.translate([ex, ey, ez+dz])))
                tslist.append(slices)
            return tslist
#
    def shaftmovement(self, bx, by, bz, ex, ey, ez):
        tslist = []
        ts = cylinder(r1=(self.shaftdiameter / 2), r2=(self.shaftdiameter / 2), h=self.shaftlength, center = False)
        ts = ts.translate([0, 0, self.shaftheight])
        tslist.append(hull(ts.translate([bx, by, bz]), ts.translate([ex, ey, ez])))
        return tslist

    def rapid(self, ex, ey, ez, laser = 0):
#        print(self.rapidcolor)
        if laser == 0:
            tm = self.toolmovement(self.xpos(), self.ypos(), self.zpos(), ex, ey, ez)
            tm = color(tm, self.shaftcolor)
            ts = self.shaftmovement(self.xpos(), self.ypos(), self.zpos(), ex, ey, ez)
            ts = color(ts, self.rapidcolor)
            self.toolpaths.extend([tm, ts])
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)

    def cutline(self, ex, ey, ez):
#        print(self.cutcolor)
#        print(ex, ey, ez)
        tm = self.toolmovement(self.xpos(), self.ypos(), self.zpos(), ex, ey, ez)
        tm = color(tm, self.cutcolor)
        ts = self.shaftmovement(self.xpos(), self.ypos(), self.zpos(), ex, ey, ez)
        ts = color(ts, self.rapidcolor)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        self.toolpaths.extend([tm, ts])

    def movetosafeZ(self):
        rapid = self.rapid(self.xpos(), self.ypos(), self.retractheight)
#        if self.generatepaths == True:
#            rapid = self.rapid(self.xpos(), self.ypos(), self.retractheight)
#            self.rapids = self.rapids.union(rapid)
#        else:
#  if (generategcode == true) {
#  //    writecomment("PREPOSITION FOR RAPID PLUNGE");Z25.650
#  //G1Z24.663F381.0, "F", str(plunge)
#        if self.generatepaths == False:
#            return rapid
#        else:
#            return cube([0.001, 0.001, 0.001])
        return rapid

    def rapidXYZ(self, ex, ey, ez):
        rapid = self.rapid(ex, ey, ez)
#        if self.generatepaths == False:
        return rapid

    def rapidXY(self, ex, ey):
        rapid = self.rapid(ex, ey, self.zpos())
#        if self.generatepaths == True:
#            self.rapids = self.rapids.union(rapid)
#        else:
#        if self.generatepaths == False:
        return rapid

    def rapidXZ(self, ex, ez):
        rapid = self.rapid(ex, self.ypos(), ez)
#        if self.generatepaths == False:
        return rapid

    def rapidYZ(self, ey, ez):
        rapid = self.rapid(self.xpos(), ey, ez)
#        if self.generatepaths == False:
        return rapid

    def rapidX(self, ex):
        rapid = self.rapid(ex, self.ypos(), self.zpos())
#        if self.generatepaths == False:
        return rapid

    def rapidY(self, ey):
        rapid = self.rapid(self.xpos(), ey, self.zpos())
#        if self.generatepaths == False:
        return rapid

    def rapidZ(self, ez):
        rapid = [self.rapid(self.xpos(), self.ypos(), ez)]
#        if self.generatepaths == True:
#            self.rapids = self.rapids.union(rapid)
#        else:
#        if self.generatepaths == False:
        return rapid

    def cutlinedxf(self, ex, ey, ez):
        self.dxfline(self.currenttoolnumber(), self.xpos(), self.ypos(), ex, ey)
        self.cutline(ex, ey, ez)

    def cutlinedxfgc(self, ex, ey, ez):
        self.dxfline(self.currenttoolnumber(), self.xpos(), self.ypos(), ex, ey)
        self.writegc("G01 X", str(ex), " Y", str(ey), " Z", str(ez))
        self.cutline(ex, ey, ez)

    def cutvertexdxf(self, ex, ey, ez):
        self.addvertex(self.currenttoolnumber(), ex, ey)
        self.writegc("G01 X", str(ex), " Y", str(ey), " Z", str(ez))
        self.cutline(ex, ey, ez)

    def cutlineXYZwithfeed(self, ex, ey, ez, feed):
        return self.cutline(ex, ey, ez)

    def cutlineXYZ(self, ex, ey, ez):
        return self.cutline(ex, ey, ez)

    def cutlineXYwithfeed(self, ex, ey, feed):
        return self.cutline(ex, ey, self.zpos())

    def cutlineXY(self, ex, ey):
        return self.cutline(ex, ey, self.zpos())

    def cutlineXZwithfeed(self, ex, ez, feed):
        return self.cutline(ex, self.ypos(), ez)

    def cutlineXZ(self, ex, ez):
        return self.cutline(ex, self.ypos(), ez)

    def cutlineXwithfeed(self, ex, feed):
        return self.cutline(ex, self.ypos(), self.zpos())

    def cutlineX(self, ex):
        return self.cutline(ex, self.ypos(), self.zpos())

    def cutlineYZ(self, ey, ez):
        return self.cutline(self.xpos(), ey, ez)

    def cutlineYwithfeed(self, ey, feed):
        return self.cutline(self.xpos(), ey, self.zpos())

    def cutlineY(self, ey):
        return self.cutline(self.xpos(), ey, self.zpos())

    def cutlineZgcfeed(self, ez, feed):
        self.writegc("G01 Z", str(ez), "F", str(feed))
        return self.cutline(self.xpos(), self.ypos(), ez)

    def cutlineZwithfeed(self, ez, feed):
        return self.cutline(self.xpos(), self.ypos(), ez)

    def cutlineZ(self, ez):
        return self.cutline(self.xpos(), self.ypos(), ez)

    def cutarcCC(self, barc, earc, xcenter, ycenter, radius, tpzreldim, stepsizearc=1):
        tpzinc = tpzreldim / (earc - barc)
        i = barc
        while i < earc:
            self.cutline(xcenter + radius * Cos(math.radians(i)), ycenter + radius * Sin(math.radians(i)), self.zpos()+tpzinc)
            i += stepsizearc
        self.setxpos(xcenter + radius * Cos(math.radians(earc)))
        self.setypos(ycenter + radius * Sin(math.radians(earc)))

    def cutarcCW(self, barc, earc, xcenter, ycenter, radius, tpzreldim, stepsizearc=1):
#        print(str(self.zpos()))
#        print(str(ez))
#        print(str(barc - earc))
#        tpzinc = ez - self.zpos() / (barc - earc)
#        print(str(tzinc))
#        global toolpath
#        print("Entering n toolpath")
        tpzinc = tpzreldim / (barc - earc)
#        cts = self.currenttoolshape
#        toolpath = cts
#        toolpath = toolpath.translate([self.xpos(), self.ypos(), self.zpos()])
#        toolpath = []
        i = barc
        while i > earc:
            self.cutline(xcenter + radius * Cos(math.radians(i)), ycenter + radius * Sin(math.radians(i)), self.zpos()+tpzinc)
#            self.setxpos(xcenter + radius * Cos(math.radians(i)))
#            self.setypos(ycenter + radius * Sin(math.radians(i)))
#            print(str(self.xpos()), str(self.ypos(), str(self.zpos())))
#            self.setzpos(self.zpos()+tpzinc)
            i += abs(stepsizearc) * -1
#        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, barc, earc)
#        if self.generatepaths == True:
#            print("Unioning n toolpath")
#            self.toolpaths = self.toolpaths.union(toolpath)
#        else:
        self.setxpos(xcenter + radius * Cos(math.radians(earc)))
        self.setypos(ycenter + radius * Sin(math.radians(earc)))
#        self.toolpaths.extend(toolpath)
#        if self.generatepaths == False:
#        return toolpath
#        else:
#            return cube([0.01, 0.01, 0.01])

    def cutarcCWdxf(self, barc, earc, xcenter, ycenter, radius, tpzreldim, stepsizearc=1):
        self.cutarcCW(barc, earc, xcenter, ycenter, radius, tpzreldim, stepsizearc=1)
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, earc, barc)
#        if self.generatepaths == False:
#        return toolpath
#        else:
#            return cube([0.01, 0.01, 0.01])

    def cutarcCCdxf(self, barc, earc, xcenter, ycenter, radius, tpzreldim, stepsizearc=1):
        self.cutarcCC(barc, earc, xcenter, ycenter, radius, tpzreldim, stepsizearc=1)
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, barc, earc)

    def cutquarterCCNE(self, ex, ey, ez, radius):
        if self.zpos() == ez:
            tpzinc = 0
        else:
            tpzinc = (ez - self.zpos()) / 90
#        print("tpzinc ", tpzinc)
        i = 1
        while i < 91:
            self.cutline(ex + radius * Cos(i), ey - radius + radius * Sin(i), self.zpos()+tpzinc)
            i += 1

    def cutquarterCCNW(self, ex, ey, ez, radius):
        if self.zpos() == ez:
            tpzinc = 0
        else:
            tpzinc = (ez - self.zpos()) / 90
#            tpzinc = (self.zpos() + ez) / 90
        print("tpzinc ", tpzinc)
        i = 91
        while i < 181:
            self.cutline(ex + radius + radius * Cos(i), ey + radius * Sin(i), self.zpos()+tpzinc)
            i += 1

    def cutquarterCCSW(self, ex, ey, ez, radius):
        if self.zpos() == ez:
            tpzinc = 0
        else:
            tpzinc = (ez - self.zpos()) / 90
#            tpzinc = (self.zpos() + ez) / 90
        print("tpzinc ", tpzinc)
        i = 181
        while i < 271:
            self.cutline(ex + radius * Cos(i), ey + radius + radius * Sin(i), self.zpos()+tpzinc)
            i += 1

    def cutquarterCCSE(self, ex, ey, ez, radius):
        if self.zpos() == ez:
            tpzinc = 0
        else:
            tpzinc = (ez - self.zpos()) / 90
#            tpzinc = (self.zpos() + ez) / 90
#        print("tpzinc ", tpzinc)
        i = 271
        while i < 361:
            self.cutline(ex - radius + radius * Cos(i), ey + radius * Sin(i), self.zpos()+tpzinc)
            i += 1

    def cutquarterCCNEdxf(self, ex, ey, ez, radius):
        self.cutquarterCCNE(ex, ey, ez, radius)
        self.dxfarc(self.currenttoolnumber(), ex, ey - radius, radius,  0, 90)

    def cutquarterCCNWdxf(self, ex, ey, ez, radius):
        self.cutquarterCCNW(ex, ey, ez, radius)
        self.dxfarc(self.currenttoolnumber(), ex + radius, ey, radius, 90, 180)

    def cutquarterCCSWdxf(self, ex, ey, ez, radius):
        self.cutquarterCCSW(ex, ey, ez, radius)
        self.dxfarc(self.currenttoolnumber(), ex, ey + radius, radius, 180, 270)

    def cutquarterCCSEdxf(self, ex, ey, ez, radius):
        self.cutquarterCCSE(ex, ey, ez, radius)
        self.dxfarc(self.currenttoolnumber(), ex - radius, ey, radius, 270, 360)

    def tool_diameter(self, ptd_tool, ptd_depth):
# Square 122, 112, 102, 201
        if ptd_tool == 122:
            return 0.79375
        if ptd_tool == 112:
            return 1.5875
        if ptd_tool == 102:
            return 3.175
        if ptd_tool == 201:
            return 6.35
# Ball 121, 111, 101, 202
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
                return ptd_tool
        if ptd_tool == 808079:
            if ptd_depth > 20.95:
                return 6.816
            else:
                return ptd_tool
# Bowl Bit
#https://www.amanatool.com/45982-carbide-tipped-bowl-tray-1-4-radius-x-3-4-dia-x-5-8-x-1-4-inch-shank.html
        if ptd_tool == 45982:
            if ptd_depth > 6.35:
                return 15.875
            else:
                return ptd_tool
# Tapered Ball Nose
        if ptd_tool == 204:
            if ptd_depth > 6.35:
                return ptd_tool
        if ptd_tool == 304:
            if ptd_depth > 6.35:
                return ptd_tool
            else:
                return ptd_tool

    def tool_radius(self, ptd_tool, ptd_depth):
        tr = self.tool_diameter(ptd_tool, ptd_depth)/2
        return tr

    def stockandtoolpaths(self, option = "stockandtoolpaths"):
        if option == "stock":
            show(self.stock)
        elif option == "toolpaths":
            show(self.toolpaths)
        elif option == "rapids":
            show(self.rapids)
        else:
            part = self.stock.difference(self.rapids)
            part = self.stock.difference(self.toolpaths)
            show(part)

    def returnstockandtoolpaths(self):
        part = self.stock.difference(self.toolpaths)
        return part

    def writegc(self, *arguments):
        if self.generategcode == True:
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

    def opengcodefile(self, basefilename = "export",
                      currenttoolnum = 102,
                      toolradius = 3.175,
                      plunge = 400,
                      feed = 1600,
                      speed = 10000
                      ):
        self.basefilename = basefilename
        self.currenttoolnum = currenttoolnum
        self.toolradius = toolradius
        self.plunge = plunge
        self.feed = feed
        self.speed = speed
        if self.generategcode == True:
            self.gcodefilename = basefilename + ".nc"
            self.gc = open(self.gcodefilename, "w")
            self.writegc("(Design File: " + self.basefilename + ")")

    def opendxffile(self, basefilename = "export"):
        self.basefilename = basefilename
#        global generatedxfs
#        global dxfclosed
        self.dxfclosed = False
        self.dxfcolor = "Black"
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

    def dxfpreamble(self, tn):
#        self.writedxf(tn, str(tn))
        self.writedxf(tn, "0")
        self.writedxf(tn, "SECTION")
        self.writedxf(tn, "2")
        self.writedxf(tn, "ENTITIES")

    def setdxfcolor(self, color):
        self.dxfcolor = color
        self.cutcolor = color

    def writedxfcolor(self, tn):
            self.writedxf(tn, "8")
            if (self.dxfcolor == "Black"):
                self.writedxf(tn, "Layer_Black")
            if (self.dxfcolor == "Red"):
                self.writedxf(tn, "Layer_Red")
            if (self.dxfcolor == "Yellow"):
                self.writedxf(tn, "Layer_Yellow")
            if (self.dxfcolor == "Green"):
                self.writedxf(tn, "Layer_Green")
            if (self.dxfcolor == "Cyan"):
                self.writedxf(tn, "Layer_Cyan")
            if (self.dxfcolor == "Blue"):
                self.writedxf(tn, "Layer_Blue")
            if (self.dxfcolor == "Magenta"):
                self.writedxf(tn, "Layer_Magenta")
            if (self.dxfcolor == "White"):
                self.writedxf(tn, "Layer_White")
            if (self.dxfcolor == "Dark Gray"):
                self.writedxf(tn, "Layer_Dark_Gray")
            if (self.dxfcolor == "Light Gray"):
                self.writedxf(tn, "Layer_Light_Gray")

            self.writedxf(tn, "62")
            if (self.dxfcolor == "Black"):
                self.writedxf(tn, "0")
            if (self.dxfcolor == "Red"):
                self.writedxf(tn, "1")
            if (self.dxfcolor == "Yellow"):
                self.writedxf(tn, "2")
            if (self.dxfcolor == "Green"):
                self.writedxf(tn, "3")
            if (self.dxfcolor == "Cyan"):
                self.writedxf(tn, "4")
            if (self.dxfcolor == "Blue"):
                self.writedxf(tn, "5")
            if (self.dxfcolor == "Magenta"):
                self.writedxf(tn, "6")
            if (self.dxfcolor == "White"):
                self.writedxf(tn, "7")
            if (self.dxfcolor == "Dark Gray"):
                self.writedxf(tn, "8")
            if (self.dxfcolor == "Light Gray"):
                self.writedxf(tn, "9")

    def dxfline(self, tn, xbegin, ybegin, xend, yend):
        self.writedxf(tn, "0")
        self.writedxf(tn, "LINE")
#
        self.writedxfcolor(tn)
#
        self.writedxf(tn, "10")
        self.writedxf(tn, str(xbegin))
        self.writedxf(tn, "20")
        self.writedxf(tn, str(ybegin))
        self.writedxf(tn, "30")
        self.writedxf(tn, "0.0")
        self.writedxf(tn, "11")
        self.writedxf(tn, str(xend))
        self.writedxf(tn, "21")
        self.writedxf(tn, str(yend))
        self.writedxf(tn, "31")
        self.writedxf(tn, "0.0")

    def beginpolyline(self, tn):#, xbegin, ybegin
        self.writedxf(tn, "0")
        self.writedxf(tn, "POLYLINE")
        self.writedxf(tn, "8")
        self.writedxf(tn, "default")
        self.writedxf(tn, "66")
        self.writedxf(tn, "1")
#
        self.writedxfcolor(tn)
#
#        self.writedxf(tn, "10")
#        self.writedxf(tn, str(xbegin))
#        self.writedxf(tn, "20")
#        self.writedxf(tn, str(ybegin))
#        self.writedxf(tn, "30")
#        self.writedxf(tn, "0.0")
        self.writedxf(tn, "70")
        self.writedxf(tn, "0")

    def addvertex(self, tn, xend, yend):
        self.writedxf(tn, "0")
        self.writedxf(tn, "VERTEX")
        self.writedxf(tn, "8")
        self.writedxf(tn, "default")
        self.writedxf(tn, "70")
        self.writedxf(tn, "32")
        self.writedxf(tn, "10")
        self.writedxf(tn, str(xend))
        self.writedxf(tn, "20")
        self.writedxf(tn, str(yend))
        self.writedxf(tn, "30")
        self.writedxf(tn, "0.0")

    def closepolyline(self, tn):
        self.writedxf(tn, "0")
        self.writedxf(tn, "SEQEND")

    def dxfarc(self, tn, xcenter, ycenter, radius, anglebegin, endangle):
        if (self.generatedxf == True):
            self.writedxf(tn, "0")
            self.writedxf(tn, "ARC")
#
            self.writedxfcolor(tn)
#
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

    def gcodearc(self, tn, xcenter, ycenter, radius, anglebegin, endangle):
        if (self.generategcode == True):
            self.writegc(tn, "(0)")

    def cutarcNECCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(), self.ypos(), self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, 0, 90)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
#        if self.generatepaths == True:
#            print("Unioning cutarcNECCdxf toolpath")
        self.arcloop(1, 90, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
#        else:
#            toolpath = self.arcloop(1, 90, xcenter, ycenter, radius)
#            print("Returning cutarcNECCdxf toolpath")
        return toolpath

    def cutarcNWCCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(), self.ypos(), self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, 90, 180)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
#        if self.generatepaths == True:
#            self.arcloop(91, 180, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
#        else:
        toolpath = self.arcloop(91, 180, xcenter, ycenter, radius)
        return toolpath

    def cutarcSWCCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(), self.ypos(), self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, 180, 270)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.arcloop(181, 270, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.arcloop(181, 270, xcenter, ycenter, radius)
            return toolpath

    def cutarcSECCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(), self.ypos(), self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, 270, 360)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.arcloop(271, 360, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.arcloop(271, 360, xcenter, ycenter, radius)
            return toolpath

    def cutarcNECWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(), self.ypos(), self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, 0, 90)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.narcloop(89, 0, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.narcloop(89, 0, xcenter, ycenter, radius)
            return toolpath

    def cutarcSECWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(), self.ypos(), self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, 270, 360)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.narcloop(359, 270, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.narcloop(359, 270, xcenter, ycenter, radius)
            return toolpath

    def cutarcSWCWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(), self.ypos(), self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, 180, 270)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.narcloop(269, 180, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.narcloop(269, 180, xcenter, ycenter, radius)
            return toolpath

    def cutarcNWCWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(), self.ypos(), self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, 90, 180)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.narcloop(179, 90, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.narcloop(179, 90, xcenter, ycenter, radius)
            return toolpath

    def arcCCgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.writegc("G03 X", str(ex), " Y", str(ey), " Z", str(ez), " R", str(radius))

    def arcCWgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.writegc("G02 X", str(ex), " Y", str(ey), " Z", str(ez), " R", str(radius))

    def cutarcNECCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == True:
            self.cutarcNECCdxf(ex, ey, ez, xcenter, ycenter, radius)
        else:
            return self.cutarcNECCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcNWCCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcNWCCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSWCCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcSWCCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSECCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcSECCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcNECWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcNECWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSECWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcSECWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSWCWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcSWCWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcNWCWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcNWCWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def dxfpostamble(self, tn):
#        self.writedxf(tn, str(tn))
        self.writedxf(tn, "0")
        self.writedxf(tn, "ENDSEC")
        self.writedxf(tn, "0")
        self.writedxf(tn, "EOF")

    def gcodepostamble(self):
        self.writegc("Z12.700")
        self.writegc("M05")
        self.writegc("M02")

    def closegcodefile(self):
        if self.generategcode == True:
            self.gcodepostamble()
            self.gc.close()

    def closedxffile(self):
        if self.generatedxf == True:
#            global dxfclosed
            self.dxfpostamble(-1)
#            self.dxfclosed = True
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

    def dxfcircle(self, tool_num, xcenter, ycenter, radius):
        self.dxfarc(tool_num, xcenter, ycenter, radius,  0, 90)
        self.dxfarc(tool_num, xcenter, ycenter, radius, 90, 180)
        self.dxfarc(tool_num, xcenter, ycenter, radius, 180, 270)
        self.dxfarc(tool_num, xcenter, ycenter, radius, 270, 360)

    def cutcircleCC(self, xcenter, ycenter, bz, ez, radius):
        self.setzpos(bz)
        self.cutquarterCCNE(xcenter, ycenter + radius, self.zpos() + ez/4, radius)
        self.cutquarterCCNW(xcenter - radius, ycenter, self.zpos() + ez/4, radius)
        self.cutquarterCCSW(xcenter, ycenter - radius, self.zpos() + ez/4, radius)
        self.cutquarterCCSE(xcenter + radius, ycenter, self.zpos() + ez/4, radius)

    def cutcircleCCdxf(self, xcenter, ycenter, bz, ez, radius):
        self.cutcircleCC(self, xcenter, ycenter, bz, ez, radius)
        self.dxfcircle(self, tool_num, xcenter, ycenter, radius)

    def dxfrectangle(self, tool_num, xorigin, yorigin, xwidth, yheight, corners = "Square", radius = 6):
        if corners == "Square":
            self.dxfline(tool_num, xorigin, yorigin, xorigin + xwidth, yorigin)
            self.dxfline(tool_num, xorigin + xwidth, yorigin, xorigin + xwidth, yorigin + yheight)
            self.dxfline(tool_num, xorigin + xwidth, yorigin + yheight, xorigin, yorigin + yheight)
            self.dxfline(tool_num, xorigin, yorigin + yheight, xorigin, yorigin)
        elif corners == "Fillet":
            self.dxfrectangleround(tool_num, xorigin, yorigin, xwidth, yheight, radius)
        elif corners == "Chamfer":
            self.dxfrectanglechamfer(tool_num, xorigin, yorigin, xwidth, yheight, radius)
        elif corners == "Flipped Fillet":
            self.dxfrectangleflippedfillet(tool_num, xorigin, yorigin, xwidth, yheight, radius)

    def dxfrectangleround(self, tool_num, xorigin, yorigin, xwidth, yheight, radius):
# begin section
        self.writedxf(tool_num, "0")
        self.writedxf(tool_num, "SECTION")
        self.writedxf(tool_num, "2")
        self.writedxf(tool_num, "ENTITIES")
        self.writedxf(tool_num, "0")
        self.writedxf(tool_num, "LWPOLYLINE")
        self.writedxf(tool_num, "5")
        self.writedxf(tool_num, "4E")
        self.writedxf(tool_num, "100")
        self.writedxf(tool_num, "AcDbEntity")
        self.writedxf(tool_num, "8")
        self.writedxf(tool_num, "0")
        self.writedxf(tool_num, "6")
        self.writedxf(tool_num, "ByLayer")
#
        self.writedxfcolor(tool_num)
#
        self.writedxf(tool_num, "370")
        self.writedxf(tool_num, "-1")
        self.writedxf(tool_num, "100")
        self.writedxf(tool_num, "AcDbPolyline")
        self.writedxf(tool_num, "90")
        self.writedxf(tool_num, "8")
        self.writedxf(tool_num, "70")
        self.writedxf(tool_num, "1")
        self.writedxf(tool_num, "43")
        self.writedxf(tool_num, "0")
#1 upper right corner before arc (counter-clockwise)
        self.writedxf(tool_num, "10")
        self.writedxf(tool_num, str(xorigin + xwidth))
        self.writedxf(tool_num, "20")
        self.writedxf(tool_num, str(yorigin + yheight - radius))
        self.writedxf(tool_num, "42")
        self.writedxf(tool_num, "0.414213562373095")
#2 upper right corner after arc
        self.writedxf(tool_num, "10")
        self.writedxf(tool_num, str(xorigin + xwidth - radius))
        self.writedxf(tool_num, "20")
        self.writedxf(tool_num, str(yorigin + yheight))
#3 upper left corner before arc (counter-clockwise)
        self.writedxf(tool_num, "10")
        self.writedxf(tool_num, str(xorigin + radius))
        self.writedxf(tool_num, "20")
        self.writedxf(tool_num, str(yorigin + yheight))
        self.writedxf(tool_num, "42")
        self.writedxf(tool_num, "0.414213562373095")
#4 upper left corner after arc
        self.writedxf(tool_num, "10")
        self.writedxf(tool_num, str(xorigin))
        self.writedxf(tool_num, "20")
        self.writedxf(tool_num, str(yorigin + yheight - radius))
#5 lower left corner before arc (counter-clockwise)
        self.writedxf(tool_num, "10")
        self.writedxf(tool_num, str(xorigin))
        self.writedxf(tool_num, "20")
        self.writedxf(tool_num, str(yorigin + radius))
        self.writedxf(tool_num, "42")
        self.writedxf(tool_num, "0.414213562373095")
#6 lower left corner after arc
        self.writedxf(tool_num, "10")
        self.writedxf(tool_num, str(xorigin + radius))
        self.writedxf(tool_num, "20")
        self.writedxf(tool_num, str(yorigin))
#7 lower right corner before arc (counter-clockwise)
        self.writedxf(tool_num, "10")
        self.writedxf(tool_num, str(xorigin + xwidth - radius))
        self.writedxf(tool_num, "20")
        self.writedxf(tool_num, str(yorigin))
        self.writedxf(tool_num, "42")
        self.writedxf(tool_num, "0.414213562373095")
#8 lower right corner after arc
        self.writedxf(tool_num, "10")
        self.writedxf(tool_num, str(xorigin + xwidth))
        self.writedxf(tool_num, "20")
        self.writedxf(tool_num, str(yorigin + radius))
# end current section
        self.writedxf(tool_num, "0")
        self.writedxf(tool_num, "SEQEND")

    def dxfrectanglechamfer(self, tool_num, xorigin, yorigin, xwidth, yheight, radius):
        self.dxfline(tool_num, xorigin + radius, yorigin, xorigin, yorigin + radius)
        self.dxfline(tool_num, xorigin, yorigin + yheight - radius, xorigin + radius, yorigin + yheight)
        self.dxfline(tool_num, xorigin + xwidth - radius, yorigin + yheight, xorigin + xwidth, yorigin + yheight - radius)
        self.dxfline(tool_num, xorigin + xwidth - radius, yorigin, xorigin + xwidth, yorigin + radius)

        self.dxfline(tool_num, xorigin + radius, yorigin, xorigin + xwidth - radius, yorigin)
        self.dxfline(tool_num, xorigin + xwidth, yorigin + radius, xorigin + xwidth, yorigin + yheight - radius)
        self.dxfline(tool_num, xorigin + xwidth - radius, yorigin + yheight, xorigin + radius, yorigin + yheight)
        self.dxfline(tool_num, xorigin, yorigin + yheight - radius, xorigin, yorigin + radius)

    def dxfrectangleflippedfillet(self, tool_num, xorigin, yorigin, xwidth, yheight, radius):
        self.dxfarc(tool_num, xorigin, yorigin, radius,  0, 90)
        self.dxfarc(tool_num, xorigin + xwidth, yorigin, radius, 90, 180)
        self.dxfarc(tool_num, xorigin + xwidth, yorigin + yheight, radius, 180, 270)
        self.dxfarc(tool_num, xorigin, yorigin + yheight, radius, 270, 360)

        self.dxfline(tool_num, xorigin + radius, yorigin, xorigin + xwidth - radius, yorigin)
        self.dxfline(tool_num, xorigin + xwidth, yorigin + radius, xorigin + xwidth, yorigin + yheight - radius)
        self.dxfline(tool_num, xorigin + xwidth - radius, yorigin + yheight, xorigin + radius, yorigin + yheight)
        self.dxfline(tool_num, xorigin, yorigin + yheight - radius, xorigin, yorigin + radius)

    def cutrectangle(self, tool_num, bx, by, bz, xwidth, yheight, zdepth):
        self.cutline(bx, by, bz)
        self.cutline(bx, by, bz - zdepth)
        self.cutline(bx + xwidth, by, bz - zdepth)
        self.cutline(bx + xwidth, by + yheight, bz - zdepth)
        self.cutline(bx, by + yheight, bz - zdepth)
        self.cutline(bx, by, bz - zdepth)

    def cutrectangledxf(self, tool_num, bx, by, bz, xwidth, yheight, zdepth):
        self.cutrectangle(tool_num, bx, by, bz, xwidth, yheight, zdepth)
        self.dxfrectangle(tool_num, bx, by, xwidth, yheight, "Square")

    def cutrectangleround(self, tool_num, bx, by, bz, xwidth, yheight, zdepth, radius):
#        self.rapid(bx + radius, by, bz)
        self.cutline(bx + radius, by, bz + zdepth)
        self.cutline(bx + xwidth - radius, by, bz + zdepth)
        self.cutquarterCCSE(bx + xwidth, by + radius, bz + zdepth, radius)
        self.cutline(bx + xwidth, by + yheight - radius, bz + zdepth)
        self.cutquarterCCNE(bx + xwidth - radius, by + yheight, bz + zdepth, radius)
        self.cutline(bx + radius, by + yheight, bz + zdepth)
        self.cutquarterCCNW(bx, by + yheight - radius, bz + zdepth, radius)
        self.cutline(bx, by + radius, bz + zdepth)
        self.cutquarterCCSW(bx + radius, by, bz + zdepth, radius)

    def cutrectanglerounddxf(self, tool_num, bx, by, bz, xwidth, yheight, zdepth, radius):
        self.cutrectangleround(tool_num, bx, by, bz, xwidth, yheight, zdepth, radius)
        self.dxfrectangleround(tool_num, bx, by, xwidth, yheight, radius)

    def cutkeyholegcdxf(self, kh_tool_num, kh_start_depth, kh_max_depth, kht_direction, kh_distance):
        if (kht_direction == "N"):
            toolpath = self.cutKHgcdxf(kh_tool_num, kh_start_depth, kh_max_depth, 90, kh_distance)
        elif (kht_direction == "S"):
            toolpath = self.cutKHgcdxf(kh_tool_num, kh_start_depth, kh_max_depth, 270, kh_distance)
        elif (kht_direction == "E"):
            toolpath = self.cutKHgcdxf(kh_tool_num, kh_start_depth, kh_max_depth, 0, kh_distance)
        elif (kht_direction == "W"):
            toolpath = self.cutKHgcdxf(kh_tool_num, kh_start_depth, kh_max_depth, 180, kh_distance)
#        if self.generatepaths == True:
#            self.toolpaths = union([self.toolpaths, toolpath])
        return toolpath
#        else:
#            return cube([0.01, 0.01, 0.01])

    def cutKHgcdxf(self, kh_tool_num, kh_start_depth, kh_max_depth, kh_angle, kh_distance):
        oXpos = self.xpos()
        oYpos = self.ypos()
        self.dxfKH(kh_tool_num, self.xpos(), self.ypos(), kh_start_depth, kh_max_depth, kh_angle, kh_distance)
        toolpath = self.cutline(self.xpos(), self.ypos(), -kh_max_depth)
        self.setxpos(oXpos)
        self.setypos(oYpos)
#        if self.generatepaths == False:
        return toolpath
#        else:
#            return cube([0.001, 0.001, 0.001])

    def dxfKH(self, kh_tool_num, oXpos, oYpos, kh_start_depth, kh_max_depth, kh_angle, kh_distance):
#        oXpos = self.xpos()
#        oYpos = self.ypos()
#Circle at entry hole
        self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 7), 0, 90)
        self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 7), 90, 180)
        self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 7), 180, 270)
        self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 7), 270, 360)
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
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), self.tool_radius(kh_tool_num, 1), 180, 270)
#Upper left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), self.tool_radius(kh_tool_num, 1), 90, 180)
#Upper right of entry hole
#            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 41.810, 90)
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, angle, 90)
#Lower right of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 270, 360-angle)
#            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), self.tool_radius(kh_tool_num, 1), 270, 270+math.acos(math.radians(self.tool_diameter(kh_tool_num, 5)/self.tool_diameter(kh_tool_num, 1))))
#Actual line of cut
#            self.dxfline(kh_tool_num, self.xpos(), self.ypos(), self.xpos()+kh_distance, self.ypos())
#upper right of end of slot (kh_max_depth+4.36))/2
            self.dxfarc(kh_tool_num, self.xpos()+kh_distance, self.ypos(), self.tool_diameter(kh_tool_num, (kh_max_depth+4.36))/2, 0, 90)
#lower right of end of slot
            self.dxfarc(kh_tool_num, self.xpos()+kh_distance, self.ypos(), self.tool_diameter(kh_tool_num, (kh_max_depth+4.36))/2, 270, 360)
#upper right slot
            self.dxfline(kh_tool_num, self.xpos()+ro, self.ypos()-(self.tool_diameter(kh_tool_num, 7)/2), self.xpos()+kh_distance, self.ypos()-(self.tool_diameter(kh_tool_num, 7)/2))
#            self.dxfline(kh_tool_num, self.xpos()+(math.sqrt((self.tool_diameter(kh_tool_num, 1)^2)-(self.tool_diameter(kh_tool_num, 5)^2))/2), self.ypos()+self.tool_diameter(kh_tool_num, (kh_max_depth))/2, ( (kh_max_depth-6.34))/2)^2-(self.tool_diameter(kh_tool_num, (kh_max_depth-6.34))/2)^2, self.xpos()+kh_distance, self.ypos()+self.tool_diameter(kh_tool_num, (kh_max_depth))/2, kh_tool_num)
#end position at top of slot
#lower right slot
            self.dxfline(kh_tool_num, self.xpos()+ro, self.ypos()+(self.tool_diameter(kh_tool_num, 7)/2), self.xpos()+kh_distance, self.ypos()+(self.tool_diameter(kh_tool_num, 7)/2))
#        dxfline(kh_tool_num, self.xpos()+(math.sqrt((self.tool_diameter(kh_tool_num, 1)^2)-(self.tool_diameter(kh_tool_num, 5)^2))/2), self.ypos()-self.tool_diameter(kh_tool_num, (kh_max_depth))/2, ( (kh_max_depth-6.34))/2)^2-(self.tool_diameter(kh_tool_num, (kh_max_depth-6.34))/2)^2, self.xpos()+kh_distance, self.ypos()-self.tool_diameter(kh_tool_num, (kh_max_depth))/2, KH_tool_num)
#end position at top of slot
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos()+kh_distance, ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(), getypos(), -kh_max_depth, feed);
#    cutwithfeed(getxpos()+kh_distance, getypos(), -kh_max_depth, feed);
#    setxpos(getxpos()-kh_distance);
#  } else if (kh_angle > 0 && kh_angle < 90) {
#//echo(kh_angle);
#  dxfarc(getxpos(), getypos(), tool_diameter(KH_tool_num, (kh_max_depth))/2, 90+kh_angle, 180+kh_angle, KH_tool_num);
#  dxfarc(getxpos(), getypos(), tool_diameter(KH_tool_num, (kh_max_depth))/2, 180+kh_angle, 270+kh_angle, KH_tool_num);
#dxfarc(getxpos(), getypos(), tool_diameter(KH_tool_num, (kh_max_depth))/2, kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)), 90+kh_angle, KH_tool_num);
#dxfarc(getxpos(), getypos(), tool_diameter(KH_tool_num, (kh_max_depth))/2, 270+kh_angle, 360+kh_angle-asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)), KH_tool_num);
#dxfarc(getxpos()+(kh_distance*cos(kh_angle)),
#  getypos()+(kh_distance*sin(kh_angle)), tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2, 0+kh_angle, 90+kh_angle, KH_tool_num);
#dxfarc(getxpos()+(kh_distance*cos(kh_angle)), getypos()+(kh_distance*sin(kh_angle)), tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2, 270+kh_angle, 360+kh_angle, KH_tool_num);
#dxfline( getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2*cos(kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2))),
# getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2*sin(kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2))),
# getxpos()+(kh_distance*cos(kh_angle))-((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)*sin(kh_angle)),
# getypos()+(kh_distance*sin(kh_angle))+((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)*cos(kh_angle)), KH_tool_num);
#//echo("a", tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2);
#//echo("c", tool_diameter(KH_tool_num, (kh_max_depth))/2);
#echo("Aangle", asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)));
#//echo(kh_angle);
# cutwithfeed(getxpos()+(kh_distance*cos(kh_angle)), getypos()+(kh_distance*sin(kh_angle)), -kh_max_depth, feed);
#            toolpath = toolpath.union(self.cutline(self.xpos()+kh_distance, self.ypos(), -kh_max_depth))
        elif (kh_angle == 90):
#Lower left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 1), 180, 270)
#Lower right of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 1), 270, 360)
#left slot
            self.dxfline(kh_tool_num, oXpos-r, oYpos+ro, oXpos-r, oYpos+kh_distance)
#right slot
            self.dxfline(kh_tool_num, oXpos+r, oYpos+ro, oXpos+r, oYpos+kh_distance)
#upper left of end of slot
            self.dxfarc(kh_tool_num, oXpos, oYpos+kh_distance, r, 90, 180)
#upper right of end of slot
            self.dxfarc(kh_tool_num, oXpos, oYpos+kh_distance, r, 0, 90)
#Upper right of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 0, 90-angle)
#Upper left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 90+angle, 180)
#            toolpath = toolpath.union(self.cutline(oXpos, oYpos+kh_distance, -kh_max_depth))
        elif (kh_angle == 180):
#Lower right of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 1), 270, 360)
#Upper right of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 1), 0, 90)
#Upper left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 90, 180-angle)
#Lower left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 180+angle, 270)
#upper slot
            self.dxfline(kh_tool_num, oXpos-ro, oYpos-r, oXpos-kh_distance, oYpos-r)
#lower slot
            self.dxfline(kh_tool_num, oXpos-ro, oYpos+r, oXpos-kh_distance, oYpos+r)
#upper left of end of slot
            self.dxfarc(kh_tool_num, oXpos-kh_distance, oYpos, r, 90, 180)
#lower left of end of slot
            self.dxfarc(kh_tool_num, oXpos-kh_distance, oYpos, r, 180, 270)
#            toolpath = toolpath.union(self.cutline(oXpos-kh_distance, oYpos, -kh_max_depth))
        elif (kh_angle == 270):
#Upper left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 1), 90, 180)
#Upper right of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, self.tool_radius(kh_tool_num, 1), 0, 90)
#left slot
            self.dxfline(kh_tool_num, oXpos-r, oYpos-ro, oXpos-r, oYpos-kh_distance)
#right slot
            self.dxfline(kh_tool_num, oXpos+r, oYpos-ro, oXpos+r, oYpos-kh_distance)
#lower left of end of slot
            self.dxfarc(kh_tool_num, oXpos, oYpos-kh_distance, r, 180, 270)
#lower right of end of slot
            self.dxfarc(kh_tool_num, oXpos, oYpos-kh_distance, r, 270, 360)
#lower right of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 180, 270-angle)
#lower left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 270+angle, 360)
#            toolpath = toolpath.union(self.cutline(oXpos, oYpos-kh_distance, -kh_max_depth))
#        print(self.zpos())
#        self.setxpos(oXpos)
#        self.setypos(oYpos)
#        if self.generatepaths == False:
#            return toolpath

#  } else if (kh_angle == 90) {
#    //Lower left of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 180, 270, KH_tool_num);
#    //Lower right of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 270, 360, KH_tool_num);
#    //Upper right of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 0, acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
#    //Upper left of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 180-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 180, KH_tool_num);
#    //Actual line of cut
#    dxfline(getxpos(), getypos(), getxpos(), getypos()+kh_distance);
#    //upper right of slot
#    dxfarc(getxpos(), getypos()+kh_distance, tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2, 0, 90, KH_tool_num);
#    //upper left of slot
#    dxfarc(getxpos(), getypos()+kh_distance, tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2, 90, 180, KH_tool_num);
#    //right of slot
#    dxfline(
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        getypos()+(math.sqrt((tool_diameter(KH_tool_num, 1)^2)-(tool_diameter(KH_tool_num, 5)^2))/2), //( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#    //end position at top of slot
#        getypos()+kh_distance,
#        KH_tool_num);
#    dxfline(getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2, getypos()+(math.sqrt((tool_diameter(KH_tool_num, 1)^2)-(tool_diameter(KH_tool_num, 5)^2))/2), getxpos()-tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2, getypos()+kh_distance, KH_tool_num);
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos()+kh_distance, zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(), getypos(), -kh_max_depth, feed);
#    cutwithfeed(getxpos(), getypos()+kh_distance, -kh_max_depth, feed);
#    setypos(getypos()-kh_distance);
#  } else if (kh_angle == 180) {
#    //Lower right of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 270, 360, KH_tool_num);
#    //Upper right of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 0, 90, KH_tool_num);
#    //Upper left of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 90, 90+acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
#    //Lower left of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 270-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 270, KH_tool_num);
#    //upper left of slot
#    dxfarc(getxpos()-kh_distance, getypos(), tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2, 90, 180, KH_tool_num);
#    //lower left of slot
#    dxfarc(getxpos()-kh_distance, getypos(), tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2, 180, 270, KH_tool_num);
#    //Actual line of cut
#    dxfline(getxpos(), getypos(), getxpos()-kh_distance, getypos());
#    //upper left slot
#    dxfline(
#        getxpos()-(math.sqrt((tool_diameter(KH_tool_num, 1)^2)-(tool_diameter(KH_tool_num, 5)^2))/2),
#        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2, //( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()-kh_distance,
#    //end position at top of slot
#        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        KH_tool_num);
#    //lower right slot
#    dxfline(
#        getxpos()-(math.sqrt((tool_diameter(KH_tool_num, 1)^2)-(tool_diameter(KH_tool_num, 5)^2))/2),
#        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2, //( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()-kh_distance,
#    //end position at top of slot
#        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        KH_tool_num);
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos()-kh_distance, ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(), getypos(), -kh_max_depth, feed);
#    cutwithfeed(getxpos()-kh_distance, getypos(), -kh_max_depth, feed);
#    setxpos(getxpos()+kh_distance);
#  } else if (kh_angle == 270) {
#    //Upper right of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 0, 90, KH_tool_num);
#    //Upper left of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 90, 180, KH_tool_num);
#    //lower right of slot
#    dxfarc(getxpos(), getypos()-kh_distance, tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2, 270, 360, KH_tool_num);
#    //lower left of slot
#    dxfarc(getxpos(), getypos()-kh_distance, tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2, 180, 270, KH_tool_num);
#    //Actual line of cut
#    dxfline(getxpos(), getypos(), getxpos(), getypos()-kh_distance);
#    //right of slot
#    dxfline(
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        getypos()-(math.sqrt((tool_diameter(KH_tool_num, 1)^2)-(tool_diameter(KH_tool_num, 5)^2))/2), //( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#    //end position at top of slot
#        getypos()-kh_distance,
#        KH_tool_num);
#    //left of slot
#    dxfline(
#        getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        getypos()-(math.sqrt((tool_diameter(KH_tool_num, 1)^2)-(tool_diameter(KH_tool_num, 5)^2))/2), //( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
#    //end position at top of slot
#        getypos()-kh_distance,
#        KH_tool_num);
#    //Lower right of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 360-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 360, KH_tool_num);
#    //Lower left of entry hole
#    dxfarc(getxpos(), getypos(), 9.525/2, 180, 180+acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos()-kh_distance, zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(), getypos(), -kh_max_depth, feed);
#    cutwithfeed(getxpos(), getypos()-kh_distance, -kh_max_depth, feed);
#    setypos(getypos()+kh_distance);
#  }
#}

    def cut_pins(self, Joint_Width, stockZthickness, Number_of_Dovetails, Spacing, Proportion, DTT_diameter, DTT_angle):
        DTO = Tan(math.radians(DTT_angle)) * (stockZthickness * Proportion)
        DTR = DTT_diameter/2 - DTO
        cpr = self.rapidXY(0, stockZthickness + Spacing/2)
        ctp = self.cutlinedxfgc(self.xpos(), self.ypos(), -stockZthickness * Proportion)
#        ctp = ctp.union(self.cutlinedxfgc(Joint_Width / (Number_of_Dovetails * 2), self.ypos(), -stockZthickness * Proportion))
        i = 1
        while i < Number_of_Dovetails * 2:
#            print(i)
            ctp = ctp.union(self.cutlinedxfgc(i * (Joint_Width / (Number_of_Dovetails * 2)), self.ypos(), -stockZthickness * Proportion))
            ctp = ctp.union(self.cutlinedxfgc(i * (Joint_Width / (Number_of_Dovetails * 2)), (stockZthickness + Spacing) + (stockZthickness * Proportion) - (DTT_diameter/2), -(stockZthickness * Proportion)))
            ctp = ctp.union(self.cutlinedxfgc(i * (Joint_Width / (Number_of_Dovetails * 2)), stockZthickness + Spacing/2, -(stockZthickness * Proportion)))
            ctp = ctp.union(self.cutlinedxfgc((i + 1) * (Joint_Width / (Number_of_Dovetails * 2)), stockZthickness + Spacing/2,-(stockZthickness * Proportion)))
            self.dxfrectangleround(self.currenttoolnumber(),
                i * (Joint_Width / (Number_of_Dovetails * 2))-DTR,
                stockZthickness + (Spacing/2) - DTR,
                DTR * 2,
                (stockZthickness * Proportion) + Spacing/2 + DTR * 2 - (DTT_diameter/2),
                DTR)
            i += 2
        self.rapidZ(0)
        return ctp

    def cut_tails(self, Joint_Width, stockZthickness, Number_of_Dovetails, Spacing, Proportion, DTT_diameter, DTT_angle):
        DTO = Tan(math.radians(DTT_angle)) * (stockZthickness * Proportion)
        DTR = DTT_diameter/2 - DTO
        cpr = self.rapidXY(0, 0)
        ctp = self.cutlinedxfgc(self.xpos(), self.ypos(), -stockZthickness * Proportion)
        ctp = ctp.union(self.cutlinedxfgc(
            Joint_Width / (Number_of_Dovetails * 2) - (DTT_diameter - DTO),
            self.ypos(),
            -stockZthickness * Proportion))
        i = 1
        while i < Number_of_Dovetails * 2:
            ctp = ctp.union(self.cutlinedxfgc(
                i * (Joint_Width / (Number_of_Dovetails * 2)) - (DTT_diameter - DTO),
                stockZthickness * Proportion - DTT_diameter / 2,
                -(stockZthickness * Proportion)))
            ctp = ctp.union(self.cutarcCWdxf(180, 90,
                i * (Joint_Width / (Number_of_Dovetails * 2)),
                stockZthickness * Proportion - DTT_diameter / 2,
#                self.ypos(),
                DTT_diameter - DTO,  0, 1))
            ctp = ctp.union(self.cutarcCWdxf(90, 0,
                i * (Joint_Width / (Number_of_Dovetails * 2)),
                stockZthickness * Proportion - DTT_diameter / 2,
                DTT_diameter - DTO,  0, 1))
            ctp = ctp.union(self.cutlinedxfgc(
                i * (Joint_Width / (Number_of_Dovetails * 2)) + (DTT_diameter - DTO),
                0,
                -(stockZthickness * Proportion)))
            ctp = ctp.union(self.cutlinedxfgc(
                (i + 2) * (Joint_Width / (Number_of_Dovetails * 2)) - (DTT_diameter - DTO),
                0,
                -(stockZthickness * Proportion)))
            i += 2
        self.rapidZ(0)
        self.rapidXY(0, 0)
        ctp = ctp.union(self.cutlinedxfgc(self.xpos(), self.ypos(), -stockZthickness * Proportion))
        self.dxfarc(self.currenttoolnumber(), 0, 0, DTR, 180, 270)
        self.dxfline(self.currenttoolnumber(), -DTR, 0, -DTR, stockZthickness + DTR)
        self.dxfarc(self.currenttoolnumber(), 0, stockZthickness + DTR, DTR, 90, 180)
        self.dxfline(self.currenttoolnumber(), 0, stockZthickness + DTR * 2, Joint_Width, stockZthickness + DTR * 2)
        i = 0
        while i < Number_of_Dovetails * 2:
            ctp = ctp.union(self.cutline(i * (Joint_Width / (Number_of_Dovetails * 2)), stockZthickness + DTO, -(stockZthickness * Proportion)))
            ctp = ctp.union(self.cutline((i+2) * (Joint_Width / (Number_of_Dovetails * 2)), stockZthickness + DTO, -(stockZthickness * Proportion)))
            ctp = ctp.union(self.cutline((i+2) * (Joint_Width / (Number_of_Dovetails * 2)), 0, -(stockZthickness * Proportion)))
            self.dxfarc(self.currenttoolnumber(), i * (Joint_Width / (Number_of_Dovetails * 2)), 0, DTR, 270, 360)
            self.dxfline(self.currenttoolnumber(),
                i * (Joint_Width / (Number_of_Dovetails * 2)) + DTR,
                0,
                i * (Joint_Width / (Number_of_Dovetails * 2)) + DTR, stockZthickness * Proportion - DTT_diameter / 2)
            self.dxfarc(self.currenttoolnumber(), (i + 1) * (Joint_Width / (Number_of_Dovetails * 2)), stockZthickness * Proportion - DTT_diameter / 2, (Joint_Width / (Number_of_Dovetails * 2)) - DTR, 90, 180)
            self.dxfarc(self.currenttoolnumber(), (i + 1) * (Joint_Width / (Number_of_Dovetails * 2)), stockZthickness * Proportion - DTT_diameter / 2, (Joint_Width / (Number_of_Dovetails * 2)) - DTR, 0, 90)
            self.dxfline(self.currenttoolnumber(),
                (i + 2) * (Joint_Width / (Number_of_Dovetails * 2)) - DTR,
                0,
                (i + 2) * (Joint_Width / (Number_of_Dovetails * 2)) - DTR, stockZthickness * Proportion - DTT_diameter / 2)
            self.dxfarc(self.currenttoolnumber(), (i + 2) * (Joint_Width / (Number_of_Dovetails * 2)), 0, DTR, 180, 270)
            i += 2
        self.dxfarc(self.currenttoolnumber(), Joint_Width, stockZthickness + DTR, DTR, 0, 90)
        self.dxfline(self.currenttoolnumber(), Joint_Width + DTR, stockZthickness + DTR, Joint_Width + DTR, 0)
        self.dxfarc(self.currenttoolnumber(), Joint_Width, 0, DTR, 270, 360)
        return ctp

    def Full_Blind_Finger_Joint_square(self, bx, by, orientation, side, width, thickness, Number_of_Pins, largeVdiameter, smallDiameter, normalormirror = "Default"):
    # Joint_Orientation = "Horizontal" "Even" == "Lower", "Odd" == "Upper"
    # Joint_Orientation = "Vertical" "Even" == "Left", "Odd" == "Right"
        if (orientation == "Vertical"):
            if (normalormirror == "Default" and side != "Both"):
                if (side == "Left"):
                     normalormirror = "Even"
                if (side == "Right"):
                     normalormirror = "Odd"
        if (orientation == "Horizontal"):
            if (normalormirror == "Default" and side != "Both"):
                if (side == "Lower"):
                     normalormirror = "Even"
                if (side == "Upper"):
                     normalormirror = "Odd"
        Finger_Width = ((Number_of_Pins * 2) - 1) * smallDiameter * 1.1
        Finger_Origin = width/2 - Finger_Width/2
        rapid = self.rapidZ(0)
        self.setdxfcolor("Cyan")
        rapid = rapid.union(self.rapidXY(bx, by))
        toolpath = (self.Finger_Joint_square(bx, by, orientation, side, width, thickness, Number_of_Pins, Finger_Origin, smallDiameter))
        if (orientation == "Vertical"):
            if (side == "Both"):
                toolpath = self.cutrectanglerounddxf(self.currenttoolnum, bx - (thickness - smallDiameter/2), by-smallDiameter/2, 0, (thickness * 2) - smallDiameter, width+smallDiameter, (smallDiameter / 2) / Tan(math.radians(45)), smallDiameter/2)
            if (side == "Left"):
                toolpath = self.cutrectanglerounddxf(self.currenttoolnum, bx - (smallDiameter/2), by-smallDiameter/2, 0, thickness, width+smallDiameter, ((smallDiameter / 2) / Tan(math.radians(45))), smallDiameter/2)
            if (side == "Right"):
                toolpath = self.cutrectanglerounddxf(self.currenttoolnum, bx - (thickness - smallDiameter/2), by-smallDiameter/2, 0, thickness, width+smallDiameter, ((smallDiameter / 2) / Tan(math.radians(45))), smallDiameter/2)
        toolpath = toolpath.union(self.Finger_Joint_square(bx, by, orientation, side, width, thickness, Number_of_Pins, Finger_Origin, smallDiameter))
        if (orientation == "Horizontal"):
            if (side == "Both"):
                toolpath = self.cutrectanglerounddxf(
                    self.currenttoolnum,
                    bx-smallDiameter/2,
                    by - (thickness - smallDiameter/2),
                    0,
                    width+smallDiameter,
                    (thickness * 2) - smallDiameter,
                    (smallDiameter / 2) / Tan(math.radians(45)),
                    smallDiameter/2)
            if (side == "Lower"):
                toolpath = self.cutrectanglerounddxf(
                    self.currenttoolnum,
                    bx - (smallDiameter/2),
                    by - smallDiameter/2,
                    0,
                    width+smallDiameter,
                    thickness,
                    ((smallDiameter / 2) / Tan(math.radians(45))),
                    smallDiameter/2)
            if (side == "Upper"):
                toolpath = self.cutrectanglerounddxf(
                    self.currenttoolnum,
                    bx - smallDiameter/2,
                    by - (thickness - smallDiameter/2),
                    0,
                    width+smallDiameter,
                    thickness,
                    ((smallDiameter / 2) / Tan(math.radians(45))),
                    smallDiameter/2)
        toolpath = toolpath.union(self.Finger_Joint_square(bx, by, orientation, side, width, thickness, Number_of_Pins, Finger_Origin, smallDiameter))
        return toolpath

    def Finger_Joint_square(self, bx, by, orientation, side, width, thickness, Number_of_Pins, Finger_Origin, smallDiameter, normalormirror = "Default"):
        jointdepth = -(thickness - (smallDiameter / 2) / Tan(math.radians(45)))
    # Joint_Orientation = "Horizontal" "Even" == "Lower", "Odd" == "Upper"
    # Joint_Orientation = "Vertical" "Even" == "Left", "Odd" == "Right"
        if (orientation == "Vertical"):
            if (normalormirror == "Default" and side != "Both"):
                if (side == "Left"):
                     normalormirror = "Even"
                if (side == "Right"):
                     normalormirror = "Odd"
        if (orientation == "Horizontal"):
            if (normalormirror == "Default" and side != "Both"):
                if (side == "Lower"):
                     normalormirror = "Even"
                if (side == "Upper"):
                     normalormirror = "Odd"
        radius = smallDiameter/2
        jointwidth = thickness - smallDiameter
        toolpath = self.currenttool()
        rapid = self.rapidZ(0)
        self.setdxfcolor("Blue")
        toolpath = toolpath.union(self.cutlineZgcfeed(jointdepth,1000))
        self.beginpolyline(self.currenttool())
        if (orientation == "Vertical"):
            rapid = rapid.union(self.rapidXY(bx, by + Finger_Origin))
            self.addvertex(self.currenttoolnumber(), self.xpos(), self.ypos())
            toolpath = toolpath.union(self.cutlineZgcfeed(jointdepth,1000))
            i = 0
            while i <= Number_of_Pins - 1:
                if (side == "Right"):
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + smallDiameter + radius/5, jointdepth))
                if (side == "Left" or side == "Both"):
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + radius, jointdepth))
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + jointwidth, self.ypos(), jointdepth))
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + radius/5, jointdepth))
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos() - jointwidth, self.ypos(), jointdepth))
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + radius, jointdepth))
                if (side == "Left"):
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + smallDiameter + radius/5, jointdepth))
                if (side == "Right" or side == "Both"):
                    if (i < (Number_of_Pins - 1)):
    #                    print(i)
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + radius, jointdepth))
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos() - jointwidth, self.ypos(), jointdepth))
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + radius/5, jointdepth))
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + jointwidth, self.ypos(), jointdepth))
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + radius, jointdepth))
                i += 1
    # Joint_Orientation = "Horizontal" "Even" == "Lower", "Odd" == "Upper"
        if (orientation == "Horizontal"):
            rapid = rapid.union(self.rapidXY(bx + Finger_Origin, by))
            self.addvertex(self.currenttoolnumber(), self.xpos(), self.ypos())
            toolpath = toolpath.union(self.cutlineZgcfeed(jointdepth,1000))
            i = 0
            while i <= Number_of_Pins - 1:
                if (side == "Upper"):
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + smallDiameter + radius/5, self.ypos(), jointdepth))
                if (side == "Lower" or side == "Both"):
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + radius, self.ypos(), jointdepth))
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + jointwidth, jointdepth))
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + radius/5, self.ypos(), jointdepth))
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() - jointwidth, jointdepth))
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + radius, self.ypos(), jointdepth))
                if (side == "Lower"):
                    toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + smallDiameter + radius/5, self.ypos(), jointdepth))
                if (side == "Upper" or side == "Both"):
                    if (i < (Number_of_Pins - 1)):
    #                    print(i)
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + radius, self.ypos(), jointdepth))
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() - jointwidth, jointdepth))
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + radius/5, self.ypos(), jointdepth))
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos(), self.ypos() + jointwidth, jointdepth))
                        toolpath = toolpath.union(self.cutvertexdxf(self.xpos() + radius, self.ypos(), jointdepth))
                i += 1
        self.closepolyline(self.currenttoolnumber())
        return toolpath

    def Full_Blind_Finger_Joint_smallV(self, bx, by, orientation, side, width, thickness, Number_of_Pins, largeVdiameter, smallDiameter):
        rapid = self.rapidZ(0)
    #    rapid = rapid.union(self.rapidXY(bx, by))
        self.setdxfcolor("Red")
        if (orientation == "Vertical"):
            rapid = rapid.union(self.rapidXY(bx, by - smallDiameter/6))
            toolpath = self.cutlineZgcfeed(-thickness,1000)
            toolpath = self.cutlinedxfgc(bx, by + width + smallDiameter/6, - thickness)
        if (orientation == "Horizontal"):
            rapid = rapid.union(self.rapidXY(bx - smallDiameter/6, by))
            toolpath = self.cutlineZgcfeed(-thickness,1000)
            toolpath = self.cutlinedxfgc(bx + width + smallDiameter/6, by, -thickness)
    #        rapid = self.rapidZ(0)

        return toolpath

    def Full_Blind_Finger_Joint_largeV(self, bx, by, orientation, side, width, thickness, Number_of_Pins, largeVdiameter, smallDiameter):
        radius = smallDiameter/2
        rapid = self.rapidZ(0)
        Finger_Width = ((Number_of_Pins * 2) - 1) * smallDiameter * 1.1
        Finger_Origin = width/2 - Finger_Width/2
    #    rapid = rapid.union(self.rapidXY(bx, by))
    # Joint_Orientation = "Horizontal" "Even" == "Lower", "Odd" == "Upper"
    # Joint_Orientation = "Vertical" "Even" == "Left", "Odd" == "Right"
        if (orientation == "Vertical"):
            rapid = rapid.union(self.rapidXY(bx, by))
            toolpath = self.cutlineZgcfeed(-thickness,1000)
            toolpath = toolpath.union(self.cutlinedxfgc(bx, by + Finger_Origin, -thickness))
            rapid = self.rapidZ(0)
            rapid = rapid.union(self.rapidXY(bx, by + width - Finger_Origin))
            self.setdxfcolor("Blue")
            toolpath = toolpath.union(self.cutlineZgcfeed(-thickness,1000))
            toolpath = toolpath.union(self.cutlinedxfgc(bx, by + width, -thickness))
            if (side == "Left" or side == "Both"):
                rapid = self.rapidZ(0)
                self.setdxfcolor("Dark Gray")
                rapid = rapid.union(self.rapidXY(bx+thickness-(smallDiameter / 2) / Tan(math.radians(45)), by - radius/2))
                toolpath = toolpath.union(self.cutlineZgcfeed(-(smallDiameter / 2) / Tan(math.radians(45)),10000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx+thickness-(smallDiameter / 2) / Tan(math.radians(45)), by + width + radius/2, -(smallDiameter / 2) / Tan(math.radians(45))))
                rapid = self.rapidZ(0)
                self.setdxfcolor("Green")
                rapid = rapid.union(self.rapidXY(bx+thickness/2, by+width))
                toolpath = toolpath.union(self.cutlineZgcfeed(-thickness/2,1000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx+thickness/2, by + width -thickness, -thickness/2))
                rapid = self.rapidZ(0)
                rapid = rapid.union(self.rapidXY(bx+thickness/2, by))
                toolpath = toolpath.union(self.cutlineZgcfeed(-thickness/2,1000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx+thickness/2, by +thickness, -thickness/2))
            if (side == "Right" or side == "Both"):
                rapid = self.rapidZ(0)
                self.setdxfcolor("Dark Gray")
                rapid = rapid.union(self.rapidXY(bx-(thickness-(smallDiameter / 2) / Tan(math.radians(45))), by - radius/2))
                toolpath = toolpath.union(self.cutlineZgcfeed(-(smallDiameter / 2) / Tan(math.radians(45)),10000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx-(thickness-(smallDiameter / 2) / Tan(math.radians(45))), by + width + radius/2, -(smallDiameter / 2) / Tan(math.radians(45))))
                rapid = self.rapidZ(0)
                self.setdxfcolor("Green")
                rapid = rapid.union(self.rapidXY(bx-thickness/2, by+width))
                toolpath = toolpath.union(self.cutlineZgcfeed(-thickness/2,1000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx-thickness/2, by + width -thickness, -thickness/2))
                rapid = self.rapidZ(0)
                rapid = rapid.union(self.rapidXY(bx-thickness/2, by))
                toolpath = toolpath.union(self.cutlineZgcfeed(-thickness/2,1000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx-thickness/2, by +thickness, -thickness/2))
    # Joint_Orientation = "Horizontal" "Even" == "Lower", "Odd" == "Upper"
        if (orientation == "Horizontal"):
            rapid = rapid.union(self.rapidXY(bx, by))
            self.setdxfcolor("Blue")
            toolpath = self.cutlineZgcfeed(-thickness,1000)
            toolpath = toolpath.union(self.cutlinedxfgc(bx + Finger_Origin, by, -thickness))
            rapid = rapid.union(self.rapidZ(0))
            rapid = rapid.union(self.rapidXY(bx + width - Finger_Origin, by))
            toolpath = toolpath.union(self.cutlineZgcfeed(-thickness,1000))
            toolpath = toolpath.union(self.cutlinedxfgc(bx + width, by, -thickness))
            if (side == "Lower" or side == "Both"):
                rapid = self.rapidZ(0)
                self.setdxfcolor("Dark Gray")
                rapid = rapid.union(self.rapidXY(bx - radius, by+thickness-(smallDiameter / 2) / Tan(math.radians(45))))
                toolpath = toolpath.union(self.cutlineZgcfeed(-(smallDiameter / 2) / Tan(math.radians(45)),10000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx + width + radius, by+thickness-(smallDiameter / 2) / Tan(math.radians(45)), -(smallDiameter / 2) / Tan(math.radians(45))))
                rapid = self.rapidZ(0)
                self.setdxfcolor("Green")
                rapid = rapid.union(self.rapidXY(bx+width, by+thickness/2))
                toolpath = toolpath.union(self.cutlineZgcfeed(-thickness/2,1000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx + width -thickness, by+thickness/2, -thickness/2))
                rapid = self.rapidZ(0)
                rapid = rapid.union(self.rapidXY(bx, by+thickness/2))
                toolpath = toolpath.union(self.cutlineZgcfeed(-thickness/2,1000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx +thickness, by+thickness/2, -thickness/2))
            if (side == "Upper" or side == "Both"):
                rapid = self.rapidZ(0)
                self.setdxfcolor("Dark Gray")
                rapid = rapid.union(self.rapidXY(bx - radius, by-(thickness-(smallDiameter / 2) / Tan(math.radians(45)))))
                toolpath = toolpath.union(self.cutlineZgcfeed(-(smallDiameter / 2) / Tan(math.radians(45)),10000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx + width + radius, by-(thickness-(smallDiameter / 2) / Tan(math.radians(45))), -(smallDiameter / 2) / Tan(math.radians(45))))
                rapid = self.rapidZ(0)
                self.setdxfcolor("Green")
                rapid = rapid.union(self.rapidXY(bx+width, by-thickness/2))
                toolpath = toolpath.union(self.cutlineZgcfeed(-thickness/2,1000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx + width -thickness, by-thickness/2, -thickness/2))
                rapid = self.rapidZ(0)
                rapid = rapid.union(self.rapidXY(bx, by-thickness/2))
                toolpath = toolpath.union(self.cutlineZgcfeed(-thickness/2,1000))
                toolpath = toolpath.union(self.cutlinedxfgc(bx +thickness, by-thickness/2, -thickness/2))
        rapid = self.rapidZ(0)
        return toolpath

    def Full_Blind_Finger_Joint(self, bx, by, orientation, side, width, thickness, largeVdiameter, smallDiameter, normalormirror = "Default", squaretool = 102, smallV = 390, largeV = 301):
        Number_of_Pins = int(((width - thickness * 2) / (smallDiameter * 2.2) / 2) + 0.0) * 2 + 1
#        print("Number of Pins: ",Number_of_Pins)
        self.movetosafeZ()
        self.toolchange(squaretool, 17000)
        toolpath = self.Full_Blind_Finger_Joint_square(bx, by, orientation, side, width, thickness, Number_of_Pins, largeVdiameter, smallDiameter)
        self.movetosafeZ()
        self.toolchange(smallV, 17000)
        toolpath = toolpath.union(self.Full_Blind_Finger_Joint_smallV(bx, by, orientation, side, width, thickness, Number_of_Pins, largeVdiameter, smallDiameter))
        self.toolchange(largeV, 17000)
        toolpath = toolpath.union(self.Full_Blind_Finger_Joint_largeV(bx, by, orientation, side, width, thickness, Number_of_Pins, largeVdiameter, smallDiameter))
        return toolpath

    def previewgcodefile(self, gc_file):
        gc_file = open(gc_file, 'r')
        gcfilecontents = []
        with gc_file as file:
            for line in file:
                command = line
                gcfilecontents.append(line)

        numlinesfound = 0
        for line in gcfilecontents:
#            print(line)
            if line[:10] == "(stockMin:":
                subdivisions = line.split()
                extentleft = float(subdivisions[0][10:-3])
                extentfb = float(subdivisions[1][:-3])
                extentd = float(subdivisions[2][:-3])
                numlinesfound = numlinesfound + 1
            if line[:13] == "(STOCK/BLOCK,":
                subdivisions = line.split()
                sizeX = float(subdivisions[0][13:-1])
                sizeY = float(subdivisions[1][:-1])
                sizeZ = float(subdivisions[4][:-1])
                numlinesfound = numlinesfound + 1
            if line[:3] == "G21":
                units = "mm"
                numlinesfound = numlinesfound + 1
            if numlinesfound >=3:
                break
#            print(numlinesfound)

        self.setupcuttingarea(sizeX, sizeY, sizeZ, extentleft, extentfb, extentd)

        commands = []
        for line in gcfilecontents:
            Xc = 0
            Yc = 0
            Zc = 0
            Fc = 0
            Xp = 0.0
            Yp = 0.0
            Zp = 0.0
            if line == "G53G0Z-5.000\n":
                 self.movetosafeZ()
            if line[:3] == "M6T":
                tool = int(line[3:])
                self.toolchange(tool)
            if line[:2] == "G0":
                machinestate = "rapid"
            if line[:2] == "G1":
                machinestate = "cutline"
            if line[:2] == "G0" or line[:2] == "G1" or line[:1] == "X" or line[:1] == "Y" or line[:1] == "Z":
                if "F" in line:
                    Fplus = line.split("F")
                    Fc = 1
                    fr = float(Fplus[1])
                    line = Fplus[0]
                if "Z" in line:
                    Zplus = line.split("Z")
                    Zc = 1
                    Zp = float(Zplus[1])
                    line = Zplus[0]
                if "Y" in line:
                    Yplus = line.split("Y")
                    Yc = 1
                    Yp = float(Yplus[1])
                    line = Yplus[0]
                if "X" in line:
                    Xplus = line.split("X")
                    Xc = 1
                    Xp = float(Xplus[1])
                if Zc == 1:
                    if Yc == 1:
                        if Xc == 1:
                            if machinestate == "rapid":
                                command = "rapidXYZ(" + str(Xp) + ", " + str(Yp) + ", " + str(Zp) + ")"
                                self.rapidXYZ(Xp, Yp, Zp)
                            else:
                                command = "cutlineXYZ(" + str(Xp) + ", " + str(Yp) + ", " + str(Zp) + ")"
                                self.cutlineXYZ(Xp, Yp, Zp)
                        else:
                            if machinestate == "rapid":
                                command = "rapidYZ(" + str(Yp) + ", " + str(Zp) + ")"
                                self.rapidYZ(Yp, Zp)
                            else:
                                command = "cutlineYZ(" + str(Yp) + ", " + str(Zp) + ")"
                                self.cutlineYZ(Yp, Zp)
                    else:
                        if Xc == 1:
                            if machinestate == "rapid":
                                command = "rapidXZ(" + str(Xp) + ", " + str(Zp) + ")"
                                self.rapidXZ(Xp, Zp)
                            else:
                                command = "cutlineXZ(" + str(Xp) + ", " + str(Zp) + ")"
                                self.cutlineXZ(Xp, Zp)
                        else:
                            if machinestate == "rapid":
                                command = "rapidZ(" + str(Zp) + ")"
                                self.rapidZ(Zp)
                            else:
                                command = "cutlineZ(" + str(Zp) + ")"
                                self.cutlineZ(Zp)
                else:
                    if Yc == 1:
                        if Xc == 1:
                            if machinestate == "rapid":
                                command = "rapidXY(" + str(Xp) + ", " + str(Yp) + ")"
                                self.rapidXY(Xp, Yp)
                            else:
                                command = "cutlineXY(" + str(Xp) + ", " + str(Yp) + ")"
                                self.cutlineXY(Xp, Yp)
                        else:
                            if machinestate == "rapid":
                                command = "rapidY(" + str(Yp) + ")"
                                self.rapidY(Yp)
                            else:
                                command = "cutlineY(" + str(Yp) + ")"
                                self.cutlineY(Yp)
                    else:
                        if Xc == 1:
                            if machinestate == "rapid":
                                command = "rapidX(" + str(Xp) + ")"
                                self.rapidX(Xp)
                            else:
                                command = "cutlineX(" + str(Xp) + ")"
                                self.cutlineX(Xp)
                commands.append(command)
#                print(line)
#                print(command)
#                print(machinestate, Xc, Yc, Zc)
#                print(Xp, Yp, Zp)
#                print("/n")

#        for command in commands:
#            print(command)

        show(self.stockandtoolpaths())

