//!OpenSCAD

use <gcodepreview.py>;
use <pygcodepreview.scad>;
include <gcodepreview.scad>;

$fa = 2;
$fs = 0.125;

/* [G-code] */
Gcode_filename = "gcode.nc"; 
/* [G-code] */
generategcode = true;

/* [DXF] */
DXF_filename = "gcode.dxf"; 
/* [DXF] */
generatedxf = true;

/* [CAM] */
feedrate = 850;
/* [CAM] */
plungerate = 425;
/* [CAM] */
toolradius = 1.5875;
/* [CAM] */
squaretoolno = 102;

/* [Feeds and Speeds] */
plunge = 100;
/* [Feeds and Speeds] */
feed = 400;
/* [Feeds and Speeds] */
speed = 16000;
/* [Feeds and Speeds] */
square_ratio = 1.0; // [0.25:2]
/* [Feeds and Speeds] */
small_V_ratio = 0.75; // [0.25:2]
/* [Feeds and Speeds] */
large_V_ratio = 0.875; // [0.25:2]

/* [Stock] */
stocklength = 219;
/* [Stock] */
stockwidth = 150;
/* [Stock] */
stockthickness = 8.35;
/* [Stock] */
zeroheight = "Top"; // [Top, Bottom]
/* [Stock] */
stockorigin = "Center"; // [Lower-Left, Center-Left, Top-Left, Center]
/* [Stock] */
retractheight = 9;

opengcodefile(Gcode_filename);
opendxffile(DXF_filename);

difference() {
setupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin);

movetosafez();

toolchange(squaretoolno,speed * square_ratio);

begintoolpath(0,0,0.25);
beginpolyline(0,0,0.25);

cutoneaxis_setfeed("Z",-1,plunge*square_ratio);

cutwithfeed(stocklength/2,stockwidth/2,-stockthickness,feed);
addpolyline(stocklength/2,stockwidth/2,-stockthickness);

endtoolpath();

}

closegcodefile();
closedxffile();
