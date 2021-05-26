from ..builtins import translate
from ..object_base import OpenSCADObject

#==================
# = m(ove)x, y, z =
#==================
def mx(x):
    return translate([x, 0, 0])

def my(y):
    return translate([0, y, 0])

def mz(z):
    return translate([0, 0, z])

OpenSCADObject.mx = lambda self, x: mx(x)(self)
OpenSCADObject.my = lambda self, y: my(y)(self)
OpenSCADObject.mz = lambda self, z: mz(z)(self)

# ==============
# = Directions =
# ==============
def up(z:float) -> OpenSCADObject:
    return translate((0, 0, z))

def down(z: float) -> OpenSCADObject:
    return translate((0, 0, -z))

def right(x: float) -> OpenSCADObject:
    return translate((x, 0, 0))

def left(x: float) -> OpenSCADObject:
    return translate((-x, 0, 0))

def forward(y: float) -> OpenSCADObject:
    return translate((0, y, 0))

def back(y: float) -> OpenSCADObject:
    return translate((0, -y, 0))

OpenSCADObject.down = lambda self, x: down(x)(self)
OpenSCADObject.up = lambda self, x: up(x)(self)
OpenSCADObject.left = lambda self, x: left(x)(self)
OpenSCADObject.right = lambda self, x: right(x)(self)
OpenSCADObject.back = lambda self, x: back(x)(self)
OpenSCADObject.forward = lambda self, x: forward(x)(self)

# ================================
# = Modifier Convenience Methods =
# ================================
def debug(openscad_obj: OpenSCADObject) -> OpenSCADObject:
    return openscad_obj.debug()

def background(openscad_obj: OpenSCADObject) -> OpenSCADObject:
    return openscad_obj.background()

def root(openscad_obj: OpenSCADObject) -> OpenSCADObject:
    return openscad_obj.root()

def disable(openscad_obj: OpenSCADObject) -> OpenSCADObject:
    return openscad_obj.disable()

