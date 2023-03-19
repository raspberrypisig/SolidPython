from solid2.core.object_base import OpenSCADObject as _OpenSCADObject,                                    OpenSCADConstant as _OpenSCADConstant
from solid2.core.scad_import import extra_scad_include as _extra_scad_include
from pathlib import Path as _Path
from .bosl2_mixin import Bosl2Mixin as _Bosl2Mixin

_extra_scad_include(f"{_Path(__file__).parent.parent / '../libs/BOSL2/turtle3d.scad'}", use_not_include=False)

class _transpart(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, T=None, **kwargs):
       super().__init__("_transpart", {"T" : T, **kwargs})

class _rotpart(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, T=None, **kwargs):
       super().__init__("_rotpart", {"T" : T, **kwargs})

class _turtle3d_state_valid(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, state=None, **kwargs):
       super().__init__("_turtle3d_state_valid", {"state" : state, **kwargs})

class turtle3d(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, commands=None, state=None, transforms=None, full_state=None, repeat=None, **kwargs):
       super().__init__("turtle3d", {"commands" : commands, "state" : state, "transforms" : transforms, "full_state" : full_state, "repeat" : repeat, **kwargs})

class _turtle3d_repeat(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, commands=None, state=None, repeat=None, **kwargs):
       super().__init__("_turtle3d_repeat", {"commands" : commands, "state" : state, "repeat" : repeat, **kwargs})

class _turtle3d_command_len(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, commands=None, index=None, **kwargs):
       super().__init__("_turtle3d_command_len", {"commands" : commands, "index" : index, **kwargs})

class _turtle3d(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, commands=None, state=None, index=None, **kwargs):
       super().__init__("_turtle3d", {"commands" : commands, "state" : state, "index" : index, **kwargs})

class _turtle3d_rotation(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, command=None, angle=None, center=None, **kwargs):
       super().__init__("_turtle3d_rotation", {"command" : command, "angle" : angle, "center" : center, **kwargs})

class _tupdate(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, state=None, tran=None, pretran=None, **kwargs):
       super().__init__("_tupdate", {"state" : state, "tran" : tran, "pretran" : pretran, **kwargs})

class _turtle3d_command(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, command=None, parm=None, parm2=None, state=None, index=None, **kwargs):
       super().__init__("_turtle3d_command", {"command" : command, "parm" : parm, "parm2" : parm2, "state" : state, "index" : index, **kwargs})

class _turtle3d_list_command(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, command=None, arcsteps=None, movescale=None, lastT=None, lastPre=None, index=None, **kwargs):
       super().__init__("_turtle3d_list_command", {"command" : command, "arcsteps" : arcsteps, "movescale" : movescale, "lastT" : lastT, "lastPre" : lastPre, "index" : index, **kwargs})

class turtle3d(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, commands=None, state=None, transforms=None, full_state=None, repeat=None, **kwargs):
       super().__init__("turtle3d", {"commands" : commands, "state" : state, "transforms" : transforms, "full_state" : full_state, "repeat" : repeat, **kwargs})

