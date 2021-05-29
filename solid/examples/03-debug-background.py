# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#======================================================

from solid import *

c = cube([10, 20, 30])

#the OpenSCAD syntax style use of debug
s = debug()(
        sphere(10)
    )

d = c - s

bg = background()(
        cylinder(r=4, h=30)
     )

(d + bg).save_as_scad()

#disable (*) and root (!) are accessible corresponding to debug and background
#NOTE: the __invert__ operator is mapped to debug:
#
#            debug()(cube(1))
#
#       can be expressed as:
#
#             ~cube(1)
#
#this file generates the following scad code:
#
#    union() {
#            difference() {
#                    cube(size = [10, 20, 30]);
#                    #sphere(r = 10);
#            };
#            %cylinder(h = 30, r = 4);
#    };

