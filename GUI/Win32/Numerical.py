#--------------------------------------------------------------
#
#   PyGUI - NumPy interface - Windows
#
#--------------------------------------------------------------

from numpy import ndarray, uint8
from GUI import GDIPlus as gdi
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
		height, width, pixel_size = shape
		if pixel_size <> len(format):
			raise ValueError("Last dimension of array does not match format")
	else:
		width, height = size
		pixel_size = len(format)
		data_size = array.size
		if data_size <> width * height * pixel_size:
			raise ValueError("Array has wrong shape for specified size and format")
		shape = (height, width, pixel_size)
		array = array.reshape(shape)
	swapped = ndarray(shape, uint8)
	swapped[..., 0] = array[..., 2]
	swapped[..., 1] = array[..., 1]
	swapped[..., 2] = array[..., 0]
	if pixel_size == 4:
		fmt = gdi.PixelFormat32bppARGB
		swapped[..., 3] = array[..., 3]
	else:
		fmt = gdi.PixelFormat24bppRGB
	data = swapped.tostring()
	bitmap = gdi.Bitmap.from_data(width, height, fmt, data)
	image = Image.__new__(Image)
	image._win_image = bitmap
	image._data = data
	return image
