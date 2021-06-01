# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================
from math import sqrt,sin

from solid.extensions.bosl2.std import path_extrude, bounding_box, heightfield,\
                                       cube, sphere, circle, xcyl,\
                                       diff, attach,\
                                       CENTER, TOP

from solid.extensions.bosl2.metric_screws import metric_bolt

#basic stuff
def bolt():
    from solid.extensions.bosl2.metric_screws import metric_bolt
    return metric_bolt(size=20, headtype='hex', l=40)

def bounding_box_wrapper(obj):
    return ~bounding_box()(obj)

def extrude_along_path():
    path = [ [0, 0, 0], [33, 33, 33], [66, 33, 40], [100, 0, 0], [150,0,0] ]
    return path_extrude(path)(circle(r=10, _fn=6))

def heightfield_test():
    def get_data():
        data = []
        for y in range(50):
            yrow = []
            data.append(yrow)
            for x in range(50):
                yrow.append(sin(sqrt((y-25)**2+(x-25)**2)))

        return data

    return heightfield(size=[100,100], bottom=-1, data=get_data())

#a little bit more complicated stuff
def bosl2_diff1():
    #let's try this:
    #diff("neg", "pos", keep="axle")
    #    sphere(d=100, $tags="pos") {
    #        attach(CENTER) xcyl(d=40, l=120, $tags="axle");
    #        attach(CENTER) cube([40,120,100], anchor=CENTER, $tags="neg");
    #    }
    return \
    diff("neg", "pos", keep="axle") (
            sphere(d=100, _tags="pos") (
                attach(CENTER) (xcyl(d=39, l=120, _tags="axle")),
                attach(CENTER) (cube([40, 120, 100], anchor=CENTER, _tags="neg"))
            )
    )

def bosl2_diff():
    #let's try this again in a pythonic manner:
    #diff("neg", "pos", keep="axle")
    #    sphere(d=100, $tags="pos") {
    #        attach(CENTER) xcyl(d=40, l=120, $tags="axle");
    #        attach(CENTER) cube([40,120,100], anchor=CENTER, $tags="neg");
    #    }

    axle = xcyl(d=39, l=120, _tags="axle")
    neg = cube([40, 120, 100], anchor=CENTER, _tags="neg")

    s = sphere(d=100, _tags="pos")

    s.add(attach(CENTER)(axle))
    s.add(attach(CENTER)(neg))

    return diff("neg", "pos", keep="axle")(s)

assembly = bounding_box_wrapper(bosl2_diff().back(100)) +\
           extrude_along_path().color("purple") +\
           bosl2_diff().back(100) +\
           bolt().left(100) +\
           heightfield_test().fwd(100)

assembly.save_as_scad()

