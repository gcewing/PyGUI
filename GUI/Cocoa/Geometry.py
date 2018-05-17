#
#   Python GUI - Points and Rectangles - PyObjC
#

from Foundation import NSMakeRect
from GUI.GGeometry import *

def rect_to_ns_rect((l, t, r, b)):
	return NSMakeRect(l, t, r - l, b - t)

def ns_rect_to_rect(((l, t), (w, h))):
	return (l, t, l + w, t + h)
