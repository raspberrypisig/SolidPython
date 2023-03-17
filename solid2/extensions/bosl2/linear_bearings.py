from ...core.object_base import OpenSCADObject, OpenSCADConstant
from ... import import_scad
from pathlib import Path

importFile = Path(__file__).absolute().parent.parent.parent / 'libs' / 'BOSL2' / 'linear_bearings.scad'
_ = import_scad(f'{importFile}', use_not_include=False)


class linear_bearing_housing(OpenSCADObject):
    def __init__(self, d=None, l=None, tab=None, gap=None, wall=None, tabwall=None, screwsize=None, anchor=None, spin=None, orient=None, **kwargs):
       super().__init__("linear_bearing_housing" ,{"d" : d, "l" : l, "tab" : tab, "gap" : gap, "wall" : wall, "tabwall" : tabwall, "screwsize" : screwsize, "anchor" : anchor, "spin" : spin, "orient" : orient, **kwargs})

class lmXuu_housing(OpenSCADObject):
    def __init__(self, size=None, tab=None, gap=None, wall=None, tabwall=None, screwsize=None, anchor=None, spin=None, orient=None, **kwargs):
       super().__init__("lmXuu_housing" ,{"size" : size, "tab" : tab, "gap" : gap, "wall" : wall, "tabwall" : tabwall, "screwsize" : screwsize, "anchor" : anchor, "spin" : spin, "orient" : orient, **kwargs})

class get_lmXuu_bearing_diam(OpenSCADObject):
    def __init__(self, size=None, **kwargs):
       super().__init__("get_lmXuu_bearing_diam" ,{"size" : size, **kwargs})

class get_lmXuu_bearing_length(OpenSCADObject):
    def __init__(self, size=None, **kwargs):
       super().__init__("get_lmXuu_bearing_length" ,{"size" : size, **kwargs})

