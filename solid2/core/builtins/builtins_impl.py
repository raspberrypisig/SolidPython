from ..scad_import import use
from ...config import config

# ====================
# = dynamic builtins =
# ====================
"""
    This loads all the built in OpenSCAD functions (like circle, square, color,
    translate.....) from builtins.openscad file.
    I intentionally didn't use a *.scad file because it would be ignore through
    .gitignore und would be a pain to maintain (unless we remove *.scad from
    .gitignore, but that would cause a lot of generated files to show up while
    developing...).
"""
if config.use_implicit_builtins:
    use(config.builtins_file, skip_render=True)
else:
    from .builtin_primitives import *

