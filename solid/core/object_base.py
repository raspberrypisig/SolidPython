from copy import deepcopy

#don't do relative imports on the global scope to be able to import this file
#from "everywhere"

class ObjectBase:
    def __init__(self):
        self.children = []

    def add(self, c):
        if isinstance(c, list):
            self.children += c
        else:
            self.children += [c]

    def copy(self):
        return deepcopy(self)

    def _render(self):
        s = ''
        for c in self.children:
            s += c._render()
        return s

    def __call__(self, *args):
        #translate(...)(cube())
        #this adds cube() to translate.children
        self.add(list(args))
        return self

    def __repr__(self):
        return self.as_scad()

    def as_scad(self, _fn=None):
        from .scad_render import scad_render
        return scad_render(self, _fn=_fn)[:-1]

    def save_as_scad(self, filename='', outdir='', _fn=None):
        from .scad_render import scad_render_to_file
        return scad_render_to_file(self, filename, outdir, _fn=_fn)

class OpenSCADObject(ObjectBase):
    def __init__(self, name, params):
        super().__init__()
        self.name = name
        self.params = params

    def _render(self):
        """
            returns the scad code for a given node tuple consiting of name, params
            and children list.

            -> translate(v = [1, 2, 3]) {children[0]; children[1]; ...};\n
        """
        from .utils import indent
        s = self.generate_scad_head()

        if self.children:
            s += " {\n"
            for child in self.children:
                s += indent(child._render())
            s += "}"

        return s + ";\n"

    def generate_scad_head(self):
        """
            for a given function name and dict of params it returns:
                {name}(p1=v1, p2=v2,...)
                -> translate(v = [1, 2, 3])
        """
        from .utils import unescape_openscad_identifier

        param_strings = []
        for p in sorted(self.params.keys()):
            scad_value = py2openscad(self.params[p])
            scad_identifier = unescape_openscad_identifier(p)

            param_strings.append(f'{scad_identifier} = {scad_value}')

        scad_identifier = unescape_openscad_identifier(self.name)
        param_str = ", ".join(param_strings)

        return f'{scad_identifier}({param_str})'

def py2openscad(o):
    if type(o) == bool:
        return str(o).lower()
    if type(o) == float:
        return f"{o:.10f}"  # type: ignore
    if type(o) == str:
        return f'\"{o}\"'  # type: ignore
    if type(o).__name__ == "ndarray":
        import numpy  # type: ignore
        return numpy.array2string(o, separator=",", threshold=1000000000)
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

