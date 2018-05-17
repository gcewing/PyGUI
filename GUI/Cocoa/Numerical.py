#--------------------------------------------------------------
#
#   PyGUI - NumPy interface - Cocoa
#
#--------------------------------------------------------------

from AppKit import NSBitmapImageRep, \
	NSAlphaNonpremultipliedBitmapFormat, NSCalibratedRGBColorSpace
from GUI import Image

# HACK! PyObjC 2.3 incorrectly wraps the following method, so we change the
# signature and pass the bitmap data in using ctypes.
NSBitmapImageRep.__dict__['initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bitmapFormat_bytesPerRow_bitsPerPixel_'].signature = '@52@0:4^v8i12i16i20i24c28c32@36I40i44i48'
import ctypes
planes_t = ctypes.c_void_p * 5

def image_from_ndarray(array, format, size = None):
	"""
	Creates an Image from a numpy ndarray object. The format
	may be 'RGB' or 'RGBA'. If a size is specified, the array
	will be implicitly reshaped to that size, otherwise the size
	is inferred from the first two dimensions of the array.
	"""
	if array.itemsize <> 1:
		raise ValueError("Color component size must be 1 byte")
	if size is not None:
		width, height = size
		data_size = array.size
		pixel_size = data_size // (width * height)
		if pixel_size <> len(format):
			raise ValueError("Array has wrong shape for specified size and format")
	else:
		height, width, pixel_size = array.shape
		if pixel_size <> len(format):
			raise ValueError("Array has wrong shape for specified format")
	bps = 8
	spp = pixel_size
	alpha = format.endswith("A")
	csp = NSCalibratedRGBColorSpace
	bpp = bps * spp
	bpr = width * pixel_size
	fmt = NSAlphaNonpremultipliedBitmapFormat
	ns_rep = NSBitmapImageRep.alloc()
	planes = planes_t(array.ctypes.data, 0, 0, 0, 0)
	ns_rep.initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bitmapFormat_bytesPerRow_bitsPerPixel_(
		ctypes.addressof(planes), width, height, bps, spp, alpha, False, csp, fmt, bpr, bpp)
	image = Image.__new__(Image)
	image._init_from_ns_rep(ns_rep)
	image._data = array
	return image
