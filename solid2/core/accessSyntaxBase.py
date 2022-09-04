from ..config import config

class AccessSyntaxBase:
    if not config.use_implicit_builtins:
        def intersection_for(self, *args, **kwargs): from . import builtins; return builtins.intersection_for(*args, **kwargs)(self)
        def color(self, *args, **kwargs):            from . import builtins; return builtins.color(*args, **kwargs)(self)
        def hull(self, *args, **kwargs):             from . import builtins; return builtins.hull(*args, **kwargs)(self)
        def render(self, *args, **kwargs):           from . import builtins; return builtins.render(*args, **kwargs)(self)
        def projection(self, *args, **kwargs):       from . import builtins; return builtins.projection(*args, **kwargs)(self)
        def surface(self, *args, **kwargs):          from . import builtins; return builtins.surface(*args, **kwargs)(self)
        def offset(self, *args, **kwargs):           from . import builtins; return builtins.offset(*args, **kwargs)(self)
        def mirror(self, *args, **kwargs):           from . import builtins; return builtins.mirror(*args, **kwargs)(self)
        def resize(self, *args, **kwargs):           from . import builtins; return builtins.resize(*args, **kwargs)(self)

        def mirrorX(self, x): from . import builtins; return builtins.mirrorX(x)(self)
        def mirrorY(self, y): from . import builtins; return builtins.mirrorY(y)(self)
        def mirrorZ(self, z): from . import builtins; return builtins.mirrorZ(z)(self)

        def resizeX(self, x): from . import builtins; return builtins.resizeX(x)(self)
        def resizeY(self, y): from . import builtins; return builtins.resizeY(y)(self)
        def resizeZ(self, z): from . import builtins; return builtins.resizeZ(z)(self)

    def union(self, *args, **kwargs):          from . import builtins; return builtins.union(*args, **kwargs)(self)
    def difference(self, *args, **kwargs):     from . import builtins; return builtins.difference(*args, **kwargs)(self)
    def intersection(self, *args, **kwargs):   from . import builtins; return builtins.intersection(*args, **kwargs)(self)
    def linear_extrude(self, *args, **kwargs): from . import builtins; return builtins.linear_extrude(*args, **kwargs)(self)
    def rotate_extrude(self, *args, **kwargs): from . import builtins; return builtins.rotate_extrude(*args, **kwargs)(self)

    def translate(self, *args, **kwargs): from . import builtins; return builtins.translate(*args, **kwargs)(self)
    def scale(self, *args, **kwargs):     from . import builtins; return builtins.scale(*args, **kwargs)(self)
    def rotate(self, *args, **kwargs):    from . import builtins; return builtins.rotate(*args, **kwargs)(self)

    def down(self, z):    from . import builtins; return builtins.down(z)(self)
    def up(self, z):      from . import builtins; return builtins.up(z)(self)
    def left(self, x):    from . import builtins; return builtins.left(x)(self)
    def right(self, x):   from . import builtins; return builtins.right(x)(self)
    def back(self, y):    from . import builtins; return builtins.back(y)(self)
    def fwd(self, y):     from . import builtins; return builtins.fwd(y)(self)
    def forward(self, y): from . import builtins; return builtins.fwd(y)(self)

    def translateX(self, x): from . import builtins; return builtins.translateX(x)(self)
    def translateY(self, y): from . import builtins; return builtins.translateY(y)(self)
    def translateZ(self, z): from . import builtins; return builtins.translateZ(z)(self)

    def rotateX(self, x): from . import builtins; return builtins.rotateX(x)(self)
    def rotateY(self, y): from . import builtins; return builtins.rotateY(y)(self)
    def rotateZ(self, z): from . import builtins; return builtins.rotateZ(z)(self)

    def scaleX(self, x): from . import builtins; return builtins.scaleX(x)(self)
    def scaleY(self, y): from . import builtins; return builtins.scaleY(y)(self)
    def scaleZ(self, z): from . import builtins; return builtins.scaleZ(z)(self)

    def debug(self):      from . import builtins; return builtins.debug()(self)
    def background(self): from . import builtins; return builtins.background()(self)
    def root(self):       from . import builtins; return builtins.root()(self)
    def disable(self):    from . import builtins; return builtins.disable()(self)

