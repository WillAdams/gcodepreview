use <gcodepreview.py>;
//use <gcptest.py>;

/* [Export] */
Base_filename = "export"; 
/* [Export] */
generatedxf = true; 
/* [Export] */
generategcode = true; 

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

/* [CAM] */
toolradius = 1.5875;
/* [CAM] */
large_ball_tool_no = 202; // [0:0,111:111,101:101,202:202]
/* [CAM] */
large_square_tool_no = 201; // [0:0,112:112,102:102,201:201]
/* [CAM] */
large_V_tool_no = 301; // [0:0,301:301,690:690]
/* [CAM] */
small_ball_tool_no = 101; // [0:0,121:121,111:111,101:101]
/* [CAM] */
small_square_tool_no = 122; // [0:0,122:122,112:112,102:102]
/* [CAM] */
small_V_tool_no = 390; // [0:0,390:390,301:301]
/* [CAM] */
KH_tool_no = 375; // [0:0,375:375]
/* [CAM] */
DT_tool_no = 814; // [0:0,814:814]
/* [CAM] */
roundover_tool_no = 1570; // [56125:56125,56142:56142,312:312,1570:1570]

psettool(small_square_tool_no);
psetupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin);

psettool(small_square_tool_no);

echo(str(xpos()));
echo(str(ypos()));
echo(str(zpos()));
echo(str(tzpos()));
echo(str(pcurrent_tool()));

psetxpos(1);
psetypos(2);
psetzpos(3);
psettzpos(4);
psettool(small_square_tool_no);

echo(str(xpos()));
echo(str(ypos()));
echo(str(zpos()));
echo(str(tzpos()));
echo(str(pcurrent_tool()));
echo(str(ptool_diameter(pcurrent_tool(), stockthickness)));

psettool(KH_tool_no);
echo(str(pcurrent_tool()));
echo(str(ptool_diameter(pcurrent_tool(), stockthickness)));

cube([1,2,3]);

popengcodefile(Base_filename);

popendxffile(Base_filename);

popendxflgblfile(Base_filename);

popendxflgsqfile(Base_filename);

popendxflgVfile(Base_filename);

popendxfsmblfile(Base_filename);

popendxfsmsqfile(Base_filename);

popendxfsmVfile(Base_filename);

popendxfKHfile(Base_filename);

popendxfDTfile(Base_filename);

writedxf("TEST");

writedxflgbl("TEST");

writedxflgsq("TEST");

writedxflgV("TEST");

writedxfsmbl("TEST");

writedxfsmsq("TEST");

writedxfsmV("TEST");

writedxfKH("TEST");

writedxfDT("TEST");

pclosegcodefile();

pclosedxffile();

pclosedxflgblfile();

pclosedxflgsqfile();

pclosedxflgVfile();

pclosedxfsmblfile();

pclosedxfsmsqfile();

pclosedxfsmVfile();

pclosedxfDTfile();

pclosedxfKHfile();
