//!OpenSCAD

module gcp_cut_radius(bx, by, bz, ex, ey, ez, es_diameter, es_radius_tip, es_radius_width) {
n = Detail;
step = 360/n;
endmillradius = es_diameter / 2;

hull(){
translate([bx,by,bz])
cylinder(step,es_radius_tip,es_radius_tip);
translate([ex,ey,ez])
cylinder(step,es_radius_tip,es_radius_tip);
}

hull(){
translate([bx,by,bz+es_radius_width])
cylinder(es_radius_width*2,es_radius_tip+es_radius_width,es_radius_tip+es_radius_width);
    
translate([ex,ey,ez+es_radius_width])
cylinder(es_radius_width*2,es_radius_tip+es_radius_width,es_radius_tip+es_radius_width);
}

for (i=[0:step:90]) {
    angle = i;
    dx = es_radius_width*cos(angle);
    dxx = es_radius_width*cos(angle+step);
    dzz = es_radius_width*sin(angle);
    dz = es_radius_width*sin(angle+step);
    dh = dz-dzz;
    hull(){
    translate([bx,by,bz+dz])
       cylinder(dh,es_radius_tip+es_radius_width-dx,es_radius_tip+es_radius_width-dxx);
    translate([ex,ey,ez+dz])
       cylinder(dh,es_radius_tip+es_radius_width-dx,es_radius_tip+es_radius_width-dxx);
        }
}
}

//gcp_cut_radius(0, 0, 0, 20, 20, 0, 6.35, 0.79375, 3.175);
//gcp_endmill_square(6.35, 19.05);
//gcp_endmill_ball(6.35, 19.05);
//gcp_endmill_v(90, 19.05);