# Some __init__ magic so we can include all solidpython code with:
#   from solid import *
#   from solid.utils import *
from .open_scad_render import scad_render,\
                              scad_render_to_file,\
                              scad_render_animated,\
                              scad_render_animated_file

from .open_scad_object import OpenSCADObject,\
                              IncludedOpenSCADObject
from .objects import *
from .patch_euclid import run_euclid_patch

# Type hints
from .objects import P2, P3, P4, Vec3 , Vec4, Vec34, P3s, P23, Points, Indexes, ScadSize, OpenSCADObjectPlus
