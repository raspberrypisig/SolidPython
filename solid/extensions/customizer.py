from ..core.object_base import scad_inline

class Customizer:
    def __init__(self):
        self.header = ""

    def register(self, name, value, options=''):
        self.header += f'{name} = {value}; //{options}\n'

    @staticmethod
    def get(name):
        return scad_inline(name)

