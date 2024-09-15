//!OpenSCAD

use <gcodepreview.py>;
use <pygcodepreview.scad>;
include <gcodepreview.scad>;

$fa = 2;
$fs = 0.125;

/* [Export] */
Base_filename = "export";
/* [Export] */
generatedxf = true;
/* [Export] */
generategcode = true;
///* [Export] */
//generatesvg = false;

/* [CAM] */
toolradius = 1.5875;
/* [CAM] */
large_ball_tool_no = 0; // [0:0,111:111,101:101,202:202]
/* [CAM] */
large_square_tool_no = 0; // [0:0,112:112,102:102,201:201]
/* [CAM] */
large_V_tool_no = 0; // [0:0,301:301,690:690]
/* [CAM] */
small_ball_tool_no = 0; // [0:0,121:121,111:111,101:101]
/* [CAM] */
small_square_tool_no = 102; // [0:0,122:122,112:112,102:102]
/* [CAM] */
small_V_tool_no = 0; // [0:0,390:390,301:301]
/* [CAM] */
KH_tool_no = 0; // [0:0,374:374,375:375,376:376,378]
/* [CAM] */
DT_tool_no = 0; // [0:0,814:814]
/* [CAM] */
Roundover_tool_no = 56125; // [56125:56125, 56142:56142,312:312, 1570:1570]
/* [CAM] */
MISC_tool_no = 0; //

/* [Feeds and Speeds] */
plunge = 100;
/* [Feeds and Speeds] */
feed = 400;
/* [Feeds and Speeds] */
speed = 16000;
/* [Feeds and Speeds] */
small_square_ratio = 0.75; // [0.25:2]
/* [Feeds and Speeds] */
small_ball_ratio = 0.75; // [0.25:2]
/* [Feeds and Speeds] */
large_ball_ratio = 1.0; // [0.25:2]
/* [Feeds and Speeds] */
small_V_ratio = 0.625; // [0.25:2]
/* [Feeds and Speeds] */
large_V_ratio = 0.875; // [0.25:2]
/* [Feeds and Speeds] */
KH_ratio = 0.75; // [0.25:2]
/* [Feeds and Speeds] */
DT_ratio = 0.75; // [0.25:2]
/* [Feeds and Speeds] */
RO_ratio = 0.5; // [0.25:2]
/* [Feeds and Speeds] */
MISC_ratio = 0.5; // [0.25:2]

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

filename_gcode = str(Base_filename, ".nc");
filename_dxf = str(Base_filename);

opengcodefile(filename_gcode);
opendxffile(filename_dxf);

difference() {
setupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin);

movetosafez();

toolchange(small_square_tool_no,speed * small_square_ratio);

begintoolpath(0,0,0.25);

cutoneaxis_setfeed("Z",0,plunge*small_square_ratio);

cutwithfeed(stocklength/2,stockwidth/2,-stockthickness,feed);
dxfpolyline(getxpos(),getypos(),stocklength/2,stockwidth/2, small_square_tool_no);

endtoolpath();
rapid(-(stocklength/4-stockwidth/16),stockwidth/4,0);
cutoneaxis_setfeed("Z",-stockthickness,plunge*small_square_ratio);

cutarcNECCdxf(-stocklength/4, stockwidth/4+stockwidth/16, -stockthickness, -stocklength/4, stockwidth/4, stockwidth/16, small_square_tool_no);
cutarcNWCCdxf(-(stocklength/4+stockwidth/16), stockwidth/4, -stockthickness, -stocklength/4, stockwidth/4, stockwidth/16, small_square_tool_no);
cutarcSWCCdxf(-stocklength/4, stockwidth/4-stockwidth/16, -stockthickness, -stocklength/4, stockwidth/4, stockwidth/16, small_square_tool_no);
cutarcSECCdxf(-(stocklength/4-stockwidth/16), stockwidth/4, -stockthickness, -stocklength/4, stockwidth/4, stockwidth/16, small_square_tool_no);

rapid(getxpos(),getypos(),stockthickness);
toolchange(KH_tool_no,speed * KH_ratio);
rapid(-stocklength/8,-stockwidth/4,0);

cutkeyhole_toolpath((stockthickness), (stockthickness), "N", stockwidth/8, KH_tool_no);
rapid(getxpos(),getypos(),stockthickness);
rapid(-stocklength/4,-stockwidth/4,0);
cutkeyhole_toolpath((stockthickness), (stockthickness), "S", stockwidth/8, KH_tool_no);
rapid(getxpos(),getypos(),stockthickness);
rapid(-stocklength/4,-stockwidth/8,0);
cutkeyhole_toolpath((stockthickness), (stockthickness), "E", stockwidth/8, KH_tool_no);
rapid(getxpos(),getypos(),stockthickness);
rapid(-stocklength/8,-stockwidth/8*3,0);
cutkeyhole_toolpath((stockthickness), (stockthickness), "W", stockwidth/8, KH_tool_no);

rapid(getxpos(),getypos(),stockthickness);
toolchange(DT_tool_no,speed * DT_ratio);
rapid(0,-(stockwidth/2+tool_diameter(DT_tool_no,0)),0);

cutoneaxis_setfeed("Z",-stockthickness,plunge*DT_ratio);
cutwithfeed(0,-(stockwidth/4),-stockthickness,feed*DT_ratio);
rapid(0,-(stockwidth/2+tool_diameter(DT_tool_no,0)),-stockthickness);

rapid(getxpos(),getypos(),stockthickness);
toolchange(Roundover_tool_no, speed * RO_ratio);
rapid(-(stocklength/2),-(stockwidth/2),0);
cutoneaxis_setfeed("Z",-4.509,plunge*RO_ratio);

cutroundovertool(-(stocklength/2++0.507/2), -(stockwidth/2+0.507/2), -4.509, stocklength/2+0.507/2, -(stockwidth/2+0.507/2), -4.509, 0.507/2, 4.509);

cutroundover(stocklength/2+0.507/2, -(stockwidth/2+0.507/2), -4.509, stocklength/2+0.507/2, stockwidth/2+0.507/2, -4.509, 1570);
cutroundover(stocklength/2+0.507/2, stockwidth/2+0.507/2, -4.509, -(stocklength/2+0.507/2), stockwidth/2+0.507/2, -4.509, 1570);
cutroundover(-(stocklength/2+0.507/2), stockwidth/2+0.507/2, -4.509, -(stocklength/2+0.507/2), -(stockwidth/2+0.507/2), -4.509, 1570);
}

closegcodefile();
closedxffile();
