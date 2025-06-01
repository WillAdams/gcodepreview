#!/usr/bin/env python

import math

from openscad import *

class threeDmodelturtle:

    def __init__(self,
                 xpos = 0,
                 ypos = 0,
                 zpos = 0,
                 XYdir = 0,
                 Zdir = 0,
                 size = 5,
                 turtle = sphere
                 ):
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.XYdir = XYdir
        self.Zdir = Zdir
        self.size = size
        self.turtle = turtle
        self.model = sphere(0.000000001)

    def left(self, angle):
        self.XYdir = self.XYdir + angle
        if self.XYdir > 360 :
            self.XYdir = self.XYdir - 360
        
    def right(self, angle):
        self.XYdir = self.XYdir + (360 - angle)
        if self.XYdir < 360 :
            self.XYdir = self.XYdir + 360

    def incline(self, angle):
        self.Zdir = self.Zdir - angle
        
    def decline(self, angle):
        self.Zdir = self.Zdir + angle

    def forward(self, steps):
        if self.turtle == sphere :
            tortoise = sphere(self.size/2)
        pastturtle = tortoise.translate([self.xpos, self.ypos, self.zpos])
        xpast = self.xpos
        ypast = self.ypos
        zpast = self.zpos
        dot = sphere(self.size/4)
        if self.XYdir == 0 :
            self.xpos = self.xpos + steps
        if (self.XYdir > 0 and self.XYdir <90) :
            self.xpos = self.xpos + math.cos(math.radians(self.XYdir)) * steps
            self.ypos = self.ypos + math.sin(math.radians(self.XYdir)) * steps
        if self.XYdir == 90 : 
            self.ypos = self.ypos + steps
        if (self.XYdir > 90 and self.XYdir <180) :
            self.xpos = self.xpos + math.sin(math.radians(90 - self.XYdir)) * steps
            self.ypos = self.ypos + math.cos(math.radians(90 - self.XYdir)) * steps
        if self.XYdir == 180 :
            self.xpos = self.xpos - steps
        if (self.XYdir > 180 and self.XYdir <270) :
            self.xpos = self.xpos - math.cos(math.radians(180 - self.XYdir)) * steps
            self.ypos = self.ypos + math.sin(math.radians(180 - self.XYdir)) * steps
        if self.XYdir == 270 : 
            self.ypos = self.ypos - steps
        if (self.XYdir > 270 and self.XYdir <360) :
            self.xpos = self.xpos - math.sin(math.radians(270 - self.XYdir)) * steps
            self.ypos = self.ypos - math.cos(math.radians(270 - self.XYdir)) * steps
        futureturtle = tortoise.translate([self.xpos, self.ypos, self.zpos])  
        path = hull(dot.translate([xpast, ypast, zpast]), dot.translate([self.xpos, self.ypos, self.zpos]))
        self.model = self.model.union(pastturtle, path, futureturtle)
    
    def climb(self,steps):
        if self.turtle == sphere :
            tortoise = sphere(self.size/2)
        zpast = self.zpos
        pastturtle = tortoise.translate([self.xpos, self.ypos, self.zpos])
        dot = sphere(self.size/4)
        self.zpos = self.zpos + steps
        futureturtle = tortoise.translate([self.xpos, self.ypos, self.zpos])  
        path = hull(dot.translate([self.xpos, self.ypos, zpast]), dot.translate([self.xpos, self.ypos, self.zpos]))
        self.model = self.model.union(pastturtle, path, futureturtle)

    def descend(self,steps):
        if self.turtle == sphere :
            tortoise = sphere(self.size/2)
        zpast = self.zpos
        pastturtle = tortoise.translate([self.xpos, self.ypos, self.zpos])
        dot = sphere(self.size/4)
        self.zpos = self.zpos - steps
        futureturtle = tortoise.translate([self.xpos, self.ypos, self.zpos])  
        path = hull(dot.translate([self.xpos, self.ypos, zpast]), dot.translate([self.xpos, self.ypos, self.zpos]))
        self.model = self.model.union(pastturtle, path, futureturtle)
        
    def showmodel(self):
        show(self.model)  
        
