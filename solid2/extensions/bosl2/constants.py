from ...core.object_base import OpenSCADObject, OpenSCADConstant
from ... import import_scad
from pathlib import Path

importFile = Path(__file__).absolute().parent.parent.parent / 'libs' / 'BOSL2' / 'constants.scad'
_ = import_scad(f'{importFile}', use_not_include=False)

_UNDEF = OpenSCADConstant('_UNDEF')
INCH = OpenSCADConstant('INCH')
LEFT = OpenSCADConstant('LEFT')
RIGHT = OpenSCADConstant('RIGHT')
FRONT = OpenSCADConstant('FRONT')
FWD = OpenSCADConstant('FWD')
FORWARD = OpenSCADConstant('FORWARD')
BACK = OpenSCADConstant('BACK')
BOTTOM = OpenSCADConstant('BOTTOM')
BOT = OpenSCADConstant('BOT')
DOWN = OpenSCADConstant('DOWN')
TOP = OpenSCADConstant('TOP')
UP = OpenSCADConstant('UP')
CENTER = OpenSCADConstant('CENTER')
CTR = OpenSCADConstant('CTR')
CENTRE = OpenSCADConstant('CENTRE')
SEGMENT = OpenSCADConstant('SEGMENT')
RAY = OpenSCADConstant('RAY')
LINE = OpenSCADConstant('LINE')
IDENT = OpenSCADConstant('IDENT')

class get_slop(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("get_slop" ,{**kwargs})

