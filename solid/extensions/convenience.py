from functools import singledispatch

from .. import builtins
from ..object_base import OpenSCADObject
from ..helpers import escpape_openscad_identifier

# ==============================================
# = overwrite translate, rotate, scale, mirror =
# ==============================================

# =============
# = translate =
# =============
@singledispatch
def translate(v):
    return builtins.translate(v)

@translate.register(int)
@translate.register(float)
def _translate(*args):
    return builtins.translate(args)

# =========
# = scale =
# =========
@singledispatch
def scale(v):
    return builtins.scale(v)

@scale.register(int)
@scale.register(float)
def _scale(*args):
    if len(args) == 1:
        return builtins.scale(args[0])
    else:
        return builtins.scale(args)

# =============
# = mirror =
# =============
@singledispatch
def mirror(v):
    return builtins.mirror(v)

@mirror.register(int)
@mirror.register(float)
def _translate(*args):
    return builtins.mirror(args)

# =========
# = rotate =
# =========
def rotate(*args, **kwargs):
    if kwargs:
        return builtins.rotate(*args, **kwargs)
    else:
        if len(args) == 1:
            return builtins.rotate(*args)
        elif     (isinstance(args[0], int) or isinstance(args[0], float)) \
             and (isinstance(args[1], list) or isinstance(args[1], tuple)):
                return builtins.rotate(a=args[0], v=args[1:])
        else:
            return builtins.rotate(args)

# =============================
# = overwrite square and cube =
# =============================
def extract_size_list(*args, **kwargs):
    size_list = []
    args_copy = list(args)

    while args_copy:
        a = args_copy.pop(0)
        if type(a) == int or type(a) == float:
            size_list += [a]
        else:
            args_copy = [a] + args_copy
            break

    if len(size_list) == 1:
        size_list = size_list[0]

    return size_list, args_copy, kwargs

def square(*args, **kwargs):
    size_list, args, kwargs = extract_size_list(*args, **kwargs)

    if size_list:
        return builtins.square(size_list, *args, **kwargs)
    else:
        return builtins.square(*args, **kwargs)

def cube(*args, **kwargs):
    size_list, args, kwargs = extract_size_list(*args, **kwargs)

    if size_list:
        return builtins.cube(size_list, *args, **kwargs)
    else:
        return builtins.cube(*args, **kwargs)

# ==============
# = Directions =
# ==============
def up(z): return builtins.translate((0, 0, z))
def down(z): return builtins.translate((0, 0, -z))
def right(x): return builtins.translate((x, 0, 0))
def left(x): return builtins.translate((-x, 0, 0))
def forward(y): return builtins.translate((0, y, 0))
def back(y): return builtins.translate((0, -y, 0))

# ============================================
# = union, difference, intersectin operators =
# ============================================
def _union_op(self, x):
    """
    This makes u = a+b identical to:
    u = union()(a, b )
    """
    res = builtins.union()

    #add self or all its children to res
    if isinstance(self, builtins.union):
        for c in self.children:
            res.add(c)
    else:
        res.add(self)

    #add x or all its children to res
    if isinstance(x, builtins.union):
        for c in x.children:
            res.add(c)
    else:
        res.add(x)

    return res

def _difference_op(self, x):
    """
    This makes u = a - b identical to:
    u = difference()(a, b )
    """
    res = builtins.difference()

    if isinstance(self, builtins.difference) and len(self.children):
        for c in self.children:
            res.add(c)
    else:
        res.add(self)

    res.add(x)
    return res

def _intersection_op(self, x):
    """
    This makes u = a * b identical to:
    u = intersection()(a, b )
    """
    res = builtins.intersection()

    if isinstance(self, builtins.intersection) and len(self.children):
        for c in self.children:
            res.add(c)
    else:
        res.add(self)

    if isinstance(x, builtins.intersection):
        for c in x.children:
            res.add(c)
    else:
        res.add(x)

    return res

# ===============================
# = monkey patch OpenSCADObject =
# ===============================

#builtin transformations
_cascading_builtins = ("union difference intersection intersection_for translate " +\
                      "scale rotate mirror resize color offset hull render " +\
                      "linear_extrude rotate_extrude projection surface").split(" ")

for name in _cascading_builtins:
    #get the builtin
    builtin = getattr(builtins, escpape_openscad_identifier(name))

    #wrap a lambda func around it
    func = lambda self, *args, **kwargs : builtin(*args, **kwargs)(self)

    #bind it to OpenSCADObject
    setattr(OpenSCADObject, escpape_openscad_identifier(name), func)


# &, |, +, -, * operators -> union, difference, intersection
OpenSCADObject.__add__ = _union_op
OpenSCADObject.__or__ = _union_op
OpenSCADObject.__radd__ = _union_op
OpenSCADObject.__sub__ = _difference_op
OpenSCADObject.__mul__ = _intersection_op
OpenSCADObject.__and__ = _intersection_op

#replace basic transformations with wrappers from this module
OpenSCADObject.translate = lambda self, *args: translate(*args)(self)
OpenSCADObject.mirror = lambda self, *args: mirror(*args)(self)
OpenSCADObject.scale = lambda self, *args: scale(*args)(self)
OpenSCADObject.rotate = lambda self, *args, **kwargs: rotate(*args, **kwargs)(self)

#translation wrappers
#this allows:
#   cube(10).up(10)
OpenSCADObject.down = lambda self, x: down(x)(self)
OpenSCADObject.up = lambda self, x: up(x)(self)
OpenSCADObject.left = lambda self, x: left(x)(self)
OpenSCADObject.right = lambda self, x: right(x)(self)
OpenSCADObject.back = lambda self, x: back(x)(self)
OpenSCADObject.forward = lambda self, x: forward(x)(self)
OpenSCADObject.mx = lambda self, x: self.translate(x, 0, 0)
OpenSCADObject.my = lambda self, y: self.translate(0, y, 0)
OpenSCADObject.mz = lambda self, z: self.translate(0, 0, z)

#debug, background, root, disable and ~
OpenSCADObject.debug = lambda self: builtins.debug()(self)
OpenSCADObject.background = lambda self: builtins.background()(self)
OpenSCADObject.root = lambda self: builtins.root()(self)
OpenSCADObject.disable = lambda self: builtins.disable()(self)
OpenSCADObject.__invert__ = lambda self: builtins.debug()(self)

