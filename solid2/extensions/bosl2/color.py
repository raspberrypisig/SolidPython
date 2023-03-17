from ...core.object_base import OpenSCADObject, OpenSCADConstant
from ... import import_scad
from pathlib import Path

importFile = Path(__file__).absolute().parent.parent.parent / 'libs' / 'BOSL2' / 'color.scad'
_ = import_scad(f'{importFile}', use_not_include=False)


class recolor(OpenSCADObject):
    def __init__(self, c=None, **kwargs):
       super().__init__("recolor" ,{"c" : c, **kwargs})

class color_this(OpenSCADObject):
    def __init__(self, c=None, **kwargs):
       super().__init__("color_this" ,{"c" : c, **kwargs})

class rainbow(OpenSCADObject):
    def __init__(self, list=None, stride=None, maxhues=None, shuffle=None, seed=None, **kwargs):
       super().__init__("rainbow" ,{"list" : list, "stride" : stride, "maxhues" : maxhues, "shuffle" : shuffle, "seed" : seed, **kwargs})

class hsl(OpenSCADObject):
    def __init__(self, h=None, s=None, l=None, a=None, **kwargs):
       super().__init__("hsl" ,{"h" : h, "s" : s, "l" : l, "a" : a, **kwargs})

class hsv(OpenSCADObject):
    def __init__(self, h=None, s=None, v=None, a=None, **kwargs):
       super().__init__("hsv" ,{"h" : h, "s" : s, "v" : v, "a" : a, **kwargs})

class hsl(OpenSCADObject):
    def __init__(self, h=None, s=None, l=None, a=None, **kwargs):
       super().__init__("hsl" ,{"h" : h, "s" : s, "l" : l, "a" : a, **kwargs})

class hsv(OpenSCADObject):
    def __init__(self, h=None, s=None, v=None, a=None, **kwargs):
       super().__init__("hsv" ,{"h" : h, "s" : s, "v" : v, "a" : a, **kwargs})

