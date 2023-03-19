from solid2.core.object_base import OpenSCADObject, OpenSCADConstant
from solid2.core.scad_import import extra_scad_include
from pathlib import Path
from .bosl2_mixin import Bosl2Mixin

extra_scad_include(f"{Path(__file__).parent.parent / '../libs/BOSL2/utility.scad'}", use_not_include=False)

class no_children(OpenSCADObject, Bosl2Mixin):
    def __init__(self, count=None, **kwargs):
       super().__init__("no_children", {"count" : count, **kwargs})

class req_children(OpenSCADObject, Bosl2Mixin):
    def __init__(self, count=None, **kwargs):
       super().__init__("req_children", {"count" : count, **kwargs})

class no_module(OpenSCADObject, Bosl2Mixin):
    def __init__(self, **kwargs):
       super().__init__("no_module", {**kwargs})

class assert_approx(OpenSCADObject, Bosl2Mixin):
    def __init__(self, got=None, expected=None, info=None, **kwargs):
       super().__init__("assert_approx", {"got" : got, "expected" : expected, "info" : info, **kwargs})

class assert_equal(OpenSCADObject, Bosl2Mixin):
    def __init__(self, got=None, expected=None, info=None, **kwargs):
       super().__init__("assert_equal", {"got" : got, "expected" : expected, "info" : info, **kwargs})

class shape_compare(OpenSCADObject, Bosl2Mixin):
    def __init__(self, eps=None, **kwargs):
       super().__init__("shape_compare", {"eps" : eps, **kwargs})

class typeof(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("typeof", {"x" : x, **kwargs})

class is_type(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, types=None, **kwargs):
       super().__init__("is_type", {"x" : x, "types" : types, **kwargs})

class is_def(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("is_def", {"x" : x, **kwargs})

class is_str(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("is_str", {"x" : x, **kwargs})

class is_int(OpenSCADObject, Bosl2Mixin):
    def __init__(self, n=None, **kwargs):
       super().__init__("is_int", {"n" : n, **kwargs})

class is_integer(OpenSCADObject, Bosl2Mixin):
    def __init__(self, n=None, **kwargs):
       super().__init__("is_integer", {"n" : n, **kwargs})

class all_integer(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("all_integer", {"x" : x, **kwargs})

class is_nan(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("is_nan", {"x" : x, **kwargs})

class is_finite(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("is_finite", {"x" : x, **kwargs})

class is_range(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("is_range", {"x" : x, **kwargs})

class valid_range(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("valid_range", {"x" : x, **kwargs})

class is_func(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("is_func", {"x" : x, **kwargs})

class is_consistent(OpenSCADObject, Bosl2Mixin):
    def __init__(self, list=None, pattern=None, **kwargs):
       super().__init__("is_consistent", {"list" : list, "pattern" : pattern, **kwargs})

class _list_pattern(OpenSCADObject, Bosl2Mixin):
    def __init__(self, list=None, **kwargs):
       super().__init__("_list_pattern", {"list" : list, **kwargs})

class same_shape(OpenSCADObject, Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("same_shape", {"a" : a, "b" : b, **kwargs})

class is_bool_list(OpenSCADObject, Bosl2Mixin):
    def __init__(self, list=None, length=None, **kwargs):
       super().__init__("is_bool_list", {"list" : list, "length" : length, **kwargs})

class any(OpenSCADObject, Bosl2Mixin):
    def __init__(self, l=None, func=None, **kwargs):
       super().__init__("any", {"l" : l, "func" : func, **kwargs})

class _any_func(OpenSCADObject, Bosl2Mixin):
    def __init__(self, l=None, func=None, i=None, out=None, **kwargs):
       super().__init__("_any_func", {"l" : l, "func" : func, "i" : i, "out" : out, **kwargs})

class _any_bool(OpenSCADObject, Bosl2Mixin):
    def __init__(self, l=None, i=None, out=None, **kwargs):
       super().__init__("_any_bool", {"l" : l, "i" : i, "out" : out, **kwargs})

class all(OpenSCADObject, Bosl2Mixin):
    def __init__(self, l=None, func=None, **kwargs):
       super().__init__("all", {"l" : l, "func" : func, **kwargs})

class _all_func(OpenSCADObject, Bosl2Mixin):
    def __init__(self, l=None, func=None, i=None, out=None, **kwargs):
       super().__init__("_all_func", {"l" : l, "func" : func, "i" : i, "out" : out, **kwargs})

class _all_bool(OpenSCADObject, Bosl2Mixin):
    def __init__(self, l=None, i=None, out=None, **kwargs):
       super().__init__("_all_bool", {"l" : l, "i" : i, "out" : out, **kwargs})

class num_true(OpenSCADObject, Bosl2Mixin):
    def __init__(self, l=None, func=None, **kwargs):
       super().__init__("num_true", {"l" : l, "func" : func, **kwargs})

class default(OpenSCADObject, Bosl2Mixin):
    def __init__(self, v=None, dflt=None, **kwargs):
       super().__init__("default", {"v" : v, "dflt" : dflt, **kwargs})

class first_defined(OpenSCADObject, Bosl2Mixin):
    def __init__(self, v=None, recursive=None, _i=None, **kwargs):
       super().__init__("first_defined", {"v" : v, "recursive" : recursive, "_i" : _i, **kwargs})

class one_defined(OpenSCADObject, Bosl2Mixin):
    def __init__(self, vals=None, names=None, dflt=None, **kwargs):
       super().__init__("one_defined", {"vals" : vals, "names" : names, "dflt" : dflt, **kwargs})

class num_defined(OpenSCADObject, Bosl2Mixin):
    def __init__(self, v=None, **kwargs):
       super().__init__("num_defined", {"v" : v, **kwargs})

class any_defined(OpenSCADObject, Bosl2Mixin):
    def __init__(self, v=None, recursive=None, **kwargs):
       super().__init__("any_defined", {"v" : v, "recursive" : recursive, **kwargs})

class all_defined(OpenSCADObject, Bosl2Mixin):
    def __init__(self, v=None, recursive=None, **kwargs):
       super().__init__("all_defined", {"v" : v, "recursive" : recursive, **kwargs})

class u_add(OpenSCADObject, Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("u_add", {"a" : a, "b" : b, **kwargs})

class u_sub(OpenSCADObject, Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("u_sub", {"a" : a, "b" : b, **kwargs})

class u_mul(OpenSCADObject, Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("u_mul", {"a" : a, "b" : b, **kwargs})

class u_div(OpenSCADObject, Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("u_div", {"a" : a, "b" : b, **kwargs})

class get_anchor(OpenSCADObject, Bosl2Mixin):
    def __init__(self, anchor=None, center=None, uncentered=None, dflt=None, **kwargs):
       super().__init__("get_anchor", {"anchor" : anchor, "center" : center, "uncentered" : uncentered, "dflt" : dflt, **kwargs})

class get_radius(OpenSCADObject, Bosl2Mixin):
    def __init__(self, r1=None, r2=None, r=None, d1=None, d2=None, d=None, dflt=None, **kwargs):
       super().__init__("get_radius", {"r1" : r1, "r2" : r2, "r" : r, "d1" : d1, "d2" : d2, "d" : d, "dflt" : dflt, **kwargs})

class scalar_vec3(OpenSCADObject, Bosl2Mixin):
    def __init__(self, v=None, dflt=None, **kwargs):
       super().__init__("scalar_vec3", {"v" : v, "dflt" : dflt, **kwargs})

class segs(OpenSCADObject, Bosl2Mixin):
    def __init__(self, r=None, **kwargs):
       super().__init__("segs", {"r" : r, **kwargs})

class no_function(OpenSCADObject, Bosl2Mixin):
    def __init__(self, name=None, **kwargs):
       super().__init__("no_function", {"name" : name, **kwargs})

class _valstr(OpenSCADObject, Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("_valstr", {"x" : x, **kwargs})

class looping(OpenSCADObject, Bosl2Mixin):
    def __init__(self, state=None, **kwargs):
       super().__init__("looping", {"state" : state, **kwargs})

class loop_while(OpenSCADObject, Bosl2Mixin):
    def __init__(self, state=None, _continue=None, **kwargs):
       super().__init__("loop_while", {"state" : state, "_continue" : _continue, **kwargs})

class loop_done(OpenSCADObject, Bosl2Mixin):
    def __init__(self, state=None, **kwargs):
       super().__init__("loop_done", {"state" : state, **kwargs})

