# import csv --- did not work

def popengcodefile(fn):
    global f
    f = open(fn, "w")

def writeln(*arguments):
    line_to_write = ""
    for element in arguments:
        line_to_write += element
    f.write(line_to_write)
    f.write("\n")

def pclosegcodefile():
    f.close()

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

def setxpos(newxpos):
    global mpx
    mpx = newxpos

def setypos(newypos):
    global mpy
    mpy = newypos

def setzpos(newzpos):
    global mpz
    mpz = newzpos
