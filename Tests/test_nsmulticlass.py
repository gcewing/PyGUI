from AppKit import NSTextField
from GUI.Utils import NSMultiClass

class X(object):
    """Class X"""

class C(NSTextField):
    __metaclass__ = NSMultiClass

print "C.__doc__ =", C.__doc__
print C.__dict__.keys()
print C.__dict__.get('__slots__', None)

c = C.alloc()
c.foo = 17
print c.foo

class D(NSTextField, X):
    """Class D"""
    __metaclass__ = NSMultiClass

print "D.__doc__ =", D.__doc__
print D.__dict__.keys()
print D.__dict__.get('__slots__', None)

d = D.alloc()
d.foo = 42
print d.foo
