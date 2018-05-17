#--------------------------------------------------------------
#
#   PyGUI - NumPy interface - Gtk
#
#--------------------------------------------------------------

from gtk import gdk
from GUI import Image

def image_from_ndarray(array, format, size = None):
	"""
	Creates an Image from a numpy ndarray object. The format
	may be 'RGB' or 'RGBA'. If a size is specified, the array
	will be implicitly reshaped to that size, otherwise the size
	is inferred from the first two dimensions of the array.
	"""
	if array.itemsize <> 1:
		raise ValueError("Color component size must be 1 byte")
	if size is None:
		shape = array.shape
		if len(shape) <> 3:
			raise ValueError("Array has wrong number of dimensions")
		width, height, pixel_size = shape
		if pixel_size <> len(format):
			raise ValueError("Last dimension of array does not match format")
	else:
		width, height = size
		pixel_size = len(format)
		data_size = array.size
		if data_size <> width * height * pixel_size:
			raise ValueError("Array has wrong shape for specified size and format")
	alpha = pixel_size == 4
	gdk_pixbuf = gdk.pixbuf_new_from_data(array, gdk.COLORSPACE_RGB, alpha,
		8, width, height, width * pixel_size)
	image = Image._from_gdk_pixbuf(gdk_pixbuf)
	#image._data = array ###
	return image
