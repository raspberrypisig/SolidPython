from ...core.object_base import OpenSCADObject, OpenSCADConstant
from ... import import_scad
from pathlib import Path

importFile = Path(__file__).absolute().parent.parent.parent / 'libs' / 'BOSL2' / 'version.scad'
_ = import_scad(f'{importFile}', use_not_include=False)

BOSL_VERSION = OpenSCADConstant('BOSL_VERSION')

class bosl_required(OpenSCADObject):
    def __init__(self, version=None, **kwargs):
       super().__init__("bosl_required" ,{"version" : version, **kwargs})

class bosl_version(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("bosl_version" ,{**kwargs})

class bosl_version_num(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("bosl_version_num" ,{**kwargs})

class bosl_version_str(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("bosl_version_str" ,{**kwargs})

class _version_split_str(OpenSCADObject):
    def __init__(self, x=None, _i=None, _out=None, _num=None, **kwargs):
       super().__init__("_version_split_str" ,{"x" : x, "_i" : _i, "_out" : _out, "_num" : _num, **kwargs})

class version_to_list(OpenSCADObject):
    def __init__(self, version=None, **kwargs):
       super().__init__("version_to_list" ,{"version" : version, **kwargs})

class version_to_str(OpenSCADObject):
    def __init__(self, version=None, **kwargs):
       super().__init__("version_to_str" ,{"version" : version, **kwargs})

class version_to_num(OpenSCADObject):
    def __init__(self, version=None, **kwargs):
       super().__init__("version_to_num" ,{"version" : version, **kwargs})

class version_cmp(OpenSCADObject):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("version_cmp" ,{"a" : a, "b" : b, **kwargs})

