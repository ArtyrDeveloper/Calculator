class Singleton(object):
    def __new__(cls, *args, **kwargds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it

        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwargds)
        return it
    
    def init(self, *args, **kwargds):
        pass