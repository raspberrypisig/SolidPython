from functools import singledispatch

from ..core import builtins

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

# ==============================================
# = overwrite translate, rotate, scale, mirror =
# ==============================================
"""
    This block overwrites translate, scale, mirror and rotate from builtins
    to allow "overloading" those functions.
    As result you don't need to pass vectors in as lists, you can provide
    them as single integers / floats.

    translate([1, 2, 3])  ->   translate(1, 2, 3)
    rotate([1, 2, 3])   -> rotate(1, 2, 3)
"""

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

# ==========
# = resize =
# ==========
def resize(*args, **kwargs):
    size_list, args, kwargs = extract_size_list(*args, **kwargs)

    if size_list:
        return builtins.resize(size_list, *args, **kwargs)
    else:
        return builtins.resize(*args, **kwargs)

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
"""
    overwrite square and cube from builtins.
    This allows to pass the size in as single integers:

    cube([1, 2, 3])   -> cube(1, 2, 3)
    square([1, 2])    -> square(1, 2)
"""
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
def fwd(y): return builtins.translate((0, y, 0))
def back(y): return builtins.translate((0, -y, 0))

