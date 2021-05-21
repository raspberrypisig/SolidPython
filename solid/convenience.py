from ..objects import *

def down(self, x):
    return translate([0, 0, -x])(self)

def up(self, x):
    return translate([0, 0, x])(self)

def left(self, x):
    return translate([-x, 0, 0])(self)

def right(self, x):
    return translate([x, 0, 0])(self)

def back(self, x):
    return translate([0, x, 0])(self)

def forward(self, x):
    return translate([0, -x, 0])(self)

OpenSCADObject.down = down
OpenSCADObject.up = up
OpenSCADObject.left = left
OpenSCADObject.right = right
OpenSCADObject.back = back
OpenSCADObject.forward = forward

