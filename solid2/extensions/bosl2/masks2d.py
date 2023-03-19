from solid2.core.object_base import OpenSCADObject as _OpenSCADObject,                                    OpenSCADConstant as _OpenSCADConstant
from solid2.core.scad_import import extra_scad_include as _extra_scad_include
from pathlib import Path as _Path
from .bosl2_mixin import Bosl2Mixin as _Bosl2Mixin

_extra_scad_include(f"{_Path(__file__).parent.parent / '../libs/BOSL2/masks2d.scad'}", use_not_include=False)

class mask2d_roundover(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, r=None, inset=None, excess=None, d=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_roundover", {"r" : r, "inset" : inset, "excess" : excess, "d" : d, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_cove(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, r=None, inset=None, excess=None, d=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_cove", {"r" : r, "inset" : inset, "excess" : excess, "d" : d, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_chamfer(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, edge=None, angle=None, inset=None, excess=None, x=None, y=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_chamfer", {"edge" : edge, "angle" : angle, "inset" : inset, "excess" : excess, "x" : x, "y" : y, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_rabbet(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, size=None, excess=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_rabbet", {"size" : size, "excess" : excess, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_dovetail(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, edge=None, angle=None, inset=None, shelf=None, excess=None, x=None, y=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_dovetail", {"edge" : edge, "angle" : angle, "inset" : inset, "shelf" : shelf, "excess" : excess, "x" : x, "y" : y, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_teardrop(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, r=None, angle=None, excess=None, d=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_teardrop", {"r" : r, "angle" : angle, "excess" : excess, "d" : d, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_ogee(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, pattern=None, excess=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_ogee", {"pattern" : pattern, "excess" : excess, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_roundover(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, r=None, inset=None, excess=None, d=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_roundover", {"r" : r, "inset" : inset, "excess" : excess, "d" : d, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_cove(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, r=None, inset=None, excess=None, d=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_cove", {"r" : r, "inset" : inset, "excess" : excess, "d" : d, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_chamfer(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, edge=None, angle=None, inset=None, excess=None, x=None, y=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_chamfer", {"edge" : edge, "angle" : angle, "inset" : inset, "excess" : excess, "x" : x, "y" : y, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_rabbet(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, size=None, excess=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_rabbet", {"size" : size, "excess" : excess, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_dovetail(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, edge=None, angle=None, inset=None, shelf=None, excess=None, x=None, y=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_dovetail", {"edge" : edge, "angle" : angle, "inset" : inset, "shelf" : shelf, "excess" : excess, "x" : x, "y" : y, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_teardrop(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, r=None, angle=None, excess=None, d=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_teardrop", {"r" : r, "angle" : angle, "excess" : excess, "d" : d, "anchor" : anchor, "spin" : spin, **kwargs})

class mask2d_ogee(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, pattern=None, excess=None, anchor=None, spin=None, **kwargs):
       super().__init__("mask2d_ogee", {"pattern" : pattern, "excess" : excess, "anchor" : anchor, "spin" : spin, **kwargs})

