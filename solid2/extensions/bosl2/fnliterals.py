from solid2.core.object_base import OpenSCADObject as _OpenSCADObject,                                    OpenSCADConstant as _OpenSCADConstant
from solid2.core.scad_import import extra_scad_include as _extra_scad_include
from pathlib import Path as _Path
from .bosl2_mixin import Bosl2Mixin as _Bosl2Mixin

_extra_scad_include(f"{_Path(__file__).parent.parent / '../libs/BOSL2/fnliterals.scad'}", use_not_include=False)

class map(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, func=None, list=None, **kwargs):
       super().__init__("map", {"func" : func, "list" : list, **kwargs})

class filter(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, func=None, list=None, **kwargs):
       super().__init__("filter", {"func" : func, "list" : list, **kwargs})

class reduce(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, func=None, list=None, init=None, **kwargs):
       super().__init__("reduce", {"func" : func, "list" : list, "init" : init, **kwargs})

class accumulate(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, func=None, list=None, init=None, **kwargs):
       super().__init__("accumulate", {"func" : func, "list" : list, "init" : init, **kwargs})

class _while(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, init=None, cond=None, func=None, **kwargs):
       super().__init__("_while", {"init" : init, "cond" : cond, "func" : func, **kwargs})

class for_n(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, n=None, init=None, func=None, **kwargs):
       super().__init__("for_n", {"n" : n, "init" : init, "func" : func, **kwargs})

class find_all(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, func=None, list=None, **kwargs):
       super().__init__("find_all", {"func" : func, "list" : list, **kwargs})

class find_first(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, func=None, list=None, start=None, **kwargs):
       super().__init__("find_first", {"func" : func, "list" : list, "start" : start, **kwargs})

class binsearch(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, key=None, list=None, idx=None, cmp=None, **kwargs):
       super().__init__("binsearch", {"key" : key, "list" : list, "idx" : idx, "cmp" : cmp, **kwargs})

class simple_hash(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("simple_hash", {"x" : x, **kwargs})

class hashmap(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, hashsize=None, items=None, table=None, **kwargs):
       super().__init__("hashmap", {"hashsize" : hashsize, "items" : items, "table" : table, **kwargs})

class f_1arg(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, target_func=None, **kwargs):
       super().__init__("f_1arg", {"target_func" : target_func, **kwargs})

class f_2arg(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, target_func=None, **kwargs):
       super().__init__("f_2arg", {"target_func" : target_func, **kwargs})

class f_2arg_simple(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, target_func=None, **kwargs):
       super().__init__("f_2arg_simple", {"target_func" : target_func, **kwargs})

class f_3arg(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, target_func=None, **kwargs):
       super().__init__("f_3arg", {"target_func" : target_func, **kwargs})

class ival(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, target_func=None, **kwargs):
       super().__init__("ival", {"target_func" : target_func, **kwargs})

class xval(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, target_func=None, **kwargs):
       super().__init__("xval", {"target_func" : target_func, **kwargs})

class f_cmp(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_cmp", {"a" : a, "b" : b, **kwargs})

class f_gt(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_gt", {"a" : a, "b" : b, **kwargs})

class f_lt(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_lt", {"a" : a, "b" : b, **kwargs})

class f_gte(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_gte", {"a" : a, "b" : b, **kwargs})

class f_lte(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_lte", {"a" : a, "b" : b, **kwargs})

class f_eq(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_eq", {"a" : a, "b" : b, **kwargs})

class f_neq(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_neq", {"a" : a, "b" : b, **kwargs})

class f_approx(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_approx", {"a" : a, "b" : b, **kwargs})

class f_napprox(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_napprox", {"a" : a, "b" : b, **kwargs})

class f_or(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_or", {"a" : a, "b" : b, **kwargs})

class f_and(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_and", {"a" : a, "b" : b, **kwargs})

class f_nor(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_nor", {"a" : a, "b" : b, **kwargs})

class f_nand(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_nand", {"a" : a, "b" : b, **kwargs})

class f_xor(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_xor", {"a" : a, "b" : b, **kwargs})

class f_not(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_not", {"a" : a, **kwargs})

class f_even(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_even", {"a" : a, **kwargs})

class f_odd(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_odd", {"a" : a, **kwargs})

class f_add(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_add", {"a" : a, "b" : b, **kwargs})

class f_sub(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_sub", {"a" : a, "b" : b, **kwargs})

class f_mul(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_mul", {"a" : a, "b" : b, **kwargs})

class f_div(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_div", {"a" : a, "b" : b, **kwargs})

class f_mod(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_mod", {"a" : a, "b" : b, **kwargs})

class f_pow(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_pow", {"a" : a, "b" : b, **kwargs})

class f_neg(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_neg", {"a" : a, **kwargs})

class f_min(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_min", {"a" : a, **kwargs})

class f_max(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_max", {"a" : a, **kwargs})

class f_min2(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_min2", {"a" : a, "b" : b, **kwargs})

class f_max2(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_max2", {"a" : a, "b" : b, **kwargs})

class f_min3(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, c=None, **kwargs):
       super().__init__("f_min3", {"a" : a, "b" : b, "c" : c, **kwargs})

class f_max3(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, c=None, **kwargs):
       super().__init__("f_max3", {"a" : a, "b" : b, "c" : c, **kwargs})

class f_sin(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_sin", {"a" : a, **kwargs})

class f_cos(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_cos", {"a" : a, **kwargs})

class f_tan(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_tan", {"a" : a, **kwargs})

class f_asin(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_asin", {"a" : a, **kwargs})

class f_acos(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_acos", {"a" : a, **kwargs})

class f_atan(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_atan", {"a" : a, **kwargs})

class f_atan2(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_atan2", {"a" : a, "b" : b, **kwargs})

class f_len(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_len", {"a" : a, **kwargs})

class f_chr(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_chr", {"a" : a, **kwargs})

class f_ord(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_ord", {"a" : a, **kwargs})

class f_str(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_str", {"a" : a, **kwargs})

class f_str2(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_str2", {"a" : a, "b" : b, **kwargs})

class f_str3(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, c=None, **kwargs):
       super().__init__("f_str3", {"a" : a, "b" : b, "c" : c, **kwargs})

class f_floor(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_floor", {"a" : a, **kwargs})

class f_round(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_round", {"a" : a, **kwargs})

class f_ceil(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_ceil", {"a" : a, **kwargs})

class f_abs(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_abs", {"a" : a, **kwargs})

class f_sign(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_sign", {"a" : a, **kwargs})

class f_ln(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_ln", {"a" : a, **kwargs})

class f_log(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_log", {"a" : a, **kwargs})

class f_exp(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_exp", {"a" : a, **kwargs})

class f_sqr(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_sqr", {"a" : a, **kwargs})

class f_sqrt(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_sqrt", {"a" : a, **kwargs})

class f_norm(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_norm", {"a" : a, **kwargs})

class f_cross(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_cross", {"a" : a, "b" : b, **kwargs})

class f_is_def(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_def", {"x" : x, **kwargs})

class f_is_undef(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_undef", {"x" : x, **kwargs})

class f_is_bool(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_bool", {"x" : x, **kwargs})

class f_is_num(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_num", {"x" : x, **kwargs})

class f_is_int(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_int", {"x" : x, **kwargs})

class f_is_nan(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_nan", {"x" : x, **kwargs})

class f_is_finite(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_finite", {"x" : x, **kwargs})

class f_is_string(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_string", {"x" : x, **kwargs})

class f_is_list(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_list", {"x" : x, **kwargs})

class f_is_range(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_range", {"x" : x, **kwargs})

class f_is_function(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, x=None, **kwargs):
       super().__init__("f_is_function", {"x" : x, **kwargs})

class f_is_vector(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_is_vector", {"a" : a, "b" : b, **kwargs})

class f_is_path(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, b=None, **kwargs):
       super().__init__("f_is_path", {"a" : a, "b" : b, **kwargs})

class f_is_region(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_is_region", {"a" : a, **kwargs})

class f_is_vnf(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_is_vnf", {"a" : a, **kwargs})

class f_is_patch(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, a=None, **kwargs):
       super().__init__("f_is_patch", {"a" : a, **kwargs})

