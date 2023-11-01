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

def popensvgfile(fn):
    global svg
    svg = open(fn, "w")

def writeln(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    f.write(line_to_write)
    f.write("\n")

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

def writesvg(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    svg.write(line_to_write)
    print(line_to_write)

def pwritesvgline():
    svg.write("\n")

def pclosegcodefile():
    f.close()

def pclosesvgfile():
    svg.close()

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

def psetupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin):
    global mpx
    mpx = float(0)
    global mpy
    mpy = float(0)
    global mpz
    mpz = float(0)
    global currenttool
    currenttool = 102

def psettool(tn):
    global currenttool
    currenttool = tn

def pcurrent_tool():
    global currenttool
    return currenttool

def xpos():
    global mpx
    return mpx

def ypos():
    global mpy
    return mpy

def zpos():
    global mpz
    return mpz

def psetxpos(newxpos):
    global mpx
    mpx = newxpos

def psetypos(newypos):
    global mpy
    mpy = newypos

def psetzpos(newzpos):
    global mpz
    mpz = newzpos
