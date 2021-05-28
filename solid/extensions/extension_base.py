from ..object_base import ObjectBase

class RootExtensionBase(ObjectBase):
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

