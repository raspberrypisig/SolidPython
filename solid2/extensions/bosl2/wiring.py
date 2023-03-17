from ...core.object_base import OpenSCADObject, OpenSCADConstant
from ... import import_scad
from pathlib import Path

baseDir = Path(__file__).absolute().parent.parent.parent
importFile = baseDir / "libs" / "BOSL2" / "wiring.scad"
_ = import_scad(f"{importFile}", use_not_include=False)

class wire_bundle(OpenSCADObject):
    def __init__(self, path=None, wires=None, wirediam=None, rounding=None, wirenum=None, corner_steps=None, **kwargs):
       super().__init__("wire_bundle", {"path" : path, "wires" : wires, "wirediam" : wirediam, "rounding" : rounding, "wirenum" : wirenum, "corner_steps" : corner_steps, **kwargs})

class _hex_offset_ring(OpenSCADObject):
    def __init__(self, d=None, lev=None, **kwargs):
       super().__init__("_hex_offset_ring", {"d" : d, "lev" : lev, **kwargs})

class _hex_offsets(OpenSCADObject):
    def __init__(self, n=None, d=None, lev=None, arr=None, **kwargs):
       super().__init__("_hex_offsets", {"n" : n, "d" : d, "lev" : lev, "arr" : arr, **kwargs})

