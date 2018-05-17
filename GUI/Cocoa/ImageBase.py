#
#		Python GUI - Common Image/Pixmap code - Cocoa
#

from AppKit import NSCompositeSourceOver
from GUI import export
from GUI.Geometry import rect_to_ns_rect
from GUI.GImageBases import ImageBase as GImageBase

class ImageBase(GImageBase):
	#
	#  Code common to Image, Pixmap and GLPixmap classes

	def _init_with_ns_image(self, ns_image, flipped):
		ns_image.setFlipped_(flipped)
		self._ns_image = ns_image
	
	def get_size(self):
		return tuple(self._ns_image.size())
	
	def get_width(self):
		return self._ns_image.size()[0]
	
	def get_height(self):
		return self._ns_image.size()[1]
	
	def draw(self, canvas, src_rect, dst_rect):
		ns_src_rect = rect_to_ns_rect(src_rect)
		ns_dst_rect = rect_to_ns_rect(dst_rect)
		self._ns_image.drawInRect_fromRect_operation_fraction_(
			ns_dst_rect, ns_src_rect, NSCompositeSourceOver, 1.0)

export(ImageBase)
