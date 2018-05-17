#
#		Python GUI - Images - Gtk
#

from gi.repository import Gdk
from GtkImageScaling import gtk_scale_pixbuf
from GImages import Image as GImage

class Image(GImage):

	def _init_from_file(self, file):
		self._gdk_pixbuf = GdkPixbuf.Pixbuf.new_from_file(file)
	
	def get_width(self):
		return self._gdk_pixbuf.get_width()
	
	def get_height(self):
		return self._gdk_pixbuf.get_height()
	
	def draw(self, canvas, src_rect, dst_rect):
		sx, sy, sr, sb = src_rect
		dx, dy, dr, db = dst_rect
		sw = sr - sx
		sh = sb - sy
		dw = dr - dx
		dh = db - dy
		gdk_pixbuf = self._gdk_pixbuf
		if sw <> dw or sh <> dh:
			gdk_scaled_pixbuf = gtk_scale_pixbuf(gdk_pixbuf, sx, sy, sw, sh, dw, dh)
			canvas._gdk_drawable.draw_pixbuf(
				canvas._gdk_gc, gdk_scaled_pixbuf,
				0, 0, dx, dy, dw, dh, Gdk.RGB_DITHER_NORMAL, 0, 0)
		else:
			canvas._gdk_drawable.draw_pixbuf(
				canvas._gdk_gc, self._gdk_pixbuf,
				sx, sy, dx, dy, sw, sh, Gdk.RGB_DITHER_NORMAL, 0, 0)
