import platform
import os
import re
import inspect
import keyword
from pathlib import Path

#don't do relative imports on the global scope to be able to import this file
#from "everywhere"

def indent(s):
    res = ''
    for ns in s.splitlines(True):
        res += f'\t{ns}'

    return res

def calling_module(stack_depth = 2):
    """
    Returns the module *2* back in the frame stack.  That means:
    code in module A calls code in module B, which asks calling_module()
    for module A.

    This means that we have to know exactly how far back in the stack
    our desired module is; if code in module B calls another function in 
    module B, we have to increase the stack_depth argument to account for
    this.

    Got that?
    """
    frm = inspect.stack()[stack_depth]
    calling_mod = inspect.getmodule(frm[0])

    # If calling_mod is None, this is being called from an interactive session.
    # Return that module.  (Note that __main__ doesn't have a __file__ attr,
    # but that's caught elsewhere.)
    if not calling_mod:
        import __main__ as main_module
        return main_module

    return calling_mod

def escpape_openscad_identifier(identifier):
    """
    Append an underscore to any python reserved word.
    Prepend an underscore to any OpenSCAD identifier starting with a digit.
    No-op for all other strings, e.g. 'or' => 'or_', 'other' => 'other'
    """
    if identifier in keyword.kwlist or identifier[0].isdigit():
        return "_" + identifier

    if identifier[0] == "$":
        return "_" + identifier[1:]

    return identifier

def unescape_openscad_identifier(identifier):
    """
    Remove trailing underscore for already-subbed python reserved words.
    Remove prepending underscore if remaining identifier starts with a digit.
    No-op for all other strings: e.g. 'or_' => 'or', 'other_' => 'other_'
    """
    if identifier.startswith("_") and identifier[1:] in keyword.kwlist:
        return identifier[1:]

    if identifier.startswith("_") and identifier[1].isdigit():
        return identifier[1:]

    if identifier.startswith("_"):
        return "$" + identifier[1:]

    return identifier

def resolve_scad_filename(scad_file):
    scad_path = Path(scad_file)
    if scad_path.is_absolute():
        return scad_path

    for p in openscad_library_paths():
        if (p / scad_path).exists():
            return p / scad_path

    return None

def openscad_library_paths():
    """
    Return system-dependent OpenSCAD library paths or paths defined in
    os.environ['OPENSCADPATH'] """
    paths = [Path('.')]

    user_path = os.environ.get('OPENSCADPATH')
    if user_path:
        for s in re.split(r'\s*[;:]\s*', user_path):
            paths.append(Path(s))

    #user wide path
    default_paths = {
        'Linux':   Path.home() / '.local/share/OpenSCAD/libraries',
        'Darwin':  Path.home() / 'Documents/OpenSCAD/libraries',
        'Windows': Path('My Documents\OpenSCAD\libraries')
    }

    paths.append(default_paths[platform.system()])

    #system wide paths
    if platform.system() == 'Linux':
        #sorry, but I've no clue what the paths are on other operating systems
        paths.append("/usr/share/openscad/libraries")

    return paths

