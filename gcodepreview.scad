//!OpenSCAD

//gcodepreview 0.4
//
//used via use <gcodepreview.py>;
//         use <pygcodepreview.scad>;
//         include <gcodepreview.scad>;
//

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

module radiuscut(bx, by, bz, ex, ey, ez, radiustn) {
    if (radiustn == 56125) {
        radiuscuttool(bx, by, bz, ex, ey, ez, 0.508/2, 1.531);
    } else if (radiustn == 56142) {
        radiuscuttool(bx, by, bz, ex, ey, ez, 0.508/2, 2.921);
    } else if (radiustn == 312) {
        radiuscuttool(bx, by, bz, ex, ey, ez, 1.524/2, 3.175);
    } else if (radiustn == 1570) {
        radiuscuttool(bx, by, bz, ex, ey, ez, 0.507/2, 4.509);
    }
}

module radiuscuttool(bx, by, bz, ex, ey, ez, tool_radius_tip, tool_radius_width) {
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

module dxfpolyline(tn,xbegin,ybegin,xend,yend) {
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

module dxfarc(tn,xcenter,ycenter,radius,anglebegin,endangle) {
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
    dxfwrite(tn,"0");
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

