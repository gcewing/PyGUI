#
#		Python GUI - Cursors - Gtk
#

from gtk import gdk
from GUI import export
from GUI.GCursors import Cursor as GCursor

class Cursor(GCursor):
	#
	#  _gtk_cursor   gtk.gdk.Cursor

	def _from_gtk_std_cursor(cls, id):
		cursor = cls.__new__(cls)
		cursor._gtk_cursor = gdk.Cursor(id)
		return cursor
	
	_from_gtk_std_cursor = classmethod(_from_gtk_std_cursor)

	def _from_nothing(cls):
		cursor = cls.__new__(cls)
		pixmap = gdk.Pixmap(None, 1, 1, 1)
		color = gdk.Color()
		cursor._gtk_cursor = gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
		return cursor
	
	_from_nothing = classmethod(_from_nothing)

	def _init_from_image_and_hotspot(self, image, hotspot):
		#print "Cursor._init_from_image_and_hotspot:", image, hotspot ###
		x, y = hotspot
		gdk_display = gdk.display_get_default()
		self._gtk_cursor = gdk.Cursor(gdk_display, image._gdk_pixbuf, x, y)

export(Cursor)
