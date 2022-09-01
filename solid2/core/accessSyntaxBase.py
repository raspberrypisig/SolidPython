from ..config import config

def getBuiltin(name):
    from .. import builtins
    f = getattr(builtins, name)
    return f

class AccessSyntaxBase:
    if not config.use_implicit_builtins:
        def intersection_for(self, *args, **kwargs): return getBuiltin("intersection_for")(*args, **kwargs)(self)
        def color(self, *args, **kwargs): return getBuiltin("color")(*args, **kwargs)(self)
        def hull(self, *args, **kwargs): return getBuiltin("hull")(*args, **kwargs)(self)
        def render(self, *args, **kwargs): return getBuiltin("render")(*args, **kwargs)(self)
        def projection(self, *args, **kwargs): return getBuiltin("projection")(*args, **kwargs)(self)
        def surface(self, *args, **kwargs): return getBuiltin("surface")(*args, **kwargs)(self)
        def offset(self, *args, **kwargs): return getBuiltin("offset")(*args, **kwargs)(self)

        def mirror(self, *args, **kwargs): return getBuiltin("mirror")(*args, **kwargs)(self)
        def mirrorX(self, x): return getBulitin("mirrorX")(x)(self)
        def mirrorY(self, y): return getBulitin("mirrorY")(y)(self)
        def mirrorZ(self, z): return getBulitin("mirrorZ")(z)(self)

        def resize(self, *args, **kwargs): return getBuiltin("resize")(*args, **kwargs)(self)
        def resizeX(self, x): return getBulitin("resizeX")(x)(self)
        def resizeY(self, y): return getBulitin("resizeY")(y)(self)
        def resizeZ(self, z): return getBulitin("resizeZ")(z)(self)

    def union(self, *args, **kwargs): return getBuiltin("union")(*args, **kwargs)(self)
    def difference(self, *args, **kwargs): return getBuiltin("difference")(*args, **kwargs)(self)
    def intersection(self, *args, **kwargs): return getBuiltin("intersection")(*args, **kwargs)(self)
    def linear_extrude(self, *args, **kwargs): return getBuiltin("linear_extrude")(*args, **kwargs)(self)
    def rotate_extrude(self, *args, **kwargs): return getBuiltin("rotate_extrude")(*args, **kwargs)(self)

    def translate(self, *args, **kwargs): return getBuiltin("translate")(*args, **kwargs)(self)
    def scale(self, *args, **kwargs): return getBuiltin("scale")(*args, **kwargs)(self)
    def rotate(self, *args, **kwargs): return getBuiltin("rotate")(*args, **kwargs)(self)

    def down(self, z): return getBuiltin("down")(z)(self)
    def up(self, z): return getBuiltin("up")(z)(self)
    def left(self, x): return getBuiltin("left")(x)(self)
    def right(self, x): return getBuiltin("right")(x)(self)
    def back(self, y): return getBuiltin("back")(y)(self)
    def fwd(self, y): return getBuiltin("fwd")(y)(self)
    def forward(self, y): return getBuiltin("fwd")(y)(self)

    def translateX(self, x): return getBulitin("translateX")(x)(self)
    def translateY(self, y): return getBulitin("translateY")(y)(self)
    def translateZ(self, z): return getBulitin("translateZ")(z)(self)
    def rotateX(self, x): return getBulitin("rotateX")(x)(self)
    def rotateY(self, y): return getBulitin("rotateY")(y)(self)
    def rotateZ(self, z): return getBulitin("rotateZ")(z)(self)
    def scaleX(self, x): return getBulitin("scaleX")(x)(self)
    def scaleY(self, y): return getBulitin("scaleY")(y)(self)
    def scaleZ(self, z): return getBulitin("scaleZ")(z)(self)

    def debug(self): return getBuiltin("debug")()(self)
    def background(self): return getBuiltin("background")()(self)
    def root(self): return getBuiltin("root")()(self)
    def disable(self): return getBuiltin("disable")()(self)

