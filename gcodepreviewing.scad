//!OpenSCAD


module setupcut(stocklength, stockwidth, stockthickness, zeroheight, stockorigin) {

writeln("(STOCK/BLOCK, ",stocklength,", ",stockwidth,", ",stockthickness,")");
	writeln("G90");
	writeln("G21");
	writeln("(Move to safe Z to avoid workholding)");
	writeln("G53G0Z-5.000");
	writeln("M05");

  if (zeroheight == "Top") {
    translate([0, 0, (-stockthickness)]){
      setstock(stocklength, stockwidth, stockthickness, stockorigin);
    }
  } else {
    setstock(stocklength, stockwidth, stockthickness, stockorigin);
  }

}

module setstock(stocklength, stockwidth, stockthickness, stockorigin) {
  if (stockorigin == "Lower-Left") {
    cube([stocklength, stockwidth, stockthickness], center=false);
  } else if (stockorigin == "Center-Left") {
    translate([0, (-stockwidth / 2), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
  } else if (stockorigin == "Top-Left") {
    translate([0, (-stockwidth), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
  } else {
    translate([(-stocklength / 2), (-stockwidth / 2), 0]){
      cube([stocklength, stockwidth, stockthickness], center=false);
    }
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
      cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=((es_diameter / 2) / tan((es_v_angle / 2))), center=false);
    }
  }
}

module garcCCWUR(bx, by, bz, ex, ey, ez, xoffset, yoffset, tn) {
  for (m = [0 : abs(Arc_Detail) : 90 - Arc_Detail * 3]) {
    gcut(bx + (xoffset * (1 - cos(((m - Arc_Detail) / 2)))) * 4, by - sin((m - Arc_Detail)) * xoffset, bz + (ez - bz) * ((m - Arc_Detail) / 90), bx + (xoffset * (1 - cos((m / 2)))) * 4, by - sin(m) * xoffset, bz + (ez - bz) * (m / 90), tn);
  }

}

module gcut(bx, by, bz, ex, ey, ez, tn) {
    writeln("G1 X",bx," Y", by, "Z", bz);
    writeln("G1 X",ex," Y", ey, "Z", ez);
  hull(){
    translate([bx, by, bz]){
      select_tool(tn);
    }
    translate([ex, ey, ez]){
      select_tool(tn);
    }
  }
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

//Stock_Width = 4;
//Stock_Length = 16.25;
//Stock_Thickness = 0.25;
//Top_Bottom_Thickness = 0.2559;
//Box_Width = 8.125;
//Box_Depth = 8.125;
//Number_of_Pins = 15;
//Lid_Position = 9;
//Joint_Offset = 0.1875;
//Tool_Diameter = 0.125;
//Ball_Nose_Tool_No = 101;
//V_endmill_Tool_No = 390;
//Units = 25.4;
//Arc_Detail = 3;
//sw = Stock_Width * Units;
//sl = Stock_Length * Units;
//st = Stock_Thickness * Units;
//tbt = Top_Bottom_Thickness * Units;
//bw = Box_Width * Units;
//bd = Box_Depth * Units;
//jo = Joint_Offset * Units;
//td = Tool_Diameter * Units;
//tr = td / 2;
//item = 0;
//difference() {
//  cube([sl, sw, st], center=false);
//
//  union(){
//    garcCCW(15, 0, st / 2, 30, 15, 0, 0, 15, Ball_Nose_Tool_No);
//    garcCCW(30, 15, st / 2, 15, 30, 0, -15, 0, Ball_Nose_Tool_No);
//    garcCCW(0, 15, st / 2, 15, 0, 0, 15, 0, Ball_Nose_Tool_No);
//    garcCCW(15, 30, st / 2, 0, 15, 0, 0, -15, Ball_Nose_Tool_No);
//  }
//}
