# gcodepreview

OpenPythonSCAD library for moving a tool in lines and arcs so as to model how a part would be cut using G-Code, so as to allow OpenPythonSCAD to function as a compleat CAD/CAM solution for subtractive 3-axis CNC (mills and routers) by writing out G-code in addition to 3D modeling (in some cases toolpaths which would not normally be feasible), and to write out DXF files which may be imported into a traditional CAM program to create toolpaths.

![OpenSCAD Cut Joinery Module](https://raw.githubusercontent.com/WillAdams/gcodepreview/main/gcodepreview_unittests.png?raw=true)

Updated to make use of Python in OpenSCAD:[^rapcad]

[^rapcad]: Previous versions had used RapCAD, so as to take advantage of the writeln command, which has since been re-written in Python.

https://pythonscad.org/ (previously this was http://www.guenther-sohler.net/openscad/ )

A BlockSCAD file for the initial version of the 
main modules is available at:

https://www.blockscad3d.com/community/projects/1244473

The project is discussed at:

https://forum.makerforums.info/t/g-code-preview-using-openscad-rapcad/85729 

and

https://forum.makerforums.info/t/openscad-and-python-looking-to-finally-be-resolved/88171

and

https://willadams.gitbook.io/design-into-3d/programming

Since it is now programmed using Literate Programming (initially a .dtx, now a .tex file) there is a PDF: https://github.com/WillAdams/gcodepreview/blob/main/gcodepreview.pdf which includes all of the source code with formatted commentary.

The files for this library are:

 - gcodepreview.py (gcpy) --- the Python functions and variables
 - pygcodepreview.scad (pyscad) --- the Python functions wrapped in OpenSCAD
 - gcodepreview.scad (gcpscad) --- OpenSCAD modules and variables
 - gcodepreview_template.scad (gcptmpl) --- example file
 - cut2Dshapes.scad (cut2D) --- code for cutting 2D shapes 

If using from OpenPythonSCAD, place the files in C:\Users\\\~\Documents\OpenSCAD\libraries and call as:[^libraries]

[^libraries]: C:\Users\\\~\Documents\RapCAD\libraries is deprecated since RapCAD is no longer needed since Python is now used for writing out files)

    use <gcodepreview.py>;
    use <pygcodepreview.scad>;
    include <gcodepreview.scad>;

Note that it is necessary to use the first two files (this allows loading the Python commands and then wrapping them in OpenSCAD commands) and then include the last file (which allows using OpenSCAD variables to selectively implement the Python commands via their being wrapped in OpenSCAD modules) and define variables which match the project and then use commands such as:

    opengcodefile(Gcode_filename);
    opendxffile(DXF_filename);
    
    difference() {
        setupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero);
    
    movetosafez();
    
    toolchange(squaretoolnum,speed * square_ratio);
    
    begintoolpath(0,0,0.25);
    beginpolyline(0,0,0.25);

    cutoneaxis_setfeed("Z",-1,plunge*square_ratio);
    addpolyline(stockXwidth/2,stockYheight/2,-stockZthickness);
    
    cutwithfeed(stockXwidth/2,stockYheight/2,-stockZthickness,feed);
    
    endtoolpath();
    endpolyline();
    
    }
    
    closegcodefile();
    closedxffile();

which makes a G-code file:

![OpenSCAD template G-code file](https://raw.githubusercontent.com/WillAdams/gcodepreview/main/gcodepreview_template.png?raw=true)

but one which could only be sent to a machine so as to cut only the softest and most yielding of materials since it makes a single full-depth pass, and of which has a matching DXF which may be imported into a CAM tool --- but which it is not directly possible to assign a toolpath in readily available CAM tools (since it varies in depth from beginning-to-end). 

Importing this DXF and actually cutting it is discussed at:

https://forum.makerforums.info/t/rewriting-gcodepreview-with-python/88617/14

Alternately, gcodepreview.py may be placed in a Python library location and used directly from Python --- note that it is possible to use it from a "normal" Python when generating only DXFs.

Tool numbers match those of tooling sold by Carbide 3D (ob. discl., I work for them). 

Comments are included in the G-code to match those expected by CutViewer.

A complete example file is: gcodepreview_template.scad Note that a Python template has since been developed as well, allowing usage without OpenSCAD code, and another example is openscad_gcodepreview_cutjoinery.tres.scad which is made from an OpenSCAD Graph Editor file:

![OpenSCAD Graph Editor Cut Joinery File](https://raw.githubusercontent.com/WillAdams/gcodepreview/main/OSGE_cutjoinery.png?raw=true)

Version 0.1 supports setting up stock, origin, rapid positioning, making cuts, and writing out matching G-code, and creating a DXF with polylines.

Added features since initial upload:

 - endpolyline(); --- this command allows ending one polyline so as to allow multiple lines in a DXF
 - separate dxf files are written out for each tool where tool is ball/square/V and small/large (10/31/23)
 - re-writing as a Literate Program using the LaTeX package docmfp (begun 4/12/24) 
 - support for additional tooling shapes such as dovetail and keyhole tools

Version 0.2 adds support for arcs 

 - DXF: support for arcs (which may be used to make circles) (6/1/24)
 - Specialty toolpaths such as Keyhole which may be used for dovetail as well as keyhole cutters

Version 0.3 

 - Support for curves along the 3rd dimension
 - support for roundover tooling
 
Version 0.4

 - Rewrite using literati documentclass, suppression of SVG code
 - dxfrectangle (without G-code support)

Version 0.5

 - more shapes
 - consolidate rectangles, arcs, and circles in gcodepreview.scad
 
Version 0.6

 - notes on modules
 - change file for setupstock

Version 0.61

 - validate all code so that it runs without errors from sample file
 - NEW: Note that this version is archived as gcodepreview-openscad_0_6.tex and the matching PDF is available as well
 
 Version 0.7
 
  - re-write completely in Python --- note that it is possible to use from within OpenPythonSCAD and an OpenSCAD wrapper is not functional at this time --- note that the OpenSCAD wrapper will need to be rewritten

Possible future improvements:

 - rewrite OpenSCAD wrapper
 - restore support for additional tooling shapes (dovetail, roundover)
 - support for additional tooling shapes such as tapered ball-nose tools or lollipop cutters or thread-cutting tools

Note for G-code generation that it is up to the user to implement Depth per Pass so as to not take a single full-depth pass. Working from a DXF of course allows one to off-load such considerations to a specialized CAM tool.

Deprecated feature:

 - exporting SVGs --- while this was begun, it turns out that these would be written out upside down due to coordinate system differences between OpenSCAD/DXFs and SVGs requiring managing the inversion of the coordinate system (it is possible that METAPOST, which shares the same orientation and which can write out SVGs will be used instead for future versions)
 