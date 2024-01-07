//!OpenSCAD

use <gcodepreview.py>;
use <pygcodepreview.scad>;

$fa = 4;
$fs = 0.25;

include <C:/Users/willa/OneDrive/Documents/OpenSCAD/libraries/gcodepreview.scad>

include <C:/Users/willa/OneDrive/Documents/OpenSCAD/libraries/cut2Dshapes.scad>

/* [Export] */
Base_filename = "export"; 

/* [Feeds and Speeds] */
feed = 400; 

/* [Export] */
generatedxf = true; 

/* [Export] */
generategcode = true; 

/* [Export] */
generatesvg = true; 

/* [Joinery] */
Glue_Gap = 0.05; 

/* [Joinery] */
Joinery_Gap = 0.1; 

/* [CAM] */
large_ball_tool_no = 0; // [0:0,111:111,101:101,202:202]

/* [CAM] */
large_square_tool_no = 0; // [0:0,112:112,102:102,201:201]

/* [Feeds and Speeds] */
large_V_ratio = 0.875; 

/* [CAM] */
large_V_tool_no = 301; // [0:0,301:301,690:690]

/* [Feeds and Speeds] */
plunge = 100; 

/* [Stock] */
retractheight = 9; 

/* [CAM] */
small_ball_tool_no = 0; // [0:0,121:121,111:111,101:101]

/* [CAM] */
small_square_tool_no = 102; // [0:0,122:122,112:112,102:102]

/* [Feeds and Speeds] */
small_V_ratio = 0.75; 

/* [CAM] */
small_V_tool_no = 390; // [0:0,390:390,301:301]

/* [Feeds and Speeds] */
speed = 16000; 

/* [Feeds and Speeds] */
square_ratio = 1; 

/* [Stock] */
stocklength = 219; 

/* [Stock] */
stockorigin = "Lower-Left"; // ["Lower-Left":"Lower-Left","Center-Left":"Center-Left","Top-Left":"Top-Left","Center":"Center"]

/* [Stock] */
stockthickness = 7.9; 

/* [Stock] */
stockwidth = 150; 

/* [CAM] */
toolradius = 1.5875; 

/* [Stock] */
zeroheight = "Top"; // ["Top":"Top","Bottom":"Bottom"]

module __Customizer_Limit__ () {}
filename_dxf = "";
filename_gcode = "";
filename_svg = "";
h_joints_no = 0;
h_joints_size = 0;
h_joints_spacing = 0;
joint_width = 0;
v_joints_no = 0;
v_joints_size = 0;
v_joints_spacing = 0;
/**
 * @param orientation [string] 
 * @param side [string] 
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 * @param square_tool_no [number] 
 * @param V_tool_no [number] 
 * @param large_V_tool_no [number] 
 */
module cutjoinery(orientation, side, bx, by, bz, ex, ey, ez, tool_radius, square_tool_no, V_tool_no, large_V_tool_no) {
    
    
    
    if (((orientation == "vertical") && (side == "both"))) {
        cutjoinery_vertical_both(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez, tool_radius = tool_radius, square_tool_no = square_tool_no, large_V_tool_no = large_V_tool_no, V_tool_no = V_tool_no);
    }
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param no_passes [number] 
 */
module cuthorizontalpasses(bx, by, bz, ex, ey, ez, no_passes) {
    begintoolpath(bx = bx, by = by, bz = (bz + toolradius));
    beginpolyline(bx = bx, by = by, bz = (bz + toolradius));
    rapid(ex = bx, ey = by, ez = (bz + toolradius));
    cutoneaxis_setfeed(axis = "Z", depth = (toolradius * -1), feed = plunge);
    * cutwithfeed(ex = bx, ey = by, ez = ez, feed = feed);
    for(var0__roY2oYC2E0GG1cfZT7P3Qg = [0:1:no_passes]) {
        cut(ex = bx, ey = (by + (((ey - by) / no_passes) * var0__roY2oYC2E0GG1cfZT7P3Qg)), ez = ez);
        addpolyline(bx = bx, by = (by + (((ey - by) / no_passes) * var0__roY2oYC2E0GG1cfZT7P3Qg)), bz = ez);
        cut(ex = ex, ey = (by + (((ey - by) / no_passes) * var0__roY2oYC2E0GG1cfZT7P3Qg)), ez = ez);
        addpolyline(bx = ex, by = (by + (((ey - by) / no_passes) * var0__roY2oYC2E0GG1cfZT7P3Qg)), bz = ez);
        if ((var0__roY2oYC2E0GG1cfZT7P3Qg < no_passes)) {
            cut(ex = bx, ey = ((by + (((ey - by) / no_passes) * var0__roY2oYC2E0GG1cfZT7P3Qg)) + ((ey - by) / no_passes)), ez = ez);
            addpolyline(bx = bx, by = ((by + (((ey - by) / no_passes) * var0__roY2oYC2E0GG1cfZT7P3Qg)) + ((ey - by) / no_passes)), bz = ez);
            cut(ex = ex, ey = ((by + (((ey - by) / no_passes) * var0__roY2oYC2E0GG1cfZT7P3Qg)) + ((ey - by) / no_passes)), ez = bz);
            addpolyline(bx = ex, by = ((by + (((ey - by) / no_passes) * var0__roY2oYC2E0GG1cfZT7P3Qg)) + ((ey - by) / no_passes)), bz = bz);
        }
    }
    
    * cut(ex = ex, ey = ey, ez = ez);
    * addpolyline(bx = ex, by = ey, bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 * @param square_tool_no [number] 
 * @param large_V_tool_no [number] 
 * @param V_tool_no [number] 
 */
module cutjoinery_horizontal_odd(bx, by, bz, ex, ey, ez, tool_radius, square_tool_no, large_V_tool_no, V_tool_no) {
    if ((square_tool_no > 0)) {
        toolchange(tool_number = square_tool_no, speed = speed);
        cut_rectangle(options = "horizontal", bx = bx, by = (by - tool_radius), bz = bz, ex = ex, ey = ((((bz - ez) + ey) - tool_radius) - tool_radius), ez = (tool_radius * -1), tr = tool_radius, stepover = 0, clearperimeter = false);
        * cuthorizontalpasses(bx = bx, by = (((by - (bz - ez)) + tool_radius) + tool_radius), bz = bz, ex = ex, ey = ((((bz - ez) + ey) - tool_radius) - tool_radius), ez = (tool_radius * -1), no_passes = round(number = ((bz - ez) / tool_radius)));
        cjho(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez, tool_radius = tool_radius);
    }
    
    if ((large_V_tool_no > 0)) {
        toolchange(tool_number = large_V_tool_no, speed = (large_V_ratio * speed));
        * cutcdxfline(bx = bx, by = ((by + ez) + tool_radius), bz = bz, ex = ex, ey = ((by + ez) + tool_radius), ez = (tool_radius * -1));
        cutcdxfline(bx = bx, by = ((by - ez) - tool_radius), bz = bz, ex = ex, ey = ((by - ez) - tool_radius), ez = (tool_radius * -1));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = (bx + (bz - ez)), ey = ey, ez = ez);
        cutcdxfline(bx = bx, by = (by - (((bz - ez) * -1) / 2)), bz = bz, ex = (bx + (bz - ez)), ey = (by - (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
        cutcdxfline(bx = bx, by = (by + (((bz - ez) * -1) / 2)), bz = bz, ex = (bx + (bz - ez)), ey = (by + (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
        cutcdxfline(bx = ex, by = ey, bz = bz, ex = (ex + ((bz - ez) * -1)), ey = ey, ez = ez);
        cutcdxfline(bx = ex, by = (by - (((bz - ez) * -1) / 2)), bz = bz, ex = (ex + ((bz - ez) * -1)), ey = (by - (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
        cutcdxfline(bx = ex, by = (by + (((bz - ez) * -1) / 2)), bz = bz, ex = (ex + ((bz - ez) * -1)), ey = (by + (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
    }
    
    if ((V_tool_no > 0)) {
        toolchange(tool_number = V_tool_no, speed = (small_V_ratio * speed));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez);
    }
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 * @param square_tool_no [number] 
 * @param large_V_tool_no [number] 
 * @param V_tool_no [number] 
 */
module cutjoinery_vertical_both(bx, by, bz, ex, ey, ez, tool_radius, square_tool_no, large_V_tool_no, V_tool_no) {
    if ((square_tool_no > 0)) {
        cut_rectangle(options = "vertical", bx = (((bx - (bz - ez)) + tool_radius) + tool_radius), by = by, bz = bz, ex = ((((bz - ez) + ex) - tool_radius) - tool_radius), ey = ey, ez = (tool_radius * -1), tr = tool_radius, stepover = 0, clearperimeter = false);
        toolchange(tool_number = square_tool_no, speed = speed);
        * cutverticalpasses(bx = (((bx - (bz - ez)) + tool_radius) + tool_radius), by = by, bz = bz, ex = ((((bz - ez) + ex) - tool_radius) - tool_radius), ey = ey, ez = (tool_radius * -1), no_passes = round(number = (((bz - ez) + ex) / tool_radius)));
        cjvb(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez, tool_radius = tool_radius);
    }
    
    if ((large_V_tool_no > 0)) {
        toolchange(tool_number = large_V_tool_no, speed = (large_V_ratio * speed));
        cutcdxfline(bx = ((bx + ez) + tool_radius), by = by, bz = bz, ex = ((bx + ez) + tool_radius), ey = ey, ez = (tool_radius * -1));
        cutcdxfline(bx = ((bx - ez) - tool_radius), by = by, bz = bz, ex = ((bx - ez) - tool_radius), ey = ey, ez = (tool_radius * -1));
        cutcdxfline(bx = (bx - ((bz - ez) / 2)), by = by, bz = (((bz - ez) / 2) * -1), ex = (bx - ((bz - ez) / 2)), ey = (ez * -1), ez = (((bz - ez) / 2) * -1));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = bx, ey = (ez * -1), ez = ez);
        cutcdxfline(bx = (((bz - ez) / 2) + bx), by = by, bz = (((bz - ez) / 2) * -1), ex = (((bz - ez) / 2) + bx), ey = (ez * -1), ez = (((bz - ez) / 2) * -1));
        cutcdxfline(bx = (bx - ((bz - ez) / 2)), by = (ey - (ez * -1)), bz = (((bz - ez) / 2) * -1), ex = (bx - ((bz - ez) / 2)), ey = ey, ez = (((bz - ez) / 2) * -1));
        cutcdxfline(bx = bx, by = (ey - (ez * -1)), bz = bz, ex = bx, ey = ey, ez = ez);
        cutcdxfline(bx = (((bz - ez) / 2) + bx), by = (ey - (ez * -1)), bz = (((bz - ez) / 2) * -1), ex = (((bz - ez) / 2) + bx), ey = ey, ez = (((bz - ez) / 2) * -1));
    }
    
    if ((V_tool_no > 0)) {
        toolchange(tool_number = V_tool_no, speed = (small_V_ratio * speed));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez);
    }
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 * @param square_tool_no [number] 
 * @param large_V_tool_no [number] 
 * @param V_tool_no [number] 
 */
module cutjoinery_vertical_odd(bx, by, bz, ex, ey, ez, tool_radius, square_tool_no, large_V_tool_no, V_tool_no) {
    if ((square_tool_no > 0)) {
        toolchange(tool_number = square_tool_no, speed = speed);
        cut_rectangle(options = "vertical", bx = (((bx - (bz - ez)) + tool_radius) + tool_radius), by = by, bz = bz, ex = (ex - tool_radius), ey = ey, ez = (tool_radius * -1), tr = tool_radius, stepover = 0, clearperimeter = false);
        * cutverticalpasses(bx = (((bx - (bz - ez)) + tool_radius) + tool_radius), by = by, bz = bz, ex = (ex - tool_radius), ey = ey, ez = (tool_radius * -1), no_passes = round(number = (((bz - ez) + ex) / tool_radius)));
        cjvodd(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez, tool_radius = tool_radius);
    }
    
    if ((large_V_tool_no > 0)) {
        toolchange(tool_number = large_V_tool_no, speed = (large_V_ratio * speed));
        cutcdxfline(bx = ((bx + ez) + tool_radius), by = by, bz = bz, ex = ((bx + ez) + tool_radius), ey = ey, ez = (tool_radius * -1));
        * cutcdxfline(bx = ((bx - ez) - tool_radius), by = by, bz = bz, ex = ((bx - ez) - tool_radius), ey = ey, ez = (tool_radius * -1));
        cutcdxfline(bx = (bx - ((bz - ez) / 2)), by = by, bz = (((bz - ez) / 2) * -1), ex = (bx - ((bz - ez) / 2)), ey = (ez * -1), ez = (((bz - ez) / 2) * -1));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = bx, ey = (ez * -1), ez = ez);
        * cutcdxfline(bx = (((bz - ez) / 2) + bx), by = by, bz = (((bz - ez) / 2) * -1), ex = (((bz - ez) / 2) + bx), ey = (ez * -1), ez = (((bz - ez) / 2) * -1));
        cutcdxfline(bx = (bx - ((bz - ez) / 2)), by = (ey - (ez * -1)), bz = (((bz - ez) / 2) * -1), ex = (bx - ((bz - ez) / 2)), ey = ey, ez = (((bz - ez) / 2) * -1));
        cutcdxfline(bx = bx, by = (ey - (ez * -1)), bz = bz, ex = bx, ey = ey, ez = ez);
        * cutcdxfline(bx = (((bz - ez) / 2) + bx), by = (ey - (ez * -1)), bz = (((bz - ez) / 2) * -1), ex = (((bz - ez) / 2) + bx), ey = ey, ez = (((bz - ez) / 2) * -1));
    }
    
    if ((V_tool_no > 0)) {
        toolchange(tool_number = V_tool_no, speed = (small_V_ratio * speed));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez);
    }
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 */
module cjvodd(bx, by, bz, ex, ey, ez, tool_radius) {
    v_joints_spacing = ((((ey - by) - ((bz - ez) * 2)) / ((round(number = ((((ey - by) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1)) - (tool_radius * 2));
    movetosafez();
    v_joints_size = (((ey - by) - ((bz - ez) * 2)) / ((round(number = ((((ey - by) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1));
    begintoolpath(bx = bx, by = by, bz = bz);
    v_joints_no = ((round(number = ((((ey - by) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1);
    beginpolyline(bx = bx, by = by, bz = bz);
    rapid(ex = bx, ey = by, ez = bz);
    joint_width = ((bz - ez) - (tool_radius * 2));
    cutoneaxis_setfeed(axis = "Z", depth = (ez + tool_radius), feed = plunge);
    cutwithfeed(ex = bx, ey = ((by + (bz - ez)) + tool_radius), ez = (ez + tool_radius), feed = feed);
    for(var0__xQDLuSws0EayFkqGQskUFw = [0:1:(round(number = (v_joints_no / 2)) - 1)]) {
        if ((var0__xQDLuSws0EayFkqGQskUFw == (round(number = (v_joints_no / 2)) - 1))) {
            cjvb_pin(bx = bx, by = ((((by + (bz - ez)) + tool_radius) + (var0__xQDLuSws0EayFkqGQskUFw * ((tool_radius * 4) + (v_joints_spacing * 2)))) - tool_radius), bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = v_joints_spacing);
        }
        else {
            cjvo_pins(bx = bx, by = ((((by + (bz - ez)) + tool_radius) + (var0__xQDLuSws0EayFkqGQskUFw * ((tool_radius * 4) + (v_joints_spacing * 2)))) - tool_radius), bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = v_joints_spacing);
        }
    }
    
    addpolyline(bx = bx, by = ((by + (bz - ez)) + tool_radius), bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 */
module cutcdxfline(bx, by, bz, ex, ey, ez) {
    movetosafez();
    begintoolpath(bx = bx, by = by, bz = bz);
    beginpolyline(bx = bx, by = by, bz = bz);
    rapid(ex = bx, ey = by, ez = bz);
    cutoneaxis_setfeed(axis = "Z", depth = ez, feed = plunge);
    cutwithfeed(ex = ex, ey = ey, ez = ez, feed = feed);
    addpolyline(bx = ex, by = ey, bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param no_passes [number] 
 */
module cutverticalpasses(bx, by, bz, ex, ey, ez, no_passes) {
    begintoolpath(bx = bx, by = by, bz = (bz + toolradius));
    beginpolyline(bx = bx, by = by, bz = (bz + toolradius));
    rapid(ex = bx, ey = by, ez = (bz + toolradius));
    cutoneaxis_setfeed(axis = "Z", depth = (toolradius * -1), feed = plunge);
    * cutwithfeed(ex = bx, ey = by, ez = ez, feed = feed);
    for(var0__ZknZRPCMkitGJfEgtjY2Q = [0:1:no_passes]) {
        cut(ex = (bx + (((ey - by) / no_passes) * var0__ZknZRPCMkitGJfEgtjY2Q)), ey = by, ez = ez);
        addpolyline(bx = (bx + (((ey - by) / no_passes) * var0__ZknZRPCMkitGJfEgtjY2Q)), by = by, bz = ez);
        cut(ex = (bx + (((ey - by) / no_passes) * var0__ZknZRPCMkitGJfEgtjY2Q)), ey = ey, ez = ez);
        addpolyline(bx = (bx + (((ey - by) / no_passes) * var0__ZknZRPCMkitGJfEgtjY2Q)), by = ey, bz = ez);
        if ((var0__ZknZRPCMkitGJfEgtjY2Q < no_passes)) {
            cut(ex = ((bx + (((ey - by) / no_passes) * var0__ZknZRPCMkitGJfEgtjY2Q)) + ((ey - by) / no_passes)), ey = ey, ez = ez);
            addpolyline(bx = ((bx + (((ey - by) / no_passes) * var0__ZknZRPCMkitGJfEgtjY2Q)) + ((ey - by) / no_passes)), by = ey, bz = ez);
            cut(ex = ((bx + (((ey - by) / no_passes) * var0__ZknZRPCMkitGJfEgtjY2Q)) + ((ey - by) / no_passes)), ey = by, ez = bz);
            addpolyline(bx = ((bx + (((ey - by) / no_passes) * var0__ZknZRPCMkitGJfEgtjY2Q)) + ((ey - by) / no_passes)), by = by, bz = bz);
        }
    }
    
    * cut(ex = ex, ey = ey, ez = ez);
    * addpolyline(bx = ex, by = ey, bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjvb_pins(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = bx, ey = (by + tr), ez = bz);
    addpolyline(bx = bx, by = (by + tr), bz = bz);
    cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = (by + tr), ez = bz);
    addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = (by + tr), bz = bz);
    cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = ((by + tr) + pin_step_size), ez = bz);
    addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = ((by + tr) + pin_step_size), ez = bz);
    addpolyline(bx = bx, by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    addpolyline(bx = bx, by = (((by + tr) + pin_step_size) + (tr * 2)), bz = bz);
    cut(ex = ((bx + (toolradius - Joinery_Gap)) + pin_width), ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    addpolyline(bx = ((bx + (toolradius - Joinery_Gap)) + pin_width), by = (((by + tr) + pin_step_size) + (tr * 2)), bz = bz);
    cut(ex = ((bx + (toolradius - Joinery_Gap)) + pin_width), ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
    addpolyline(bx = ((bx + (toolradius - Joinery_Gap)) + pin_width), by = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), bz = bz);
    cut(ex = bx, ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
    addpolyline(bx = bx, by = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), bz = bz);
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjvb_pin(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = bx, ey = (by + tr), ez = bz);
    addpolyline(bx = bx, by = (by + tr), bz = bz);
    cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = (by + tr), ez = bz);
    addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = (by + tr), bz = bz);
    cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = ((by + tr) + pin_step_size), ez = bz);
    addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = ((by + tr) + pin_step_size), ez = bz);
    addpolyline(bx = bx, by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    addpolyline(bx = bx, by = (((by + tr) + pin_step_size) + (tr * 2)), bz = bz);
    * cut(ex = (bx + (pin_width + (toolradius - Joinery_Gap))), ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    * cut(ex = (bx + (pin_width + (toolradius - Joinery_Gap))), ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
    * cut(ex = bx, ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 * @param square_tool_no [number] 
 * @param large_V_tool_no [number] 
 * @param V_tool_no [number] 
 */
module cutjoinery_horizontal_both(bx, by, bz, ex, ey, ez, tool_radius, square_tool_no, large_V_tool_no, V_tool_no) {
    if ((square_tool_no > 0)) {
        toolchange(tool_number = square_tool_no, speed = speed);
        cut_rectangle(options = "horizontal", bx = bx, by = (((by - (bz - ez)) + tool_radius) + tool_radius), bz = bz, ex = ex, ey = ((((bz - ez) + ey) - tool_radius) - tool_radius), ez = (tool_radius * -1), tr = tool_radius, stepover = 0, clearperimeter = false);
        * cuthorizontalpasses(bx = bx, by = (((by - (bz - ez)) + tool_radius) + tool_radius), bz = bz, ex = ex, ey = ((((bz - ez) + ey) - tool_radius) - tool_radius), ez = (tool_radius * -1), no_passes = round(number = ((bz - ez) / tool_radius)));
        cjhb(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez, tool_radius = tool_radius);
    }
    
    if ((large_V_tool_no > 0)) {
        toolchange(tool_number = large_V_tool_no, speed = (large_V_ratio * speed));
        cutcdxfline(bx = bx, by = ((by + ez) + tool_radius), bz = bz, ex = ex, ey = ((by + ez) + tool_radius), ez = (tool_radius * -1));
        cutcdxfline(bx = bx, by = ((by - ez) - tool_radius), bz = bz, ex = ex, ey = ((by - ez) - tool_radius), ez = (tool_radius * -1));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = (bx + (bz - ez)), ey = ey, ez = ez);
        cutcdxfline(bx = bx, by = (by - (((bz - ez) * -1) / 2)), bz = bz, ex = (bx + (bz - ez)), ey = (by - (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
        cutcdxfline(bx = bx, by = (by + (((bz - ez) * -1) / 2)), bz = bz, ex = (bx + (bz - ez)), ey = (by + (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
        cutcdxfline(bx = ex, by = ey, bz = bz, ex = (ex + ((bz - ez) * -1)), ey = ey, ez = ez);
        cutcdxfline(bx = ex, by = (by - (((bz - ez) * -1) / 2)), bz = bz, ex = (ex + ((bz - ez) * -1)), ey = (by - (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
        cutcdxfline(bx = ex, by = (by + (((bz - ez) * -1) / 2)), bz = bz, ex = (ex + ((bz - ez) * -1)), ey = (by + (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
    }
    
    if ((V_tool_no > 0)) {
        toolchange(tool_number = V_tool_no, speed = (small_V_ratio * speed));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez);
    }
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 */
module cjvb(bx, by, bz, ex, ey, ez, tool_radius) {
    v_joints_spacing = ((((ey - by) - ((bz - ez) * 2)) / ((round(number = ((((ey - by) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1)) - (tool_radius * 2));
    movetosafez();
    v_joints_size = (((ey - by) - ((bz - ez) * 2)) / ((round(number = ((((ey - by) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1));
    begintoolpath(bx = bx, by = by, bz = bz);
    v_joints_no = ((round(number = ((((ey - by) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1);
    beginpolyline(bx = bx, by = by, bz = bz);
    rapid(ex = bx, ey = by, ez = bz);
    joint_width = ((bz - ez) - (tool_radius * 2));
    cutoneaxis_setfeed(axis = "Z", depth = (ez + tool_radius), feed = plunge);
    cutwithfeed(ex = bx, ey = ((by + (bz - ez)) + tool_radius), ez = (ez + tool_radius), feed = feed);
    for(var0__NBgGTXHKE6huL5HFz08MA = [0:1:(round(number = (v_joints_no / 2)) - 1)]) {
        if ((var0__NBgGTXHKE6huL5HFz08MA == (round(number = (v_joints_no / 2)) - 1))) {
            cjvb_pin(bx = bx, by = ((((by + (bz - ez)) + tool_radius) + (var0__NBgGTXHKE6huL5HFz08MA * ((tool_radius * 4) + (v_joints_spacing * 2)))) - tool_radius), bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = v_joints_spacing);
        }
        else {
            cjvb_pins(bx = bx, by = ((((by + (bz - ez)) + tool_radius) + (var0__NBgGTXHKE6huL5HFz08MA * ((tool_radius * 4) + (v_joints_spacing * 2)))) - tool_radius), bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = v_joints_spacing);
        }
    }
    
    addpolyline(bx = bx, by = ((by + (bz - ez)) + tool_radius), bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjvo_pins(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = bx, ey = (by + tr), ez = bz);
    addpolyline(bx = bx, by = (by + tr), bz = bz);
    cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = (by + tr), ez = bz);
    addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = (by + tr), bz = bz);
    cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = ((by + tr) + pin_step_size), ez = bz);
    addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = ((by + tr) + pin_step_size), ez = bz);
    addpolyline(bx = bx, by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    addpolyline(bx = bx, by = (((by + tr) + pin_step_size) + (tr * 2)), bz = bz);
    * cut(ex = ((bx + (toolradius - Joinery_Gap)) + pin_width), ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    * addpolyline(bx = ((bx + (toolradius - Joinery_Gap)) + pin_width), by = (((by + tr) + pin_step_size) + (tr * 2)), bz = bz);
    * cut(ex = ((bx + (toolradius - Joinery_Gap)) + pin_width), ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
    * addpolyline(bx = ((bx + (toolradius - Joinery_Gap)) + pin_width), by = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), bz = bz);
    cut(ex = bx, ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
    addpolyline(bx = bx, by = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), bz = bz);
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 * @param square_tool_no [number] 
 * @param large_V_tool_no [number] 
 * @param V_tool_no [number] 
 */
module cutjoinery_vertical_even(bx, by, bz, ex, ey, ez, tool_radius, square_tool_no, large_V_tool_no, V_tool_no) {
    if ((square_tool_no > 0)) {
        toolchange(tool_number = square_tool_no, speed = speed);
        cut_rectangle(options = "vertical", bx = bx, by = by, bz = bz, ex = ((((bz - ez) + ex) - tool_radius) - tool_radius), ey = ey, ez = (tool_radius * -1), tr = tool_radius, stepover = 0, clearperimeter = false);
        * cutverticalpasses(bx = bx, by = by, bz = bz, ex = ((((bz - ez) + ex) - tool_radius) - tool_radius), ey = ey, ez = (tool_radius * -1), no_passes = round(number = (((bz - ez) + ex) / tool_radius)));
        cjveven(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez, tool_radius = tool_radius);
    }
    
    if ((large_V_tool_no > 0)) {
        toolchange(tool_number = large_V_tool_no, speed = (large_V_ratio * speed));
        * cutcdxfline(bx = ((bx + ez) + tool_radius), by = by, bz = bz, ex = ((bx + ez) + tool_radius), ey = ey, ez = (tool_radius * -1));
        cutcdxfline(bx = ((bx - ez) - tool_radius), by = by, bz = bz, ex = ((bx - ez) - tool_radius), ey = ey, ez = (tool_radius * -1));
        cutcdxfline(bx = (bx - ((bz - ez) / 2)), by = by, bz = (((bz - ez) / 2) * -1), ex = (bx - ((bz - ez) / 2)), ey = (ez * -1), ez = (((bz - ez) / 2) * -1));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = bx, ey = (ez * -1), ez = ez);
        cutcdxfline(bx = (((bz - ez) / 2) + bx), by = by, bz = (((bz - ez) / 2) * -1), ex = (((bz - ez) / 2) + bx), ey = (ez * -1), ez = (((bz - ez) / 2) * -1));
        cutcdxfline(bx = (bx - ((bz - ez) / 2)), by = (ey - (ez * -1)), bz = (((bz - ez) / 2) * -1), ex = (bx - ((bz - ez) / 2)), ey = ey, ez = (((bz - ez) / 2) * -1));
        cutcdxfline(bx = bx, by = (ey - (ez * -1)), bz = bz, ex = bx, ey = ey, ez = ez);
        cutcdxfline(bx = (((bz - ez) / 2) + bx), by = (ey - (ez * -1)), bz = (((bz - ez) / 2) * -1), ex = (((bz - ez) / 2) + bx), ey = ey, ez = (((bz - ez) / 2) * -1));
    }
    
    if ((V_tool_no > 0)) {
        toolchange(tool_number = V_tool_no, speed = (small_V_ratio * speed));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez);
    }
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 */
module cjveven(bx, by, bz, ex, ey, ez, tool_radius) {
    v_joints_spacing = ((((ey - by) - ((bz - ez) * 2)) / ((round(number = ((((ey - by) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1)) - (tool_radius * 2));
    movetosafez();
    v_joints_size = (((ey - by) - ((bz - ez) * 2)) / ((round(number = ((((ey - by) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1));
    begintoolpath(bx = bx, by = by, bz = bz);
    v_joints_no = ((round(number = ((((ey - by) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1);
    beginpolyline(bx = bx, by = by, bz = bz);
    rapid(ex = bx, ey = by, ez = bz);
    joint_width = ((bz - ez) - (tool_radius * 2));
    cutoneaxis_setfeed(axis = "Z", depth = (ez + tool_radius), feed = plunge);
    cutwithfeed(ex = bx, ey = ((by + (bz - ez)) + tool_radius), ez = (ez + tool_radius), feed = feed);
    for(var0__BujiOl6gCkKiXAxvM4lCA = [0:1:(round(number = (v_joints_no / 2)) - 1)]) {
        if ((var0__BujiOl6gCkKiXAxvM4lCA == (round(number = (v_joints_no / 2)) - 1))) {
            cjve_pin(bx = bx, by = ((((by + (bz - ez)) + tool_radius) + (var0__BujiOl6gCkKiXAxvM4lCA * ((tool_radius * 4) + (v_joints_spacing * 2)))) - tool_radius), bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = v_joints_spacing);
        }
        else {
            cjve_pins(bx = bx, by = ((((by + (bz - ez)) + tool_radius) + (var0__BujiOl6gCkKiXAxvM4lCA * ((tool_radius * 4) + (v_joints_spacing * 2)))) - tool_radius), bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = v_joints_spacing);
        }
    }
    
    addpolyline(bx = bx, by = ((by + (bz - ez)) + tool_radius), bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjve_pins(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = bx, ey = (by + tr), ez = bz);
    addpolyline(bx = bx, by = (by + tr), bz = bz);
    * cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = (by + tr), ez = bz);
    * addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = (by + tr), bz = bz);
    * cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = ((by + tr) + pin_step_size), ez = bz);
    * addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = ((by + tr) + pin_step_size), ez = bz);
    addpolyline(bx = bx, by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    addpolyline(bx = bx, by = (((by + tr) + pin_step_size) + (tr * 2)), bz = bz);
    cut(ex = ((bx + (toolradius - Joinery_Gap)) + pin_width), ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    addpolyline(bx = ((bx + (toolradius - Joinery_Gap)) + pin_width), by = (((by + tr) + pin_step_size) + (tr * 2)), bz = bz);
    cut(ex = ((bx + (toolradius - Joinery_Gap)) + pin_width), ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
    addpolyline(bx = ((bx + (toolradius - Joinery_Gap)) + pin_width), by = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), bz = bz);
    cut(ex = bx, ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
    addpolyline(bx = bx, by = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), bz = bz);
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjve_pin(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = bx, ey = (by + tr), ez = bz);
    addpolyline(bx = bx, by = (by + tr), bz = bz);
    * cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = (by + tr), ez = bz);
    * addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = (by + tr), bz = bz);
    * cut(ex = ((bx - (toolradius - Joinery_Gap)) - pin_width), ey = ((by + tr) + pin_step_size), ez = bz);
    * addpolyline(bx = ((bx - (toolradius - Joinery_Gap)) - pin_width), by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = ((by + tr) + pin_step_size), ez = bz);
    addpolyline(bx = bx, by = ((by + tr) + pin_step_size), bz = bz);
    cut(ex = bx, ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    addpolyline(bx = bx, by = (((by + tr) + pin_step_size) + (tr * 2)), bz = bz);
    * cut(ex = (bx + (pin_width + (toolradius - Joinery_Gap))), ey = (((by + tr) + pin_step_size) + (tr * 2)), ez = bz);
    * cut(ex = (bx + (pin_width + (toolradius - Joinery_Gap))), ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
    * cut(ex = bx, ey = ((((by + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ez = bz);
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 */
module cjhb(bx, by, bz, ex, ey, ez, tool_radius) {
    h_joints_spacing = ((((ex - bx) - ((bz - ez) * 2)) / ((round(number = ((((ex - bx) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1)) - (tool_radius * 2));
    movetosafez();
    h_joints_size = (((ex - bx) - ((bz - ez) * 2)) / ((round(number = ((((ex - bx) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1));
    begintoolpath(bx = bx, by = by, bz = bz);
    h_joints_no = ((round(number = ((((ex - bx) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1);
    beginpolyline(bx = bx, by = by, bz = bz);
    rapid(ex = bx, ey = by, ez = bz);
    joint_width = ((bz - ez) - (tool_radius * 2));
    cutoneaxis_setfeed(axis = "Z", depth = (ez + tool_radius), feed = plunge);
    cutwithfeed(ex = ((bx + (bz - ez)) + tool_radius), ey = by, ez = (ez + tool_radius), feed = feed);
    for(var0__hWOgPcN6rEeqJLm8g1nC5g = [0:1:(round(number = (h_joints_no / 2)) - 1)]) {
        if ((var0__hWOgPcN6rEeqJLm8g1nC5g == (round(number = (h_joints_no / 2)) - 1))) {
            cjhb_pin(bx = ((((bx + (bz - ez)) + tool_radius) + (var0__hWOgPcN6rEeqJLm8g1nC5g * ((tool_radius * 4) + (h_joints_spacing * 2)))) - tool_radius), by = by, bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = h_joints_spacing);
        }
        else {
            cjhb_pins(bx = ((((bx + (bz - ez)) + tool_radius) + (var0__hWOgPcN6rEeqJLm8g1nC5g * ((tool_radius * 4) + (h_joints_spacing * 2)))) - tool_radius), by = by, bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = h_joints_spacing);
        }
    }
    
    addpolyline(bx = ((bx + (bz - ez)) + tool_radius), by = bx, bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjhb_pins(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = (bx + tr), ey = by, ez = bz);
    addpolyline(bx = (bx + tr), by = by, bz = bz);
    cut(ex = (bx + tr), ey = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), ez = bz);
    addpolyline(bx = (bx + tr), by = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), bz = bz);
    cut(ex = ((bx + tr) + (pin_step_size + Glue_Gap)), ey = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), ez = bz);
    addpolyline(bx = ((bx + tr) + (pin_step_size + Glue_Gap)), by = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), bz = bz);
    cut(ex = ((bx + tr) + (pin_step_size + Glue_Gap)), ey = by, ez = bz);
    addpolyline(bx = bx, by = ((bx + tr) + (pin_step_size + Glue_Gap)), bz = bz);
    cut(ex = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), ey = by, ez = bz);
    addpolyline(bx = bx, by = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), bz = bz);
    cut(ex = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = ((bx + by) + pin_width), by = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), bz = bz);
    cut(ex = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + (pin_step_size + Glue_Gap)), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = ((bx + by) + pin_width), by = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + pin_step_size), bz = bz);
    cut(ex = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + (pin_step_size + Glue_Gap)), ey = by, ez = bz);
    * addpolyline(bx = bx, by = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + pin_step_size), bz = bz);
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 * @param square_tool_no [number] 
 * @param large_V_tool_no [number] 
 * @param V_tool_no [number] 
 */
module cutjoinery_horizontal_even(bx, by, bz, ex, ey, ez, tool_radius, square_tool_no, large_V_tool_no, V_tool_no) {
    if ((square_tool_no > 0)) {
        cut_rectangle(options = "horizontal", bx = bx, by = (((by - (bz - ez)) + tool_radius) + tool_radius), bz = bz, ex = ex, ey = ey, ez = (tool_radius * -1), tr = tool_radius, stepover = 0, clearperimeter = false);
        toolchange(tool_number = square_tool_no, speed = speed);
        * cuthorizontalpasses(bx = bx, by = (((by - (bz - ez)) + tool_radius) + tool_radius), bz = bz, ex = ex, ey = ((((bz - ez) + ey) - tool_radius) - tool_radius), ez = (tool_radius * -1), no_passes = round(number = ((bz - ez) / tool_radius)));
        cjhe(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez, tool_radius = tool_radius);
    }
    
    if ((large_V_tool_no > 0)) {
        toolchange(tool_number = large_V_tool_no, speed = (large_V_ratio * speed));
        cutcdxfline(bx = bx, by = ((by + ez) + tool_radius), bz = bz, ex = ex, ey = ((by + ez) + tool_radius), ez = (tool_radius * -1));
        * cutcdxfline(bx = bx, by = ((by - ez) - tool_radius), bz = bz, ex = ex, ey = ((by - ez) - tool_radius), ez = (tool_radius * -1));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = (bx + (bz - ez)), ey = ey, ez = ez);
        cutcdxfline(bx = bx, by = (by - (((bz - ez) * -1) / 2)), bz = bz, ex = (bx + (bz - ez)), ey = (by - (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
        cutcdxfline(bx = bx, by = (by + (((bz - ez) * -1) / 2)), bz = bz, ex = (bx + (bz - ez)), ey = (by + (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
        cutcdxfline(bx = ex, by = ey, bz = bz, ex = (ex + ((bz - ez) * -1)), ey = ey, ez = ez);
        cutcdxfline(bx = ex, by = (by - (((bz - ez) * -1) / 2)), bz = bz, ex = (ex + ((bz - ez) * -1)), ey = (by - (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
        cutcdxfline(bx = ex, by = (by + (((bz - ez) * -1) / 2)), bz = bz, ex = (ex + ((bz - ez) * -1)), ey = (by + (((bz - ez) * -1) / 2)), ez = (ez - (((bz - ez) * -1) / 2)));
    }
    
    if ((V_tool_no > 0)) {
        toolchange(tool_number = V_tool_no, speed = (small_V_ratio * speed));
        cutcdxfline(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez);
    }
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjhb_pin(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = (bx + tr), ey = by, ez = bz);
    addpolyline(bx = (bx + tr), by = by, bz = bz);
    cut(ex = (bx + tr), ey = ((by + (tr - Joinery_Gap)) + pin_width), ez = bz);
    addpolyline(bx = (bx + tr), by = ((by + (tr - Joinery_Gap)) + pin_width), bz = bz);
    cut(ex = ((bx + tr) + pin_step_size), ey = ((by + (tr - Joinery_Gap)) + pin_width), ez = bz);
    addpolyline(bx = ((bx + tr) + pin_step_size), by = ((by + (tr - Joinery_Gap)) + pin_width), bz = bz);
    cut(ex = ((bx + tr) + pin_step_size), ey = by, ez = bz);
    addpolyline(bx = ((bx + tr) + pin_step_size), by = by, bz = bz);
    cut(ex = (((bx + tr) + pin_step_size) + (tr * 2)), ey = by, ez = bz);
    addpolyline(bx = (((bx + tr) + pin_step_size) + (tr * 2)), by = by, bz = bz);
    * cut(ex = (((bx + tr) + pin_step_size) + (tr * 2)), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = ((bx + by) + pin_width), by = (((bx + tr) + pin_step_size) + (tr * 2)), bz = bz);
    * cut(ex = ((((bx + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = ((bx + by) + pin_width), by = ((((bx + tr) + pin_step_size) + (tr * 2)) + pin_step_size), bz = bz);
    cut(ex = ((((bx + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ey = by, ez = bz);
    addpolyline(bx = ((((bx + tr) + pin_step_size) + (tr * 2)) + pin_step_size), by = by, bz = bz);
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjho_pin(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = (bx + tr), ey = by, ez = bz);
    addpolyline(bx = (bx + tr), by = by, bz = bz);
    cut(ex = (bx + tr), ey = ((by + (tr - Joinery_Gap)) + pin_width), ez = bz);
    addpolyline(bx = (bx + tr), by = ((by + (tr - Joinery_Gap)) + pin_width), bz = bz);
    cut(ex = ((bx + tr) + pin_step_size), ey = ((by + (tr - Joinery_Gap)) + pin_width), ez = bz);
    addpolyline(bx = ((bx + tr) + pin_step_size), by = ((by + (tr - Joinery_Gap)) + pin_width), bz = bz);
    cut(ex = ((bx + tr) + pin_step_size), ey = by, ez = bz);
    addpolyline(bx = ((bx + tr) + pin_step_size), by = by, bz = bz);
    cut(ex = (((bx + tr) + pin_step_size) + (tr * 2)), ey = by, ez = bz);
    addpolyline(bx = (((bx + tr) + pin_step_size) + (tr * 2)), by = by, bz = bz);
    * cut(ex = (((bx + tr) + pin_step_size) + (tr * 2)), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = ((bx + by) + pin_width), by = (((bx + tr) + pin_step_size) + (tr * 2)), bz = bz);
    * cut(ex = ((((bx + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = ((bx + by) + pin_width), by = ((((bx + tr) + pin_step_size) + (tr * 2)) + pin_step_size), bz = bz);
    cut(ex = ((((bx + tr) + pin_step_size) + (tr * 2)) + pin_step_size), ey = by, ez = bz);
    addpolyline(bx = ((((bx + tr) + pin_step_size) + (tr * 2)) + pin_step_size), by = by, bz = bz);
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 */
module cjho(bx, by, bz, ex, ey, ez, tool_radius) {
    h_joints_spacing = ((((ex - bx) - ((bz - ez) * 2)) / ((round(number = ((((ex - bx) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1)) - (tool_radius * 2));
    movetosafez();
    h_joints_size = (((ex - bx) - ((bz - ez) * 2)) / ((round(number = ((((ex - bx) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1));
    begintoolpath(bx = bx, by = by, bz = bz);
    h_joints_no = ((round(number = ((((ex - bx) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1);
    beginpolyline(bx = bx, by = by, bz = bz);
    rapid(ex = bx, ey = by, ez = bz);
    joint_width = ((bz - ez) - (tool_radius * 2));
    cutoneaxis_setfeed(axis = "Z", depth = (ez + tool_radius), feed = plunge);
    cutwithfeed(ex = ((bx + (bz - ez)) + tool_radius), ey = by, ez = (ez + tool_radius), feed = feed);
    for(var0__jvbrcJdlUadWowb6CRslA = [0:1:(round(number = (h_joints_no / 2)) - 1)]) {
        if ((var0__jvbrcJdlUadWowb6CRslA == (round(number = (h_joints_no / 2)) - 1))) {
            cjho_pin(bx = ((((bx + (bz - ez)) + tool_radius) + (var0__jvbrcJdlUadWowb6CRslA * ((tool_radius * 4) + (h_joints_spacing * 2)))) - tool_radius), by = by, bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = h_joints_spacing);
        }
        else {
            cjho_pins(bx = ((((bx + (bz - ez)) + tool_radius) + (var0__jvbrcJdlUadWowb6CRslA * ((tool_radius * 4) + (h_joints_spacing * 2)))) - tool_radius), by = by, bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = h_joints_spacing);
        }
    }
    
    addpolyline(bx = ((bx + (bz - ez)) + tool_radius), by = bx, bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjho_pins(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = (bx + tr), ey = by, ez = bz);
    addpolyline(bx = (bx + tr), by = by, bz = bz);
    cut(ex = (bx + tr), ey = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), ez = bz);
    addpolyline(bx = (bx + tr), by = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), bz = bz);
    cut(ex = ((bx + tr) + (pin_step_size + Glue_Gap)), ey = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), ez = bz);
    addpolyline(bx = ((bx + tr) + (pin_step_size + Glue_Gap)), by = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), bz = bz);
    cut(ex = ((bx + tr) + (pin_step_size + Glue_Gap)), ey = by, ez = bz);
    addpolyline(bx = bx, by = ((bx + tr) + (pin_step_size + Glue_Gap)), bz = bz);
    cut(ex = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), ey = by, ez = bz);
    addpolyline(bx = bx, by = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), bz = bz);
    * cut(ex = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = ((bx + by) + pin_width), by = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), bz = bz);
    * cut(ex = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + (pin_step_size + Glue_Gap)), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = undef, by = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + pin_step_size), bz = bz);
    cut(ex = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + (pin_step_size + Glue_Gap)), ey = by, ez = bz);
    addpolyline(bx = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + (pin_step_size + Glue_Gap)), by = by, bz = bz);
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tool_radius [number] 
 */
module cjhe(bx, by, bz, ex, ey, ez, tool_radius) {
    h_joints_spacing = ((((ex - bx) - ((bz - ez) * 2)) / ((round(number = ((((ex - bx) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1)) - (tool_radius * 2));
    movetosafez();
    h_joints_size = (((ex - bx) - ((bz - ez) * 2)) / ((round(number = ((((ex - bx) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1));
    begintoolpath(bx = bx, by = by, bz = bz);
    h_joints_no = ((round(number = ((((ex - bx) - ((bz - ez) * 2)) / 4) / ((tool_radius * 1.1) + Glue_Gap))) * 2) - 1);
    beginpolyline(bx = bx, by = by, bz = bz);
    rapid(ex = bx, ey = by, ez = bz);
    joint_width = ((bz - ez) - (tool_radius * 2));
    cutoneaxis_setfeed(axis = "Z", depth = (ez + tool_radius), feed = plunge);
    cutwithfeed(ex = ((bx + (bz - ez)) + tool_radius), ey = by, ez = (ez + tool_radius), feed = feed);
    for(var0__imcMZ5QSUCodGUaNSOw = [0:1:(round(number = (h_joints_no / 2)) - 1)]) {
        if ((var0__imcMZ5QSUCodGUaNSOw == (round(number = (h_joints_no / 2)) - 1))) {
            * cjhb_pin(bx = ((((bx + (bz - ez)) + tool_radius) + (var0__imcMZ5QSUCodGUaNSOw * ((tool_radius * 4) + (h_joints_spacing * 2)))) - tool_radius), by = by, bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = h_joints_spacing);
        }
        else {
            cjhe_pins(bx = ((((bx + (bz - ez)) + tool_radius) + (var0__imcMZ5QSUCodGUaNSOw * ((tool_radius * 4) + (h_joints_spacing * 2)))) - tool_radius), by = by, bz = (ez + tool_radius), tr = tool_radius, pin_width = joint_width, pin_step_size = h_joints_spacing);
        }
    }
    
    addpolyline(bx = ((bx + (bz - ez)) + tool_radius), by = bx, bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param tr [number] 
 * @param pin_width [number] 
 * @param pin_step_size [number] 
 */
module cjhe_pins(bx, by, bz, tr, pin_width, pin_step_size) {
    cut(ex = bx, ey = by, ez = bz);
    addpolyline(bx = bx, by = by, bz = bz);
    cut(ex = (bx + tr), ey = by, ez = bz);
    addpolyline(bx = (bx + tr), by = by, bz = bz);
    * cut(ex = (bx + tr), ey = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), ez = bz);
    * addpolyline(bx = (bx + tr), by = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), bz = bz);
    * cut(ex = ((bx + tr) + (pin_step_size + Glue_Gap)), ey = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), ez = bz);
    * addpolyline(bx = ((bx + tr) + (pin_step_size + Glue_Gap)), by = ((by + (tr - Joinery_Gap)) + (pin_width - Glue_Gap)), bz = bz);
    cut(ex = ((bx + tr) + (pin_step_size + Glue_Gap)), ey = by, ez = bz);
    addpolyline(bx = bx, by = ((bx + tr) + (pin_step_size + Glue_Gap)), bz = bz);
    cut(ex = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), ey = by, ez = bz);
    addpolyline(bx = bx, by = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), bz = bz);
    cut(ex = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = ((bx + by) + pin_width), by = (((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)), bz = bz);
    cut(ex = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + (pin_step_size + Glue_Gap)), ey = ((by - (tr - Joinery_Gap)) - pin_width), ez = bz);
    * addpolyline(bx = ((bx + by) + pin_width), by = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + pin_step_size), bz = bz);
    cut(ex = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + (pin_step_size + Glue_Gap)), ey = by, ez = bz);
    * addpolyline(bx = bx, by = ((((bx + tr) + (pin_step_size + Glue_Gap)) + ((tr * 2) - Glue_Gap)) + pin_step_size), bz = bz);
}

difference() {
    union() {
        opengcodefile(fn = filename_gcode);
        opendxffile(fn = filename_dxf);
        opensvgfile(fn = filename_svg);
        setupstock(stocklength = stocklength, stockwidth = stockwidth, stockthickness = stockthickness, zeroheight = zeroheight, stockorigin = stockorigin);
    }
    
    movetosafeheight();
    * cutjoinery_vertical_both(bx = (stocklength / 2), by = 0, bz = 0, ex = (stocklength / 2), ey = stockwidth, ez = (stockthickness * -1), tool_radius = toolradius, square_tool_no = small_square_tool_no, large_V_tool_no = large_V_tool_no, V_tool_no = small_V_tool_no);
    * cutjoinery_vertical_odd(bx = stocklength, by = 0, bz = 0, ex = stocklength, ey = stockwidth, ez = (stockthickness * -1), tool_radius = toolradius, square_tool_no = small_square_tool_no, large_V_tool_no = large_V_tool_no, V_tool_no = small_V_tool_no);
    * cutjoinery_vertical_even(bx = 0, by = 0, bz = 0, ex = 0, ey = stockwidth, ez = (stockthickness * -1), tool_radius = toolradius, square_tool_no = small_square_tool_no, large_V_tool_no = large_V_tool_no, V_tool_no = small_V_tool_no);
    cutjoinery_horizontal_both(bx = 0, by = (stockwidth / 2), bz = 0, ex = stocklength, ey = (stockwidth / 2), ez = (stockthickness * -1), tool_radius = toolradius, square_tool_no = small_square_tool_no, large_V_tool_no = large_V_tool_no, V_tool_no = small_V_tool_no);
    * cutjoinery_horizontal_odd(bx = 0, by = 0, bz = 0, ex = stocklength, ey = 0, ez = (stockthickness * -1), tool_radius = toolradius, square_tool_no = small_square_tool_no, large_V_tool_no = large_V_tool_no, V_tool_no = small_V_tool_no);
    * cutjoinery_horizontal_even(bx = 0, by = stockwidth, bz = 0, ex = stocklength, ey = stockwidth, ez = (stockthickness * -1), tool_radius = toolradius, square_tool_no = small_square_tool_no, large_V_tool_no = large_V_tool_no, V_tool_no = small_V_tool_no);
    endtoolpath();
    closegcodefile();
    closedxffile();
    closesvgfile();
}

filename_gcode = str(Base_filename, ".nc");
filename_dxf = Base_filename;
filename_svg = str(Base_filename, ".svg");