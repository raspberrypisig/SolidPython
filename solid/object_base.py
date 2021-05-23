import tempfile
import sys
import os
import subprocess
import keyword

from typing import Dict, Optional, List, Union, Sequence, Iterable

from .helpers import unsubbed_keyword, indent, resolve_scad_filename

# These are features added to SolidPython but NOT in OpenSCAD.
# Mark them for special treatment

non_rendered_classes = ['hole', 'part']

class OpenSCADObject:

    def __init__(self, name: str, params: dict):
        self.name = name
        self.params = params
        self.children: List["OpenSCADObject"] = []
        self.modifier = ""
        self.parent: Optional["OpenSCADObject"] = None

    def set_modifier(self, m: str) -> "OpenSCADObject":
        """
        Used to add one of the 4 single-character modifiers:
        #(debug) !(root) %(background) or *(disable)
        """
        string_vals = {'disable': '*',
                       'debug': '#',
                       'background': '%',
                       'root': '!',
                       '*': '*',
                       '#': '#',
                       '%': '%',
                       '!': '!'}

        self.modifier = string_vals.get(m.lower(), '')
        return self

    def _render(self) -> str:
        """
        NOTE: In general, you won't want to call this method. For most purposes,
        you really want scad_render(), 
        Calling obj._render won't include necessary 'use' or 'include' statements
        """
        s = ""

        # First, render all children
        for child in self.children:
            s += child._render()

        if not self.children:
            s = self._render_str_no_children() + ";"
        else:
            s = self._render_str_no_children() + " {" + indent(s) + "\n}"

        return s

    def _render_str_no_children(self) -> str:
        callable_name = unsubbed_keyword(self.name)
        s = "\n" + self.modifier + callable_name + "("
        first = True

        # Re: https://github.com/SolidCode/SolidPython/issues/99
        # OpenSCAD will accept Python reserved words as callables or argument names,
        # but they won't compile in Python. Those have already been substituted
        # out (e.g 'or' => 'or_'). Sub them back here.
        self.params = {unsubbed_keyword(k): v for k, v in self.params.items()}

        # OpenSCAD doesn't have a 'segments' argument, but it does
        # have '$fn'.  Swap one for the other
        if 'segments' in self.params:
            self.params['$fn'] = self.params.pop('segments')

        valid_keys = self.params.keys()

        # intkeys are the positional parameters
        intkeys = list(filter(lambda x: type(x) == int, valid_keys))
        intkeys.sort()

        # named parameters
        nonintkeys = list(filter(lambda x: not type(x) == int, valid_keys))
        all_params_sorted = intkeys + nonintkeys
        if all_params_sorted:
            all_params_sorted = sorted(all_params_sorted)

        for k in all_params_sorted:
            v = self.params[k]
            if v is None:
                continue

            if not first:
                s += ", "
            first = False

            if type(k) == int:
                s += py2openscad(v)
            else:
                s += k + " = " + py2openscad(v)

        s += ")"
        return s

    def add(self, child: Union["OpenSCADObject", Sequence["OpenSCADObject"]]) -> "OpenSCADObject":
        """
        if child is a single object, assume it's an OpenSCADObjects and 
        add it to self.children

        if child is a list, assume its members are all OpenSCADObjects and
        add them all to self.children
        """
        if isinstance(child, (list, tuple)):
            # __call__ passes us a list inside a tuple, but we only care
            # about the list, so skip single-member tuples containing lists
            if len(child) == 1 and isinstance(child[0], (list, tuple)):
                child = child[0]
            [self.add(c) for c in child]
        elif isinstance(child, int):
            # Allowing for creating object by adding to 0 (as in sum())
            if child != 0:
                raise ValueError
        else:
            self.children.append(child)  # type: ignore
            child.set_parent(self)  # type: ignore
        return self

    def set_parent(self, parent: "OpenSCADObject"):
        self.parent = parent

    def add_param(self, k: str, v: float) -> "OpenSCADObject":
        if k == '$fn':
            k = 'segments'
        self.params[k] = v
        return self

    def copy(self) -> "OpenSCADObject":
        """
        Provides a copy of this object and all children,
        but doesn't copy self.parent, meaning the new object belongs
        to a different tree
        Initialize an instance of this class with the same params
        that created self, the object being copied.
        """

        # Python can't handle an '$fn' argument, while openSCAD only wants
        # '$fn'.  Swap back and forth as needed; the final renderer will
        # sort this out.
        if '$fn' in self.params:
            self.params['segments'] = self.params.pop('$fn')

        other = type(self)(**self.params)
        other.modifier = self.modifier
        for c in self.children:
            other.add(c.copy())
        return other

    def __call__(self, *args: "OpenSCADObject") -> "OpenSCADObject":
        """
        Adds all objects in args to self.  This enables OpenSCAD-like syntax,
        e.g.:
        union()(
            cube(),
            sphere()
        )
        """
        return self.add(args)

    def __add__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        """
        This makes u = a+b identical to:
        u = union()(a, b )
        """
        from .builtins import union
        res = union()
        if isinstance(self, union):
            for c in self.children:
                res.add(c)
        else:
            res.add(self)

        if isinstance(x, union):
            for c in x.children:
                res.add(c)
        else:
            res.add(x)

        return x

    def __radd__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        return self.__add__(x)

    def __sub__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        """
        This makes u = a - b identical to:
        u = difference()(a, b )
        """
        from .builtins import difference

        res = difference()

        if isinstance(self, difference) and len(self.children):
            for c in self.children:
                res.add(c)
        else:
            res.add(self)


        res.add(x)
        return res

    def __mul__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        """
        This makes u = a * b identical to:
        u = intersection()(a, b )
        """
        from .builtins import intersection
        res = intersection()

        if isinstance(self, intersection):
            for c in self.children:
                res.add(c)
        else:
            res.add(self)

        if isinstance(x, intersection):
            for c in x.children:
                res.add(c)
        else:
            res.add(x)

        return intersection()(self, x)

    def debug(self):
        self.modifier = "#"
        return self

    def background(self):
        self.modifier = "%"
        return self

    def root(self):
        self.modifier = "!"
        return self

    def disable(self):
        self.modifier = "*"
        return self

    def _repr_png_(self) -> Optional[bytes]:
        """
        Allow rich clients such as the IPython Notebook, to display the current
        OpenSCAD rendering of this object.
        """
        png_data = None
        tmp = tempfile.NamedTemporaryFile(suffix=".scad", delete=False)
        tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        try:
            scad_text = scad_render(self).encode("utf-8")
            tmp.write(scad_text)
            tmp.close()
            tmp_png.close()
            subprocess.Popen([
                "openscad",
                "--preview",
                "-o", tmp_png.name,
                tmp.name
            ]).communicate()

            with open(tmp_png.name, "rb") as png:
                png_data = png.read()
        finally:
            os.unlink(tmp.name)
            os.unlink(tmp_png.name)

        return png_data

class IncludedOpenSCADObject(OpenSCADObject):
    """
    Identical to OpenSCADObject, but each subclass of IncludedOpenSCADObject
    represents imported scad code, so each instance needs to store the path
    to the scad file it's included from.
    """

    def __init__(self, name, params, include_file_path, use_not_include=False, **kwargs):
        self.include_file_path = resolve_scad_filename(include_file_path)

        use_str = 'use' if use_not_include else 'include'
        self.include_string = f'{use_str} <{self.include_file_path}>\n'

        # Just pass any extra arguments straight on to OpenSCAD; it'll accept
        # them
        if kwargs:
            params.update(kwargs)

        OpenSCADObject.__init__(self, name, params)

def py2openscad(o: Union[bool, float, str, Iterable]) -> str:
    if type(o) == bool:
        return str(o).lower()
    if type(o) == float:
        return f"{o:.10f}"  # type: ignore
    if type(o) == str:
        return f'\"{o}\"'  # type: ignore
    if type(o).__name__ == "ndarray":
        import numpy  # type: ignore
        return numpy.array2string(o, separator=",", threshold=1000000000)
    if isinstance(o, IncludedOpenSCADObject):
        return o._render()[1:-1]
    if hasattr(o, "__iter__"):
        s = "["
        first = True
        for i in o:  # type: ignore
            if not first:
                s += ", "
            first = False
            s += py2openscad(i)
        s += "]"
        return s
    return str(o)

