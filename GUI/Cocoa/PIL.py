#--------------------------------------------------------------
#
#   PyGUI - PIL interface - Cocoa
#
#--------------------------------------------------------------

import ctypes
from AppKit import NSBitmapImageRep, \
	NSAlphaNonpremultipliedBitmapFormat, NSFloatingPointSamplesBitmapFormat, \
	NSDeviceCMYKColorSpace, NSCalibratedRGBColorSpace
from GUI import Image

def hack_objc_sig():
	#print "GUI[Cocoa].PIL: Hacking objc method signature" ###
	# HACK! PyObjC 2.3 incorrectly wraps the following method, so we change the
	# signature and pass the bitmap data in using ctypes.
	NSBitmapImageRep.__dict__['initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bitmapFormat_bytesPerRow_bitsPerPixel_'].signature = '@52@0:4^v8i12i16i20i24c28c32@36I40i44i48'

planes_t = ctypes.c_char_p * 5

debug_pil = False

def image_from_pil_image(pil_image):
	"""Creates an Image from a Python Imaging Library (PIL)
	Image object."""
	mode = pil_image.mode
	w, h = pil_image.size
	data = pil_image.tostring()
	alpha = False
	cmyk = False
	floating = False
	if mode == "1":
		bps = 1; spp = 1
	elif mode == "L":
		bps = 8; spp = 1
	elif mode == "RGB":
		bps = 8; spp = 3
	elif mode == "RGBA":
		bps = 8; spp = 4; alpha = True
	elif mode == "CMYK":
		bps = 8; spp = 4; cmyk = True
	elif mode == "I":
		bps = 32; spp = 1
	elif mode == "F":
		bps = 32; spp = 1; floating = True
	else:
		raise ValueError("Unsupported PIL image mode '%s'" % mode)
	if cmyk:
		csp = NSDeviceCMYKColorSpace
	else:
		csp = NSCalibratedRGBColorSpace
	fmt = NSAlphaNonpremultipliedBitmapFormat
	if floating:
		fmt |= NSFloatingPointSamplesBitmapFormat
	bpp = bps * spp
	bpr = w * ((bpp + 7) // 8)
	if debug_pil:
		print "GUI.PIL:"
		print "image size =", (w, h)
		print "data size =", len(data)
		print "bits per sample =", bps
		print "samples per pixel =", spp
		print "bits per pixel =", bpp
		print "bytes per row =", bpr
	hack_objc_sig()
	ns_rep = NSBitmapImageRep.alloc()
	planes = planes_t(data, "", "", "", "")
	ns_rep.initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bitmapFormat_bytesPerRow_bitsPerPixel_(
		ctypes.addressof(planes), w, h, bps, spp, alpha, False, csp, fmt, bpr, bpp)
#	planes = (data, "", "", "", "")
#	ns_rep.initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
#		planes, w, h, bps, spp, alpha, False, csp, bpr, bpp)
	image = Image.__new__(Image)
	image._init_from_ns_rep(ns_rep)
	image._data = data
	return image


