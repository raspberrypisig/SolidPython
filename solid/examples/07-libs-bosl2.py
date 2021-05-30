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
# If the BOSL2 docs say you have to include certain files you unfortunately
# have to explicitly include the files in the same order as mentioned.
# Furthermore you have to include (and not use) them.

from types import SimpleNamespace

def basic_bosl2_usage():
    bosl2 = SimpleNamespace()

    #explicitly include std.scad (first!) and set the include flag
    bosl2.std = import_scad("BOSL2/std.scad", use_not_include=False)
    #explicitly include std.metrics_screws and set the include flag
    bosl2.metric_screws = import_scad("BOSL2/metric_screws.scad", use_not_include=False)

    #use it to generate a metric screw
    screw = bosl2.metric_screws.metric_bolt(size=6, headtype='hex', l=20)

    return screw

def bosl2_attachments_full_namespace():
    #let's try this:
    #   include <BOSL2/std.scad>
    #   spheroid(d=20) {
    #       attach(TOP) down(1.5) cyl(l=11.5, d1=10, d2=5, anchor=BOTTOM);
    #       attach(RIGHT, BOTTOM) down(1.5) cyl(l=11.5, d1=10, d2=5);
    #       attach(FRONT, BOTTOM, overlap=1.5) cyl(l=11.5, d1=10, d2=5);
    #   }

    bosl2 = SimpleNamespace()
    bosl2.std = import_scad("BOSL2/std.scad", use_not_include=False)
    bosl2.constants = import_scad("BOSL2/constants.scad", use_not_include=False)
    bosl2.shapes = import_scad("BOSL2/shapes.scad", use_not_include=False)
    bosl2.attachments = import_scad("BOSL2/attachments.scad", use_not_include=False)

    bosl2.shapes.spheroid(d=20)(
        bosl2.attachments.attach(bosl2.constants.TOP)(
            down(1.5)(
                     bosl2.shapes.cyl(l=11.5, d1=10, d2=5, anchor = bosl2.constants.BOTTOM)
                )
            ),
        bosl2.attachments.attach(bosl2.constants.RIGHT, bosl2.constants.BOTTOM)(
            down(1.5)(
                     bosl2.shapes.cyl(l=11.5, d1=10, d2=5, anchor = bosl2.constants.BOTTOM)
                )
            )
        ).save_as_scad()

#works great, but no one can read it let's try it again wth global includes

include("BOSL2/std.scad")
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
    mutators = import_scad("BOSL2/mutators.scad")
    return ~mutators.bounding_box()(obj)

boslshit = bosl2_attachments_include() & sphere(20).left(5)
bbox = bosl2_bounding_box(boslshit)

assembly = boslshit + bbox + basic_bosl2_usage().left(30)
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
