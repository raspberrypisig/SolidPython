from ..object_base import OpenSCADObject
from .extension_base import InvisibleExtensionBase

class ModifierBase(InvisibleExtensionBase):
    def __init__(self, child=None):
        super().__init__()
        if child:
            self.children += [child]

class debug(ModifierBase):
    def _render(self):
        return "#" + super()._render()

class background(ModifierBase):
    def _render(self):
        return "%" + super()._render()

class root(ModifierBase):
    def _render(self):
        return "!" + super()._render()

class disable(ModifierBase):
    def _render(self):
        return "*" + super()._render()

OpenSCADObject.debug = lambda self: debug()(self)
OpenSCADObject.background = lambda self: background()(self)
OpenSCADObject.root = lambda self: root()(self)
OpenSCADObject.disable = lambda self: disable()(self)

OpenSCADObject.__invert__ = lambda self: debug()(self)

