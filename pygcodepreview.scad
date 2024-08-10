//!OpenSCAD

//gcodepreview 0.4

 module osetupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin) {
     psetupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin);
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

function getxpos() = xpos();
function getypos() = ypos();
function getzpos() = zpos();
function gettzpos() = tzpos();

module setxpos(newxpos) {
    psetxpos(newxpos);
}

module setypos(newypos) {
    psetypos(newypos);
}

module setzpos(newzpos) {
    psetzpos(newzpos);
}

module settzpos(newtzpos) {
    psettzpos(newtzpos);
}

module osettool(tn){
    psettool(tn);
}

function current_tool() = pcurrent_tool();

function otool_diameter(td_tool, td_depth) = ptool_diameter(td_tool, td_depth);

module oopengcodefile(fn) {
    popengcodefile(fn);
}

module oopendxffile(fn) {
    echo(fn);
    popendxffile(fn);
}

module oopendxflgblfile(fn) {
    popendxflgblfile(fn);
}

module oopendxflgsqfile(fn) {
    popendxflgsqfile(fn);
}

module oopendxflgVfile(fn) {
    popendxflgVfile(fn);
}

module oopendxfsmblfile(fn) {
    popendxfsmblfile(fn);
}

module oopendxfsmsqfile(fn) {
    echo(fn);
    popendxfsmsqfile(fn);
}

module oopendxfsmVfile(fn) {
    popendxfsmVfile(fn);
}

module oopendxfKHfile(fn) {
    popendxfKHfile(fn);
}

module oopendxfDTfile(fn) {
    popendxfDTfile(fn);
}

module owritecomment(comment) {
    writeln("(",comment,")");
}

module dxfwriteone(first) {
    writedxf(first);
//    writeln(first);
//    echo(first);
}

module dxfwritelgbl(first) {
    writedxflgbl(first);
}

module dxfwritelgsq(first) {
    writedxflgsq(first);
}

module dxfwritelgV(first) {
    writedxflgV(first);
}

module dxfwritesmbl(first) {
    writedxfsmbl(first);
}

module dxfwritesmsq(first) {
    writedxfsmsq(first);
}

module dxfwritesmV(first) {
    writedxfsmV(first);
}

module dxfwriteKH(first) {
    writedxfKH(first);
}

module dxfwriteDT(first) {
    writedxfDT(first);
}

module owriteone(first) {
    writeln(first);
}

module owritetwo(first, second) {
    writeln(first, second);
}

module owritethree(first, second, third) {
    writeln(first, second, third);
}

module owritefour(first, second, third, fourth) {
    writeln(first, second, third, fourth);
}

module owritefive(first, second, third, fourth, fifth) {
    writeln(first, second, third, fourth, fifth);
}

module owritesix(first, second, third, fourth, fifth, sixth) {
    writeln(first, second, third, fourth, fifth, sixth);
}

module owriteseven(first, second, third, fourth, fifth, sixth, seventh) {
    writeln(first, second, third, fourth, fifth, sixth, seventh);
}

module owriteeight(first, second, third, fourth, fifth, sixth, seventh,eighth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh,eighth);
}

module owritenine(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth);
}

module owriteten(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth);
}

module owriteeleven(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh);
}

module owritetwelve(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth);
}

module owritethirteen(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth);
}

module oclosegcodefile() {
    pclosegcodefile();
}

module oclosedxffile() {
    pclosedxffile();
}

module oclosedxflgblfile() {
    pclosedxflgblfile();
}

module oclosedxflgsqfile() {
    pclosedxflgsqfile();
}

module oclosedxflgVfile() {
    pclosedxflgVfile();
}

module oclosedxfsmblfile() {
    pclosedxfsmblfile();
}

module oclosedxfsmsqfile() {
    pclosedxfsmsqfile();
}

module oclosedxfsmVfile() {
    pclosedxfsmVfile();
}

module oclosedxfDTfile() {
    pclosedxfDTfile();
}

module oclosedxfKHfile() {
    pclosedxfKHfile();
}

