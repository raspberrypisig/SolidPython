#! /usr/bin/env python

#    Simple Python OpenSCAD Code Generator
#    Copyright (C) 2009    Philipp Tiefenbacher <wizards23@gmail.com>
#    Amendments & additions, (C) 2011-2019 Evan Jones <evan_t_jones@mac.com>
#
#   License: LGPL 2.1 or later
#

from __future__ import annotations

import datetime
import inspect
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import keyword

from typing import Set, Sequence, List, Callable, Optional, Union, Iterable

from types import ModuleType
from typing import Callable, Iterable, List, Optional, Sequence, Set, Union, Dict

import pkg_resources
import regex as re

from solid.open_scad_object import *

PathStr = Union[Path, str]
AnimFunc = Callable[[Optional[float]], 'OpenSCADObject']

# Words reserved in Python but not OpenSCAD
# Re: https://github.com/SolidCode/SolidPython/issues/99

PYTHON_ONLY_RESERVED_WORDS = keyword.kwlist

# =========================================
# = Rendering Python code to OpenSCAD code=
# =========================================
def _find_include_strings(obj: Union[IncludedOpenSCADObject, OpenSCADObject]) -> Set[str]:
    include_strings = set()
    if isinstance(obj, IncludedOpenSCADObject):
        include_strings.add(obj.include_string)
    for child in obj.children:
        include_strings.update(_find_include_strings(child))
    # We also accept IncludedOpenSCADObject instances as parameters to functions, 
    # so search in obj.params as well
    for param in obj.params.values():
        if isinstance(param, OpenSCADObject):
            include_strings.update(_find_include_strings(param))
    return include_strings

def scad_render(scad_object: OpenSCADObject, file_header: str = '') -> str:
    # Make this object the root of the tree
    root = scad_object

    # Scan the tree for all instances of
    # IncludedOpenSCADObject, storing their strings
    include_strings = _find_include_strings(root)

    # and render the string
    includes = ''.join(include_strings) + "\n"
    scad_body = root._render()

    if file_header and not file_header.endswith('\n'): 
        file_header += '\n'

    return file_header + includes + scad_body

def scad_render_animated(func_to_animate: AnimFunc, 
                         steps: int =20, 
                         back_and_forth: bool=True, 
                         file_header: str='') -> str:
    # func_to_animate takes a single float argument, _time in [0, 1), and
    # returns an OpenSCADObject instance.
    #
    # Outputs an OpenSCAD file with func_to_animate() evaluated at "steps"
    # points between 0 & 1, with time never evaluated at exactly 1

    # If back_and_forth is True, smoothly animate the full extent of the motion
    # and then reverse it to the beginning; this avoids skipping between beginning
    # and end of the animated motion

    # NOTE: This is a hacky way to solve a simple problem.  To use OpenSCAD's
    # animation feature, our code needs to respond to changes in the value
    # of the OpenSCAD variable $t, but I can't think of a way to get a
    # float variable from our code and put it into the actual SCAD code.
    # Instead, we just evaluate our code at each desired step, and write it
    # all out in the SCAD code for each case, with an if/else tree.  Depending
    # on the number of steps, this could create hundreds of times more SCAD
    # code than is needed.  But... it does work, with minimal Python code, so
    # here it is. Better solutions welcome. -ETJ 28 Mar 2013

    # NOTE: information on the OpenSCAD manual wiki as of November 2012 implies
    # that the OpenSCAD app does its animation irregularly; sometimes it animates
    # one loop in steps iterations, and sometimes in (steps + 1).  Do it here
    # in steps iterations, meaning that we won't officially reach $t =1.

    # Note also that we check for ranges of time rather than equality; this
    # should avoid any rounding error problems, and doesn't require the file
    # to be animated with an identical number of steps to the way it was
    # created. -ETJ 28 Mar 2013
    scad_obj = func_to_animate(_time=0)  # type: ignore
    include_strings = _find_include_strings(scad_obj)
    # and render the string
    includes = ''.join(include_strings) + "\n"

    rendered_string = file_header + includes

    if back_and_forth:
        steps *= 2

    for i in range(steps):
        time = i * 1.0 / steps
        end_time = (i + 1) * 1.0 / steps
        eval_time = time
        # Looping back and forth means there's no jump between the start and
        # end position
        if back_and_forth:
            if time < 0.5:
                eval_time = time * 2
            else:
                eval_time = 2 - 2 * time
        scad_obj = func_to_animate(_time=eval_time)  # type: ignore

        scad_str = indent(scad_obj._render())
        rendered_string += f"if ($t >= {time} && $t < {end_time}){{" \
                           f"   {scad_str}\n" \
                           f"}}\n"
    return rendered_string

def scad_render_animated_file(func_to_animate:AnimFunc, 
                              steps: int=20, 
                              back_and_forth: bool=True, 
                              filepath: Optional[str]=None, 
                              out_dir: PathStr=None, 
                              file_header: str='', 
                              include_orig_code: bool=True) -> str:
    rendered_string = scad_render_animated(func_to_animate, steps, 
                                            back_and_forth, file_header)
    return _write_code_to_file(rendered_string, filepath, out_dir=out_dir, 
                include_orig_code=include_orig_code)

def scad_render_to_file(scad_object: OpenSCADObject,
                        filepath: PathStr=None, 
                        out_dir: PathStr=None,
                        file_header: str='', 
                        include_orig_code: bool=True) -> str:
    header = file_header
    if include_orig_code:
        version = _get_version()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"// Generated by SolidPython {version} on {date}\n" + file_header

    rendered_string = scad_render(scad_object, header)
    return _write_code_to_file(rendered_string, filepath, out_dir, include_orig_code)

def _write_code_to_file(rendered_string: str, 
                        filepath: PathStr=None, 
                        out_dir: PathStr=None, 
                        include_orig_code: bool=True) -> str:
    try:
        calling_file = Path(calling_module(stack_depth=3).__file__).absolute()
        # Output path is determined four ways:
        # -- If filepath is supplied, use filepath
        # -- If no filepath is supplied but an out_dir is supplied, 
        #       give the calling file a .scad suffix and put it in out_dir
        # -- If neither filepath nor out_dir are supplied, give the new
        #       file a .scad suffix and put it next to the calling file
        # -- If no path info is supplied and we can't find a calling file 
        #       (i.e, this is being called from an interactive terminal), 
        #       write a file to Path.cwd() / 'solid.scad'
        out_path = Path()
        if filepath:
            out_path = Path(filepath)
        elif out_dir:
            odp = Path(out_dir)
            if not odp.exists():
                odp.mkdir()
            out_path = odp / calling_file.with_suffix('.scad').name
        else:
            out_path = calling_file.with_suffix('.scad')
        
        if include_orig_code:
            rendered_string += sp_code_in_scad_comment(calling_file)
    except AttributeError as e:
        # If no calling_file was found, this is being called from the terminal.
        # We can't read original code from a file, so don't try,
        # and can't read filename from the calling file either, so just save to
        # solid.scad.

        if filepath:
            out_path = Path(filepath)
        else:
            odp = Path(out_dir) if out_dir else Path.cwd()
            if not odp.exists():
                odp.mkdir()
            out_path = odp / 'solid.scad'

    out_path.write_text(rendered_string)
    return out_path.absolute().as_posix()

def _get_version() -> str:
    """
    Returns SolidPython version
    Returns '<Unknown>' if no version can be found
    """
    version = '<Unknown>'
    try:
        # if SolidPython is installed use `pkg_resources`
        version = pkg_resources.get_distribution('solidpython').version

    except pkg_resources.DistributionNotFound:
        # if the running SolidPython is not the one installed via pip,
        # try to read it from the project setup file
        version_pattern = re.compile(r"version = ['\"]([^'\"]*)['\"]")
        version_file_path = Path(__file__).parent.parent / 'pyproject.toml'
        if version_file_path.exists():
            version_match = version_pattern.search(version_file_path.read_text())
            if version_match:
                version = version_match.group(1)
    return version

def sp_code_in_scad_comment(calling_file: PathStr) -> str:
    """
    Once a SCAD file has been created, it's difficult to reconstruct
    how it got there, since it has no variables, modules, etc.  So, include
    the Python code that generated the scad code as comments at the end of
    the SCAD code
    """
    pyopenscad_str = Path(calling_file).read_text()

    # TODO: optimally, this would also include a version number and
    # git hash (& date & github URL?) for the version of solidpython used
    # to create a given file; That would future-proof any given SP-created
    # code because it would point to the relevant dependencies as well as
    # the actual code
    pyopenscad_str = (f"\n"
                      f"/***********************************************\n"
                      f"*********      SolidPython code:      **********\n"
                      f"************************************************\n"
                      f" \n"
                      f"{pyopenscad_str} \n"
                      f" \n"
                      f"************************************************/\n")
    return pyopenscad_str


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

    if keyword in PYTHON_ONLY_RESERVED_WORDS:
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
