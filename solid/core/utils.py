import platform
import os
import re
import inspect
import keyword
from pathlib import Path

from ..config import config

#don't do relative imports on the global scope to be able to import this file
#from "everywhere"

def indent(s):
    res = ''
    for ns in s.splitlines(True):
        res += f'\t{ns}'

    return res

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

    for p in config.openscad_library_paths:
        if (p / scad_path).exists():
            return p / scad_path

    return None

