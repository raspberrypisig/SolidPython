from solid2.core.object_base import OpenSCADObject as _OpenSCADObject,                                    OpenSCADConstant as _OpenSCADConstant
from solid2.core.scad_import import extra_scad_include as _extra_scad_include
from pathlib import Path as _Path
from .bosl2_mixin import Bosl2Mixin as _Bosl2Mixin

_extra_scad_include(f"{_Path(__file__).parent.parent / '../libs/BOSL2/affine.scad'}", use_not_include=False)

class affine2d_identity(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, **kwargs):
       super().__init__("affine2d_identity", {**kwargs})

class affine2d_translate(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, v=None, **kwargs):
       super().__init__("affine2d_translate", {"v" : v, **kwargs})

class affine2d_scale(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, v=None, **kwargs):
       super().__init__("affine2d_scale", {"v" : v, **kwargs})

class affine2d_zrot(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, ang=None, **kwargs):
       super().__init__("affine2d_zrot", {"ang" : ang, **kwargs})

class affine2d_mirror(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, v=None, **kwargs):
       super().__init__("affine2d_mirror", {"v" : v, **kwargs})

class affine2d_skew(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, xa=None, ya=None, **kwargs):
       super().__init__("affine2d_skew", {"xa" : xa, "ya" : ya, **kwargs})

class affine3d_identity(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, **kwargs):
       super().__init__("affine3d_identity", {**kwargs})

class affine3d_translate(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, v=None, **kwargs):
       super().__init__("affine3d_translate", {"v" : v, **kwargs})

class affine3d_scale(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, v=None, **kwargs):
       super().__init__("affine3d_scale", {"v" : v, **kwargs})

class affine3d_xrot(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, ang=None, **kwargs):
       super().__init__("affine3d_xrot", {"ang" : ang, **kwargs})

class affine3d_yrot(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, ang=None, **kwargs):
       super().__init__("affine3d_yrot", {"ang" : ang, **kwargs})

class affine3d_zrot(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, ang=None, **kwargs):
       super().__init__("affine3d_zrot", {"ang" : ang, **kwargs})

class affine3d_rot_by_axis(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, u=None, ang=None, **kwargs):
       super().__init__("affine3d_rot_by_axis", {"u" : u, "ang" : ang, **kwargs})

class affine3d_rot_from_to(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, _from=None, to=None, **kwargs):
       super().__init__("affine3d_rot_from_to", {"_from" : _from, "to" : to, **kwargs})

class affine3d_mirror(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, v=None, **kwargs):
       super().__init__("affine3d_mirror", {"v" : v, **kwargs})

class affine3d_skew(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, sxy=None, sxz=None, syx=None, syz=None, szx=None, szy=None, **kwargs):
       super().__init__("affine3d_skew", {"sxy" : sxy, "sxz" : sxz, "syx" : syx, "syz" : syz, "szx" : szx, "szy" : szy, **kwargs})

class affine3d_skew_xy(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, xa=None, ya=None, **kwargs):
       super().__init__("affine3d_skew_xy", {"xa" : xa, "ya" : ya, **kwargs})

class affine3d_skew_xz(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, xa=None, za=None, **kwargs):
       super().__init__("affine3d_skew_xz", {"xa" : xa, "za" : za, **kwargs})

class affine3d_skew_yz(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, ya=None, za=None, **kwargs):
       super().__init__("affine3d_skew_yz", {"ya" : ya, "za" : za, **kwargs})

