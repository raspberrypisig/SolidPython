from copy import deepcopy

from .scad_code_generation import scad_code
from .scad_render import scad_render

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
        #translate()(cube())
        #this adds cube() to translate.children
        self.add(list(args))
        return self

    def __repr__(self):
        return scad_render(self)[:-1]

class OpenSCADObject(ObjectBase):
    def __init__(self, name, params, include_string = ''):
        super().__init__()
        self.include_string = include_string
        self.name = name
        self.params = params

    def _render(self):
        return scad_code(self.name, self.params, self.children)

