#--------------------------------------------------------------
#
#   PyGUI - PIL interface - Gtk
#
#--------------------------------------------------------------

from gtk import gdk
from gtk.gdk import COLORSPACE_RGB
from GUI import Image

def image_from_pil_image(pil_image):
	"""Creates an Image from a Python Imaging Library (PIL)
	Image object."""
	mode = pil_image.mode
	w, h = pil_image.size
	data = pil_image.tostring()
	if mode == "RGB":
		bps = 3; alpha = False
	elif mode == "RGBA":
		bps = 4; alpha = True
	else:
		raise ValueError("Unsupported PIL image mode '%s'" % mode)
	bpr = w * bps
	image = Image.__new__(Image)
	image._gdk_pixbuf = gdk.pixbuf_new_from_data(data, COLORSPACE_RGB,
		alpha, 8, w, h, bpr)
	return image
