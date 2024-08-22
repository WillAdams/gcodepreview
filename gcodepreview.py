#!/usr/bin/env python
#"C:\Program Files\OpenSCAD\bin\openscad.exe" --trust-python
#Currently tested with 2023.11.30 and Python 3.11
#gcodepreview 0.5, see gcodepreview.scad

def writeln(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    f.write(line_to_write)
    f.write("\n")

def psetupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin):
    global mpx
    mpx = float(0)
    global mpy
    mpy = float(0)
    global mpz
    mpz = float(0)
    global tpz
    tpz = float(0)
    global currenttool
    currenttool = 102

def xpos():
    global mpx
    return mpx

def ypos():
    global mpy
    return mpy

def zpos():
    global mpz
    return mpz

def tzpos():
    global tpz
    return tpz

def psetxpos(newxpos):
    global mpx
    mpx = newxpos

def psetypos(newypos):
    global mpy
    mpy = newypos

def psetzpos(newzpos):
    global mpz
    mpz = newzpos

def psettzpos(newtzpos):
    global tpz
    tpz = newtzpos

def psettool(tn):
    global currenttool
    currenttool = tn

def pcurrent_tool():
    global currenttool
    return currenttool

def ptool_diameter(ptd_tool, ptd_depth):
    if ptd_tool == 201:
        return 6.35
    if ptd_tool == 202:
        if ptd_depth > 3.175:
            return 6.35
        else:
            return 0
    if ptd_tool == 102:
        return 3.175
    if ptd_tool == 101:
        if ptd_depth > 1.5875:
            return 3.175
        else:
            return 0
    if ptd_tool == 301:
        return 0
    if ptd_tool == 302:
        return 0
    if ptd_tool == 390:
        return 0
    if ptd_tool == 375:
        if ptd_depth < 6.35:
            return 9.525
        else:
            return 6.35
    if ptd_tool == 814:
        if ptd_depth > 12.7:
            return 6.35
        else:
            return 12.7

def popengcodefile(fn):
    global f
    f = open(fn, "w")

def popendxffile(fn):
    global dxf
    dxf = open(fn, "w")

def popendxlgblffile(fn):
    global dxflgbl
    dxflgbl = open(fn, "w")

def popendxflgsqfile(fn):
    global dxfldsq
    dxflgsq = open(fn, "w")

def popendxflgVfile(fn):
    global dxflgV
    dxflgV = open(fn, "w")

def popendxfsmblfile(fn):
    global dxfsmbl
    dxfsmbl = open(fn, "w")

def popendxfsmsqfile(fn):
    global dxfsmsq
    dxfsmsq = open(fn, "w")

def popendxfsmVfile(fn):
    global dxfsmV
    dxfsmV = open(fn, "w")

def popendxfKHfile(fn):
    global dxfKH
    dxfKH = open(fn, "w")

def popendxDTfile(fn):
    global dxfDT
    dxfDT = open(fn, "w")

def writedxf(*arguments):
    line_to_write = ""
    for element in arguments:
       line_to_write += element
    dxf.write(line_to_write)
    dxf.write("\n")

def writedxflgbl(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    dxflgbl.write(line_to_write)
    print(line_to_write)
    dxflgbl.write("\n")

def writedxflgsq(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    dxflgsq.write(line_to_write)
    print(line_to_write)
    dxflgsq.write("\n")

def writedxflgV(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    dxflgV.write(line_to_write)
    print(line_to_write)
    dxflgV.write("\n")

def writedxfsmbl(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    dxfsmbl.write(line_to_write)
    print(line_to_write)
    dxfsmbl.write("\n")

def writedxfsmsq(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    dxfsmsq.write(line_to_write)
    print(line_to_write)
    dxfsmsq.write("\n")

def writedxfsmV(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    dxfsmV.write(line_to_write)
    print(line_to_write)
    dxfsmV.write("\n")

def writedxfKH(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    dxfKH.write(line_to_write)
    print(line_to_write)
    dxfKH.write("\n")

def writedxfDT(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    dxfDT.write(line_to_write)
    print(line_to_write)
    dxfDT.write("\n")

def pclosegcodefile():
    f.close()

def pclosedxffile():
    dxf.close()

def pclosedxflgblfile():
    dxflgbl.close()

def pclosedxflgsqfile():
    dxflgsq.close()

def pclosedxflgVfile():
    dxflgV.close()

def pclosedxfsmblfile():
    dxfsmbl.close()

def pclosedxfsmsqfile():
    dxfsmsq.close()

def pclosedxfsmVfile():
    dxfsmV.close()

def pclosedxfDTfile():
    dxfDT.close()

def pclosedxfKHfile():
    dxfKH.close()

