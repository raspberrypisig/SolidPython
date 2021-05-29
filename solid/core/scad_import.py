from types import SimpleNamespace
import inspect

from .utils import resolve_scad_filename, escpape_openscad_identifier
from .object_base import OpenSCADObject

# ===========
# = Parsing =
# ===========
def parse_scad_callables(filename):
    from ..libs.py_scadparser import scad_parser

    modules, functions, _ = scad_parser.parseFile(filename)

    callables = []
    for c in modules + functions:
        args = [p.name for p in c.parameters if not p.optional]
        kwargs = [p.name for p in c.parameters if p.optional]

        callables.append({'name': c.name, 'args': args, 'kwargs': kwargs})

    return callables

def check_signature(name, args_def, kwargs_def, *args, **kwargs):
    #check whether the args and kwargs fit a function signature definition
    #defined with args_def and kwargs_def. args_def and kwargs_def are lists
    #of all parameter names the function {name} accepts

    if len(args) + len(kwargs) > len(args_def) + len(kwargs_def):
        raise TypeError(f"too many arguments to {name}(...)")

    full_args_tuples = list(zip(args_def + kwargs_def, args))
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
            raise TypeError(f"{name}(...) has no parameter {a} or it is " +\
                            f"already occupied by a positional argument")

    #are there still unmatched parameters left?
    if full_args_names:
        if not args_def_copy and not kwargs_def_copy:
            raise TypeError(f"{name}(...) too many arguments")
        else:
            assert(False)

    #are there still unmet args in args_def?
    if args_def_copy and not full_args_names:
        raise TypeError(f"not enough parameters to {name}(...)")

def create_openscad_wrapper_from_symbols(name, args, kwargs, include_str):

    #this is the function we'll bind to the init function of the new class
    #that we'll create to represent the openscad function
    def init_func(self, *args, **kwargs):

        #check whether the *args and **kwargs meet our parameter definitions
        check_signature(name, args_def, kwargs_def, *args, **kwargs)

        #zip the args with the def dicts and update it with kwargs
        #to get a single complete kwargs list
        params = dict(zip(args_def + kwargs_def, args))
        params.update(kwargs)

        #call OpenSCADObject ctor
        return super(self.__class__, self).__init__(name, params, include_str)


    #escape all identifiers
    name = escpape_openscad_identifier(name)
    args_def = list(map(escpape_openscad_identifier, args))
    kwargs_def = list(map(escpape_openscad_identifier, kwargs))

    #create the class and bind an "instance of" _init_func it's __init__ function
    class_declaration = type(name, (OpenSCADObject,), {"__init__" : init_func})

    #add the function signature as __doc__ string, so ExpSolidNamespace can
    #display it
    param_str = ",".join([str(x) for x in args])
    param_str += "," if param_str else ''
    param_str += ",".join([str(x) + "=..." for x in kwargs])
    class_declaration.__doc__ = f'{name}({param_str})'

    return class_declaration

class ExpSolidNamespace(SimpleNamespace):
    """
    we create our own namespace class for imported openscad modules to be able
    to overwrite the __repr__ func. This enables in a python shell

        s = import_scad("...")
        print(s)

    to list the "contents" of this namespace
    """
    def __init__(self, filename):
        super().__init__()
        self.__filename__ = filename

    def __repr__(self):
        node_strings = []
        for k in sorted(self.__dict__):
            if not k.startswith("__"):
                i = self.__dict__[k]
                if isinstance(i, ExpSolidNamespace):
                    node_strings += [f'\t{k}']
                else:
                    node_strings += [f'\t{i.__doc__}']

        return '\n'.join([f'{self.__filename__}:'] + node_strings)

# ===========================
# = IMPORTING OPENSCAD CODE =
# ===========================
module_cache_by_resolved_filename = {}

def import_scad(scad_file_or_dir, dest_namespace = None):
    '''
    Recursively look in current directory & OpenSCAD library directories for
    OpenSCAD files. Create Python mappings for all OpenSCAD modules & functions
    Return a namespace or raise ValueError if no scad files found
    '''
    global module_cache_by_resolved_filename

    resolved_scad = resolve_scad_filename(scad_file_or_dir)

    if not resolved_scad:
        raise ValueError(f'Could not find .scad files at or under ' + \
                         f'{scad_file_or_dir}.')

    if resolved_scad in module_cache_by_resolved_filename.keys():
        return module_cache_by_resolved_filename[resolved_scad]

    namespace = load_package(resolved_scad, dest_namespace)

    if not namespace:
        raise ValueError(f'Could not import .scad file ' + \
                         f'{resolved_scad.as_posix()}.')

    module_cache_by_resolved_filename[resolved_scad] = namespace
    return namespace

def load_package(scad, dest_namespace=None):
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
        dest_namespace = ExpSolidNamespace(scad)

    if scad.is_file():
        use(scad.absolute(), dest_namespace_dict=dest_namespace.__dict__)
        return dest_namespace

    assert(scad.is_dir())

    for f in scad.iterdir():
        #skip non .scad files
        if f.suffix != ".scad":
            continue

        #recurse into the files and subdirs
        subspace = import_scad(f)
        if subspace:
            identifier = escpape_openscad_identifier(f.stem)
            setattr(dest_namespace, identifier, subspace)

    return dest_namespace

# use() & include() mimic OpenSCAD's use/include mechanics.
# -- use() makes methods in scad_file_path.scad available to be called.
# --include() makes those methods available AND executes all code in
#   scad_file_path.scad, which may have side effects.
#   Unless you have a specific need, call use().
def use(scad_file_path, use_not_include = True,
        dest_namespace_dict=None, builtins=False):
    """
    Opens scad_file_path, parses it for all usable calls,
    and adds them to caller's namespace.
    """
    def include_str_from_filename(filename, use_not_include, builtins):
        if not filename or builtins:
            return None

        include_file_path = resolve_scad_filename(filename)
        use_str = 'use' if use_not_include else 'include'
        return f'{use_str} <{include_file_path}>\n'

    def get_callers_namespace_dict(depth=2):
        frame = inspect.currentframe()
        for i in range(depth):
            frame = frame.f_back
        return frame.f_locals

    #resolve filename
    scad_file_path = resolve_scad_filename(scad_file_path)

    #get symbols from the parser
    symbols_dicts = parse_scad_callables(scad_file_path)

    #set the dest_namespace to the module calling this function
    if dest_namespace_dict == None:
        dest_namespace_dict = get_callers_namespace_dict(2 if use_not_include else 3)

    #create a wrapper for each module and function in symbols
    for sd in symbols_dicts:
        include_str = include_str_from_filename(scad_file_path,
                                                use_not_include,
                                                builtins)

        c = create_openscad_wrapper_from_symbols(sd["name"],
                                                 sd["args"],
                                                 sd["kwargs"],
                                                 include_str)

        #add it to the dest_namespace
        #setattr(dest_namespace_dict, escpape_openscad_identifier(sd["name"]), c)
        dest_namespace_dict[escpape_openscad_identifier(sd["name"])] = c

def include(scad_file_path):
    return use(scad_file_path, use_not_include=False)

