#
#		Python GUI - Cursors - Cocoa
#

from AppKit import NSCursor
from GUI import export
from GUI.GCursors import Cursor as GCursor

class Cursor(GCursor):
	#
	#  _ns_cursor   NSCursor

	def _from_ns_cursor(cls, ns_cursor):
		cursor = cls.__new__(cls)
		cursor._ns_cursor = ns_cursor
		return cursor

	_from_ns_cursor = classmethod(_from_ns_cursor)

	def _init_from_image_and_hotspot(self, image, hotspot):
		#print "Cursor._init_from_image_and_hotspot:", image, hotspot ###
		ns_image = image._ns_image.copy()
		ns_image.setFlipped_(False)
		self._ns_cursor = NSCursor.alloc().initWithImage_hotSpot_(
			ns_image, hotspot)

export(Cursor)
