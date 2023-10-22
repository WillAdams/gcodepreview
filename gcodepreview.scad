//!OpenSCAD

//gcodepreview 0.1
//
//used via use <gcodepreview.py>;
//         use <pygcodepreview.scad>;
//         include <gcodepreview.scad>;
//
//supports setting up stock, origin, rapdi positioning, making cuts, and writing out matching G-code

module opengcodefile(fn) {
if (generategcode == true) {
	oopengcodefile(fn);
    echo(fn);
    owritecomment(fn);
}
}

module opendxffile(fn) {
if (generatedxf == true) {
	oopendxffile(fn);
    echo(fn);
    dxfwriteone("0");
    dxfwriteone("SECTION");
    dxfwriteone("2");
    dxfwriteone("ENTITIES");
    dxfwriteone("0");
}
}

module beginpolyline(bx,by,bz) {
if (generatedxf == true) {
    dxfwriteone("POLYLINE");
    dxfwriteone("8");
    dxfwriteone("default");
    dxfwriteone("66");
    dxfwriteone("1");
    dxfwriteone("70");
    dxfwriteone("0");
    dxfwriteone("0");
    dxfwriteone("VERTEX");
    dxfwriteone("8");
    dxfwriteone("default");
    dxfwriteone("70");
    dxfwriteone("32");
    dxfwriteone("10");
    dxfwriteone(str(bx));
    dxfwriteone("20");
    dxfwriteone(str(by));
    dxfwriteone("0");
}
}

module addpolyline(bx,by,bz) {
if (generatedxf == true) {
    dxfwriteone("VERTEX");
    dxfwriteone("8");
    dxfwriteone("default");
    dxfwriteone("70");
    dxfwriteone("32");
    dxfwriteone("10");
    dxfwriteone(str(bx));
    dxfwriteone("20");
    dxfwriteone(str(by));
    dxfwriteone("0");
}
}

module closepolyline() {
if (generatedxf == true) {
    dxfwriteone("SEQEND");
    dxfwriteone("0");
}
}

module writecomment(comment) {
if (generategcode == true) {
	owritecomment(comment);
}
}

module closegcodefile() {
if (generategcode == true) {
    owriteone("M05");
    owriteone("M02");
	oclosegcodefile();
}
}

module closedxffile() {
if (generatedxf == true) {
//    dxfwriteone("SEQEND");
//    dxfwriteone("0");
    dxfwriteone("ENDSEC");
    dxfwriteone("0");
    dxfwriteone("EOF");
	oclosedxffile();
    echo("CLOSING");
    }
}

module oset(ex, ey, ez) {
setxpos(ex);
setypos(ey);
setzpos(ez);
}

module otm(ex, ey, ez, r,g,b) {
color([r,g,b]) hull(){
    translate([xpos(), ypos(), zpos()]){
      select_tool(current_tool());
    }
    translate([ex, ey, ez]){
      select_tool(current_tool());
    }
  }
oset(ex, ey, ez);
}

module ocut(ex, ey, ez) {
//color([0.2,1,0.2]) hull(){
otm(ex, ey, ez, 0.2,1,0.2);
}

module orapid(ex, ey, ez) {
//color([0.93,0,0]) hull(){
otm(ex, ey, ez, 0.93,0,0);
}

module setupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin) {
  osetupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin);
//initialize default tool and XYZ origin
  osettool(102);
  oset(0,0,0);
  if (zeroheight == "Top") {
    if (stockorigin == "Lower-Left") {
    translate([0, 0, (-stockthickness)]){
    cube([stocklength, stockwidth, stockthickness], center=false);
if (generategcode == true) {
//	owriteone("(setupstock)");
owritethree("(stockMin:0.00mm, 0.00mm, -",str(stockthickness),"mm)");
owritefive("(stockMax:",str(stocklength),"mm, ",str(stockwidth),"mm, 0.00mm)");
    owritenine("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),", 0.00, 0.00, ",str(stockthickness),")");
}
}
}
     else if (stockorigin == "Center-Left") {
    translate([0, (-stockwidth / 2), -stockthickness]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    if (generategcode == true) {
//	owriteone("(setupstock)");
owritefive("(stockMin:0.00mm, -",str(stockwidth/2),"mm, -",str(stockthickness),"mm)");
owritefive("(stockMax:",str(stocklength),"mm, ",str(stockwidth/2),"mm, 0.00mm)");
    owriteeleven("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),", 0.00, ",str(stockwidth/2),", ",str(stockthickness),")");
    }
    }
    } else if (stockorigin == "Top-Left") {
    translate([0, (-stockwidth), -stockthickness]){
      cube([stocklength, stockwidth, stockthickness], center=false);
if (generategcode == true) {
//	owriteone("(setupstock)");
owritefive("(stockMin:0.00mm, -",str(stockwidth),"mm, -",str(stockthickness),"mm)");
owritethree("(stockMax:",str(stocklength),"mm, 0.00mm, 0.00mm)");
owriteeleven("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),", 0.00, ",str(stockwidth),", ",str(stockthickness),")");
    }
    }
    }
	else if (stockorigin == "Center") {
//owritecomment("Center");
    translate([(-stocklength / 2), (-stockwidth / 2), -stockthickness]){
      cube([stocklength, stockwidth, stockthickness], center=false);
if (generategcode == true) {
//	owriteone("(setupstock)");
owriteseven("(stockMin: -",str(stocklength/2),", -",str(stockwidth/2),"mm, -",str(stockthickness),"mm)");
owritefive("(stockMax:",str(stocklength/2),"mm, ",str(stockwidth/2),"mm, 0.00mm)");
owritethirteen("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),", ",str(stocklength/2),", ", str(stockwidth/2),", ",str(stockthickness),")");
}
}
}
} else if (zeroheight == "Bottom") {
//owritecomment("Bottom");
    if (stockorigin == "Lower-Left") {
    cube([stocklength, stockwidth, stockthickness], center=false);
if (generategcode == true) {
//	owriteone("(setupstock)");
owriteone("(stockMin:0.00mm, 0.00mm, 0.00mm)");
owriteseven("(stockMax:",str(stocklength),"mm, ",str(stockwidth),"mm, ",str(stockthickness),"mm)");
owriteseven("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),",0.00, 0.00, 0.00)");
    }
}	else if (stockorigin == "Center-Left") {
    translate([0, (-stockwidth / 2), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
if (generategcode == true) {
//	owriteone("(setupstock)");
owritethree("(stockMin:0.00mm, -",str(stockwidth/2),"mm, 0.00mm)");
owriteseven("(stockMax:",str(stocklength),"mm, ",str(stockwidth/2),"mm, ",str(stockthickness),"mm)");
owritenine("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),",0.00, ",str(stockwidth/2),", 0.00)");
    }
    } 
	} else if (stockorigin == "Top-Left") {
    translate([0, (-stockwidth), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
if (generategcode == true) {
//	owriteone("(setupstock)");
owritethree("(stockMin:0.00mm, -",str(stockwidth),"mm, 0.00mm)");
owritefive("(stockMax:",str(stocklength),"mm, 0.00mm, ",str(stockthickness),"mm)");
owritenine("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),", 0.00, ", str(stockwidth),", 0.00)");
}
}	else if (stockorigin == "Center") {
    translate([(-stocklength / 2), (-stockwidth / 2), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
if (generategcode == true) {
//	owriteone("(setupstock)");
owritefive("(stockMin:-",str(stocklength/2),", -",str(stockwidth/2),"mm, 0.00mm)");
owriteseven("(stockMax:",str(stocklength/2),"mm, ",str(stockwidth/2),"mm, ",str(stockthickness),"mm)");
owriteeleven("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),", ",str(stocklength/2),", ", str(stockwidth/2),", 0.00)");
}
}
}
if (generategcode == true) {
	owriteone("G90");
	owriteone("G21");
//	owriteone("(Move to safe Z to avoid workholding)");
//	owriteone("G53G0Z-5.000");
}
//owritecomment("ENDSETUP");
}

module select_tool(tool_number) {
echo(tool_number);
  if (tool_number == 201) {
    gcp_endmill_square(6.35, 19.05);
  } else if (tool_number == 202) {
    gcp_endmill_ball(6.35, 19.05);
  } else if (tool_number == 102) {
    gcp_endmill_square(3.175, 19.05);
  } else if (tool_number == 101) {
    gcp_endmill_ball(3.175, 19.05);
  } else if (tool_number == 301) {
    gcp_endmill_v(90, 12.7);
  } else if (tool_number == 302) {
    gcp_endmill_v(60, 12.7);
  } else if (tool_number == 390) {
    gcp_endmill_v(90, 3.175);
  }
}

module toolchange(tool_number,speed) {
   osettool(tool_number); 
if (generategcode == true) {
	writecomment("Toolpath");
	owriteone("M05");
//	writecomment("Move to safe Z to avoid workholding");
//	owriteone("G53G0Z-5.000");
//    writecomment("Begin toolpath");
  if (tool_number == 201) {
	writecomment("TOOL/MILL,6.35, 0.00, 0.00, 0.00");
  } else if (tool_number == 202) {
	writecomment("TOOL/MILL,6.35, 3.17, 0.00, 0.00");
  } else if (tool_number == 102) {
	writecomment("TOOL/MILL,3.17, 0.00, 0.00, 0.00");
  } else if (tool_number == 101) {
	writecomment("TOOL/MILL,3.17, 1.58, 0.00, 0.00");
  } else if (tool_number == 301) {
	writecomment("TOOL/MILL,0.03, 0.00, 6.35, 45.00");
  } else if (tool_number == 302) {
	writecommment("TOOL/MILL,0.03, 0.00, 10.998, 30.00");
  } else if (tool_number == 390) {
	writecomment("TOOL/MILL,0.03, 0.00, 1.5875, 45.00");
  }
    select_tool(tool_number);
	owritetwo("M6T",str(tool_number));
	owritetwo("M03S",str(speed));
}
}

module gcp_endmill_square(es_diameter, es_flute_length) {
  cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=false);
}

module gcp_endmill_ball(es_diameter, es_flute_length) {
  translate([0, 0, (es_diameter / 2)]){
    union(){
      sphere(r=(es_diameter / 2));
      cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=false);
    }
  }
}

module gcp_endmill_v(es_v_angle, es_diameter) {
  union(){
    cylinder(r1=0, r2=(es_diameter / 2), h=((es_diameter / 2) / tan((es_v_angle / 2))), center=false);
    translate([0, 0, ((es_diameter / 2) / tan((es_v_angle / 2)))]){
      cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=((es_diameter * 8) ), center=false);/// tan((es_v_angle / 2))
    }
  }
}

module rapidbx(bx, by, bz, ex, ey, ez) {
//	writeln("G0 X",bx," Y", by, "Z", bz);
if (generategcode == true) {
	writecomment("rapid");
	owritesix("G0 X",str(ex)," Y", str(ey), " Z", str(ez));
}
    orapid(ex, ey, ez);
}

module rapid(ex, ey, ez) {
//	writeln("G0 X",bx," Y", by, "Z", bz);
if (generategcode == true) {
	writecomment("rapid");
	owritesix("G0 X",str(ex)," Y", str(ey), " Z", str(ez));
}
    orapid(ex, ey, ez);
}

module movetosafez() {
//this should be move to retract height
if (generategcode == true) {
	writecomment("Move to safe Z to avoid workholding");
    owriteone("G53G0Z-5.000");
}
    orapid(getxpos(), getypos(), retractheight+5);
}

module begintoolpath(bx,by,bz) {
if (generategcode == true) {
	writecomment("PREPOSITION FOR RAPID PLUNGE");
    owritefour("G0X", str(bx), "Y",str(by));
    owritetwo("Z", str(bz));
    }
    orapid(bx,by,bz);
}

module movetosafeheight() {
//this should be move to machine position
if (generategcode == true) {
//	writecomment("PREPOSITION FOR RAPID PLUNGE");Z25.650
//G1Z24.663F381.0 ,"F",str(plunge)
if (zeroheight == "Top") {
    owritetwo("Z",str(retractheight));
}
}
    orapid(getxpos(), getypos(), retractheight+5);
}

module cutoneaxis_setfeed(axis,depth,feed) {
if (generategcode == true) {
//	writecomment("PREPOSITION FOR RAPID PLUNGE");Z25.650
//G1Z24.663F381.0 ,"F",str(plunge) G1Z7.612F381.0
if (zeroheight == "Top") {
    owritefive("G1",axis,str(depth),"F",str(feed));
}
}
if (axis == "X") {setxpos(depth);}
if (axis == "Y") {setypos(depth);}
if (axis == "Z") {setzpos(depth);}
}

module cut(ex, ey, ez) {
//	writeln("G0 X",bx," Y", by, "Z", bz);
if (generategcode == true) {
//	writecomment("rapid");
	owritesix("G1 X",str(ex)," Y", str(ey), " Z", str(ez));
}
ocut(ex, ey, ez);
}

module cutwithfeed(ex, ey, ez, feed) {
//	writeln("G0 X",bx," Y", by, "Z", bz);
if (generategcode == true) {
//	writecomment("rapid");
	owriteeight("G1 X",str(ex)," Y", str(ey), " Z", str(ez),"F",str(feed));
}
ocut(ex, ey, ez);
}

module endtoolpath() {
if (generategcode == true) {
//Z31.750
//	owriteone("G53G0Z-5.000");
    owritetwo("Z",str(retractheight));
}
    orapid(getxpos(),getypos(),retractheight);
}
