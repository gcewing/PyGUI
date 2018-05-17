#
#   PyGUI - Image Base - Gtk
#

from __future__ import division
from GUI import export
from GUI.GImageBases import ImageBase as GImageBase

class ImageBase(GImageBase):

#	def get_width(self):
#		return self._gtk_surface.get_width()
#	
#	def get_height(self):
#		return self._gtk_surface.get_height()
	
	def draw(self, canvas, src_rect, dst_rect):
		sx, sy, sr, sb = src_rect
		dx, dy, dr, db = dst_rect
		sw = sr - sx
		sh = sb - sy
		dw = dr - dx
		dh = db - dy
		ctx = canvas._gtk_ctx
		ctx.save()
		ctx.translate(dx, dy)
		ctx.new_path()
		ctx.rectangle(0, 0, dw, dh)
		ctx.clip()
		ctx.scale(dw / sw, dh / sh)
		self._gtk_set_source(canvas._gtk_ctx, -sx, -sy)
		ctx.paint()
		ctx.restore()

export(ImageBase)
