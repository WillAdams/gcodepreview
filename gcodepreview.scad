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

module toolchange(tool_number,speed){
    gcp.toolchange(tool_number,speed);
}

function tool_diameter(td_tool, td_depth) = otool_diameter(td_tool, td_depth);

module movetosafeZ(){
    gcp.rapid(gcp.xpos(),gcp.ypos(),retractheight);
}

module rapid(ex, ey, ez) {
    gcp.rapid(ex, ey, ez);
}

module rapidXY(ex, ey) {
    gcp.rapid(ex, ey, gcp.zpos());
}

module rapidZ(ez) {
    gcp.rapid(gcp.xpos(),gcp.ypos(),ez);
}

module cutline(ex, ey, ez){
    gcp.cutline(ex, ey, ez);
}

module cutlinedxfgc(ex, ey, ez){
    gcp.cutlinedxfgc(ex, ey, ez);
}

module cutarcCC(barc, earc, xcenter, ycenter, radius, tpzreldim){
    gcp.cutarcCC(barc, earc, xcenter, ycenter, radius, tpzreldim);
}

module cutarcCW(barc, earc, xcenter, ycenter, radius, tpzreldim){
    gcp.cutarcCW(barc, earc, xcenter, ycenter, radius, tpzreldim);
}

module cutkeyholegcdxf(kh_tool_num, kh_start_depth, kh_max_depth, kht_direction, kh_distance){
    gcp.cutkeyholegcdxf(kh_tool_num, kh_start_depth, kh_max_depth, kht_direction, kh_distance);
}

module stockandtoolpaths(){
    gcp.stockandtoolpaths();
}

module stockwotoolpaths(){
    gcp.stockandtoolpaths("stock");
}

module outputtoolpaths(){
    gcp.stockandtoolpaths("toolpaths");
}

module outputrapids(){
    gcp.stockandtoolpaths("rapids");
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

