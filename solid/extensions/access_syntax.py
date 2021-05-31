from ..core import builtins
from . import convenience
from ..core.utils import escape_openscad_identifier
from ..core.object_base import ObjectBase

__nothing__ = None

# ===============================
# = monkey patch ObjectBase =
# ===============================
"""
    Patch ObjectBase to allow .-access syntax style:

    cube(20).translate(1, 2, 3) + cylinder(r=0.5, h=5).up(5).rotate(20, 30, 40)
"""

#builtin transformations
_cascading_builtins = ("union difference intersection intersection_for translate " +\
                      "scale rotate mirror resize color offset hull render " +\
                      "linear_extrude rotate_extrude projection surface").split(" ")

def add_builtin_to_object_base(name):
    #get the builtin
    builtin = getattr(builtins, escape_openscad_identifier(name))

    func = lambda self, *args, **kwargs : builtin(*args, **kwargs)(self)

    setattr(ObjectBase, escape_openscad_identifier(name), func)

for name in _cascading_builtins:
    add_builtin_to_object_base(name)

#replace basic transformations with wrappers from the convenience module
ObjectBase.translate = lambda self, *args: convenience.translate(*args)(self)
ObjectBase.mirror = lambda self, *args: convenience.mirror(*args)(self)
ObjectBase.scale = lambda self, *args: convenience.scale(*args)(self)
ObjectBase.resize = lambda self, *args: convenience.resize(*args)(self)
ObjectBase.rotate = lambda self, *args, **kwargs: convenience.rotate(*args, **kwargs)(self)

#translation wrappers
ObjectBase.down = lambda self, x: convenience.down(x)(self)
ObjectBase.up = lambda self, x: convenience.up(x)(self)
ObjectBase.left = lambda self, x: convenience.left(x)(self)
ObjectBase.right = lambda self, x: convenience.right(x)(self)
ObjectBase.back = lambda self, x: convenience.back(x)(self)
ObjectBase.fwd = lambda self, x: convenience.fwd(x)(self)
ObjectBase.forward = lambda self, x: convenience.fwd(x)(self)

#debug, background, root, disable and ~
ObjectBase.debug = lambda self: builtins.debug()(self)
ObjectBase.background = lambda self: builtins.background()(self)
ObjectBase.root = lambda self: builtins.root()(self)
ObjectBase.disable = lambda self: builtins.disable()(self)

