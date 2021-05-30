from ..core.scad_import import import_scad

def import_bosl2(name):
    return import_scad(f"BOSL2/{name}.scad", use_not_include=False)

#load the files from std.scad
std = import_bosl2("std")
constants = import_bosl2("constants")
transforms = import_bosl2("transforms")
distributors = import_bosl2("distributors")
mutators = import_bosl2("mutators")
attachments = import_bosl2("attachments")
primitives = import_bosl2("primitives")
shapes = import_bosl2("shapes")
shapes2d = import_bosl2("shapes2d")
masks = import_bosl2("masks")
paths = import_bosl2("paths")
edges = import_bosl2("edges")
arrays = import_bosl2("arrays")
math = import_bosl2("math")
vectors = import_bosl2("vectors")
quaternions = import_bosl2("quaternions")
affine = import_bosl2("affine")
coords = import_bosl2("coords")
geometry = import_bosl2("geometry")
hull = import_bosl2("hull")
regions = import_bosl2("regions")
strings = import_bosl2("strings")
skin = import_bosl2("skin")
vnf = import_bosl2("vnf")
common = import_bosl2("common")
debug = import_bosl2("debug")

