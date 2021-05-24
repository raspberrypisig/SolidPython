import inspect
import keyword
from pathlib import Path

from types import ModuleType
from typing import List

def indent(s: str) -> str:
    return s.replace("\n", "\n\t")

def calling_module(stack_depth: int = 2) -> ModuleType:
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
        import __main__ as calling_mod  # type: ignore
    return calling_mod

def escpape_openscad_identifier(identifier: str) -> str:
    """
    Append an underscore to any python reserved word.
    Prepend an underscore to any OpenSCAD identifier starting with a digit.
    No-op for all other strings, e.g. 'or' => 'or_', 'other' => 'other'
    """
    new_identifier = identifier

    if identifier in keyword.kwlist:
        new_identifier = identifier + "_"

    if identifier[0].isdigit():
        new_identifier = "_" + identifier

    if new_identifier != identifier:
        print(f"\nFound OpenSCAD code that's not compatible with Python. \n"
              f"Imported OpenSCAD code using `{identifier}` \n"
              f"can be accessed with `{new_identifier}` in SolidPython\n")
    return new_identifier

def unescape_openscad_identifier(identifier: str) -> str:
    """
    Remove trailing underscore for already-subbed python reserved words.
    Remove prepending underscore if remaining identifier starts with a digit.
    No-op for all other strings: e.g. 'or_' => 'or', 'other_' => 'other_'
    """
    if identifier.endswith("_") and identifier[:-1] in keyword.kwlist:
        return identifier[:-1]

    if identifier.startswith("_") and identifier[1].isdigit():
        return identifier[1:]

    return identifier

def resolve_scad_filename(scad_file):
    scad_path = Path(scad_file)
    if scad_path.is_absolute():
        return scad_path

    for p in openscad_library_paths():
        if (p / scad_path).exists():
            return p / scad_path

    return None

def openscad_library_paths() -> List[Path]:
    """
    Return system-dependent OpenSCAD library paths or paths defined in os.environ['OPENSCADPATH']
    """
    import platform
    import os
    import re

    paths = [Path('.')]

    user_path = os.environ.get('OPENSCADPATH')
    if user_path:
        for s in re.split(r'\s*[;:]\s*', user_path):
            paths.append(Path(s))

    default_paths = {
        'Linux':   Path.home() / '.local/share/OpenSCAD/libraries',
        'Darwin':  Path.home() / 'Documents/OpenSCAD/libraries',
        'Windows': Path('My Documents\OpenSCAD\libraries')
    }

    paths.append(default_paths[platform.system()])
    return paths

