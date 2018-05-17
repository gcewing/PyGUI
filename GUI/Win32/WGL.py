#------------------------------------------------------------------------------
#
#   PyGUI - WGL - Win32
#
#------------------------------------------------------------------------------

from ctypes import *
gdi32 = windll.gdi32

def SetPixelFormat(hdc, ipf):
	gdi32.SetPixelFormat(hdc, ipf, None)

def attr_array(d):
	a = []
	for k, v in d.iteritems():
		a.append(k)
		a.append(v)
	a.append(0)
	return a

def attr_dict(keys, values):
	return dict(zip(keys, values))
