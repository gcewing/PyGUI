#--------------------------------------------------------------
#
#   PyGUI - PIL interface - Windows
#
#--------------------------------------------------------------

from __future__ import absolute_import
from GUI import GDIPlus as gdi
from GUI import Image
from Image import merge

def image_from_pil_image(pil_image):
	"""Creates an Image from a Python Imaging Library (PIL)
	Image object."""
	pil_image.load()
	mode = pil_image.mode
	w, h = pil_image.size
	if mode == "RGB":
		r, g, b = pil_image.split()
		pil_image = merge(mode, (b, g, r))
		fmt = gdi.PixelFormat24bppRGB
	elif mode == "RGBA":
		r, g, b, a = pil_image.split()
		pil_image = merge(mode, (b, g, r, a))
		fmt = gdi.PixelFormat32bppARGB
	else:
		raise ValueError("Unsupported PIL image mode '%s'" % mode)
	data = pil_image.tostring()
	bitmap = gdi.Bitmap.from_data(w, h, fmt, data)
	image = Image.__new__(Image)
	image._win_image = bitmap
	image._data = data
	return image
