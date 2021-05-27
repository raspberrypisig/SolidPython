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
_OPENSCAD_BUILTINS_FILE = Path(__file__).absolute().parent / "builtins.openscad"

_builtins_symbols = use(_OPENSCAD_BUILTINS_FILE, builtins=True)

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
def _add_to_openSCADObject(name):
    """
        This functions adds a (lambda) wrapper for each builtin as member function
        to OpenSCADObject.

        It retrieves the builtin class from the local namespace and creates a lambda
        wrapper with the signature (self, *args, **kwargs) for each builtin and
        binds it to OpenSCADObject.

        It basicly does this:

    OpenSCADObject.<buildin> = lambda self, *args, **kwargs : builtin(*args, **kwargs)(self)

    """
    #get the builtin
    builtin = globals()[name]

    #wrap a lambda func around it
    func = lambda self, *args, **kwargs : builtin(*args, **kwargs)(self)

    #bind it to OpenSCADObject
    setattr(OpenSCADObject, name, func)

#the list of builtins that should be added as member functions to OpenSCADObject
#(it makes no sense to include circle or cube...)
_cascading_builtins = ("union difference intersection intersection_for translate " +\
                      "scale rotate mirror resize color offset hull render " +\
                      "linear_extrude rotate_extrude projection surface").split(" ")

for b in _cascading_builtins:
    _add_to_openSCADObject(escpape_openscad_identifier(b))

