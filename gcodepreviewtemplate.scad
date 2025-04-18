//!OpenSCAD

use <gcodepreview.py>
include <gcodepreview.scad>

$fa = 2;
$fs = 0.125;
fa = 2;
fs = 0.125;

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
generatepaths = true;
/* [Export] */
generatedxf = true;
/* [Export] */
generategcode = true;

/* [CAM] */
toolradius = 1.5875;
/* [CAM] */
large_square_tool_num = 0; // [0:0, 112:112, 102:102, 201:201]
/* [CAM] */
small_square_tool_num = 102; // [0:0, 122:122, 112:112, 102:102]
/* [CAM] */
large_ball_tool_num = 0; // [0:0, 111:111, 101:101, 202:202]
/* [CAM] */
small_ball_tool_num = 0; // [0:0, 121:121, 111:111, 101:101]
/* [CAM] */
large_V_tool_num = 0; // [0:0, 301:301, 690:690]
/* [CAM] */
small_V_tool_num = 0; // [0:0, 390:390, 301:301]
/* [CAM] */
DT_tool_num = 0; // [0:0, 814:814, 808079:808079]
/* [CAM] */
KH_tool_num = 0; // [0:0, 374:374, 375:375, 376:376, 378:378]
/* [CAM] */
Roundover_tool_num = 0; // [56142:56142, 56125:56125, 1570:1570]
/* [CAM] */
MISC_tool_num = 0; // [648:648, 45982:45982]
//648 threadmill_shaft(2.4, 0.75, 18)
//45982 Carbide Tipped Bowl & Tray 1/4 Radius x 3/4 Dia x 5/8 x 1/4 Inch Shank

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

thegeneratepaths = generatepaths == true ? 1 : 0;
thegeneratedxf = generatedxf == true ? 1 : 0;
thegenerategcode = generategcode == true ? 1 : 0;

gcp = gcodepreview(thegeneratepaths,
                   thegenerategcode,
                   thegeneratedxf,
                   );

opengcodefile(Base_filename);
opendxffile(Base_filename);
opendxffiles(Base_filename,
                 large_square_tool_num,
                 small_square_tool_num,
                 large_ball_tool_num,
                 small_ball_tool_num,
                 large_V_tool_num,
                 small_V_tool_num,
                 DT_tool_num,
                 KH_tool_num,
                 Roundover_tool_num,
                 MISC_tool_num);

setupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero);

//echo(gcp);
//gcpversion();

//c = myfunc(4);
//echo(c);

//echo(getvv());

cutline(stockXwidth/2, stockYheight/2, -stockZthickness);

rapidZ(retractheight);
toolchange(201, 10000);
rapidXY(0, stockYheight/16);
rapidZ(0);
cutlinedxfgc(stockXwidth/16*7, stockYheight/2, -stockZthickness);


rapidZ(retractheight);
toolchange(202, 10000);
rapidXY(0, stockYheight/8);
rapidZ(0);
cutlinedxfgc(stockXwidth/16*6, stockYheight/2, -stockZthickness);

rapidZ(retractheight);
toolchange(101, 10000);
rapidXY(0, stockYheight/16*3);
rapidZ(0);
cutlinedxfgc(stockXwidth/16*5, stockYheight/2, -stockZthickness);

rapidZ(retractheight);
toolchange(390, 10000);
rapidXY(0, stockYheight/16*4);
rapidZ(0);

cutlinedxfgc(stockXwidth/16*4, stockYheight/2, -stockZthickness);
rapidZ(retractheight);

toolchange(301, 10000);
rapidXY(0, stockYheight/16*6);
rapidZ(0);

cutlinedxfgc(stockXwidth/16*2, stockYheight/2, -stockZthickness);


movetosafeZ();
rapid(gcp.xpos(), gcp.ypos(), retractheight);
toolchange(102, 10000);

//rapidXY(stockXwidth/4+stockYheight/8+stockYheight/16, +stockYheight/8);
rapidXY(-stockXwidth/4+stockXwidth/16, (stockYheight/4));//+stockYheight/16
rapidZ(0);

//cutarcCW(360, 270, gcp.xpos()-stockYheight/16, gcp.ypos(), stockYheight/16, -stockZthickness);
//gcp.cutarcCW(270, 180, gcp.xpos(), gcp.ypos()+stockYheight/16, stockYheight/16))
cutarcCC(0, 90, gcp.xpos()-stockYheight/16, gcp.ypos(), stockYheight/16, -stockZthickness/4);
cutarcCC(90, 180, gcp.xpos(), gcp.ypos()-stockYheight/16, stockYheight/16, -stockZthickness/4);
cutarcCC(180, 270, gcp.xpos()+stockYheight/16, gcp.ypos(), stockYheight/16, -stockZthickness/4);
cutarcCC(270, 360, gcp.xpos(), gcp.ypos()+stockYheight/16, stockYheight/16, -stockZthickness/4);

movetosafeZ();
//rapidXY(stockXwidth/4+stockYheight/8-stockYheight/16, -stockYheight/8);
rapidXY(stockXwidth/4-stockYheight/16, -(stockYheight/4));
rapidZ(0);

cutarcCW(180, 90, gcp.xpos()+stockYheight/16, gcp.ypos(), stockYheight/16, -stockZthickness/4);
cutarcCW(90, 0, gcp.xpos(), gcp.ypos()-stockYheight/16, stockYheight/16, -stockZthickness/4);
cutarcCW(360, 270, gcp.xpos()-stockYheight/16, gcp.ypos(), stockYheight/16, -stockZthickness/4);
cutarcCW(270, 180, gcp.xpos(), gcp.ypos()+stockYheight/16, stockYheight/16, -stockZthickness/4);

movetosafeZ();
toolchange(201, 10000);
rapidXY(stockXwidth /2 -6.34, - stockYheight /2);
rapidZ(0);
cutarcCW(180, 90, stockXwidth /2, -stockYheight/2, 6.34, - stockZthickness);

movetosafeZ();
rapidXY(stockXwidth/2, -stockYheight/2);
rapidZ(0);

gcp.cutlinedxfgc(gcp.xpos(), gcp.ypos(), -stockZthickness);

movetosafeZ();
toolchange(814, 10000);
rapidXY(0, -(stockYheight/2+12.7));
rapidZ(0);

cutlinedxfgc(xpos(), ypos(), -stockZthickness);
cutlinedxfgc(xpos(), -12.7, -stockZthickness);
rapidXY(0, -(stockYheight/2+12.7));

//rapidXY(stockXwidth/2-6.34, -stockYheight/2);
//rapidZ(0);

//movetosafeZ();
//toolchange(374, 10000);
//rapidXY(-(stockXwidth/4 - stockXwidth /16), -(stockYheight/4 + stockYheight/16))

//cutline(xpos(), ypos(), (stockZthickness/2) * -1);
//cutlinedxfgc(xpos() + stockYheight /9, ypos(), zpos());
//cutline(xpos() - stockYheight /9, ypos(), zpos());
//cutline(xpos(), ypos(), 0);

movetosafeZ();

toolchange(374, 10000);
rapidXY(-stockXwidth/4-stockXwidth/16, -(stockYheight/4+stockYheight/16))
//rapidXY(-(stockXwidth/4 - stockXwidth /16), -(stockYheight/4 + stockYheight/16))
rapidZ(0);

cutline(xpos(), ypos(), (stockZthickness/2) * -1);
cutlinedxfgc(xpos() + stockYheight /9, ypos(), zpos());
cutline(xpos() - stockYheight /9, ypos(), zpos());
cutline(xpos(), ypos(), 0);

rapidZ(retractheight);
rapidXY(-stockXwidth/4+stockXwidth/16, -(stockYheight/4+stockYheight/16));
rapidZ(0);
cutline(gcp.xpos(), gcp.ypos(), -stockZthickness/2);
cutlinedxfgc(gcp.xpos(), gcp.ypos()+stockYheight/9, gcp.zpos());
cutline(gcp.xpos(), gcp.ypos()-stockYheight/9, gcp.zpos());
cutline(gcp.xpos(), gcp.ypos(), 0);

rapidZ(retractheight);
rapidXY(-stockXwidth/4+stockXwidth/16, -(stockYheight/4-stockYheight/8));
rapidZ(0);
cutline(gcp.xpos(), gcp.ypos(), -stockZthickness/2);
cutlinedxfgc(gcp.xpos()-stockYheight/9, gcp.ypos(), gcp.zpos());
cutline(gcp.xpos()+stockYheight/9, gcp.ypos(), gcp.zpos());
cutline(gcp.xpos(), gcp.ypos(), 0);

rapidZ(retractheight);
rapidXY(-stockXwidth/4-stockXwidth/16, -(stockYheight/4-stockYheight/8));
rapidZ(0);
cutline(gcp.xpos(), gcp.ypos(), -stockZthickness/2);
cutlinedxfgc(gcp.xpos(), gcp.ypos()-stockYheight/9, gcp.zpos());
cutline(gcp.xpos(), gcp.ypos()+stockYheight/9, gcp.zpos());
cutline(gcp.xpos(), gcp.ypos(), 0);



rapidZ(retractheight);
gcp.toolchange(56142, 10000);
gcp.rapidXY(-stockXwidth/2, -(stockYheight/2+0.508/2));
cutlineZgcfeed(-1.531, plunge);
//cutline(gcp.xpos(), gcp.ypos(), -1.531);
cutlinedxfgc(stockXwidth/2+0.508/2, -(stockYheight/2+0.508/2), -1.531);

rapidZ(retractheight);
//#gcp.toolchange(56125, 10000)
cutlineZgcfeed(-1.531, plunge);
//toolpaths = toolpaths.union(gcp.cutline(gcp.xpos(), gcp.ypos(), -1.531))
cutlinedxfgc(stockXwidth/2+0.508/2, (stockYheight/2+0.508/2), -1.531);

stockandtoolpaths();
//stockwotoolpaths();
//outputtoolpaths();

//makecube(3, 2, 1);

//instantiatecube();

closegcodefile();
closedxffiles();
closedxffile();

