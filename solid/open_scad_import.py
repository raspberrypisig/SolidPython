from typing import Optional, Union, List, Sequence, Dict
from types import SimpleNamespace
from pathlib import Path
PathStr = Union[Path, str]

from solid.utilityFunctions import subbed_keyword

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
    class_name = subbed_keyword(class_name)

    args = map(subbed_keyword, args)  # type: ignore
    for arg in args:
        args_str += ', ' + arg
        args_pairs += f"'{arg}':{arg}, "

    # kwargs have a default value defined in their SCAD versions.  We don't
    # care what that default value will be (SCAD will take care of that), just
    # that one is defined.
    kwargs = map(subbed_keyword, kwargs)  # type: ignore
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

# ===========================
# = IMPORTING OPENSCAD CODE =
# ===========================
def import_scad(scad_file_or_dir: PathStr) -> SimpleNamespace:
    '''
    Recursively look in current directory & OpenSCAD library directories for
        OpenSCAD files. Create Python mappings for all OpenSCAD modules & functions
    Return a namespace or raise ValueError if no scad files found
    '''
    scad = Path(scad_file_or_dir)
    candidates: List[Path] = [scad]
    if not scad.is_absolute():
        candidates = [d/scad for d in _openscad_library_paths()]

    for candidate_path in candidates:
        namespace = _import_scad(candidate_path)
        if namespace is not None:
            return namespace
    raise ValueError(f'Could not find .scad files at or under {scad}. \nLocations searched were: {candidates}')

def _import_scad(scad: Path) -> Optional[SimpleNamespace]:
    '''
    cases:
        single scad file:
            return a namespace populated with `use()`
        directory
            recurse into all subdirectories and *.scad files
            return namespace if scad files are underneath, otherwise None
        non-scad file:
            return None            
    '''
    namespace: Optional[SimpleNamespace] = None
    if scad.is_file() and scad.suffix == '.scad':
        namespace = SimpleNamespace()
        use(scad.absolute(), dest_namespace_dict=namespace.__dict__)
    elif scad.is_dir():
        subspaces = [(f, _import_scad(f)) for f in scad.iterdir() if f.is_dir() or f.suffix == '.scad']
        for f, subspace in subspaces:
            if subspace:
                if namespace is None:
                    namespace = SimpleNamespace()
                # Add a subspace to namespace named by the file/dir it represents
                setattr(namespace, f.stem, subspace)

    return namespace
   
def _openscad_library_paths() -> List[Path]:
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

def _find_library(library_name: PathStr) -> Path:
    result = Path(library_name)

    if not result.is_absolute():
        paths = _openscad_library_paths()
        for p in paths:
            f = p / result
            # print(f'Checking {f} -> {f.exists()}')
            if f.exists():
                result = f

    return result
 
# use() & include() mimic OpenSCAD's use/include mechanics.
# -- use() makes methods in scad_file_path.scad available to be called.
# --include() makes those methods available AND executes all code in
#   scad_file_path.scad, which may have side effects.
#   Unless you have a specific need, call use().
def use(scad_file_path: PathStr, use_not_include: bool = True, dest_namespace_dict: Dict = None):
    """
    Opens scad_file_path, parses it for all usable calls,
    and adds them to caller's namespace.
    """
    scad_file_path = _find_library(scad_file_path) 

    symbols_dicts = parse_scad_callables(scad_file_path)

    for sd in symbols_dicts:
        class_str = new_openscad_class_str(sd['name'], sd['args'], sd['kwargs'],
                                           scad_file_path.as_posix(), use_not_include)
        # If this is called from 'include', we have to look deeper in the stack
        # to find the right module to add the new class to.
        if dest_namespace_dict is None:
            stack_depth = 2 if use_not_include else 3
            dest_namespace_dict = calling_module(stack_depth).__dict__
        try:
            exec(class_str, dest_namespace_dict)
        except Exception as e:
            classname = sd['name']
            msg = f"Unable to import SCAD module: `{classname}` from `{scad_file_path.name}`, with error: {e}"
            print(msg)

    return True

def include(scad_file_path: PathStr) -> bool:
    return use(scad_file_path, use_not_include=False)

