#
#   Python GUI - Pixmap - Generic
#

from GUI import ImageBase

class Pixmap(ImageBase):
	"""A Pixmap is an offscreen area that can be used both as a
	destination for drawing and a source of image data for drawing
	in a View or another Pixmap.
	
	Constructor:
		Pixmap(width, height)
	"""
	
	def with_canvas(self, proc):
		"""Call the given procedure with a canvas suitable for drawing on
		this Pixmap. The canvas is valid only for the duration of the call,
		and should not be retained beyond it."""
		raise NotImplementedError
