import inspect

from ..object_base import OpenSCADObject
from ..helpers import indent
from .extension_base import RootExtensionBase, InvisibleExtensionBase, default_extension_manager


# the "OpenSCAD"-Node that get's injected into the tree when ever a
# decorated functions gets called
class py2scad_module(InvisibleExtensionBase):
    def __init__(self, name, signature, *args, **kwargs):
        #name & signature are the python function name and it's signature
        super().__init__()
        self.name = name
        self.signature = signature
        #args and kwargs are the actual parameters to be passed for this
        #particular call!
        self.args = args
        self.kwargs = kwargs

    def _render(self):
        #in the regular render process we want to render a call to the
        #function
        s = self.name + "(";
        for a in self.args:
            s += str(a) + ","
        for a in self.kwargs:
            s += a + "=" + str(self.kwargs[a]) + ","

        #remove last "," from parameter list
        if len(self.args) + len(self.kwargs):
            s = s[:-1]

        s += ");"

        return s

    def get_full_signature(self):
        return self.name + str(self.signature)

    def _render_module(self):
        #and when our root extensions calls, we want to render the function declaration
        s = f'module {self.get_full_signature()}{{'
        for child in self.children:
            s += indent(child._render())
        s += "\n}\n"
        return s

def scad_module(*args, **kwargs):
    def wrap(f):
        def wrapped_f(*wargs, **wkwargs):
            scad_obj = f(*wargs, **wkwargs)
            name = f.__module__ + "__" + f.__name__
            import inspect
            print(inspect.getsource(f))
            return py2scad_module(name, inspect.signature(f), *wargs, **wkwargs)(scad_obj)

        return wrapped_f

    return wrap

class SolidFunctionExtension(RootExtensionBase):
    def _pre_render(self, root):
        s = ''

        done_modules = []
        module_calls = traverse_tree_and_find_modules(root)
        for call in module_calls:
            if not call.get_full_signature() in done_modules:
                s += call._render_module()
                done_modules = call.get_full_signature()

        return s

default_extension_manager.register_root_extension(SolidFunctionExtension)

# ==========================
# = local helper functions =
# ==========================

def is_solid_module(obj):
    return isinstance(obj, py2scad_module)

def traverse_tree_and_find_modules(obj):
    s = []
    if is_solid_module(obj):
        s.append(obj)

    for c in obj.children:
        s += traverse_tree_and_find_modules(c)

    return s

