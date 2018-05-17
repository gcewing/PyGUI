#
#		Python GUI - Images - Gtk
#

from __future__ import division
from array import array
import cairo
from gi.repository import Gdk, GdkPixbuf
from GUI.GImages import Image as GImage

class Image(GImage):

	def _init_from_file(self, file):
		self._gdk_pixbuf = GdkPixbuf.Pixbuf.new_from_file(file)

	def _gtk_set_source(self, ctx, x, y):
		ctx.set_source_pixbuf(self._gdk_pixbuf, x, y)

	def get_width(self):
		return self._gdk_pixbuf.get_width()
	
	def get_height(self):
		return self._gdk_pixbuf.get_height()
