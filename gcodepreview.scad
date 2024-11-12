//!OpenSCAD

//gcodepreview 0.7
//
//used via use <gcodepreview.py>;
//         use <pygcodepreview.scad>;
//         include <gcodepreview.scad>;
//

module setupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero) {
  osetupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero);
}

//module oset(ex, ey, ez) {
//    setxpos(ex);
//    setypos(ey);
//    setzpos(ez);
//}
//
//module osettz(tz) {
//    settzpos(tz);
//}
//
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
//    echo(fn);
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
    if (large_ball_tool_num >  0) {    oopendxflgblfile(str(fn,".",large_ball_tool_num,".dxf"));
      dxfpreamble(large_ball_tool_num);
    }
    if (large_square_tool_num >  0) {    oopendxflgsqfile(str(fn,".",large_square_tool_num,".dxf"));
      dxfpreamble(large_square_tool_num);
    }
    if (large_V_tool_num >  0) {    oopendxflgVfile(str(fn,".",large_V_tool_num,".dxf"));
      dxfpreamble(large_V_tool_num);
    }
    if (small_ball_tool_num >  0) { oopendxfsmblfile(str(fn,".",small_ball_tool_num,".dxf"));
      dxfpreamble(small_ball_tool_num);
    }
    if (small_square_tool_num >  0) {    oopendxfsmsqfile(str(fn,".",small_square_tool_num,".dxf"));
//    echo(str("tool number ",small_square_tool_num));
      dxfpreamble(small_square_tool_num);
    }
    if (small_V_tool_num >  0) {    oopendxfsmVfile(str(fn,".",small_V_tool_num,".dxf"));
      dxfpreamble(small_V_tool_num);
    }
    if (KH_tool_num >  0) {    oopendxfKHfile(str(fn,".",KH_tool_num,".dxf"));
      dxfpreamble(KH_tool_num);
    }
    if (DT_tool_num >  0) {    oopendxfDTfile(str(fn,".",DT_tool_num,".dxf"));
      dxfpreamble(DT_tool_num);
    }
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

module addpolyline(bx,by,bz) {
if (generatedxf == true) {
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
//    echo("CLOSING");
    if (large_ball_tool_num >  0) {    dxfpostamble(large_ball_tool_num);
      oclosedxflgblfile();
    }
    if (large_square_tool_num >  0) {    dxfpostamble(large_square_tool_num);
      oclosedxflgsqfile();
    }
    if (large_V_tool_num >  0) {    dxfpostamble(large_V_tool_num);
      oclosedxflgVfile();
    }
    if (small_ball_tool_num >  0) {    dxfpostamble(small_ball_tool_num);
      oclosedxfsmblfile();
    }
    if (small_square_tool_num >  0) {    dxfpostamble(small_square_tool_num);
      oclosedxfsmsqfile();
    }
    if (small_V_tool_num >  0) {    dxfpostamble(small_V_tool_num);
      oclosedxfsmVfile();
    }
    if (DT_tool_num >  0) {    dxfpostamble(DT_tool_num);
      oclosedxfDTfile();
    }
    if (KH_tool_num >  0) {    dxfpostamble(KH_tool_num);
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

module cutkeyhole_toolpath(kh_start_depth, kh_max_depth, kht_direction, kh_distance, kh_tool_num) {
if (kht_direction == "N") {
  cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, 90, kh_distance, kh_tool_num);
    } else if (kht_direction == "S") {
  cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, 270, kh_distance, kh_tool_num);
    } else if (kht_direction == "E") {
  cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, 0, kh_distance, kh_tool_num);
    } else if (kht_direction == "W") {
  cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, 180, kh_distance, kh_tool_num);
    }
}

module cutKH_toolpath_degrees(kh_start_depth, kh_max_depth, kh_angle, kh_distance, kh_tool_num) {
//Circle at entry hole
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (7))/2,0,90, KH_tool_num);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (7))/2,90,180, KH_tool_num);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (7))/2,180,270, KH_tool_num);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (7))/2,270,360, KH_tool_num);

//Outlines of entry hole and slot
  if (kh_angle == 0) {
    //Lower left of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,180,270, KH_tool_num);
    //Upper left of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,90,180, KH_tool_num);
    //Upper right of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,90-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 90, KH_tool_num);
    //Lower right of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,270, 270+acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
    //Actual line of cut
    dxfpolyline(getxpos(),getypos(),getxpos()+kh_distance,getypos());
    //upper right of slot
    dxfarc(getxpos()+kh_distance,getypos(),tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,0,90, KH_tool_num);
    //lower right of slot
    dxfarc(getxpos()+kh_distance,getypos(),tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,270,360, KH_tool_num);
    //upper right slot
    dxfpolyline(
        getxpos()+(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),
        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
        getxpos()+kh_distance,
    //end position at top of slot
        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
        KH_tool_num);
    //lower right slot
    dxfpolyline(
        getxpos()+(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),
        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
        getxpos()+kh_distance,
    //end position at top of slot
        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
        KH_tool_num);
    hull(){
      translate([xpos(), ypos(), zpos()]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
      translate([xpos(), ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
    }
    hull(){
      translate([xpos(), ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
      translate([xpos()+kh_distance, ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
    }
    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
    cutwithfeed(getxpos()+kh_distance,getypos(),-kh_max_depth,feed);
    setxpos(getxpos()-kh_distance);
  } else if (kh_angle > 0 && kh_angle < 90) {
//echo(kh_angle);
  dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,90+kh_angle,180+kh_angle, KH_tool_num);
  dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,180+kh_angle,270+kh_angle, KH_tool_num);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)),90+kh_angle, KH_tool_num);
dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,270+kh_angle,360+kh_angle-asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)), KH_tool_num);
dxfarc(getxpos()+(kh_distance*cos(kh_angle)),
  getypos()+(kh_distance*sin(kh_angle)),tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,0+kh_angle,90+kh_angle, KH_tool_num);
dxfarc(getxpos()+(kh_distance*cos(kh_angle)),getypos()+(kh_distance*sin(kh_angle)),tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,270+kh_angle,360+kh_angle, KH_tool_num);
dxfpolyline( getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2*cos(kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2))),
 getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2*sin(kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2))),
 getxpos()+(kh_distance*cos(kh_angle))-((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)*sin(kh_angle)),
 getypos()+(kh_distance*sin(kh_angle))+((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)*cos(kh_angle)), KH_tool_num);
//echo("a",tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2);
//echo("c",tool_diameter(KH_tool_num, (kh_max_depth))/2);
echo("Aangle",asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)));
//echo(kh_angle);
 cutwithfeed(getxpos()+(kh_distance*cos(kh_angle)),getypos()+(kh_distance*sin(kh_angle)),-kh_max_depth,feed);
 setxpos(getxpos()-(kh_distance*cos(kh_angle)));
 setypos(getypos()-(kh_distance*sin(kh_angle)));
  } else if (kh_angle == 90) {
    //Lower left of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,180,270, KH_tool_num);
    //Lower right of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,270,360, KH_tool_num);
    //Upper right of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,0,acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
    //Upper left of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,180-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 180,KH_tool_num);
    //Actual line of cut
    dxfpolyline(getxpos(),getypos(),getxpos(),getypos()+kh_distance);
    //upper right of slot
    dxfarc(getxpos(),getypos()+kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,0,90, KH_tool_num);
    //upper left of slot
    dxfarc(getxpos(),getypos()+kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,90,180, KH_tool_num);
    //right of slot
    dxfpolyline(
        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
        getypos()+(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
    //end position at top of slot
        getypos()+kh_distance,
        KH_tool_num);
    dxfpolyline(getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2, getypos()+(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2), getxpos()-tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,getypos()+kh_distance, KH_tool_num);
    hull(){
      translate([xpos(), ypos(), zpos()]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
      translate([xpos(), ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
    }
    hull(){
      translate([xpos(), ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
      translate([xpos(), ypos()+kh_distance, zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
    }
    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
    cutwithfeed(getxpos(),getypos()+kh_distance,-kh_max_depth,feed);
    setypos(getypos()-kh_distance);
  } else if (kh_angle == 180) {
    //Lower right of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,270,360, KH_tool_num);
    //Upper right of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,0,90, KH_tool_num);
    //Upper left of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,90, 90+acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
    //Lower left of entry hole
    dxfarc(getxpos(),getypos(),9.525/2, 270-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 270, KH_tool_num);
    //upper left of slot
    dxfarc(getxpos()-kh_distance,getypos(),tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,90,180, KH_tool_num);
    //lower left of slot
    dxfarc(getxpos()-kh_distance,getypos(),tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,180,270, KH_tool_num);
    //Actual line of cut
    dxfpolyline(getxpos(),getypos(),getxpos()-kh_distance,getypos());
    //upper left slot
    dxfpolyline(
        getxpos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),
        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
        getxpos()-kh_distance,
    //end position at top of slot
        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
        KH_tool_num);
    //lower right slot
    dxfpolyline(
        getxpos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),
        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
        getxpos()-kh_distance,
    //end position at top of slot
        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
        KH_tool_num);
    hull(){
      translate([xpos(), ypos(), zpos()]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
      translate([xpos(), ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
    }
    hull(){
      translate([xpos(), ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
      translate([xpos()-kh_distance, ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
    }
    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
    cutwithfeed(getxpos()-kh_distance,getypos(),-kh_max_depth,feed);
    setxpos(getxpos()+kh_distance);
  } else if (kh_angle == 270) {
    //Upper right of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,0,90, KH_tool_num);
    //Upper left of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,90,180, KH_tool_num);
    //lower right of slot
    dxfarc(getxpos(),getypos()-kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,270,360, KH_tool_num);
    //lower left of slot
    dxfarc(getxpos(),getypos()-kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,180,270, KH_tool_num);
    //Actual line of cut
    dxfpolyline(getxpos(),getypos(),getxpos(),getypos()-kh_distance);
    //right of slot
    dxfpolyline(
        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
        getypos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
    //end position at top of slot
        getypos()-kh_distance,
        KH_tool_num);
    //left of slot
    dxfpolyline(
        getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
        getypos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
        getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
    //end position at top of slot
        getypos()-kh_distance,
        KH_tool_num);
    //Lower right of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,360-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 360, KH_tool_num);
    //Lower left of entry hole
    dxfarc(getxpos(),getypos(),9.525/2,180, 180+acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
    hull(){
      translate([xpos(), ypos(), zpos()]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
      translate([xpos(), ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
    }
    hull(){
      translate([xpos(), ypos(), zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
      translate([xpos(), ypos()-kh_distance, zpos()-kh_max_depth]){
        gcp_keyhole_shaft(6.35, 9.525);
      }
    }
    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
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

