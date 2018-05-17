#
#		Python GUI - Images - Gtk
#

from __future__ import division
from array import array
import cairo
from gtk import gdk
from GUI import export
from GUI.GImages import Image as GImage

class Image(GImage):

	def _init_from_file(self, file):
		self._gdk_pixbuf = gdk.pixbuf_new_from_file(file)
	
	def _from_gdk_pixbuf(cls, gdk_pixbuf):
		self = cls.__new__(cls)
		self._gdk_pixbuf = gdk_pixbuf
		return self
	
	_from_gdk_pixbuf = classmethod(_from_gdk_pixbuf)

	def _gtk_set_source(self, ctx, x, y):
		ctx.set_source_pixbuf(self._gdk_pixbuf, x, y)

	def get_width(self):
		return self._gdk_pixbuf.get_width()
	
	def get_height(self):
		return self._gdk_pixbuf.get_height()

export(Image)
