from typing import Optional, Union, List, Sequence, Dict
from types import SimpleNamespace
from pathlib import Path
PathStr = Union[Path, str]

from .helpers import calling_module, resolve_scad_filename, escpape_openscad_identifier
from .object_base import OpenSCADObject, IncludedOpenSCADObject

# ===========
# = Parsing =
# ===========
def parse_scad_callables(filename: str) -> List[dict]:
    from .libs.py_scadparser import scad_parser

    modules, functions, _ = scad_parser.parseFile(filename)

    callables = []
    for c in modules + functions:
        args = []
        kwargs = []

        #for some reason solidpython needs to treat all openscad arguments as if
        #they where optional. I don't know why, but at least to pass the tests
        #it's neccessary to handle it like this !?!?!
        for p in c.parameters:
            kwargs.append(p.name)
            #if p.optional:
            #    kwargs.append(p.name)
            #else:
            #    args.append(p.name)

        callables.append({'name': c.name, 'args': args, 'kwargs': kwargs})

    return callables


def check_signature(name, args_def, kwargs_def, *args, **kwargs):
    #check whether the args and kwargs fit a function signature definition
    #defined with args_def and kwargs_def. args_def and kwargs_def are lists
    #of all parameter names the function {name} accepts

    if len(args) + len(kwargs) > len(args_def) + len(kwargs_def):
        raise TypeError(f"too many arguments to {name}(...)")

    full_defs = args_def + kwargs_def

    full_args_tuples = list(zip(full_defs, args))
    full_args_tuples += list(zip(kwargs.keys(), kwargs.values()))

    full_args_names = [x[0] for x in full_args_tuples]

    args_def_copy = args_def[:]
    kwargs_def_copy = kwargs_def[:]

    while full_args_names and (args_def_copy or kwargs_def_copy):
        a = full_args_names.pop()

        if a in args_def_copy:
            args_def_copy.remove(a)

        elif a in kwargs_def_copy:
            kwargs_def_copy.remove(a)

        else:
            raise TypeError(f"{name}(...) has no parameter {a} or it is already occupied by a positional argument")

    #are there still unmatched parameters left?
    if full_args_names:
        if not args_def_copy and not kwargs_def_copy:
            raise TypeError(f"{name}(...) too many arguments")
        else:
            assert(False)

    #are there still unmet args in args_def?
    if args_def_copy and not full_args_names:
        raise TypeError(f"not enough parameters to {name}(...)")

def create_openscad_wrapper_from_symbols(name,
                                         args,
                                         kwargs,
                                         filename,
                                         use_not_include):

    #this is the function we'll bind to the init function of the new class
    #that we'll create to represent the openscad function
    def init_func(self, *args, **kwargs):

        #check whether the *args and **kwargs meet our parameter definitions
        check_signature(name, args_def, kwargs_def, *args, **kwargs)

        #zip the args with the def dicts and update it with kwargs
        #to get a single complete kwargs list
        #->OpenSCADObject Interface
        params = dict(zip(args_def + kwargs_def, args))
        params.update(kwargs)

        #call IncludedOpenSCADObject ctor
        super(self.__class__, self).__init__(name, params, filename, use_not_include)


    #escape all identifiers
    name = escpape_openscad_identifier(name)
    args_def = list(map(escpape_openscad_identifier, args))
    kwargs_def = list(map(escpape_openscad_identifier, kwargs))

    #create the class and bind an "instance of" newclass_init_func -- wrapped
    #in init_func -- to it's __init__ function
    class_declaration = type(name, (IncludedOpenSCADObject,), {"__init__" : init_func})

    return class_declaration


# ===========================
# = IMPORTING OPENSCAD CODE =
# ===========================
module_cache_by_name = {}
module_cache_by_resolved_filename = {}

def import_scad(scad_file_or_dir: PathStr, dest_namespace = None) -> SimpleNamespace:
    '''
    Recursively look in current directory & OpenSCAD library directories for
        OpenSCAD files. Create Python mappings for all OpenSCAD modules & functions
    Return a namespace or raise ValueError if no scad files found
    '''
    global module_cache_by_name, module_cache_by_resolved_filename

    if scad_file_or_dir in module_cache_by_name.keys():
        return module_cache_by_name[scad_file_or_dir]

    resolved_scad = resolve_scad_filename(scad_file_or_dir)

    if resolved_scad in module_cache_by_resolved_filename.keys():
        return module_cache_by_resolved_filename[resolved_scad]

    if not resolved_scad:
        raise ValueError(f'Could not find .scad files at or under {scad_file_or_dir}.')

    namespace = _import_scad(resolved_scad, dest_namespace)

    if not namespace:
        raise ValueError(f'Could not import .scad file {resolved_scad.as_posix()}.')

    module_cache_by_name[scad_file_or_dir] = namespace
    module_cache_by_resolved_filename[resolved_scad] = namespace
    return namespace

def _import_scad(scad: Path, dest_namespace=None) -> Optional[SimpleNamespace]:
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
    if not scad.exists():
        return None

    if dest_namespace == None:
        dest_namespace = SimpleNamespace()
    if scad.is_file():
        use(scad.absolute(), dest_namespace_dict=dest_namespace.__dict__)
        return dest_namespace

    assert(scad.is_dir())

    for f in scad.iterdir():
        #skip non .scad files
        if f.suffix != ".scad":
            continue

        #recurse into the files and subdirs
        subspace = _import_scad(f)
        if subspace:
            identifier = escpape_openscad_identifier(f.stem)
            setattr(dest_namespace, identifier, subspace)

    return dest_namespace

    assert(False)


# use() & include() mimic OpenSCAD's use/include mechanics.
# -- use() makes methods in scad_file_path.scad available to be called.
# --include() makes those methods available AND executes all code in
#   scad_file_path.scad, which may have side effects.
#   Unless you have a specific need, call use().
def use(scad_file_path: PathStr, use_not_include: bool = True, dest_namespace_dict: Dict = None, builtins=False):
    """
    Opens scad_file_path, parses it for all usable calls,
    and adds them to caller's namespace.
    """
    #resolve filename
    scad_file_path = resolve_scad_filename(scad_file_path)

    #get symbols from the parser
    symbols_dicts = parse_scad_callables(scad_file_path)

    #set the dest_namespace to the module calling this function
    if dest_namespace_dict == None:
        dest_namespace_dict = calling_module(2).__dict__

    #create a wrapper for each module and function in symbols
    for sd in symbols_dicts:
        c = create_openscad_wrapper_from_symbols(sd["name"],
                                                 sd["args"],
                                                 sd["kwargs"],
                                                 scad_file_path if not builtins else None,
                                                 use_not_include)
        #add it to the dest_namespace
        dest_namespace_dict[sd["name"]] = c

    #return the symbols (they are used to add the builtins as OpenSCADObject functions, see builtins.py)
    return symbols_dicts

def include(scad_file_path: PathStr) -> bool:
    return use(scad_file_path, use_not_include=False, dest_namespace_dict = calling_module(3).__dict__)

