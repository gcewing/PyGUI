#
#		Python GUI - Pixmaps - Cocoa
#

from Foundation import NSSize
from AppKit import NSImage, NSCachedImageRep, NSBitmapImageRep, \
	NSCalibratedRGBColorSpace, NSImageCacheNever, NSGraphicsContext, \
	NSAffineTransform
from GUI import export
from GUI import Canvas
from GUI.GPixmaps import Pixmap as GPixmap

class Pixmap(GPixmap):
	#  _ns_bitmap_image_rep  NSBitmapImageRep

	def __init__(self, width, height):
		GPixmap.__init__(self)
		#ns_size = NSSize(width, height)
		#ns_image = NSImage.alloc().initWithSize_(ns_size)
		ns_image = NSImage.alloc().init()
		ns_image.setCacheMode_(NSImageCacheNever)
		row_bytes = 4 * width
		ns_bitmap = NSBitmapImageRep.alloc().\
			initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
			None, width, height, 8, 4, True, False, NSCalibratedRGBColorSpace, row_bytes, 32)
		ns_image.addRepresentation_(ns_bitmap)
		ns_bitmap_context = NSGraphicsContext.graphicsContextWithBitmapImageRep_(ns_bitmap)
		ns_graphics_context = FlippedNSGraphicsContext.alloc().initWithBase_(ns_bitmap_context)
		ns_tr = NSAffineTransform.transform()
		ns_tr.translateXBy_yBy_(0.0, height)
		ns_tr.scaleXBy_yBy_(1.0, -1.0)
		#  Using __class__ to get +saveGraphicsState instead of -saveGraphicsState
		NSGraphicsContext.__class__.saveGraphicsState()
		try:
			NSGraphicsContext.setCurrentContext_(ns_graphics_context)
			ns_tr.concat()
		finally:
			NSGraphicsContext.__class__.restoreGraphicsState()
		self._init_with_ns_image(ns_image, flipped = True) #False)
		self._ns_bitmap_image_rep = ns_bitmap
		self._ns_graphics_context = ns_graphics_context
	
	def with_canvas(self, proc):
		NSGraphicsContext.__class__.saveGraphicsState()
		NSGraphicsContext.setCurrentContext_(self._ns_graphics_context)
		try:
			canvas = Canvas()
			proc(canvas)
		finally:
			NSGraphicsContext.__class__.restoreGraphicsState()

class FlippedNSGraphicsContext(NSGraphicsContext):

	def initWithBase_(self, base):
		self.base = base
		self.graphics_port = base.graphicsPort()
		return self

	def isFlipped(self):
		return True
	
	def graphicsPort(self):
		return self.graphics_port
	
	def isDrawingToScreen(self):
		return self.base.isDrawingToScreen()

	def setCompositingOperation_(self, x):
		self.base.setCompositingOperation_(x)

	def focusStack(self):
		return self.base.focusStack()

	def saveGraphicsState(self):
		return self.base.saveGraphicsState()

	def restoreGraphicsState(self):
		return self.base.restoreGraphicsState()

export(Pixmap)
