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
 KH_tool_no = 0; // [0:0,375:375]

 /* [CAM] */
 DT_tool_no = 0; // [0:0,814:814]

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

 filename_gcode = str(Base_filename, ".nc");
 filename_dxf = str(Base_filename);
 //filename_svg = str(Base_filename, ".svg");

 opengcodefile(filename_gcode);
 opendxffile(filename_dxf);

 difference() {
 setupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin);

 movetosafez();

 toolchange(small_square_tool_no,speed * square_ratio);

 begintoolpath(0,0,0.25);
 beginpolyline(0,0,0.25);

 cutoneaxis_setfeed("Z",0,plunge*square_ratio);

 cutwithfeed(stocklength/2,stockwidth/2,-stockthickness,feed);
 addpolyline(stocklength/2,stockwidth/2,-stockthickness);

 endtoolpath();
 closepolyline();
 }

 closegcodefile();
 closedxffile();
