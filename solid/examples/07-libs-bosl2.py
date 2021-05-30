# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================

from solid import *

# BOSL2 is a little bit tricky to import but we get there step by step.
#
# There's a little extension to make it more straight forward to work with bosl2
# It's work in progress, it's just a first sketch yet

from types import SimpleNamespace

def basic_bosl2_usage():
    from solid.extensions.bosl2 import import_bosl2
    metric_screws = import_bosl2("metric_screws")

    return metric_screws.metric_bolt(size=20, headtype='hex', l=40)

def bosl2_attachments_full_namespace():
    #let's try this:
    #   include <BOSL2/std.scad>
    #   spheroid(d=20) {
    #       attach(TOP) down(1.5) cyl(l=11.5, d1=10, d2=5, anchor=BOTTOM);
    #       attach(RIGHT, BOTTOM) down(1.5) cyl(l=11.5, d1=10, d2=5);
    #       attach(FRONT, BOTTOM, overlap=1.5) cyl(l=11.5, d1=10, d2=5);
    #   }

    from solid.extensions.bosl2 import constants, shapes, attachments
    return \
    shapes.spheroid(d=20)(
        attachments.attach(constants.TOP)(
            down(1.5)(
                     shapes.cyl(l=11.5, d1=10, d2=5, anchor = constants.BOTTOM)
                )
            ),
        attachments.attach(constants.RIGHT, constants.BOTTOM)(
            down(1.5)(
                     shapes.cyl(l=11.5, d1=10, d2=5, anchor = constants.BOTTOM)
                )
            )
        )

#works great, but let's try it again wth global includes

include("BOSL2/constants.scad")
include("BOSL2/shapes.scad")
include("BOSL2/attachments.scad")

def bosl2_attachments_include():
    #let's try this again:
    #   include <BOSL2/std.scad>
    #   spheroid(d=20) {
    #       attach(TOP) down(1.5) cyl(l=11.5, d1=10, d2=5, anchor=BOTTOM);
    #       attach(RIGHT, BOTTOM) down(1.5) cyl(l=11.5, d1=10, d2=5);
    #       attach(FRONT, BOTTOM, overlap=1.5) cyl(l=11.5, d1=10, d2=5);
    #   }

    boslshit =  spheroid(d=20)(
                    attach(TOP)( down(1.5)(
                            cyl(l=11.5, d1=10, d2=5, anchor = BOTTOM))),
                    attach(RIGHT, BOTTOM)( down(1.5)(
                            cyl(l=11.5, d1=10, d2=5, anchor = BOTTOM))),
                    attach(FRONT, BOTTOM, overlap=1.5)( down(1.5)(
                            cyl(l=11.5, d1=10, d2=5, anchor = BOTTOM)))
                    )

    #YEAHA, we got it!

    return boslshit

def bosl2_bounding_box(obj):
    from solid.extensions.bosl2 import mutators
    return ~mutators.bounding_box()(obj)

def extrude_along_path():
    from solid.extensions.bosl2 import paths
    path = [ [0, 0, 0], [33, 33, 33], [66, 33, 40], [100, 0, 0], [150,0,0] ]
    return paths.path_extrude(path)(circle(r=10, _fn=6))

def bosl2_diff():
    #diff("neg", "pos", keep="axle")
    #    sphere(d=100, $tags="pos") {
    #        attach(CENTER) xcyl(d=39, l=120, $tags="axle");
    #        attach(CENTER) cube([40,120,100], anchor=CENTER, $tags="neg");
    #    }

    #the other modules are already in the global namespace =(
    from solid.extensions.bosl2 import primitives
    return \
    diff("neg", "pos", keep="axle") (
            primitives.sphere(d=100, _tags="pos") (
                attach(CENTER) (xcyl(d=39, l=120, _tags="axle")),
                attach(CENTER) (primitives.cube([40, 120, 100], anchor=CENTER, _tags="neg"))
            )
    )

boslshit = (bosl2_attachments_full_namespace() & sphere(20).left(5)).scale(3).up(100)
bbox = bosl2_bounding_box(boslshit)

assembly = boslshit +\
           bbox +\
           basic_bosl2_usage().left(30) +\
           extrude_along_path().color("purple") +\
           bosl2_diff().back(100)

assembly.save_as_scad()

#BOSL2 TODO:
#       ExpSolid does not follow includes inside imported OpenSCAD modules.
#       That's the reason why we have to import each module by hand.....
#       We still need to explicitly import std.scad and constants.scad because
#       They contain a lot of global constants that are used by all the other
#       modules and we need to put the include into the scad file that's the
#       reason why we have to include them even though we don't gain anything
#       from it on python side.
#
#      -> recursiv use and include
#           if bla.scad uses / includes blub.scad, the globals from blub.scad
#           should be available if you import bla.scad
#
