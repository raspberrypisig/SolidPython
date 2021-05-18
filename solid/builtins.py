from typing import Tuple, Union, Sequence
from pathlib import Path

from .object_base import OpenSCADObject, IncludedOpenSCADObject

#base data types -> why do we need them? What happened to the good ol' duck typing?
P2 = Tuple[float, float]
P3 = Tuple[float, float, float]
P4 = Tuple[float, float, float, float]
Vec3 = P3
Vec4 = P4
Vec34 = Union[Vec3, Vec4]
P3s = Sequence[P3]
P23 = Union[P2, P3]
Points = Sequence[P23]
Indexes = Union[Sequence[int], Sequence[Sequence[int]]]
ScadSize = Union[int, Sequence[float]]

#do we need this??? or is this some old unused stuff?
#Is it used in the public interface? git grep says it's unused internally -jeff
OpenSCADObjectPlus = Union[OpenSCADObject, Sequence[OpenSCADObject]]

# = dynamic builtins =
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

from .scad_import import use
use(OPENSCAD_BUILTINS_FILE, builtins=True)


# = Modifier Convenience Methods =
def debug(openscad_obj: OpenSCADObject) -> OpenSCADObject:
    return openscad_obj.set_modifier("#")

def background(openscad_obj: OpenSCADObject) -> OpenSCADObject:
    return openscad_obj.set_modifier("%")

def root(openscad_obj: OpenSCADObject) -> OpenSCADObject:
    return openscad_obj.set_modifier("!")

def disable(openscad_obj: OpenSCADObject) -> OpenSCADObject:
    return openscad_obj.set_modifier("*")

