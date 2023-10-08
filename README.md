# gcodepreview
OpenSCAD library for moving a tool in lines and arcs so as to model how a part would be cut using G-Code, so as to allow OpenSCAD to function as a compleat CAD/CAM solution for subtractive CNC (mills and routers).

Updated to make use of Python in OpenSCAD:

http://www.guenther-sohler.net/openscad/

(previous versions had used RapCAD)

A BlockSCAD file for the main modules is available at:

https://www.blockscad3d.com/community/projects/1244473

The project is discussed at:

https://forum.makerforums.info/t/g-code-preview-using-openscad-rapcad/85729 

and

https://forum.makerforums.info/t/openscad-and-python-looking-to-finally-be-resolved/88171

and

https://willadams.gitbook.io/design-into-3d/programming

Usage is:

Place the file in C:\Users\\\~\Documents\OpenSCAD\libraries (C:\Users\\\~\Documents\RapCAD\libraries is deprecated since RapCAD is not longer needed since Python is now used for writing out files)

(While it was updated for use w/ RapCAD, so as to take advantage of the writeln command, it was possible to write that in Python)

    use <gcodepreview.py>;
    use <pygcodepreview.scad>;
    include <gcodepreview.scad>;

Note that it is necessary to use the first two files (this allows loading the Python commands and then wrapping them in OpenSCAD commands) and then include the last file (which allows using OpenSCAD variables to selectively implement the Python commands via their being wrapped in OpenSCAD modules)

and define variables which match the project and then use commands such as:

    opengcodefile(Gcode_filename);
    opendxffile(DXF_filename);
    
    difference() {
        setupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin);
    
    movetosafez();
    
    toolchange(squaretoolno,speed * square_ratio);
    
    begintoolpath(0,0,0.25);
    beginpolyline(0,0,0.25);

    cutoneaxis_setfeed("Z",-1,plunge*square_ratio);
    addpolyline(stocklength/2,stockwidth/2,-stockthickness);
    
    cutwithfeed(stocklength/2,stockwidth/2,-stockthickness,feed);
    
    endtoolpath();
    
    }
    
    closegcodefile();
    closedxffile();

Tool numbers match those of tooling sold by Carbide 3D (ob. discl., I work for them). Comments are included in the G-code to match those expected by CutViewer.

A complete example file is: gcodepreview_template.scad

Version 0.1 supports setting up stock, origin, rapdi positioning, making cuts, and writing out matching G-code, and creating a DXF with polylines.

Possible future improvements:

 - G-code: support for G2/G3 arcs
 - DXF support for curves and the 3rd dimension
 - G-code: import external tool libraries and feeds and speeds from JSON or CSV files
 - support for additional tooling shapes such as dovetail tools, or roundover tooling
 - general coding improvements --- current coding style is quite prosaic
 - documentation beyond: https://willadams.gitbook.io/design-into-3d/programming
 - possibly re-writing as a literate program
 - generalized modules for cutting out various shapes/geometries
