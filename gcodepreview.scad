//!OpenSCAD

//gcodepreview 0.5
//
//used via use <gcodepreview.py>;
//         use <pygcodepreview.scad>;
//         include <gcodepreview.scad>;
//

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
owritefive("(stockMin:0.00mm, -",str(stockwidth/2),"mm, -",str(stockthickness),"mm)");
owritefive("(stockMax:",str(stocklength),"mm, ",str(stockwidth/2),"mm, 0.00mm)");
    owriteeleven("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),", 0.00, ",str(stockwidth/2),", ",str(stockthickness),")");
    }
  }
    } else if (stockorigin == "Top-Left") {
    translate([0, (-stockwidth), -stockthickness]){
      cube([stocklength, stockwidth, stockthickness], center=false);
if (generategcode == true) {
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
owriteone("(stockMin:0.00mm, 0.00mm, 0.00mm)");
owriteseven("(stockMax:",str(stocklength),"mm, ",str(stockwidth),"mm, ",str(stockthickness),"mm)");
owriteseven("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),",0.00, 0.00, 0.00)");
    }
}    else if (stockorigin == "Center-Left") {
    translate([0, (-stockwidth / 2), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
if (generategcode == true) {
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
owritethree("(stockMin:0.00mm, -",str(stockwidth),"mm, 0.00mm)");
owritefive("(stockMax:",str(stocklength),"mm, 0.00mm, ",str(stockthickness),"mm)");
owritenine("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),", 0.00, ", str(stockwidth),", 0.00)");
  }
}    else if (stockorigin == "Center") {
    translate([(-stocklength / 2), (-stockwidth / 2), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
if (generategcode == true) {
owritefive("(stockMin:-",str(stocklength/2),", -",str(stockwidth/2),"mm, 0.00mm)");
owriteseven("(stockMax:",str(stocklength/2),"mm, ",str(stockwidth/2),"mm, ",str(stockthickness),"mm)");
owriteeleven("(STOCK/BLOCK, ",str(stocklength),", ",str(stockwidth),", ",str(stockthickness),", ",str(stocklength/2),", ", str(stockwidth/2),", 0.00)");
    }
  }
}
if (generategcode == true) {
    owriteone("G90");
    owriteone("G21");
//    owriteone("(Move to safe Z to avoid workholding)");
//    owriteone("G53G0Z-5.000");
  }
//owritecomment("ENDSETUP");
}

module oset(ex, ey, ez) {
    setxpos(ex);
    setypos(ey);
    setzpos(ez);
}

module osettz(tz) {
    settzpos(tz);
}

module toolchange(tool_number,speed) {
   osettool(tool_number);
if (generategcode == true) {
    writecomment("Toolpath");
    owriteone("M05");
//    writecomment("Move to safe Z to avoid workholding");
//    owriteone("G53G0Z-5.000");
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
   } else if (tool_number == 375) {
     writecomment("TOOL/MILL,9.53, 0.00, 3.17, 0.00");
   } else if (tool_number == 814) {
     writecomment("TOOL/MILL,12.7, 6.367, 12.7, 0.00");
   }
     select_tool(tool_number);
     owritetwo("M6T",str(tool_number));
     owritetwo("M03S",str(speed));
 }
}

module select_tool(tool_number) {
//echo(tool_number);
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
  } else if (tool_number == 375) {
    gcp_keyhole(9.525, 3.175);
  } else if (tool_number == 814) {
    gcp_dovetail(12.7, 6.367, 12.7, 14);
  }
}

module gcp_endmill_square(es_diameter, es_flute_length) {
  cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=false);
}

module gcp_keyhole(es_diameter, es_flute_length) {
  cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=false);
}

module gcp_dovetail(dt_bottomdiameter, dt_topdiameter, dt_height, dt_angle) {
  cylinder(r1=(dt_bottomdiameter / 2), r2=(dt_topdiameter / 2), h= dt_height, center=false);
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

module cutroundover(bx, by, bz, ex, ey, ez, radiustn) {
    if (radiustn == 56125) {
        cutroundovertool(bx, by, bz, ex, ey, ez, 0.508/2, 1.531);
    } else if (radiustn == 56142) {
        cutroundovertool(bx, by, bz, ex, ey, ez, 0.508/2, 2.921);
    } else if (radiustn == 312) {
        cutroundovertool(bx, by, bz, ex, ey, ez, 1.524/2, 3.175);
    } else if (radiustn == 1570) {
        cutroundovertool(bx, by, bz, ex, ey, ez, 0.507/2, 4.509);
    }
}

module cutroundovertool(bx, by, bz, ex, ey, ez, tool_radius_tip, tool_radius_width) {
n = 90 + $fn*3;
step = 360/n;

hull(){
    translate([bx,by,bz])
    cylinder(step,tool_radius_tip,tool_radius_tip);
    translate([ex,ey,ez])
    cylinder(step,tool_radius_tip,tool_radius_tip);
}

hull(){
translate([bx,by,bz+tool_radius_width])
cylinder(tool_radius_width*2,tool_radius_tip+tool_radius_width,tool_radius_tip+tool_radius_width);

translate([ex,ey,ez+tool_radius_width])
  cylinder(tool_radius_width*2,tool_radius_tip+tool_radius_width,tool_radius_tip+tool_radius_width);
}

for (i=[0:step:90]) {
    angle = i;
    dx = tool_radius_width*cos(angle);
    dxx = tool_radius_width*cos(angle+step);
    dzz = tool_radius_width*sin(angle);
    dz = tool_radius_width*sin(angle+step);
    dh = dz-dzz;
    hull(){
        translate([bx,by,bz+dz])
            cylinder(dh,tool_radius_tip+tool_radius_width-dx,tool_radius_tip+tool_radius_width-dxx);
        translate([ex,ey,ez+dz])
            cylinder(dh,tool_radius_tip+tool_radius_width-dx,tool_radius_tip+tool_radius_width-dxx);
        }
    }
}

function tool_diameter(td_tool, td_depth) = otool_diameter(td_tool, td_depth);

function tool_radius(td_tool, td_depth) = otool_diameter(td_tool, td_depth)/2;

module opengcodefile(fn) {
if (generategcode == true) {
    oopengcodefile(fn);
    echo(fn);
    owritecomment(fn);
    }
}

module opendxffile(fn) {
  if (generatedxf == true) {
      oopendxffile(str(fn,".dxf"));
//    echo(fn);
      dxfwriteone("0");
      dxfwriteone("SECTION");
      dxfwriteone("2");
      dxfwriteone("ENTITIES");
    if (large_ball_tool_no >  0) {    oopendxflgblfile(str(fn,".",large_ball_tool_no,".dxf"));
      dxfpreamble(large_ball_tool_no);
    }
    if (large_square_tool_no >  0) {    oopendxflgsqfile(str(fn,".",large_square_tool_no,".dxf"));
      dxfpreamble(large_square_tool_no);
    }
    if (large_V_tool_no >  0) {    oopendxflgVfile(str(fn,".",large_V_tool_no,".dxf"));
      dxfpreamble(large_V_tool_no);
    }
    if (small_ball_tool_no >  0) { oopendxfsmblfile(str(fn,".",small_ball_tool_no,".dxf"));
      dxfpreamble(small_ball_tool_no);
    }
    if (small_square_tool_no >  0) {    oopendxfsmsqfile(str(fn,".",small_square_tool_no,".dxf"));
//    echo(str("tool no",small_square_tool_no));
      dxfpreamble(small_square_tool_no);
    }
    if (small_V_tool_no >  0) {    oopendxfsmVfile(str(fn,".",small_V_tool_no,".dxf"));
      dxfpreamble(small_V_tool_no);
    }
    if (KH_tool_no >  0) {    oopendxfKHfile(str(fn,".",KH_tool_no,".dxf"));
      dxfpreamble(KH_tool_no);
    }
    if (DT_tool_no >  0) {    oopendxfDTfile(str(fn,".",DT_tool_no,".dxf"));
      dxfpreamble(DT_tool_no);
    }
  }
}

module dxfwrite(tn,arg) {
if (tn == large_ball_tool_no) {
    dxfwritelgbl(arg);}
if (tn == large_square_tool_no) {
    dxfwritelgsq(arg);}
if (tn == large_V_tool_no) {
    dxfwritelgV(arg);}
if (tn == small_ball_tool_no) {
    dxfwritesmbl(arg);}
if (tn == small_square_tool_no) {
    dxfwritesmsq(arg);}
if (tn == small_V_tool_no) {
    dxfwritesmV(arg);}
if (tn == DT_tool_no) {
    dxfwriteDT(arg);}
if (tn == KH_tool_no) {
    dxfwriteKH(arg);}
}

module dxfpreamble(tn) {
//    echo(str("dxfpreamble",small_square_tool_no));
    dxfwrite(tn,"0");
    dxfwrite(tn,"SECTION");
    dxfwrite(tn,"2");
    dxfwrite(tn,"ENTITIES");
}

module dxfpl(tn,xbegin,ybegin,xend,yend) {
    dxfwrite(tn,"0");
    dxfwrite(tn,"LWPOLYLINE");
    dxfwrite(tn,"90");
    dxfwrite(tn,"2");
    dxfwrite(tn,"70");
    dxfwrite(tn,"0");
    dxfwrite(tn,"43");
    dxfwrite(tn,"0");
    dxfwrite(tn,"10");
    dxfwrite(tn,str(xbegin));
    dxfwrite(tn,"20");
    dxfwrite(tn,str(ybegin));
    dxfwrite(tn,"10");
    dxfwrite(tn,str(xend));
    dxfwrite(tn,"20");
    dxfwrite(tn,str(yend));
}

module dxfpolyline(xbegin,ybegin,xend,yend, tn) {
if (generatedxf == true) {
    dxfwriteone("0");
    dxfwriteone("LWPOLYLINE");
    dxfwriteone("90");
    dxfwriteone("2");
    dxfwriteone("70");
    dxfwriteone("0");
    dxfwriteone("43");
    dxfwriteone("0");
    dxfwriteone("10");
    dxfwriteone(str(xbegin));
    dxfwriteone("20");
    dxfwriteone(str(ybegin));
    dxfwriteone("10");
    dxfwriteone(str(xend));
    dxfwriteone("20");
    dxfwriteone(str(yend));
    dxfpl(tn,xbegin,ybegin,xend,yend);
    }
}

module dxfa(tn,xcenter,ycenter,radius,anglebegin,endangle) {
    dxfwrite(tn,"0");
    dxfwrite(tn,"ARC");
    dxfwrite(tn,"10");
    dxfwrite(tn,str(xcenter));
    dxfwrite(tn,"20");
    dxfwrite(tn,str(ycenter));
    dxfwrite(tn,"40");
    dxfwrite(tn,str(radius));
    dxfwrite(tn,"50");
    dxfwrite(tn,str(anglebegin));
    dxfwrite(tn,"51");
    dxfwrite(tn,str(endangle));
}

module dxfarc(xcenter, ycenter, radius, anglebegin, endangle, tn) {
if (generatedxf == true) {
    dxfwriteone("0");
    dxfwriteone("ARC");
    dxfwriteone("10");
    dxfwriteone(str(xcenter));
    dxfwriteone("20");
    dxfwriteone(str(ycenter));
    dxfwriteone("40");
    dxfwriteone(str(radius));
    dxfwriteone("50");
    dxfwriteone(str(anglebegin));
    dxfwriteone("51");
    dxfwriteone(str(endangle));
    dxfa(tn,xcenter,ycenter,radius,anglebegin,endangle);
    }
}

module dxfbpl(tn,bx,by) {
    dxfwrite(tn,"0");
    dxfwrite(tn,"POLYLINE");
    dxfwrite(tn,"8");
    dxfwrite(tn,"default");
    dxfwrite(tn,"66");
    dxfwrite(tn,"1");
    dxfwrite(tn,"70");
    dxfwrite(tn,"0");
    dxfwrite(tn,"0");
    dxfwrite(tn,"VERTEX");
    dxfwrite(tn,"8");
    dxfwrite(tn,"default");
    dxfwrite(tn,"70");
    dxfwrite(tn,"32");
    dxfwrite(tn,"10");
    dxfwrite(tn,str(bx));
    dxfwrite(tn,"20");
    dxfwrite(tn,str(by));
}

module beginpolyline(bx,by,bz) {
if (generatedxf == true) {
    dxfwriteone("0");
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
    dxfbpl(current_tool(),bx,by);}
}

module dxfapl(tn,bx,by) {
    dxfwriteone("0");
    dxfwrite(tn,"VERTEX");
    dxfwrite(tn,"8");
    dxfwrite(tn,"default");
    dxfwrite(tn,"70");
    dxfwrite(tn,"32");
    dxfwrite(tn,"10");
    dxfwrite(tn,str(bx));
    dxfwrite(tn,"20");
    dxfwrite(tn,str(by));
}

module addpolyline(bx,by,bz) {
if (generatedxf == true) {
//    dxfwrite(tn,"0");
    dxfwriteone("VERTEX");
    dxfwriteone("8");
    dxfwriteone("default");
    dxfwriteone("70");
    dxfwriteone("32");
    dxfwriteone("10");
    dxfwriteone(str(bx));
    dxfwriteone("20");
    dxfwriteone(str(by));
    dxfapl(current_tool(),bx,by);
    }
}

module dxfcpl(tn) {
    dxfwrite(tn,"0");
    dxfwrite(tn,"SEQEND");
}

module closepolyline() {
  if (generatedxf == true) {
    dxfwriteone("0");
    dxfwriteone("SEQEND");
    dxfcpl(current_tool());
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

module dxfpostamble(arg) {
    dxfwrite(arg,"0");
    dxfwrite(arg,"ENDSEC");
    dxfwrite(arg,"0");
    dxfwrite(arg,"EOF");
}

module closedxffile() {
  if (generatedxf == true) {
    dxfwriteone("0");
    dxfwriteone("ENDSEC");
    dxfwriteone("0");
    dxfwriteone("EOF");
    oclosedxffile();
    echo("CLOSING");
    if (large_ball_tool_no >  0) {    dxfpostamble(large_ball_tool_no);
      oclosedxflgblfile();
    }
    if (large_square_tool_no >  0) {    dxfpostamble(large_square_tool_no);
      oclosedxflgsqfile();
    }
    if (large_V_tool_no >  0) {    dxfpostamble(large_V_tool_no);
      oclosedxflgVfile();
    }
    if (small_ball_tool_no >  0) {    dxfpostamble(small_ball_tool_no);
      oclosedxfsmblfile();
    }
    if (small_square_tool_no >  0) {    dxfpostamble(small_square_tool_no);
      oclosedxfsmsqfile();
    }
    if (small_V_tool_no >  0) {    dxfpostamble(small_V_tool_no);
      oclosedxfsmVfile();
    }
    if (DT_tool_no >  0) {    dxfpostamble(DT_tool_no);
      oclosedxfDTfile();
    }
    if (KH_tool_no >  0) {    dxfpostamble(KH_tool_no);
      oclosedxfKHfile();
    }
  }
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

module rapidbx(bx, by, bz, ex, ey, ez) {
  //    writeln("G0 X",bx," Y", by, "Z", bz);
  if (generategcode == true) {
    writecomment("rapid");
    owritesix("G0 X",str(ex)," Y", str(ey), " Z", str(ez));
  }
    orapid(ex, ey, ez);
}

module rapid(ex, ey, ez) {
  //    writeln("G0 X",bx," Y", by, "Z", bz);
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
  orapid(getxpos(), getypos(), retractheight+55);
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
  //    writecomment("PREPOSITION FOR RAPID PLUNGE");Z25.650
  //G1Z24.663F381.0 ,"F",str(plunge)
    if (zeroheight == "Top") {
      owritetwo("Z",str(retractheight));
    }
  }
    orapid(getxpos(), getypos(), retractheight+55);
}

module cutoneaxis_setfeed(axis,depth,feed) {
  if (generategcode == true) {
  //    writecomment("PREPOSITION FOR RAPID PLUNGE");Z25.650
  //G1Z24.663F381.0 ,"F",str(plunge) G1Z7.612F381.0
    if (zeroheight == "Top") {
      owritefive("G1",axis,str(depth),"F",str(feed));
    }
  }
  if (axis == "X") {setxpos(depth);
    ocut(depth, getypos(), getzpos());}
    if (axis == "Y") {setypos(depth);
      ocut(getxpos(), depth, getzpos());
    }
      if (axis == "Z") {setzpos(depth);
        ocut(getxpos(), getypos(), depth);
      }
}

module cut(ex, ey, ez) {
  //    writeln("G0 X",bx," Y", by, "Z", bz);
  if (generategcode == true) {
     owritesix("G1 X",str(ex)," Y", str(ey), " Z", str(ez));
  }
  //if (generatesvg == true) {
  //    owritesix("G1 X",str(ex)," Y", str(ey), " Z", str(ez));
  //    orapid(getxpos(), getypos(), retractheight+5);
  //    writesvgline(getxpos(),getypos(),ex,ey);
  //}
  ocut(ex, ey, ez);
}

module cutwithfeed(ex, ey, ez, feed) {
  //    writeln("G0 X",bx," Y", by, "Z", bz);
  if (generategcode == true) {
  //    writecomment("rapid");
    owriteeight("G1 X",str(ex)," Y", str(ey), " Z", str(ez),"F",str(feed));
  }
  ocut(ex, ey, ez);
}

module endtoolpath() {
  if (generategcode == true) {
  //Z31.750
  //    owriteone("G53G0Z-5.000");
    owritetwo("Z",str(retractheight));
  }
  orapid(getxpos(),getypos(),retractheight);
}

module arcloop(barc,earc, xcenter, ycenter, radius) {
  for (i = [barc : abs(1) : earc]) {
        cut(xcenter + radius * cos(i),
        ycenter + radius * sin(i),
        getzpos()-(gettzpos())
        );
    setxpos(xcenter + radius * cos(i));
    setypos(ycenter + radius * sin(i));
  }
}

module narcloop(barc,earc, xcenter, ycenter, radius) {
  for (i = [barc : -1 : earc]) {
        cut(xcenter + radius * cos(i),
        ycenter + radius * sin(i),
        getzpos()-(gettzpos())
        );
    setxpos(xcenter + radius * cos(i));
    setypos(ycenter + radius * sin(i));
  }
}

module cutarcNECCdxf(ex, ey, ez, xcenter, ycenter, radius, tn) {
  dxfarc(xcenter,ycenter,radius,0,90, tn);
  settzpos((getzpos()-ez)/90);
    arcloop(1,90, xcenter, ycenter, radius);
}

module cutarcNWCCdxf(ex, ey, ez, xcenter, ycenter, radius, tn) {
  dxfarc(xcenter,ycenter,radius,90,180, tn);
  settzpos((getzpos()-ez)/90);
    arcloop(91,180, xcenter, ycenter, radius);
}

module cutarcSWCCdxf(ex, ey, ez, xcenter, ycenter, radius, tn) {
  dxfarc(xcenter,ycenter,radius,180,270, tn);
  settzpos((getzpos()-ez)/90);
    arcloop(181,270, xcenter, ycenter, radius);
}

module cutarcSECCdxf(ex, ey, ez, xcenter, ycenter, radius, tn) {
  dxfarc(xcenter,ycenter,radius,270,360, tn);
  settzpos((getzpos()-ez)/90);
    arcloop(271,360, xcenter, ycenter, radius);
}

module cutarcNECWdxf(ex, ey, ez, xcenter, ycenter, radius, tn) {
  dxfarc(xcenter,ycenter,radius,0,90, tn);
  settzpos((getzpos()-ez)/90);
    narcloop(89,0, xcenter, ycenter, radius);
}

module cutarcSECWdxf(ex, ey, ez, xcenter, ycenter, radius, tn) {
  dxfarc(xcenter,ycenter,radius,270,360, tn);
  settzpos((getzpos()-ez)/90);
    narcloop(359,270, xcenter, ycenter, radius);
}

module cutarcSWCWdxf(ex, ey, ez, xcenter, ycenter, radius, tn) {
  dxfarc(xcenter,ycenter,radius,180,270, tn);
  settzpos((getzpos()-ez)/90);
    narcloop(269,180, xcenter, ycenter, radius);
}

module cutarcNWCWdxf(ex, ey, ez, xcenter, ycenter, radius, tn) {
  dxfarc(xcenter,ycenter,radius,90,180, tn);
  settzpos((getzpos()-ez)/90);
    narcloop(179,90, xcenter, ycenter, radius);
}

module cutkeyhole_toolpath(kh_start_depth, kh_max_depth, kht_direction, kh_distance, kh_tool_no) {
if (kht_direction == "N") {
  cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, 90, kh_distance, kh_tool_no);
    } else if (kht_direction == "S") {
  cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, 270, kh_distance, kh_tool_no);
    } else if (kht_direction == "E") {
  cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, 0, kh_distance, kh_tool_no);
    } else if (kht_direction == "W") {
  cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, 180, kh_distance, kh_tool_no);
    }
}

module cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, kh_angle, kh_distance, kh_tool_no) {
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,0,90, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,90,180, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,180,270, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,270,360, KH_tool_no);

  if (kh_angle == 0) {
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180,270, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90,180, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),90, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270,360-asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)), KH_tool_no);
dxfarc(getxpos()+kh_distance,getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,0,90, KH_tool_no);
dxfarc(getxpos()+kh_distance,getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,270,360, KH_tool_no);
dxfpolyline(getxpos()+sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2), getypos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2, getxpos()+kh_distance, getypos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2, KH_tool_no);
dxfpolyline(getxpos()+sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2), getypos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2, getxpos()+kh_distance, getypos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2, KH_tool_no);
dxfpolyline(getxpos(),getypos(),getxpos()+kh_distance,getypos(), KH_tool_no);
cutwithfeed(getxpos()+kh_distance,getypos(),-kh_max_depth,feed);
setxpos(getxpos()-kh_distance);
  } else if (kh_angle > 0 && kh_angle < 90) {
echo(kh_angle);
  dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90+kh_angle,180+kh_angle, KH_tool_no);
  dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180+kh_angle,270+kh_angle, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,kh_angle+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),90+kh_angle, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270+kh_angle,360+kh_angle-asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)), KH_tool_no);
dxfarc(getxpos()+(kh_distance*cos(kh_angle)),
  getypos()+(kh_distance*sin(kh_angle)),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,0+kh_angle,90+kh_angle, KH_tool_no);
dxfarc(getxpos()+(kh_distance*cos(kh_angle)),getypos()+(kh_distance*sin(kh_angle)),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,270+kh_angle,360+kh_angle, KH_tool_no);
dxfpolyline( getxpos()+tool_diameter(KH_tool_no, (kh_max_depth))/2*cos(kh_angle+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2))),
 getypos()+tool_diameter(KH_tool_no, (kh_max_depth))/2*sin(kh_angle+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2))),
 getxpos()+(kh_distance*cos(kh_angle))-((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)*sin(kh_angle)),
 getypos()+(kh_distance*sin(kh_angle))+((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)*cos(kh_angle)), KH_tool_no);
echo("a",tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2);
echo("c",tool_diameter(KH_tool_no, (kh_max_depth))/2);
echo("Aangle",asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)));
echo(kh_angle);
 cutwithfeed(getxpos()+(kh_distance*cos(kh_angle)),getypos()+(kh_distance*sin(kh_angle)),-kh_max_depth,feed);
 setxpos(getxpos()-(kh_distance*cos(kh_angle)));
 setypos(getypos()-(kh_distance*sin(kh_angle)));
  } else if (kh_angle == 90) {
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180,270, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270,360, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,0,90-asin(
    (tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)), KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90+asin(
    (tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),180, KH_tool_no);
 dxfpolyline(getxpos(),getypos(),getxpos(),getypos()+kh_distance);
dxfarc(getxpos(),getypos()+kh_distance,tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,0,90, KH_tool_no);
dxfarc(getxpos(),getypos()+kh_distance,tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,90,180, KH_tool_no);
 dxfpolyline(getxpos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()+sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),getxpos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()+kh_distance, KH_tool_no);
 dxfpolyline(getxpos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()+sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),getxpos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()+kh_distance, KH_tool_no);
 cutwithfeed(getxpos(),getypos()+kh_distance,-kh_max_depth,feed);
 setypos(getypos()-kh_distance);
  } else if (kh_angle == 180) {
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,0,90, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270,360, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90,180-asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)), KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),270, KH_tool_no);
dxfarc(getxpos()-kh_distance,getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,90,180, KH_tool_no);
dxfarc(getxpos()-kh_distance,getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,180,270, KH_tool_no);
dxfpolyline(getxpos()-sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),
 getypos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,
 getxpos()-kh_distance,
 getypos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2, KH_tool_no);
dxfpolyline( getxpos()-sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),
 getypos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,
 getxpos()-kh_distance,
 getypos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2, KH_tool_no);
 dxfpolyline(getxpos(),getypos(),getxpos()-kh_distance,getypos(), KH_tool_no);
 cutwithfeed(getxpos()-kh_distance,getypos(),-kh_max_depth,feed);
 setxpos(getxpos()+kh_distance);
  } else if (kh_angle == 270) {
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,0,90, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90,180, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),360, KH_tool_no);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180, 270-asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)), KH_tool_no);
dxfarc(getxpos(),getypos()-kh_distance,tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,180,270, KH_tool_no);
dxfarc(getxpos(),getypos()-kh_distance,tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,270,360, KH_tool_no);
 dxfpolyline(getxpos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()-sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),getxpos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()-kh_distance, KH_tool_no);
 dxfpolyline(getxpos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()-sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),getxpos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()-kh_distance, KH_tool_no);
 dxfpolyline(getxpos(),getypos(),getxpos(),getypos()-kh_distance, KH_tool_no);
 cutwithfeed(getxpos(),getypos()-kh_distance,-kh_max_depth,feed);
 setypos(getypos()+kh_distance);
  }
}

module begincutdxf(rh, ex, ey, ez, fr) {
  rapid(getxpos(),getypos(),rh);
  cutwithfeed(ex,ey,ez,fr);
}

module continuecutdxf(ex, ey, ez, fr) {
  cutwithfeed(ex,ey,ez,fr);
}

module cutrectangledxf(bx, by, bz, rwidth, rheight, rdepth, rtn) {//passes
  movetosafez();
  hull(){
    //  for (i = [0 : abs(1) : passes]) {
    //      rapid(bx+tool_radius(rtn)+i*(rwidth-tool_diameter(current_tool()))/passes,bx+tool_radius(rtn),1);
    //      cutwithfeed(bx+tool_radius(rtn)+i*(rwidth-tool_diameter(current_tool()))/passes,by+tool_radius(rtn),bz-rdepth,feed);
    //      cutwithfeed(bx+tool_radius(rtn)+i*(rwidth-tool_diameter(current_tool()))/passes,by+rheight-tool_radius(rtn),bz-rdepth,feed);

    cutwithfeed(bx+tool_radius(rtn),by+tool_radius(rtn),bz-rdepth,feed);
    cutwithfeed(bx+rwidth-tool_radius(rtn),by+tool_radius(rtn),bz-rdepth,feed);
    cutwithfeed(bx+rwidth-tool_radius(rtn),by+rheight-tool_radius(rtn),bz-rdepth,feed);
    cutwithfeed(bx+tool_radius(rtn),by+rheight-tool_radius(rtn),bz-rdepth,feed);
  }
  //dxfarc(xcenter,ycenter,radius,anglebegin,endangle, tn)
  dxfarc(bx+tool_radius(rtn),by+tool_radius(rtn),tool_radius(rtn),180,270, rtn);
  //dxfpolyline(xbegin,ybegin,xend,yend, tn)
  dxfpolyline(bx,by+tool_radius(rtn),bx,by+rheight-tool_radius(rtn), rtn);
  dxfarc(bx+tool_radius(rtn),by+rheight-tool_radius(rtn),tool_radius(rtn),90,180, rtn);
  dxfpolyline(bx+tool_radius(rtn),by+rheight,bx+rwidth-tool_radius(rtn),by+rheight, rtn);
  dxfarc(bx+rwidth-tool_radius(rtn),by+rheight-tool_radius(rtn),tool_radius(rtn),0,90, rtn);
  dxfpolyline(bx+rwidth,by+rheight-tool_radius(rtn),bx+rwidth,by+tool_radius(rtn), rtn);
  dxfarc(bx+rwidth-tool_radius(rtn),by+tool_radius(rtn),tool_radius(rtn),270,360, rtn);
  dxfpolyline(bx+rwidth-tool_radius(rtn),by,bx+tool_radius(rtn),by, rtn);
}

module cutrectangleoutlinedxf(bx, by, bz, rwidth, rheight, rdepth, rtn) {//passes
  movetosafez();
  cutwithfeed(bx+tool_radius(rtn),by+tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+rwidth-tool_radius(rtn),by+tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+rwidth-tool_radius(rtn),by+rheight-tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+tool_radius(rtn),by+rheight-tool_radius(rtn),bz-rdepth,feed);
  dxfarc(bx+tool_radius(rtn),by+tool_radius(rtn),tool_radius(rtn),180,270, rtn);
  dxfpolyline(bx,by+tool_radius(rtn),bx,by+rheight-tool_radius(rtn), rtn);
  dxfarc(bx+tool_radius(rtn),by+rheight-tool_radius(rtn),tool_radius(rtn),90,180, rtn);
  dxfpolyline(bx+tool_radius(rtn),by+rheight,bx+rwidth-tool_radius(rtn),by+rheight, rtn);
  dxfarc(bx+rwidth-tool_radius(rtn),by+rheight-tool_radius(rtn),tool_radius(rtn),0,90, rtn);
  dxfpolyline(bx+rwidth,by+rheight-tool_radius(rtn),bx+rwidth,by+tool_radius(rtn), rtn);
  dxfarc(bx+rwidth-tool_radius(rtn),by+tool_radius(rtn),tool_radius(rtn),270,360, rtn);
  dxfpolyline(bx+rwidth-tool_radius(rtn),by,bx+tool_radius(rtn),by, rtn);
}

module rectangleoutlinedxf(bx, by, bz, rwidth, rheight, rtn) {
  dxfpolyline(bx,by,bx,by+rheight, rtn);
  dxfpolyline(bx,by+rheight,bx+rwidth,by+rheight, rtn);
  dxfpolyline(bx+rwidth,by+rheight,bx+rwidth,by, rtn);
  dxfpolyline(bx+rwidth,by,bx,by, rtn);
}

module cutoutrectangledxf(bx, by, bz, rwidth, rheight, rdepth, rtn) {
  movetosafez();
  cutwithfeed(bx-tool_radius(rtn),by-tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+rwidth+tool_radius(rtn),by-tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+rwidth+tool_radius(rtn),by+rheight+tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx-tool_radius(rtn),by+rheight+tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx-tool_radius(rtn),by-tool_radius(rtn),bz-rdepth,feed);
  dxfpolyline(bx,by,bx,by+rheight, rtn);
  dxfpolyline(bx,by+rheight,bx+rwidth,by+rheight, rtn);
  dxfpolyline(bx+rwidth,by+rheight,bx+rwidth,by, rtn);
  dxfpolyline(bx+rwidth,by,bx,by, rtn);
}

