 //!OpenSCAD

 module arcloop(barc,earc, xcenter, ycenter, radius) {
   for (i = [barc : abs(1) : earc]) {
         cut(xcenter + radius * cos(i),
         ycenter + radius * sin(i),
         getzpos()-(gettzpos())
         );
     setxpos(xcenter + radius * cos(i));
     setypos(ycenter + radius * sin(i));
   }
 }

 module narcloop(barc,earc, xcenter, ycenter, radius) {
   for (i = [barc : -1 : earc]) {
         cut(xcenter + radius * cos(i),
         ycenter + radius * sin(i),
         getzpos()-(gettzpos())
         );
     setxpos(xcenter + radius * cos(i));
     setypos(ycenter + radius * sin(i));
   }
 }

 module cutarcNECCdxf(tn, ex, ey, ez, xcenter, ycenter, radius) {
   dxfarc(tn,xcenter,ycenter,radius,0,90);
   settzpos((getzpos()-ez)/90);
     arcloop(1,90, xcenter, ycenter, radius);
 }

 module cutarcNWCCdxf(tn, ex, ey, ez, xcenter, ycenter, radius) {
   dxfarc(tn,xcenter,ycenter,radius,90,180);
   settzpos((getzpos()-ez)/90);
     arcloop(91,180, xcenter, ycenter, radius);
 }

 module cutarcSWCCdxf(tn, ex, ey, ez, xcenter, ycenter, radius) {
   dxfarc(tn,xcenter,ycenter,radius,180,270);
   settzpos((getzpos()-ez)/90);
     arcloop(181,270, xcenter, ycenter, radius);
 }

 module cutarcSECCdxf(tn, ex, ey, ez, xcenter, ycenter, radius) {
   dxfarc(tn,xcenter,ycenter,radius,270,360);
   settzpos((getzpos()-ez)/90);
     arcloop(271,360, xcenter, ycenter, radius);
 }

 module cutarcNECWdxf(tn, ex, ey, ez, xcenter, ycenter, radius) {
   dxfarc(tn,xcenter,ycenter,radius,0,90);
   settzpos((getzpos()-ez)/90);
     narcloop(89,0, xcenter, ycenter, radius);
 }

 module cutarcSECWdxf(tn, ex, ey, ez, xcenter, ycenter, radius) {
   dxfarc(tn,xcenter,ycenter,radius,270,360);
   settzpos((getzpos()-ez)/90);
     narcloop(359,270, xcenter, ycenter, radius);
 }

 module cutarcSWCWdxf(tn, ex, ey, ez, xcenter, ycenter, radius) {
   dxfarc(tn,xcenter,ycenter,radius,180,270);
   settzpos((getzpos()-ez)/90);
     narcloop(269,180, xcenter, ycenter, radius);
 }

 module cutarcNWCWdxf(tn, ex, ey, ez, xcenter, ycenter, radius) {
   dxfarc(tn,xcenter,ycenter,radius,90,180);
   settzpos((getzpos()-ez)/90);
     narcloop(179,90, xcenter, ycenter, radius);
 }

 module keyhole_toolpath(kh_tool_no, kh_start_depth, kh_max_depth, kht_angle, kh_length) {
 if (kht_angle == "N") {
   keyhole_toolpath_degrees(kh_tool_no, kh_start_depth, kh_max_depth, 90, kh_length);
     } else if (kht_angle == "S") {
   keyhole_toolpath_degrees(kh_tool_no, kh_start_depth, kh_max_depth, 270, kh_length);
     } else if (kht_angle == "E") {
   keyhole_toolpath_degrees(kh_tool_no, kh_start_depth, kh_max_depth, 0, kh_length);
     } else if (kht_angle == "W") {
   keyhole_toolpath_degrees(kh_tool_no, kh_start_depth, kh_max_depth, 180, kh_length);
     }
 }
 module keyhole_toolpath_degrees(kh_tool_no, kh_start_depth, kh_max_depth, kh_angle, kh_length) {
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,0,90);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,90,180);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,180,270);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,270,360);
   if (kh_angle == 0) {
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180,270);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90,180);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),90);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270,360-asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)));
 dxfarc(KH_tool_no,getxpos()+kh_length,getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,0,90);
 dxfarc(KH_tool_no,getxpos()+kh_length,getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,270,360);
 dxfpolyline(KH_tool_no,
  getxpos()+sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),
  getypos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,
  getxpos()+kh_length,
  getypos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2);
 dxfpolyline(KH_tool_no,
  getxpos()+sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),
  getypos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,
  getxpos()+kh_length,
  getypos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2);
 dxfpolyline(KH_tool_no,getxpos(),getypos(),getxpos()+kh_length,getypos());
  cutwithfeed(getxpos()+kh_length,getypos(),-kh_max_depth,feed);
  setxpos(getxpos()-kh_length);
   } else if (kh_angle > 0 && kh_angle < 90) {
 echo(kh_angle);
   dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90+kh_angle,180+kh_angle);
   dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180+kh_angle,270+kh_angle);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,kh_angle+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),90+kh_angle);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270+kh_angle,360+kh_angle-asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)));
 dxfarc(KH_tool_no,
   getxpos()+(kh_length*cos(kh_angle)),
   getypos()+(kh_length*sin(kh_angle)),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,0+kh_angle,90+kh_angle);
 dxfarc(KH_tool_no,getxpos()+(kh_length*cos(kh_angle)),getypos()+(kh_length*sin(kh_angle)),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,270+kh_angle,360+kh_angle);
 dxfpolyline(KH_tool_no,
  getxpos()+tool_diameter(KH_tool_no, (kh_max_depth))/2*cos(kh_angle+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2))),
  getypos()+tool_diameter(KH_tool_no, (kh_max_depth))/2*sin(kh_angle+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2))),
  getxpos()+(kh_length*cos(kh_angle))-((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)*sin(kh_angle)),
  getypos()+(kh_length*sin(kh_angle))+((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)*cos(kh_angle)));
 echo("a",tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2);
 echo("c",tool_diameter(KH_tool_no, (kh_max_depth))/2);
 echo("Aangle",asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)));
 echo(kh_angle);
  cutwithfeed(getxpos()+(kh_length*cos(kh_angle)),getypos()+(kh_length*sin(kh_angle)),-kh_max_depth,feed);
  setxpos(getxpos()-(kh_length*cos(kh_angle)));
  setypos(getypos()-(kh_length*sin(kh_angle)));
   } else if (kh_angle == 90) {
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180,270);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270,360);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,0,90-asin(
     (tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)));
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90+asin(
     (tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),180);
  dxfpolyline(KH_tool_no,getxpos(),getypos(),getxpos(),getypos()+kh_length);
 dxfarc(KH_tool_no,getxpos(),getypos()+kh_length,tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,0,90);
 dxfarc(KH_tool_no,getxpos(),getypos()+kh_length,tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,90,180);
  dxfpolyline(KH_tool_no,getxpos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()+sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),getxpos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()+kh_length);
  dxfpolyline(KH_tool_no,getxpos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()+sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),getxpos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()+kh_length);
  cutwithfeed(getxpos(),getypos()+kh_length,-kh_max_depth,feed);
  setypos(getypos()-kh_length);
   } else if (kh_angle == 180) {
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,0,90);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270,360);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90,180-asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)));
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),270);
 dxfarc(KH_tool_no,getxpos()-kh_length,getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,90,180);
 dxfarc(KH_tool_no,getxpos()-kh_length,getypos(),tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,180,270);
 dxfpolyline(KH_tool_no,
  getxpos()-sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),
  getypos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,
  getxpos()-kh_length,
  getypos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2);
 dxfpolyline(KH_tool_no,
  getxpos()-sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),
  getypos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,
  getxpos()-kh_length,
  getypos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2);
  dxfpolyline(KH_tool_no,getxpos(),getypos(),getxpos()-kh_length,getypos());
  cutwithfeed(getxpos()-kh_length,getypos(),-kh_max_depth,feed);
  setxpos(getxpos()+kh_length);
   } else if (kh_angle == 270) {
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,0,90);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,90,180);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,270+asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)),360);
 dxfarc(KH_tool_no,getxpos(),getypos(),tool_diameter(KH_tool_no, (kh_max_depth))/2,180, 270-asin((tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_no, (kh_max_depth))/2)));
 dxfarc(KH_tool_no,getxpos(),getypos()-kh_length,tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,180,270);
 dxfarc(KH_tool_no,getxpos(),getypos()-kh_length,tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,270,360);
  dxfpolyline(KH_tool_no,getxpos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()-sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),getxpos()+tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()-kh_length);
  dxfpolyline(KH_tool_no,getxpos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()-sqrt((tool_diameter(KH_tool_no, (kh_max_depth))/2)^2-(tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2)^2),getxpos()-tool_diameter(KH_tool_no, (kh_max_depth+4.36))/2,getypos()-kh_length);
  dxfpolyline(KH_tool_no,getxpos(),getypos(),getxpos(),getypos()-kh_length);
  cutwithfeed(getxpos(),getypos()-kh_length,-kh_max_depth,feed);
  setypos(getypos()+kh_length);
   }
 }

