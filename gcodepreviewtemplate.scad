//!OpenSCAD

use <gcodepreview.py>;
use <pygcodepreview.scad>;
include <gcodepreview.scad>;

$fa = 2;
$fs = 0.125;

/* [Stock] */
stockXwidth = 219;
/* [Stock] */
stockYheight = 150;
/* [Stock] */
stockZthickness = 8.35;
/* [Stock] */
zeroheight = "Top"; // [Top, Bottom]
/* [Stock] */
stockzero = "Center"; // [Lower-Left, Center-Left, Top-Left, Center]
/* [Stock] */
retractheight = 9;

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
large_square_tool_num = 0; // [0:0,112:112,102:102,201:201]
/* [CAM] */
small_square_tool_num = 102; // [0:0,122:122,112:112,102:102]
/* [CAM] */
large_ball_tool_num = 0; // [0:0,111:111,101:101,202:202]
/* [CAM] */
small_ball_tool_num = 0; // [0:0,121:121,111:111,101:101]
/* [CAM] */
large_V_tool_num = 0; // [0:0,301:301,690:690]
/* [CAM] */
small_V_tool_num = 0; // [0:0,390:390,301:301]
/* [CAM] */
DT_tool_num = 0; // [0:0,814:814]
/* [CAM] */
KH_tool_num = 0; // [0:0,374:374,375:375,376:376,378]
/* [CAM] */
Roundover_tool_num = 0; // [56142:56142, 56125:56125, 1570:1570]
/* [CAM] */
MISC_tool_num = 0; //

/* [Feeds and Speeds] */
plunge = 100;
/* [Feeds and Speeds] */
feed = 400;
/* [Feeds and Speeds] */
speed = 16000;
/* [Feeds and Speeds] */
small_square_ratio = 0.75; // [0.25:2]
/* [Feeds and Speeds] */
large_ball_ratio = 1.0; // [0.25:2]
/* [Feeds and Speeds] */
small_ball_ratio = 0.75; // [0.25:2]
/* [Feeds and Speeds] */
large_V_ratio = 0.875; // [0.25:2]
/* [Feeds and Speeds] */
small_V_ratio = 0.625; // [0.25:2]
/* [Feeds and Speeds] */
DT_ratio = 0.75; // [0.25:2]
/* [Feeds and Speeds] */
KH_ratio = 0.75; // [0.25:2]
/* [Feeds and Speeds] */
RO_ratio = 0.5; // [0.25:2]
/* [Feeds and Speeds] */
MISC_ratio = 0.5; // [0.25:2]

filename_gcode = str(Base_filename, ".nc");
filename_dxf = str(Base_filename);

opengcodefile(filename_gcode);
opendxffile(filename_dxf);

difference() {
setupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero);

movetosafez();

toolchange(small_square_tool_num,speed * small_square_ratio);

begintoolpath(0,0,0.25);

cutoneaxis_setfeed("Z",0,plunge*small_square_ratio);

cutwithfeed(stockXwidth/2,stockYheight/2,-stockZthickness,feed);
dxfline(getxpos(),getypos(),stockXwidth/2,stockYheight/2, small_square_tool_num);

endtoolpath();
rapid(-(stockXwidth/4-stockYheight/16),stockYheight/4,0);
cutoneaxis_setfeed("Z",-stockZthickness,plunge*small_square_ratio);

cutarcNECCdxf(-stockXwidth/4, stockYheight/4+stockYheight/16, -stockZthickness, -stockXwidth/4, stockYheight/4, stockYheight/16, small_square_tool_num);
cutarcNWCCdxf(-(stockXwidth/4+stockYheight/16), stockYheight/4, -stockZthickness, -stockXwidth/4, stockYheight/4, stockYheight/16, small_square_tool_num);
cutarcSWCCdxf(-stockXwidth/4, stockYheight/4-stockYheight/16, -stockZthickness, -stockXwidth/4, stockYheight/4, stockYheight/16, small_square_tool_num);
cutarcSECCdxf(-(stockXwidth/4-stockYheight/16), stockYheight/4, -stockZthickness, -stockXwidth/4, stockYheight/4, stockYheight/16, small_square_tool_num);

rapid(getxpos(),getypos(),stockZthickness);
toolchange(KH_tool_num,speed * KH_ratio);
rapid(-stockXwidth/8,-stockYheight/4,0);

cutkeyhole_toolpath((stockZthickness), (stockZthickness), "N", stockYheight/8, KH_tool_num);
rapid(getxpos(),getypos(),stockZthickness);
rapid(-stockXwidth/4,-stockYheight/4,0);
cutkeyhole_toolpath((stockZthickness), (stockZthickness), "S", stockYheight/8, KH_tool_num);
rapid(getxpos(),getypos(),stockZthickness);
rapid(-stockXwidth/4,-stockYheight/8,0);
cutkeyhole_toolpath((stockZthickness), (stockZthickness), "E", stockYheight/8, KH_tool_num);
rapid(getxpos(),getypos(),stockZthickness);
rapid(-stockXwidth/8,-stockYheight/8*3,0);
cutkeyhole_toolpath((stockZthickness), (stockZthickness), "W", stockYheight/8, KH_tool_num);

rapid(getxpos(),getypos(),stockZthickness);
toolchange(DT_tool_num,speed * DT_ratio);
rapid(0,-(stockYheight/2+tool_diameter(DT_tool_num,0)),0);

cutoneaxis_setfeed("Z",-stockZthickness,plunge*DT_ratio);
cutwithfeed(0,-(stockYheight/4),-stockZthickness,feed*DT_ratio);
rapid(0,-(stockYheight/2+tool_diameter(DT_tool_num,0)),-stockZthickness);

rapid(getxpos(),getypos(),stockZthickness);
toolchange(Roundover_tool_num, speed * RO_ratio);
rapid(-(stockXwidth/2),-(stockYheight/2),0);
cutoneaxis_setfeed("Z",-4.509,plunge*RO_ratio);

cutroundovertool(-(stockXwidth/2++0.507/2), -(stockYheight/2+0.507/2), -4.509, stockXwidth/2+0.507/2, -(stockYheight/2+0.507/2), -4.509, 0.507/2, 4.509);

cutroundover(stockXwidth/2+0.507/2, -(stockYheight/2+0.507/2), -4.509, stockXwidth/2+0.507/2, stockYheight/2+0.507/2, -4.509, 1570);
cutroundover(stockXwidth/2+0.507/2, stockYheight/2+0.507/2, -4.509, -(stockXwidth/2+0.507/2), stockYheight/2+0.507/2, -4.509, 1570);
cutroundover(-(stockXwidth/2+0.507/2), stockYheight/2+0.507/2, -4.509, -(stockXwidth/2+0.507/2), -(stockYheight/2+0.507/2), -4.509, 1570);

//for (i = [0 : abs(1) : 80]) {
//  cutwithfeed(stockXwidth/4,-stockYheight/4,-stockZthickness/4,feed);
//  cutwithfeed(stockXwidth/8+(stockXwidth/256*i),-stockYheight/2,-stockZthickness*3/4,feed);
//  }

hull(){
  cutwithfeed(stockXwidth/4,-stockYheight/4,-stockZthickness/4,feed);
  cutwithfeed(stockXwidth/8,-stockYheight/2,-stockZthickness*3/4,feed);
  cutwithfeed(stockXwidth/8+(stockXwidth*0.3125),-stockYheight/2,-stockZthickness*3/4,feed);
  }
}

closegcodefile();
closedxffile();
