from solid2.core.object_base import OpenSCADObject as _OpenSCADObject,                                    OpenSCADConstant as _OpenSCADConstant
from solid2.core.scad_import import extra_scad_include as _extra_scad_include
from pathlib import Path as _Path
from .bosl2_mixin import Bosl2Mixin as _Bosl2Mixin

_extra_scad_include(f"{_Path(__file__).parent.parent / '../libs/BOSL2/paths.scad'}", use_not_include=False)

class is_path(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, list=None, dim=None, fast=None, **kwargs):
       super().__init__("is_path", {"list" : list, "dim" : dim, "fast" : fast, **kwargs})

class is_1region(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, name=None, **kwargs):
       super().__init__("is_1region", {"path" : path, "name" : name, **kwargs})

class force_path(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, name=None, **kwargs):
       super().__init__("force_path", {"path" : path, "name" : name, **kwargs})

class is_closed_path(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, eps=None, **kwargs):
       super().__init__("is_closed_path", {"path" : path, "eps" : eps, **kwargs})

class close_path(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, eps=None, **kwargs):
       super().__init__("close_path", {"path" : path, "eps" : eps, **kwargs})

class cleanup_path(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, eps=None, **kwargs):
       super().__init__("cleanup_path", {"path" : path, "eps" : eps, **kwargs})

class _path_select(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, s1=None, u1=None, s2=None, u2=None, closed=None, **kwargs):
       super().__init__("_path_select", {"path" : path, "s1" : s1, "u1" : u1, "s2" : s2, "u2" : u2, "closed" : closed, **kwargs})

class path_merge_collinear(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, eps=None, **kwargs):
       super().__init__("path_merge_collinear", {"path" : path, "closed" : closed, "eps" : eps, **kwargs})

class path_length(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, **kwargs):
       super().__init__("path_length", {"path" : path, "closed" : closed, **kwargs})

class path_segment_lengths(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, **kwargs):
       super().__init__("path_segment_lengths", {"path" : path, "closed" : closed, **kwargs})

class path_length_fractions(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, **kwargs):
       super().__init__("path_length_fractions", {"path" : path, "closed" : closed, **kwargs})

class _path_self_intersections(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, eps=None, **kwargs):
       super().__init__("_path_self_intersections", {"path" : path, "closed" : closed, "eps" : eps, **kwargs})

class _sum_preserving_round(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, data=None, index=None, **kwargs):
       super().__init__("_sum_preserving_round", {"data" : data, "index" : index, **kwargs})

class subdivide_path(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, n=None, refine=None, maxlen=None, closed=None, exact=None, method=None, **kwargs):
       super().__init__("subdivide_path", {"path" : path, "n" : n, "refine" : refine, "maxlen" : maxlen, "closed" : closed, "exact" : exact, "method" : method, **kwargs})

class resample_path(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, n=None, spacing=None, closed=None, **kwargs):
       super().__init__("resample_path", {"path" : path, "n" : n, "spacing" : spacing, "closed" : closed, **kwargs})

class is_path_simple(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, eps=None, **kwargs):
       super().__init__("is_path_simple", {"path" : path, "closed" : closed, "eps" : eps, **kwargs})

class path_closest_point(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, pt=None, closed=None, **kwargs):
       super().__init__("path_closest_point", {"path" : path, "pt" : pt, "closed" : closed, **kwargs})

class path_tangents(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, uniform=None, **kwargs):
       super().__init__("path_tangents", {"path" : path, "closed" : closed, "uniform" : uniform, **kwargs})

class path_normals(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, tangents=None, closed=None, **kwargs):
       super().__init__("path_normals", {"path" : path, "tangents" : tangents, "closed" : closed, **kwargs})

class path_curvature(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, **kwargs):
       super().__init__("path_curvature", {"path" : path, "closed" : closed, **kwargs})

class path_torsion(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, **kwargs):
       super().__init__("path_torsion", {"path" : path, "closed" : closed, **kwargs})

class _path_cut_points(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, dists=None, closed=None, direction=None, **kwargs):
       super().__init__("_path_cut_points", {"path" : path, "dists" : dists, "closed" : closed, "direction" : direction, **kwargs})

class _path_cut_points_recurse(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, dists=None, closed=None, pind=None, dtotal=None, dind=None, result=None, **kwargs):
       super().__init__("_path_cut_points_recurse", {"path" : path, "dists" : dists, "closed" : closed, "pind" : pind, "dtotal" : dtotal, "dind" : dind, "result" : result, **kwargs})

class _path_cut_single(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, dist=None, closed=None, ind=None, eps=None, **kwargs):
       super().__init__("_path_cut_single", {"path" : path, "dist" : dist, "closed" : closed, "ind" : ind, "eps" : eps, **kwargs})

class _path_cuts_normals(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, cuts=None, dirs=None, closed=None, **kwargs):
       super().__init__("_path_cuts_normals", {"path" : path, "cuts" : cuts, "dirs" : dirs, "closed" : closed, **kwargs})

class _path_plane(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, ind=None, i=None, closed=None, **kwargs):
       super().__init__("_path_plane", {"path" : path, "ind" : ind, "i" : i, "closed" : closed, **kwargs})

class _path_cuts_dir(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, cuts=None, closed=None, eps=None, **kwargs):
       super().__init__("_path_cuts_dir", {"path" : path, "cuts" : cuts, "closed" : closed, "eps" : eps, **kwargs})

class path_cut(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, cutdist=None, closed=None, **kwargs):
       super().__init__("path_cut", {"path" : path, "cutdist" : cutdist, "closed" : closed, **kwargs})

class _path_cut_getpaths(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, cutlist=None, closed=None, **kwargs):
       super().__init__("_path_cut_getpaths", {"path" : path, "cutlist" : cutlist, "closed" : closed, **kwargs})

class _cut_to_seg_u_form(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, pathcut=None, path=None, closed=None, **kwargs):
       super().__init__("_cut_to_seg_u_form", {"pathcut" : pathcut, "path" : path, "closed" : closed, **kwargs})

class split_path_at_self_crossings(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, closed=None, eps=None, **kwargs):
       super().__init__("split_path_at_self_crossings", {"path" : path, "closed" : closed, "eps" : eps, **kwargs})

class _tag_self_crossing_subpaths(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, path=None, nonzero=None, closed=None, eps=None, **kwargs):
       super().__init__("_tag_self_crossing_subpaths", {"path" : path, "nonzero" : nonzero, "closed" : closed, "eps" : eps, **kwargs})

class polygon_parts(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, poly=None, nonzero=None, eps=None, **kwargs):
       super().__init__("polygon_parts", {"poly" : poly, "nonzero" : nonzero, "eps" : eps, **kwargs})

class _extreme_angle_fragment(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, seg=None, fragments=None, rightmost=None, eps=None, **kwargs):
       super().__init__("_extreme_angle_fragment", {"seg" : seg, "fragments" : fragments, "rightmost" : rightmost, "eps" : eps, **kwargs})

class _assemble_a_path_from_fragments(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, fragments=None, rightmost=None, startfrag=None, eps=None, **kwargs):
       super().__init__("_assemble_a_path_from_fragments", {"fragments" : fragments, "rightmost" : rightmost, "startfrag" : startfrag, "eps" : eps, **kwargs})

class _assemble_path_fragments(_OpenSCADObject, _Bosl2Mixin):
    def __init__(self, fragments=None, eps=None, _finished=None, **kwargs):
       super().__init__("_assemble_path_fragments", {"fragments" : fragments, "eps" : eps, "_finished" : _finished, **kwargs})

