from solid2.core.object_base import OpenSCADObject as _OpenSCADObject,                                    OpenSCADConstant as _OpenSCADConstant
from solid2.core.scad_import import extra_scad_include as _extra_scad_include
from pathlib import Path as _Path
from .bosl2_mixin import Bosl2Mixin as _Bosl2Mixin

_extra_scad_include(f"{_Path(__file__).parent.parent / '../libs/BOSL2/linear_bearings.scad'}", use_not_include=False)

class get_lmXuu_bearing_diam(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, size=None, **kwargs):
       super().__init__("get_lmXuu_bearing_diam", {"size" : size, **kwargs})

class get_lmXuu_bearing_length(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, size=None, **kwargs):
       super().__init__("get_lmXuu_bearing_length", {"size" : size, **kwargs})

class linear_bearing_housing(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, d=None, l=None, tab=None, gap=None, wall=None, tabwall=None, screwsize=None, anchor=None, spin=None, orient=None, **kwargs):
       super().__init__("linear_bearing_housing", {"d" : d, "l" : l, "tab" : tab, "gap" : gap, "wall" : wall, "tabwall" : tabwall, "screwsize" : screwsize, "anchor" : anchor, "spin" : spin, "orient" : orient, **kwargs})

class lmXuu_housing(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, size=None, tab=None, gap=None, wall=None, tabwall=None, screwsize=None, anchor=None, spin=None, orient=None, **kwargs):
       super().__init__("lmXuu_housing", {"size" : size, "tab" : tab, "gap" : gap, "wall" : wall, "tabwall" : tabwall, "screwsize" : screwsize, "anchor" : anchor, "spin" : spin, "orient" : orient, **kwargs})

