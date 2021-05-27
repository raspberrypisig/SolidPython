from copy import deepcopy
from typing import Optional, List, Union, Sequence, Iterable

from .helpers import indent, resolve_scad_filename, unescape_openscad_identifier

class OpenSCADObject:

    def __init__(self, name, params):
        self.name = name
        self.params = params
        self.children: List["OpenSCADObject"] = []

    def _render(self):
        """
        NOTE: In general, you won't want to call this method. For most purposes,
        you really want scad_render(), 
        Calling obj._render won't include necessary 'use' or 'include' statements
        """
        s = self._render_str_no_children()

        if not self.children:
            return s + ";\n"

        s += " {\n"

        for child in self.children:
            s += indent(child._render())

        return s + "}\n"

    def _render_str_no_children(self):
        s = unescape_openscad_identifier(self.name) + "("

        parameter_count = 0
        for p in sorted(self.params.keys()):
            v = self.params[p]
            if v is None:
                continue

            parameter_count += 1

            vv = py2openscad(v)
            up = unescape_openscad_identifier(p)
            s += f'{up} = {vv}, '

        #remove trailing ,
        if parameter_count:
            s = s[:-2]

        s += ")"
        return s

    def add(self, child):
        """
        if child is a single object, assume it's an OpenSCADObjects and 
        add it to self.children

        if child is a list, assume its members are all OpenSCADObjects and
        add them all to self.children
        """
        # Allowing for creating object by adding to 0 (as in sum())
        # why do we need this? --jeff
        if isinstance(child, int):
            if child != 0:
                raise ValueError
            return self

        if isinstance(child, list):
            self.children += child
        else:
            self.children += [child]

        return self

    def copy(self):
        return deepcopy(self)

    def __call__(self, *args):
        """
        Adds all objects in args to self.  This enables OpenSCAD-like syntax,
        e.g.:
        union()(
            cube(),
            sphere()
        )
        """
        return self.add(list(args))

    def __add__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        """
        This makes u = a+b identical to:
        u = union()(a, b )
        """
        from .builtins import union
        res = union()

        #add self or all its children to res
        if isinstance(self, union) and not len(self.modifier):
            for c in self.children:
                res.add(c)
        else:
            res.add(self)

        #add x or all its children to res
        if isinstance(x, union) and not len(x.modifier):
            for c in x.children:
                res.add(c)
        else:
            res.add(x)

        return res

    def __radd__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        return self.__add__(x)

    def __sub__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        """
        This makes u = a - b identical to:
        u = difference()(a, b )
        """
        from .builtins import difference

        res = difference()

        if isinstance(self, difference) and len(self.children) and not len(self.modifier):
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

        if isinstance(self, intersection) and not len(self.modifier):
            for c in self.children:
                res.add(c)
        else:
            res.add(self)

        if isinstance(x, intersection) and not len(x.modifier):
            for c in x.children:
                res.add(c)
        else:
            res.add(x)

        return intersection()(self, x)

class IncludedOpenSCADObject(OpenSCADObject):
    """
    Identical to OpenSCADObject, but each subclass of IncludedOpenSCADObject
    represents imported scad code, so each instance needs to store the path
    to the scad file it's included from.
    """

    def __init__(self, name, params, include_file_path, use_not_include=False):

        if include_file_path:
            self.include_file_path = resolve_scad_filename(include_file_path)
            use_str = 'use' if use_not_include else 'include'
            self.include_string = f'{use_str} <{self.include_file_path}>\n\n'
        else:
            self.include_string = None

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
        return o._render()[:-2]
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

