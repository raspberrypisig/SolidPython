#! /usr/bin/env python

#    Simple Python OpenSCAD Code Generator
#    Copyright (C) 2009    Philipp Tiefenbacher <wizards23@gmail.com>
#    Amendments & additions, (C) 2011-2019 Evan Jones <evan_t_jones@mac.com>
#
#   License: LGPL 2.1 or later
#

from __future__ import annotations

import keyword

# ===========
# = Parsing =
# ===========
def parse_scad_callables(filename: str) -> List[dict]:
    from .py_scadparser import scad_parser

    _, _, modules, functions, _ = scad_parser.parseFile(filename)

    callables = []
    for c in modules + functions:
        args = []
        kwargs = []

        for p in c.parameters:
            if p.optional:
                kwargs.append(p.name)
            else:
                args.append(p.name)

        callables.append({'name': c.name, 'args': args, 'kwargs': kwargs})

    return callables

def new_openscad_class_str(class_name: str,
                           args: Sequence[str] = None,
                           kwargs: Sequence[str] = None,
                           include_file_path: Optional[str] = None,
                           use_not_include: bool = True) -> str:
    args_str = ''
    args_pairs = ''

    args = args or []
    kwargs = kwargs or []

    # Re: https://github.com/SolidCode/SolidPython/issues/99
    # Don't allow any reserved words as argument names or module names
    # (They might be valid OpenSCAD argument names, but not in Python)
    class_name = _subbed_keyword(class_name)

    args = map(_subbed_keyword, args)  # type: ignore
    for arg in args:
        args_str += ', ' + arg
        args_pairs += f"'{arg}':{arg}, "

    # kwargs have a default value defined in their SCAD versions.  We don't
    # care what that default value will be (SCAD will take care of that), just
    # that one is defined.
    kwargs = map(_subbed_keyword, kwargs)  # type: ignore
    for kwarg in kwargs:
        args_str += f', {kwarg}=None'
        args_pairs += f"'{kwarg}':{kwarg}, "

    if include_file_path:
        # include_file_path may include backslashes on Windows; escape them
        # again here so any backslashes don't get used as escape characters
        # themselves
        include_file_str = Path(include_file_path).as_posix()

        # NOTE the explicit import of 'solid' below. This is a fix for:
        # https://github.com/SolidCode/SolidPython/issues/20 -ETJ 16 Jan 2014
        result = (f"import solid\n"
                  f"class {class_name}(solid.IncludedOpenSCADObject):\n"
                  f"   def __init__(self{args_str}, **kwargs):\n"
                  f"       solid.IncludedOpenSCADObject.__init__(self, '{class_name}', {{{args_pairs} }}, include_file_path='{include_file_str}', use_not_include={use_not_include}, **kwargs )\n"
                  f"   \n"
                  f"\n")
    else:
        result = (f"class {class_name}(OpenSCADObject):\n"
                  f"   def __init__(self{args_str}):\n"
                  f"       OpenSCADObject.__init__(self, '{class_name}', {{{args_pairs }}})\n"
                  f"   \n"
                  f"\n")

    return result

def _subbed_keyword(keyword: str) -> str:
    """
    Append an underscore to any python reserved word.
    Prepend an underscore to any OpenSCAD identifier starting with a digit.
    No-op for all other strings, e.g. 'or' => 'or_', 'other' => 'other'
    """
    new_key = keyword

    if keyword in keyword.kwlist:
        new_key = keyword + "_"

    if keyword[0].isdigit():
        new_key = "_" + keyword

    if new_key != keyword:
        print(f"\nFound OpenSCAD code that's not compatible with Python. \n"
              f"Imported OpenSCAD code using `{keyword}` \n"
              f"can be accessed with `{new_key}` in SolidPython\n")
    return new_key

# now that we have the base class defined, we can do a circular import
from . import objects

def indent(s: str) -> str:
    return s.replace("\n", "\n\t")
