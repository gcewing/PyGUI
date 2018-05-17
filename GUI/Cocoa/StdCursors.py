#
#		Python GUI - Standard Cursors - Cocoa
#

from AppKit import NSCursor
from GUI import Cursor

__all__ = [
	'arrow',
	'ibeam', 
	'crosshair', 
	'fist', 
	'hand', 
	'finger', 
	'invisible', 
]

_empty_cursor = None

def _make_empty_cursor():
	global _empty_cursor
	if not _empty_cursor:
		from AppKit import NSCursor, NSImage, NSBitmapImageRep, NSDeviceRGBColorSpace
		from GUI import Cursor
		import sys
		if sys.version_info >= (3, 0):
			b = bytes([0])
		else:
			b = "\x00"
		d = b * 1024
		ns_bitmap = NSBitmapImageRep.alloc().\
			initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_\
			((d, d, d, d, d), 16, 16, 8, 4, True, False, NSDeviceRGBColorSpace, 64, 32)
		ns_image = NSImage.alloc().initWithSize_((16, 16))
		ns_image.addRepresentation_(ns_bitmap)
		ns_cursor = NSCursor.alloc().initWithImage_hotSpot_(ns_image, (0, 0))
		_empty_cursor = Cursor._from_ns_cursor(ns_cursor)
		_empty_cursor._data = d
	return _empty_cursor

arrow = Cursor._from_ns_cursor(NSCursor.arrowCursor())
ibeam = Cursor._from_ns_cursor(NSCursor.IBeamCursor())
crosshair = Cursor._from_ns_cursor(NSCursor.crosshairCursor())
fist = Cursor._from_ns_cursor(NSCursor.closedHandCursor())
hand = Cursor._from_ns_cursor(NSCursor.openHandCursor())
finger = Cursor._from_ns_cursor(NSCursor.pointingHandCursor())
invisible = _make_empty_cursor()

mac_poof = Cursor._from_ns_cursor(NSCursor.disappearingItemCursor())

del NSCursor
del Cursor
del _make_empty_cursor

def empty_cursor():
	return invisible
