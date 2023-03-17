from ...core.object_base import OpenSCADObject, OpenSCADConstant
from ... import import_scad
from pathlib import Path

importFile = Path(__file__).absolute().parent.parent.parent / 'libs' / 'BOSL2' / 'tripod_mounts.scad'
_ = import_scad(f'{importFile}', use_not_include=False)


class manfrotto_rc2_plate(OpenSCADObject):
    def __init__(self, chamfer=None, anchor=None, orient=None, spin=None, **kwargs):
       super().__init__("manfrotto_rc2_plate" ,{"chamfer" : chamfer, "anchor" : anchor, "orient" : orient, "spin" : spin, **kwargs})

