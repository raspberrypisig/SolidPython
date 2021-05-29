# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================

from solid import *

# =============
# = Extension =
# =============
# This is more or less the same as -- the regular SolidPython -- does when
# rendering a "scene". It appends the python source to the end of the *.scad
# file. In otherwords: the contents of this file we be appended as comment to
# the generated *.scad file.
#
# If you like this, you can simply but this extension (function including the
# register call) into a python module and import it in your project that'll do
# it.
#
def attach_code_post_render(root):
    #find the "root" file
    calling_file = None

    import __main__
    # not called from a terminal?
    if hasattr(__main__, "__file__"):
        # extract filename and replace suffix
        calling_file = Path(__main__.__file__).absolute()
        outfile = calling_file.with_suffix(".scad")

    if not calling_file:
        return '' # no code available. Called from withing a python shell

    assert(calling_file.exists())

    # read source file
    with calling_file.open("r") as f:
        code_str = f.read()

        # escape /* and */ because otherwise it would end this comment block which
        # we use to inject the solid code
        code_str = code_str.replace("/*", "/_*")
        code_str = code_str.replace("*/", "*_/")

        # return the string to be appended to the *.scad file
        return f'/* Generated from the following ExpSolid code:\n\n' +\
               f'{code_str}*/'

    assert(False)

# register the post_render extension. This hooks it into the "_render" routine.
# It will be called after the root gets rendered. It's return string will be
# appended to the rendered string.
from solid.core.extension_manager import default_extension_manager
default_extension_manager.register_post_render(attach_code_post_render)

# =============

c = cube(10)

c.save_as_scad()

