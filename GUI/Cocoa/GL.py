#
#   PyGUI - OpenGL View - Cocoa
#

__all__ = ['GLConfig', 'GLView', 'GLPixmap']

import AppKit
from Foundation import NSSize
from AppKit import NSOpenGLPixelFormat, NSOpenGLView, \
	NSBitmapImageRep, NSCachedImageRep, NSImage, NSAlphaFirstBitmapFormat, \
	NSFloatingPointSamplesBitmapFormat
from Foundation import NSMakeRect
from OpenGL.GL import glViewport, glFlush, glFinish, glReadPixels, \
	GL_RGB, GL_RGBA, GL_LUMINANCE, GL_LUMINANCE_ALPHA, \
	GL_UNSIGNED_BYTE, GL_UNSIGNED_SHORT, GL_UNSIGNED_INT, GL_FLOAT, \
	glReadPixelsub, glTexImage2D, glPixelStorei, GL_UNPACK_ALIGNMENT
from OpenGL.GLU import gluBuild2DMipmaps
from GUI.GGLViews import GLView as GGLView
from GUI.GGLPixmaps import GLPixmap as GGLPixmap
from GUI.GGLConfig import GLConfig as GGLConfig
from GUI.GLContexts import GLContext
from GUI.GLTextures import Texture
from GUI.GLDisplayLists import DisplayList
from GUI.Utils import NSMultiClass, PyGUI_NS_ViewBase


#------------------------------------------------------------------------------

class GLConfig(GGLConfig):
	#  _ns_pixel_format   NSOpenGLPixelFormat
	
	def _ns_get_pixel_format(self, offscreen = False):
		attrs = [AppKit.NSOpenGLPFAColorSize, self._color_size]
		if self._double_buffer:
			attrs += [AppKit.NSOpenGLPFADoubleBuffer]
		if self._alpha:
			attrs += [AppKit.NSOpenGLPFAAlphaSize, self._alpha_size]
		if self._stereo:
			attrs += [AppKit.NSOpenGLPFAStereo]
		if self._aux_buffers:
			attrs += [AppKit.NSOpenGLPFAAuxBuffers, self._aux_buffers]
		if self._depth_buffer:
			attrs += [AppKit.NSOpenGLPFADepthSize, self._depth_size]
		if self._stencil_buffer:
			attrs += [AppKit.NSOpenGLPFAStencilSize, self._stencil_size]
		if self._accum_buffer:
			attrs += [AppKit.NSOpenGLPFAAccumSize, self._accum_size]
		if self._multisample:
			attrs += [AppKit.NSOpenGLPFASampleBuffers, 1]
			attrs += [AppKit.NSOpenGLPFASamples, self._samples_per_pixel]
		if offscreen:
			attrs += [AppKit.NSOpenGLPFAOffScreen]
		attrs.append(0)
		ns_pf = NSOpenGLPixelFormat.alloc().initWithAttributes_(attrs)
		if not ns_pf and self._double_buffer:
			attrs.remove(AppKit.NSOpenGLPFADoubleBuffer)
			ns_pf = NSOpenGLPixelFormat.alloc().initWithAttributes_(attrs)
		if not ns_pf:
			raise GLConfigError
		return ns_pf
	
	def _ns_set_pixel_format(self, ns_pf):
		def ns_attr(attr):
			return ns_pf.getValues_forAttribute_forVirtualScreen_(attr, 0)[0]
		self._ns_pixel_format = ns_pf
		self._double_buffer = ns_attr(AppKit.NSOpenGLPFADoubleBuffer)
		self._color_size = ns_attr(AppKit.NSOpenGLPFAColorSize)
		self._alpha_size = ns_attr(AppKit.NSOpenGLPFAAlphaSize)
		self._alpha = self._alpha_size > 0
		self._stereo = ns_attr(AppKit.NSOpenGLPFAStereo)
		self._aux_buffers = ns_attr(AppKit.NSOpenGLPFAAuxBuffers)
		self._depth_size = ns_attr(AppKit.NSOpenGLPFADepthSize)
		self._depth_buffer = self._depth_size > 0
		self._stencil_size = ns_attr(AppKit.NSOpenGLPFAStencilSize)
		self._stencil_buffer = self._stencil_size > 0
		self._accum_size = ns_attr(AppKit.NSOpenGLPFAAccumSize)
		self._accum_buffer = self._accum_size > 0
		self._multisample = ns_attr(AppKit.NSOpenGLPFASampleBuffers) > 0
		self._samples_per_pixel = ns_attr(AppKit.NSOpenGLPFASamples)

	def supported(self, mode = 'both'):
		try:
			ns_pf = self._ns_get_pixel_format()
			pf = GLConfig.__new__()
			pf._ns_set_pixel_format(ns_pf)
			return pf
		except GLConfigError:
			return None

#------------------------------------------------------------------------------

class GLView(GGLView):
	#  _ns_view      NSOpenGLView
	#  _ns_context   NSOpenGLContext
	#  _ns_flush     function for flushing/swapping buffers

	def __init__(self, config = None, share_group = None, **kwds):
		pf = GLConfig._from_args(config, kwds)
		ns_pf = pf._ns_get_pixel_format()
		width, height = GGLView._default_size
		ns_rect = NSMakeRect(0, 0, width, height)
		ns_view = _PyGUI_NSOpenGLView.alloc().initWithFrame_pixelFormat_(
			ns_rect, ns_pf)
		ns_view.pygui_component = self
		GGLView.__init__(self, _ns_view = ns_view)
		GLContext.__init__(self, share_group = share_group, _ns_pixel_format = ns_pf)
		ns_context = self._ns_context
		ns_view.setOpenGLContext_(ns_context)
		#ns_context.setView_(ns_view) # Docs say this is needed, but
		# prints warning and seems to work without.
		if pf.double_buffer:
			self._ns_flush = ns_context.flushBuffer
		else:
			self._ns_flush = glFlush
		self.set(**kwds)
		self.with_context(self._init_context)
	
	def destroy(self):
		#print "GLView.destroy:", self ###
		ns_view = self._ns_view
		GGLView.destroy(self)
		#print "GLView.destroy: breaking back link from", ns_view ###
		ns_view.pygui_component = None
	
	def invalidate(self):
		self._ns_view.setNeedsDisplay_(True)
	
	def update(self):
		self._ns_view.displayIfNeeded()

	def track_mouse(self):
		return self._ns_track_mouse(self._ns_view)
	
#------------------------------------------------------------------------------

class GLPixmap(GGLPixmap):

	def __init__(self, width, height, config = None, share_group = None, **kwds):
		pf = GLConfig._from_args(config, kwds)
		ns_pf = pf._ns_get_pixel_format()
		ns_size = NSSize(width, height)
		ns_cache = NSCachedImageRep.alloc().initWithSize_depth_separate_alpha_(
			ns_size, 0, True, True)
		ns_image = NSImage.alloc().initWithSize_(ns_size)			
		GLContext.__init__(self, share_group = share_group, _ns_pixel_format = ns_pf)
		self._ns_context.setView_(ns_cache.window().contentView())
		self._init_with_ns_image(ns_image, flipped = False)
		self._ns_cache = ns_cache
		self.with_context(self._init_context)
	
	def _ns_flush(self):
		glFlush()
		width, height = self.size
		pixels = glReadPixels(0, 0, int(width), int(height), GL_RGBA, GL_UNSIGNED_BYTE)
		bytes_per_row = int(width) * 4
		ns_new_bitmap = NSBitmapImageRep.alloc().\
			initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
			(pixels, "", "", "", ""), int(width), int(height), 8, 4, True, False, AppKit.NSDeviceRGBColorSpace, bytes_per_row, 0)
		ns_image = NSImage.alloc().initWithSize_(NSSize(width, height))
		ns_image.addRepresentation_(ns_new_bitmap)
		ns_image.lockFocus()
		ns_image.unlockFocus()
		self._ns_image = ns_image
		self._ns_bitmap_image_rep = ns_new_bitmap

#------------------------------------------------------------------------------

class _PyGUI_NSOpenGLView(NSOpenGLView, PyGUI_NS_ViewBase):
	__metaclass__ = NSMultiClass
	#
	#  pygui_component   GLView

	__slots__ = ['pygui_component']

	def isFlipped(self):
		return True

	def reshape(self):
		comp = self.pygui_component
		if comp.window:
			comp.with_context(comp._update_viewport)

	def drawRect_(self, rect):
		comp = self.pygui_component
		comp.with_context(comp._render, flush = True)
