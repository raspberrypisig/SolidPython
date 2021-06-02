from ..core.object_base import OpenSCADConstant

class ScadInterface:
    def __init__(self):
        self.header = ''

    def register_customizer_var(self, name, value, options=''):
        self.header += f'{name} = {value}; //{options}\n'

    def set_global_var(self, name, value):
        self.header += f'{name} = {value};\n'

    def get_header_str(self):
        return self.header

    def register_font(self, filename):
        self.header += f'use <{filename}>\n'

    @staticmethod
    def get(name):
        return self.inline(name)

    @staticmethod
    def inline(code):
        return scad_inline(code)

