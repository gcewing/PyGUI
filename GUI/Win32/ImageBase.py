#--------------------------------------------------------------------
#
#   PyGUI - ImageBase - Win32
#
#--------------------------------------------------------------------

from GUI import export
from GUI.GImageBases import ImageBase as GImageBase

class ImageBase(GImageBase):
	#  _win_image   GdiPlus.Image
	
	def get_width(self):
		return self._win_image.GetWidth()

	def get_height(self):
		return self._win_image.GetHeight()

	def draw(self, canvas, src_rect, dst_rect):
		canvas._win_graphics.DrawImage_rr(self._win_image, dst_rect, src_rect)

export(ImageBase)
