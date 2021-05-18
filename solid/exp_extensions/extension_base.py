from ..object_base import OpenSCADObject

class InvisibleExtensionBase(OpenSCADObject):
    def __init__(self):
        #set the OpenSCADIdentifier to a non identifer to
        #raise a compile error if rendered
        super().__init__('extension base not .=:!23nd32-4813!:=.', {})

    def _render(self):
        # only render the children, this is an invisible node
        s = ""
        for child in self.children:
            s += child._render()
        return s

class RootExtensionBase(InvisibleExtensionBase):
    def _pre_render(self, root):
        return ''

class ExtensionManager():
    def __init__(self):
        self.extensions = []

    def register_root_extension(self, ext):
        self.extensions.append(ext)

    def call_pre_render_and_wrap_root_node(self, root):
        pre_render_str = ''
        new_root_node = root
        for e in self.extensions:
            new_root_node = e()(new_root_node)
            if issubclass(e, RootExtensionBase):
                pre_render_str += new_root_node._pre_render(root)

        return new_root_node, pre_render_str

default_extension_manager = ExtensionManager()

