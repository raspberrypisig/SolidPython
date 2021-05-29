# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================

from solid import *

# you can use OpenSCAD libraries in SolidPython. This examples needs the bosl
# library to be installed in the OpenSCAD library path
# (~.local/share/OpenSCAD/libraries)
#
# NOTE: you can import any *.scad file not only "libraries"

#import bosl.metric_screw and wrap it in a simple namespace
from types import SimpleNamespace
bosl = SimpleNamespace()
bosl.metric_screws = import_scad("BOSL/metric_screws.scad")

#use it to generate a metric screw
screw = bosl.metric_screws.metric_bolt(size=6, headtype='hex', l=20)

screw.save_as_scad()

#NOTE: BOSL2 is not working properly at the moment because it uses
#      OpenSCAD features extensively that are not supported by the ExpSolid
#      import mechanism at the moment.
#      -> global variables
#      -> you need multiple includes for a single module
#
#           include <BOSL2/std.scad> //has to be included to be able to use
#           include <BOSL2/linear_bearings.scad>
#
#           To make this work the include mechanism needs to be refactored to
#           simply include everything that was ever included and not just the
#           "include_strings" attached to certain OpenSCADObjects.
#
#      -> recursiv use and include
#           if bla.scad uses / includes blub.scad, the globals from blub.scad
#           should be available if you import bla.scad
