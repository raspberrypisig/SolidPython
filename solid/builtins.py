from pathlib import Path

from .object_base import OpenSCADObject
from .helpers import escpape_openscad_identifier
from .scad_import import use

# ====================
# = dynamic builtins =
# ====================
"""
    This block loads all the built in OpenSCAD functions (like circle, square,
    color, translate.....) from builtins.openscad file.
    I intentionally didn't use a *.scad file because it would be ignore through
    .gitignore und would be a pain to maintain (unless we remove *.scad from
    .gitignore, but that would cause a lot of generated files to show up while
    developing...). The only drawback is, that you have to setup your editor to
    also use OpenScad syntax highlighting for *.openscad files.
"""
OPENSCAD_BUILTINS_FILE = Path(__file__).absolute().parent / "builtins.openscad"

builtins_symbols = use(OPENSCAD_BUILTINS_FILE, builtins=True)

# ========================
# = Cascading Operations =
# ========================
"""
    This is a "hack" to add cascading operations like:
        cube([10, 20, 30]).translate([-5, 0, 0])
    It simply takes every symbol (function or module name) and adds a wrapper
    function to the OpenSCADObject class. :D

    I really like this style and I don't see any reason why SolidPython should
    not support it. Are there any?
"""
def add_to_openSCADObject(name):
    def wrapper(self, *args, **kwargs):
        #retrieve the builtin from the local namespace
        builtin = globals()[name]
        #and return an instance of it with self as child
        return builtin(*args, **kwargs)(self)

    #set OpenSCADObject.{name} = wrapper
    #this means for example solidpython code like
    #   c.translate(...)
    #       will call the wrapper and will retrieve an instance of an translate
    #       node wrapped around c
    setattr(OpenSCADObject, name, wrapper)

cascading_builtins = ("union difference intersection intersection_for translate " +\
                      "scale rotate mirror resize color offset hull render " +\
                      "linear_extrude rotate_extrude projection surface").split(" ")

for b in cascading_builtins:
    add_to_openSCADObject(escpape_openscad_identifier(b))

