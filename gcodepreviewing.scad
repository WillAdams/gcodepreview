//!OpenSCAD

module plungegcutretract(bx, by, bz, ex, ey, ez, tn, retract, plungerate, feedrate) {
rapid(bx, by, retract*2, bx, by, retract);
gcutfeed(bx, by, retract, bx, by, bz, tn, plungerate);
gcutfeed(bx, by, bz, ex, ey, ez, tn, feedrate);
rapid(ex, ey, ez, ex, ey, retract);
}

module plungegcutsetfeed(bx, by, bz, ex, ey, ez, tn, plungerate, feedrate) {
cut(bx, by, bz, ex, ey, ez, tn);
if (generategcode == true) {
	writeln("(plungegcutsetfeed)");
	writeln("(PREPOSITION FOR RAPID PLUNGE)");
	writeln("G0 X",bx," Y", by);
	writeln("G1 Z", ez,"F",plungerate);
	writeln("G1 X",ex," Y", ey, "Z", ez,"F",feedrate);
}
}

module rapid(bx, by, bz, ex, ey, ez) {
//	writeln("G0 X",bx," Y", by, "Z", bz);
if (generategcode == true) {
	writeln("(rapid)");
	writeln("G0 X",ex," Y", ey, "Z", ez);
}
hull(){
    translate([bx, by, bz]){
      select_tool(102);
    }
    translate([ex, ey, ez]){
      select_tool(102);
    }
  }
}

module setupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin) {
  if (zeroheight == "Top") {
    if (stockorigin == "Lower-Left") {
    translate([0, 0, (-stockthickness)]){
    cube([stocklength, stockwidth, stockthickness], center=false);
    }
if (generategcode == true) {
	writeln("(setupstock)");
writeln("(STOCK/BLOCK, ",stocklength,", ",stockwidth,", ",stockthickness,", ", "0.00, 0.00",", ",stockthickness,")");
}
    } else if (stockorigin == "Center-Left") {
    translate([0, (-stockwidth / 2), -stockthickness]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    } 
if (generategcode == true) {
	writeln("(setupstock)");
writeln("(STOCK/BLOCK, ",stocklength,", ",stockwidth,", ",stockthickness,", ", "0.00, ",stockwidth/2,", ",stockthickness,")");
}
	} else if (stockorigin == "Top-Left") {
    translate([0, (-stockwidth), -stockthickness]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
if (generategcode == true) {
	writeln("(setupstock)");
writeln("(STOCK/BLOCK, ",stocklength,", ",stockwidth,", ",stockthickness,", ", "0.00, ",stockwidth,", ",stockthickness,")");
}
}	else if (stockorigin == "Center") {
    translate([(-stocklength / 2), (-stockwidth / 2), -stockthickness]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
if (generategcode == true) {
	writeln("(setupstock)");
writeln("(STOCK/BLOCK, ",stocklength,", ",stockwidth,", ",stockthickness,", ",stocklength/2,", ", stockwidth/2,", ",stockthickness,")");
}
}
}
else {
    if (stockorigin == "Lower-Left") {
    cube([stocklength, stockwidth, stockthickness], center=false);
if (generategcode == true) {
	writeln("(setupstock)");
writeln("(STOCK/BLOCK, ",stocklength,", ",stockwidth,", ",stockthickness,",0.00, 0.00, 0.00)");
    }
}	else if (stockorigin == "Center-Left") {
    translate([0, (-stockwidth / 2), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    } 
	} else if (stockorigin == "Top-Left") {
    translate([0, (-stockwidth), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
if (generategcode == true) {
	writeln("(setupstock)");
writeln("(STOCK/BLOCK, ",stocklength,", ",stockwidth,", ",stockthickness,", 0.00, ", stockwidth,", 0.00)");
}
}	else if (stockorigin == "Center") {
    translate([(-stocklength / 2), (-stockwidth / 2), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
if (generategcode == true) {
	writeln("(setupstock)");
writeln("(STOCK/BLOCK, ",stocklength,", ",stockwidth,", ",stockthickness,", ",stocklength/2,", ", stockwidth/2,", 0.00)");
}
}
}
if (generategcode == true) {
	writeln("G90");
	writeln("G21");
	writeln("(Move to safe Z to avoid workholding)");
	writeln("G53G0Z-5.000");
}
}

module closecut(retract) {
if (generategcode == true) {
	writeln("(closecut)");
	writeln("Z",retract);
	writeln("M02");
}
}

module retract(retract) {
if (generategcode == true) {
	writeln("(retract)");
	writeln("Z",retract);
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

module garcCCWUR(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn) {
  for (m = [0 : abs(Arc_Detail) : 90 - Arc_Detail * 3]) {
    gcut(bx + (xoffset * (1 - cos(((m - Arc_Detail) / 2)))) * 4, by - sin((m - Arc_Detail)) * xoffset, bz + (ez - bz) * ((m - Arc_Detail) / 90), bx + (xoffset * (1 - cos((m / 2)))) * 4, by - sin(m) * xoffset, bz + (ez - bz) * (m / 90), tn);
  }

}

module cut(bx, by, bz, ex, ey, ez, tn) {
  hull(){
    translate([bx, by, bz]){
      select_tool(tn);
    }
    translate([ex, ey, ez]){
      select_tool(tn);
    }
  }
}

module gcut(bx, by, bz, ex, ey, ez, tn) {
//	writeln("G1 X",bx," Y", by, "Z", bz);
if (generategcode == true) {
	writeln("(gcut)");
	writeln("G1 X",ex," Y", ey, "Z", ez);
}
cut(bx, by, bz, ex, ey, ez, tn);
}

module gcutfeed(bx, by, bz, ex, ey, ez, tn, feed) {
//	writeln("G1 X",bx," Y", by, "Z", bz);
if (generategcode == true) {
	writeln("(gcutfeed)");
	writeln("G1 X",ex," Y", ey, "Z", ez,"F",feed);
}
cut(bx, by, bz, ex, ey, ez, tn);
}

module garcCCW(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn) {
  if (xoffset < 0 && yoffset == 0) {
    garcCCWUR(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn);
  } else if (xoffset == 0 && yoffset < 0) {
    garcCWUL(ex, ey, ez, bx, by, bz, -yoffset, xoffset, tn);
  } else if (xoffset > 0 && yoffset == 0) {
    garcCWLL(ex, ey, ez, bx, by, bz, yoffset, xoffset, tn);
  } else if (xoffset == 0 && yoffset > 0) {
    garcCCWLR(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn);
  }

}

module garcCW(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn) {
  if (xoffset == 0 && yoffset < 0) {
    garcCCWUR(ex, ey, ez, bx, by, bz, yoffset, xoffset, tn);
  } else if (xoffset > 0 && yoffset == 0) {
    garcCWUL(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn);
  } else if (xoffset == 0 && yoffset > 0) {
    garcCWLL(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn);
  } else if (xoffset < 0 && yoffset == 0) {
    garcCCWLR(ex, ey, ez, bx, by, bz, yoffset, -xoffset, tn);
  }

}

module select_tool(tool_number) {
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

module toolchange(tool_number) {
if (generategcode == true) {
	writeln("(toolchange)");
	writeln("M05");
	writeln("(Move to safe Z to avoid workholding)");
	writeln("G53G0Z-5.000");
  if (tool_number == 201) {
	writeln("(TOOL/MILL,6.35, 0.00, 0.00, 0.00)");
  } else if (tool_number == 202) {
	writeln("(TOOL/MILL,6.35, 3.17, 0.00, 0.00)");
  } else if (tool_number == 102) {
	writeln("(TOOL/MILL,3.17, 0.00, 0.00, 0.00)");
  } else if (tool_number == 101) {
	writeln("(TOOL/MILL,3.17, 1.58, 0.00, 0.00)");
  } else if (tool_number == 301) {
	writeln("(TOOL/MILL,0.03, 0.00, 6.35, 45.00)");
  } else if (tool_number == 302) {
	writeln("(TOOL/MILL,0.03, 0.00, 10.998, 30.00)");
  } else if (tool_number == 390) {
	writeln("(TOOL/MILL,0.03, 0.00, 1.5875, 45.00)");
  }
	writeln(str("M6T",tool_number));
}
}

module startspindle(speed) {
if (generategcode == true) {
	writeln(str("(startspindle)"));
	writeln(str("M03S",speed));
}
}

module garcCWLL(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn) {
  for (m = [0 : abs(Arc_Detail) : 90 - Arc_Detail * 3]) {
    gcut(bx - sin((m - Arc_Detail)) * yoffset, by + (yoffset * (1 - cos(((m - Arc_Detail) / 2)))) * 4, bz + (ez - bz) * ((m - Arc_Detail) / 90), bx - sin(m) * yoffset, by + (yoffset * (1 - cos((m / 2)))) * 4, bz + (ez - bz) * (m / 90), tn);
  }

}

module garcCWUL(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn) {
  for (m = [0 : abs(Arc_Detail) : 90 - Arc_Detail * 3]) {
    gcut(bx + (xoffset * (1 - cos(((m - Arc_Detail) / 2)))) * 4, by + sin((m - Arc_Detail)) * xoffset, bz + (ez - bz) * ((m - Arc_Detail) / 90), bx + (xoffset * (1 - cos((m / 2)))) * 4, by + sin(m) * xoffset, bz + (ez - bz) * (m / 90), tn);
  }

}

module garcCCWLR(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn) {
  for (m = [0 : abs(Arc_Detail) : 90 - Arc_Detail * 3]) {
    gcut(bx + sin((m - Arc_Detail)) * yoffset, by + (yoffset * (1 - cos(((m - Arc_Detail) / 2)))) * 4, bz + (ez - bz) * ((m - Arc_Detail) / 90), bx + sin(m) * yoffset, by + (yoffset * (1 - cos((m / 2)))) * 4, bz + (ez - bz) * (m / 90), tn);
  }

}

module writecomment(comment) {
if (generategcode == true) {
	writeln("(",comment,")");
}
}
