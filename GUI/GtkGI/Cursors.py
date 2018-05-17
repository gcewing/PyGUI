#
#		Python GUI - Cursors - Gtk
#

from gi.repository import Gdk
from GUI.GCursors import Cursor as GCursor

class Cursor(GCursor):
	#
	#  _gtk_cursor   Gdk.Cursor

	def _from_gtk_std_cursor(cls, id):
		cursor = cls.__new__(cls)
		cursor._gtk_cursor = Gdk.Cursor.new(id)
		return cursor
	
	_from_gtk_std_cursor = classmethod(_from_gtk_std_cursor)

	def _from_nothing(cls):
#		cursor = cls.__new__(cls)
#		pixmap = GdkPixmap.Pixmap(None, 1, 1, 1)
#		color = Gdk.Color()
#		cursor._gtk_cursor = Gdk.Cursor.new(pixmap, pixmap, color, color, 0, 0)
#		return cursor
		return cls._from_gtk_std_cursor(Gdk.CursorType.BLANK_CURSOR)
	
	_from_nothing = classmethod(_from_nothing)

	def _init_from_image_and_hotspot(self, image, hotspot):
		#print "Cursor._init_from_image_and_hotspot:", image, hotspot ###
		x, y = hotspot
		gdk_display = Gdk.Display.get_default()
		self._gtk_cursor = Gdk.Cursor.new_from_pixbuf(gdk_display,
			image._gdk_pixbuf, x, y)
