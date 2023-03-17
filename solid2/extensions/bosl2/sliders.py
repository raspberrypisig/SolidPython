from ...core.object_base import OpenSCADObject, OpenSCADConstant
from ... import import_scad
from pathlib import Path

importFile = Path(__file__).absolute().parent.parent.parent / 'libs' / 'BOSL2' / 'sliders.scad'
_ = import_scad(f'{importFile}', use_not_include=False)


class slider(OpenSCADObject):
    def __init__(self, l=None, w=None, h=None, base=None, wall=None, ang=None, anchor=None, spin=None, orient=None, **kwargs):
       super().__init__("slider" ,{"l" : l, "w" : w, "h" : h, "base" : base, "wall" : wall, "ang" : ang, "anchor" : anchor, "spin" : spin, "orient" : orient, **kwargs})

class rail(OpenSCADObject):
    def __init__(self, l=None, w=None, h=None, chamfer=None, ang=None, anchor=None, spin=None, orient=None, **kwargs):
       super().__init__("rail" ,{"l" : l, "w" : w, "h" : h, "chamfer" : chamfer, "ang" : ang, "anchor" : anchor, "spin" : spin, "orient" : orient, **kwargs})

class slider(OpenSCADObject):
    def __init__(self, l=None, w=None, h=None, base=None, wall=None, ang=None, anchor=None, spin=None, orient=None, **kwargs):
       super().__init__("slider" ,{"l" : l, "w" : w, "h" : h, "base" : base, "wall" : wall, "ang" : ang, "anchor" : anchor, "spin" : spin, "orient" : orient, **kwargs})

class rail(OpenSCADObject):
    def __init__(self, l=None, w=None, h=None, chamfer=None, ang=None, anchor=None, spin=None, orient=None, **kwargs):
       super().__init__("rail" ,{"l" : l, "w" : w, "h" : h, "chamfer" : chamfer, "ang" : ang, "anchor" : anchor, "spin" : spin, "orient" : orient, **kwargs})

