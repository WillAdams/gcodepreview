# gcodepreview
OpenSCAD library for moving a tool in lines and arcs so as to model how a part would be cut using G-Code.

A BlockSCAD file for the main modules is available at:

https://www.blockscad3d.com/community/projects/1244473

The project is discussed at:

https://community.carbide3d.com/t/previewing-g-code-using-openscad/35153

Usage is:

Place the file in C:\Users\~\Documents\OpenSCAD\libraries

    include <gcodepreview.scad>;

and then use the commands:

difference() {
  cube([Stock Length, Stock Width, Stock Thickness], center=false);

  gcut(bx, by, bz, ex, ey, ez, tn);

  garcCW(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn);

  garcCCW(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn);
  
}

Where:

beginning coordinates:
  bx
  by
  bz

ending coordinates:
  ex
  ey
  ez
  
offsets:
  xoffset
  yoffset
  
Tool Number:
  tn
