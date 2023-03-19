#TODO: extend this with all kinds of bosl2 features

class Bosl2Mixin:
    def tag(self, tag=None, **kwargs):
        from .std import tag as tagClass
        return tagClass(tag, **kwargs)(self)

    def attach(self, _from=None, to=None, overlap=None, norot=None, **kwargs):
        from .std import attach
        return attach(_from, to, overlap, norot, **kwargs)(self)

