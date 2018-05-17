#
#   Python GUI - Image Base - Generic
#

from GUI.Properties import Properties, overridable_property
from GUI.Geometry import rect_sized

class ImageBase(Properties):
	"""Abstract base class for Image, Pixmap and GLPixmap."""

	width = overridable_property('width', "Width of the image in pixels (read only).")
	height = overridable_property('height', "Height of the image in pixels (read only).")
	size = overridable_property('size', "Size of the image in pixels (read only).")
	bounds = overridable_property('bounds', "Bounding rectangle of the image in pixels (read only).")

	def get_size(self):
		return (self.width, self.height)
	
	def get_bounds(self):
		return rect_sized((0, 0), self.size)
	
	def draw(self, canvas, src_rect, dst_rect):
		"""Draw the part of the image specified by src_rect on the given canvas,
		scaled to fit within dst_rect."""
		raise NotImplementedError

