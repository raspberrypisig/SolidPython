# Some __init__ magic so we can include all solidpython code with:
#   from solid import *
#   from solid.utils import *
from .scad_render import scad_render,\
                         scad_render_to_file,\
                         scad_render_animated,\
                         scad_render_animated_file

from .object_base import OpenSCADObject,\
                         IncludedOpenSCADObject

from .builtins import *
from .scad_import import import_scad, use

from .extensions.convenience import *

#why is / was this included here and not in solid.utils?
#from .extensions.patch_euclid import run_euclid_patch

