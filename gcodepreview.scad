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
//    } else if (radiustn == 312) {
//        cutroundovertool(bx, by, bz, ex, ey, ez, 1.524/2, 3.175);
    } else if (radiustn == 1570) {
        cutroundovertool(bx, by, bz, ex, ey, ez, 0.507/2, 4.509);
    }
}

function tool_diameter(td_tool, td_depth) = otool_diameter(td_tool, td_depth);

module opengcodefile(fn) {
if (generategcode == true) {
    oopengcodefile(fn);
//    echo(fn);
    owritecomment(fn);
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
  //dxfline(xbegin,ybegin,xend,yend, tn)
  dxfline(bx,by+tool_radius(rtn),bx,by+rheight-tool_radius(rtn), rtn);
  dxfarc(bx+tool_radius(rtn),by+rheight-tool_radius(rtn),tool_radius(rtn),90,180, rtn);
  dxfline(bx+tool_radius(rtn),by+rheight,bx+rwidth-tool_radius(rtn),by+rheight, rtn);
  dxfarc(bx+rwidth-tool_radius(rtn),by+rheight-tool_radius(rtn),tool_radius(rtn),0,90, rtn);
  dxfline(bx+rwidth,by+rheight-tool_radius(rtn),bx+rwidth,by+tool_radius(rtn), rtn);
  dxfarc(bx+rwidth-tool_radius(rtn),by+tool_radius(rtn),tool_radius(rtn),270,360, rtn);
  dxfline(bx+rwidth-tool_radius(rtn),by,bx+tool_radius(rtn),by, rtn);
}

module cutrectangleoutlinedxf(bx, by, bz, rwidth, rheight, rdepth, rtn) {//passes
  movetosafez();
  cutwithfeed(bx+tool_radius(rtn),by+tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+rwidth-tool_radius(rtn),by+tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+rwidth-tool_radius(rtn),by+rheight-tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+tool_radius(rtn),by+rheight-tool_radius(rtn),bz-rdepth,feed);
  dxfarc(bx+tool_radius(rtn),by+tool_radius(rtn),tool_radius(rtn),180,270, rtn);
  dxfline(bx,by+tool_radius(rtn),bx,by+rheight-tool_radius(rtn), rtn);
  dxfarc(bx+tool_radius(rtn),by+rheight-tool_radius(rtn),tool_radius(rtn),90,180, rtn);
  dxfline(bx+tool_radius(rtn),by+rheight,bx+rwidth-tool_radius(rtn),by+rheight, rtn);
  dxfarc(bx+rwidth-tool_radius(rtn),by+rheight-tool_radius(rtn),tool_radius(rtn),0,90, rtn);
  dxfline(bx+rwidth,by+rheight-tool_radius(rtn),bx+rwidth,by+tool_radius(rtn), rtn);
  dxfarc(bx+rwidth-tool_radius(rtn),by+tool_radius(rtn),tool_radius(rtn),270,360, rtn);
  dxfline(bx+rwidth-tool_radius(rtn),by,bx+tool_radius(rtn),by, rtn);
}

module rectangleoutlinedxf(bx, by, bz, rwidth, rheight, rtn) {
  dxfline(bx,by,bx,by+rheight, rtn);
  dxfline(bx,by+rheight,bx+rwidth,by+rheight, rtn);
  dxfline(bx+rwidth,by+rheight,bx+rwidth,by, rtn);
  dxfline(bx+rwidth,by,bx,by, rtn);
}

module cutoutrectangledxf(bx, by, bz, rwidth, rheight, rdepth, rtn) {
  movetosafez();
  cutwithfeed(bx-tool_radius(rtn),by-tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+rwidth+tool_radius(rtn),by-tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx+rwidth+tool_radius(rtn),by+rheight+tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx-tool_radius(rtn),by+rheight+tool_radius(rtn),bz-rdepth,feed);
  cutwithfeed(bx-tool_radius(rtn),by-tool_radius(rtn),bz-rdepth,feed);
  dxfline(bx,by,bx,by+rheight, rtn);
  dxfline(bx,by+rheight,bx+rwidth,by+rheight, rtn);
  dxfline(bx+rwidth,by+rheight,bx+rwidth,by, rtn);
  dxfline(bx+rwidth,by,bx,by, rtn);
}

