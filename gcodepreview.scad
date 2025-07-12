//!OpenSCAD

//gcodepreview version 0.8
//
//used via include <gcodepreview.scad>;
//

use <gcodepreview.py>

module gcpversion(){
echo(pygcpversion());
}

//function myfunc(var) = gcp.myfunc(var);
//
//function getvv() = gcp.getvv();
//
//module makecube(xdim, ydim, zdim){
//gcp.makecube(xdim, ydim, zdim);
//}
//
//module placecube(){
//gcp.placecube();
//}
//
//module instantiatecube(){
//gcp.instantiatecube();
//}
//
function xpos() = gcp.xpos();

function ypos() = gcp.ypos();

function zpos() = gcp.zpos();

module setupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero, retractheight) {
    gcp.setupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero, retractheight);
}

module shiftstock(shiftX, shiftY, shiftZ) {
    gcp.shiftstock(shiftX, shiftY, shiftZ);
}

module addtostock(stockXwidth, stockYheight, stockZthickness, shiftX, shiftY, shiftZ) {
    gcp.addtostock(stockXwidth, stockYheight, stockZthickness, shiftX, shiftY, shiftZ);
}

module toolchange(tool_number, speed){
    gcp.toolchange(tool_number, speed);
}

module movetosafeZ(){
    gcp.rapid(gcp.xpos(), gcp.ypos(), retractheight);
}

module rapid(ex, ey, ez) {
    gcp.rapid(ex, ey, ez);
}

module rapidXY(ex, ey) {
    gcp.rapid(ex, ey, gcp.zpos());
}

module rapidXZ(ex, ez) {
    gcp.rapid(ex, gcp.zpos(), ez);
}

module rapidZ(ez) {
    gcp.rapid(gcp.xpos(), gcp.ypos(), ez);
}

module cutline(ex, ey, ez){
    gcp.cutline(ex, ey, ez);
}

module cutlinedxfgc(ex, ey, ez){
    gcp.cutlinedxfgc(ex, ey, ez);
}

module cutlineZgcfeed(ez, feed){
    gcp.cutlineZgcfeed(ez, feed);
}

module cutarcCC(barc, earc, xcenter, ycenter, radius, tpzreldim){
    gcp.cutarcCC(barc, earc, xcenter, ycenter, radius, tpzreldim);
}

module cutarcCW(barc, earc, xcenter, ycenter, radius, tpzreldim){
    gcp.cutarcCW(barc, earc, xcenter, ycenter, radius, tpzreldim);
}

module cutquarterCCNE(ex, ey, ez, radius){
     gcp.cutquarterCCNE(ex, ey, ez, radius);
}

module cutquarterCCNW(ex, ey, ez, radius){
     gcp.cutquarterCCNW(ex, ey, ez, radius);
}

module cutquarterCCSW(ex, ey, ez, radius){
    gcp.cutquarterCCSW(ex, ey, ez, radius);
}

module cutquarterCCSE(self, ex, ey, ez, radius){
    gcp.cutquarterCCSE(ex, ey, ez, radius);
}

module cutquarterCCNEdxf(ex, ey, ez, radius){
     gcp.cutquarterCCNEdxf(ex, ey, ez, radius);
}

module cutquarterCCNWdxf(ex, ey, ez, radius){
     gcp.cutquarterCCNWdxf(ex, ey, ez, radius);
}

module cutquarterCCSWdxf(ex, ey, ez, radius){
    gcp.cutquarterCCSWdxf(ex, ey, ez, radius);
}

module cutquarterCCSEdxf(self, ex, ey, ez, radius){
    gcp.cutquarterCCSEdxf(ex, ey, ez, radius);
}

function tool_diameter(td_tool, td_depth) = otool_diameter(td_tool, td_depth);

module stockandtoolpaths(){
    gcp.returnstockandtoolpaths();
}

module opendxffile(basefilename){
    gcp.opendxffile(basefilename);
}

module opendxffiles(Base_filename, large_square_tool_num, small_square_tool_num, large_ball_tool_num, small_ball_tool_num, large_V_tool_num, small_V_tool_num, DT_tool_num, KH_tool_num, Roundover_tool_num, MISC_tool_num) {
    gcp.opendxffiles(Base_filename, large_square_tool_num, small_square_tool_num, large_ball_tool_num, small_ball_tool_num, large_V_tool_num, small_V_tool_num, DT_tool_num, KH_tool_num, Roundover_tool_num, MISC_tool_num);
}

module opengcodefile(basefilename, currenttoolnum, toolradius, plunge, feed, speed) {
    gcp.opengcodefile(basefilename, currenttoolnum, toolradius, plunge, feed, speed);
}

module setdxfcolor(color){
    gcp.setdxfcolor(color);
}

module cutarcNECCdxfgc(ex, ey, ez, xcenter, ycenter, radius){
    gcp.cutarcNECCdxfgc(ex, ey, ez, xcenter, ycenter, radius);
}

module cutarcNWCCdxfgc(ex, ey, ez, xcenter, ycenter, radius){
    gcp.cutarcNWCCdxfgc(ex, ey, ez, xcenter, ycenter, radius);
}

module cutarcSWCCdxfgc(ex, ey, ez, xcenter, ycenter, radius){
    gcp.cutarcSWCCdxfgc(ex, ey, ez, xcenter, ycenter, radius);
}

module cutarcSECCdxfgc(ex, ey, ez, xcenter, ycenter, radius){
    gcp.cutarcSECCdxfgc(ex, ey, ez, xcenter, ycenter, radius);
}

module closegcodefile(){
    gcp.closegcodefile();
}

module closedxffiles(){
    gcp.closedxffiles();
}

module closedxffile(){
    gcp.closedxffile();
}

module cutkeyholegcdxf(kh_tool_num, kh_start_depth, kh_max_depth, kht_direction, kh_distance){
    gcp.cutkeyholegcdxf(kh_tool_num, kh_start_depth, kh_max_depth, kht_direction, kh_distance);
}

