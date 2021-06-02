# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================

import sys
sys.argv.append("--implicit")

from solid import *

#these are the Implicit examples from https://www.implicitcad.org/examples

scene = \
        \
linear_extrude (height = 30, twist = 180, r=2) (
  union (r=2) (
    square(x=[-2,2], y=[-10,10], r=2),
    square(x=[-10,10], y=[-2,2], r=2),
  ))

# this (twist(h)) is unfortunately not working...... and I do not have an idea
# how to make it work at the moment
#
#linear_extrude (height = 40, twist(h) = 90*cos(h*2*pi/40))
scene += \
         \
linear_extrude (height = 40, twist = scad_inline("90*cos(40*2*pi/40)")) (
  difference () (
    shell(2) (circle (10)),
    square(x=[0,20], y=[-4,4]),
  )).left(30)

scene += \
         \
union() (
  cylinder(r=19, h=10, _fn=6, center=True),
  cylinder(r=10, h=40),
  rotate_extrude(4*360, translate=[0,38]) (
    translate ([10,0])( square([8,4], center=True))),
).right(30)


scene.save_as_scad()

