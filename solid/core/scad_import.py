from types import SimpleNamespace
import inspect
from collections import namedtuple

from .utils import resolve_scad_filename, escpape_openscad_identifier
from .object_base import OpenSCADObject, OpenSCADConstant

# ===========
# = Parsing =
# ===========
def parse_scad_callables(filename):
    from ..libs.py_scadparser import scad_parser
    callables_entry = namedtuple("callables_entry", ["name", "args", "kwargs"])

    modules, functions, global_vars = scad_parser.parseFile(filename)

    callables = []
    for c in modules + functions:
        #args = [p.name for p in c.parameters if not p.optional]
        #kwargs = [p.name for p in c.parameters if p.optional]
        kwargs = [p.name for p in c.parameters]

        callables.append(callables_entry(c.name, [], kwargs))

    return callables, global_vars

def check_signature(name, args_def, kwargs_def, *args, **kwargs):
    #check whether the args and kwargs fit a function signature definition
    #defined with args_def and kwargs_def. args_def and kwargs_def are lists
    #of all parameter names the function {name} accepts

    filtered_kwargs = {k: kwargs[k] for k in kwargs if not k.startswith("_")}
    if len(args) + len(filtered_kwargs) > len(args_def) + len(kwargs_def):
        raise TypeError(f"too many arguments to {name}(...)")

    full_args_tuples = list(zip(args_def + kwargs_def, args))
    full_args_tuples += list(zip(filtered_kwargs.keys(), filtered_kwargs.values()))

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

def create_openscad_wrapper_from_symbols(name, args, kwargs):

    #this is the function we'll bind to the init function of the new class
    #that we'll create to represent the openscad function
    def init_func(self, *args, **kwargs):
        def legacy_patch(kwargs):
            # this function patches the kwargs to be backward compatible
            import keyword
            if "segments" in kwargs.keys():
                kwargs["_fn"] = kwargs.pop("segments")
            keys_to_replace = []

            #replace keyword_ with _keyword
            for k in kwargs.keys():
                if k.endswith("_") and keyword.iskeyword(k[:-1]):
                    keys_to_replace.append(k)
            for k in keys_to_replace:
                kwargs["_" + k[:-1]] = kwargs.pop(k)

            #replace __[0-9]... with _[0-9]
            keys_to_replace = []
            for k in kwargs.keys():
                if k.startswith("__") and k[2].isdigit():
                    keys_to_replace.append(k)
            for k in keys_to_replace:
                kwargs["_" + k[2:]] = kwargs.pop(k)

        legacy_patch(kwargs)

        #check whether the *args and **kwargs meet our parameter definitions
        check_signature(name, args_def, kwargs_def, *args, **kwargs)

        #zip the args with the def dicts and update it with kwargs
        #to get a single complete kwargs list
        params = dict(zip(args_def + kwargs_def, args))
        params.update(kwargs)

        #call OpenSCADObject ctor
        return super(self.__class__, self).__init__(name, params)


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
def import_scad(scad_file_or_dir, dest_namespace=None, use_not_include=True):
    '''
    Recursively look in current directory & OpenSCAD library directories for
    OpenSCAD files. Create Python mappings for all OpenSCAD modules & functions
    Return a namespace or raise ValueError if no scad files found
    '''
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
    resolved_scad = resolve_scad_filename(scad_file_or_dir)

    if not resolved_scad:
        raise ValueError(f'Could not find .scad files at or under ' + \
                         f'{scad_file_or_dir}.')

    if not resolved_scad.exists():
        return None

    if dest_namespace == None:
        dest_namespace = ExpSolidNamespace(resolved_scad)

    if resolved_scad.is_file():
        use(resolved_scad.absolute(),
            use_not_include=use_not_include,
            dest_namespace_dict=dest_namespace.__dict__)

        return dest_namespace

    assert(resolved_scad.is_dir())

    for f in resolved_scad.iterdir():
        #skip non .scad files
        if f.suffix != ".scad":
            continue

        #recurse into the files and subdirs
        subspace = import_scad(f, use_not_include=use_not_include)
        if subspace:
            identifier = escpape_openscad_identifier(f.stem)
            setattr(dest_namespace, identifier, subspace)

    if not dest_namespace:
        raise ValueError(f'Could not import .scad file ' + \
                         f'{resolved_scad.as_posix()}.')

    return dest_namespace

# use() & include() mimic OpenSCAD's use/include mechanics.
# -- use() makes methods in scad_file_path.scad available to be called.
# --include() makes those methods available AND executes all code in
#   scad_file_path.scad, which may have side effects.
#   Unless you have a specific need, call use().
module_cache_by_resolved_filename = {}

def get_callers_namespace_dict(depth=2):
    frame = inspect.currentframe()
    for i in range(depth):
        frame = frame.f_back

    if frame.f_code.co_name == "<module>":
        return frame.f_locals
    else:
        raise Exception("use & include can not be used inside a function!\n" +\
              "they would polute the modules namespace and only if executed. This\n" +\
              "has strange side effects! Use them on module level.\n")

        return frame.f_globals

def use(scad_file_path, use_not_include = True,
        dest_namespace_dict=None):
    """
    Opens scad_file_path, parses it for all usable calls,
    and adds them to caller's namespace.
    """
    global module_cache_by_resolved_filename

    #resolve filename
    resolved_scad = resolve_scad_filename(scad_file_path)

    if not resolved_scad:
        raise ValueError(f'Could not find .scad file {scad_file_path}.')

    #set the dest_namespace to the module calling this function
    if dest_namespace_dict == None:
        dest_namespace_dict = get_callers_namespace_dict(2)

    #check the module cache for the requested module
    if resolved_scad in module_cache_by_resolved_filename.keys():
        cache_entry = module_cache_by_resolved_filename[resolved_scad]

        #if this is a include call and the module was only used until now
        #set the "use/include" flag in the module cache
        if not use_not_include and cache_entry[1]:
            module_cache_by_resolved_filename[resolved_scad] = (cache_entry[0], False)
        dest_namespace_dict.update(cache_entry[0])
        return

    #get symbols from the parser
    callables, constants = parse_scad_callables(resolved_scad)

    new_namespace_dict = {}
    for c in callables:
        wrapper = create_openscad_wrapper_from_symbols(c.name, c.args, c.kwargs)
        new_namespace_dict[escpape_openscad_identifier(c.name)] = wrapper

    for c in constants:
        new_namespace_dict[escpape_openscad_identifier(c.name)] = OpenSCADConstant(c.name)

    dest_namespace_dict.update(new_namespace_dict)

    module_cache_by_resolved_filename[resolved_scad] = (new_namespace_dict, use_not_include)

def include(scad_file_path):
    return use(scad_file_path, dest_namespace_dict=get_callers_namespace_dict(2), use_not_include=False)

