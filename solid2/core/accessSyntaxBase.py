from ..config import config

def builtins():
    from . import builtins
    return builtins

class AccessSyntaxBase:
    if not config.use_implicit_builtins:
        def intersection_for(self, *args, **kwargs): return builtins().intersection_for(*args, **kwargs)(self)
        def color(self, *args, **kwargs):            return builtins().color(*args, **kwargs)(self)
        def hull(self, *args, **kwargs):             return builtins().hull(*args, **kwargs)(self)
        def render(self, *args, **kwargs):           return builtins().render(*args, **kwargs)(self)
        def projection(self, *args, **kwargs):       return builtins().projection(*args, **kwargs)(self)
        def surface(self, *args, **kwargs):          return builtins().surface(*args, **kwargs)(self)
        def offset(self, *args, **kwargs):           return builtins().offset(*args, **kwargs)(self)
        def mirror(self, *args, **kwargs):           return builtins().mirror(*args, **kwargs)(self)
        def resize(self, *args, **kwargs):           return builtins().resize(*args, **kwargs)(self)

        def mirrorX(self, x): return builtins().mirrorX(x)(self)
        def mirrorY(self, y): return builtins().mirrorY(y)(self)
        def mirrorZ(self, z): return builtins().mirrorZ(z)(self)

        def resizeX(self, x): return builtins().resizeX(x)(self)
        def resizeY(self, y): return builtins().resizeY(y)(self)
        def resizeZ(self, z): return builtins().resizeZ(z)(self)

    def union(self, *args, **kwargs):          return builtins().union(*args, **kwargs)(self)
    def difference(self, *args, **kwargs):     return builtins().difference(*args, **kwargs)(self)
    def intersection(self, *args, **kwargs):   return builtins().intersection(*args, **kwargs)(self)
    def linear_extrude(self, *args, **kwargs): return builtins().linear_extrude(*args, **kwargs)(self)
    def rotate_extrude(self, *args, **kwargs): return builtins().rotate_extrude(*args, **kwargs)(self)

    def translate(self, *args, **kwargs): return builtins().translate(*args, **kwargs)(self)
    def scale(self, *args, **kwargs):     return builtins().scale(*args, **kwargs)(self)
    def rotate(self, *args, **kwargs):    return builtins().rotate(*args, **kwargs)(self)

    def down(self, z):    return builtins().down(z)(self)
    def up(self, z):      return builtins().up(z)(self)
    def left(self, x):    return builtins().left(x)(self)
    def right(self, x):   return builtins().right(x)(self)
    def back(self, y):    return builtins().back(y)(self)
    def fwd(self, y):     return builtins().fwd(y)(self)
    def forward(self, y): return builtins().fwd(y)(self)

    def translateX(self, x): return builtins().translateX(x)(self)
    def translateY(self, y): return builtins().translateY(y)(self)
    def translateZ(self, z): return builtins().translateZ(z)(self)

    def rotateX(self, x): return builtins().rotateX(x)(self)
    def rotateY(self, y): return builtins().rotateY(y)(self)
    def rotateZ(self, z): return builtins().rotateZ(z)(self)

    def scaleX(self, x): return builtins().scaleX(x)(self)
    def scaleY(self, y): return builtins().scaleY(y)(self)
    def scaleZ(self, z): return builtins().scaleZ(z)(self)

    def debug(self):      return builtins().debug()(self)
    def background(self): return builtins().background()(self)
    def root(self):       return builtins().root()(self)
    def disable(self):    return builtins().disable()(self)

