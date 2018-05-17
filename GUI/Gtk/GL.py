#
#   PyGUI - OpenGL View - Gtk/GtkGLExt
#

try:
	from gtk import gdkgl, gtkgl
	from OpenGL.GL import glViewport
except ImportError, e:
	raise ImportError("OpenGL support is not available (%s)" % e)

from GUI.GGLConfig import GLConfig as GGLConfig, GLConfigError
from GUI.GGLViews import GLView as GGLView
from GUI.GGLPixmaps import GLPixmap as GGLPixmap
from GUI import ImageBase
from GUI.GtkPixmaps import GtkPixmap
from GUI.GLContexts import GLContext
from GUI.GLTextures import Texture
from GUI.GLDisplayLists import DisplayList

#------------------------------------------------------------------------------

def gtk_find_config_default(attr, mode_bit):
	try:
		cfg = gdkgl.Config(mode = mode_bit)
		value = cfg.get_attrib(attr)[0]
	except gdkgl.NoMatches:
		value = 0
	print "default for attr", attr, "=", value
	return value

#------------------------------------------------------------------------------

class GLConfig(GGLConfig):
	
	_alpha = False
	_color_size = 1
	_alpha_size = 1
	_depth_size = 1
	_stencil_size = 1
	_accum_size = 1
	
	def _gtk_get_config(self):
		csize = self._color_size
		asize = 0
		dsize = 0
		ssize = 0
		acsize = 0
		aasize = 0
		if self._alpha:
			asize = self._alpha_size
		if self._depth_buffer:
			dsize = self._depth_size
		if self._stencil_buffer:
			ssize = self._stencil_size
		if self._accum_buffer:
			acsize = self._accum_size
			if self._alpha:
				aasize = acsize
		attrs = [
			gdkgl.RGBA,
			gdkgl.RED_SIZE, csize,
			gdkgl.GREEN_SIZE, csize,
			gdkgl.BLUE_SIZE, csize,
			gdkgl.ALPHA_SIZE, asize,
			gdkgl.AUX_BUFFERS, self._aux_buffers,
			gdkgl.DEPTH_SIZE, dsize,
			gdkgl.STENCIL_SIZE, ssize,
			gdkgl.ACCUM_RED_SIZE, acsize,
			gdkgl.ACCUM_GREEN_SIZE, acsize,
			gdkgl.ACCUM_BLUE_SIZE, acsize,
			gdkgl.ACCUM_ALPHA_SIZE, aasize,
		]
		if self._double_buffer:
			attrs += [gdkgl.DOUBLEBUFFER]
		if self._stereo:
			attrs += [gdkgl.STEREO]
		if self._multisample:
			attrs += [
				gdkgl.SAMPLE_BUFFERS, 1,
				gdkgl.SAMPLES, self._samples_per_pixel
			]
		result = self._gdkgl_config(attrs)
		if not result and self._double_buffer:
			attrs.remove(gdkgl.DOUBLEBUFFER)
			result = self._gdkgl_config(attrs)
		if not result:
			raise GLConfigError
		return result
	
	def _gdkgl_config(self, attrs):
		try:
			return gdkgl.Config(attrib_list = attrs)
		except gdkgl.NoMatches:
			return None
	
	def _gtk_set_config(self, gtk_config):
		def attr(key):
			return gtk_config.get_attrib(key)[0]
		self._color_size = attr(gdkgl.RED_SIZE)
		self._alpha_size = attr(gdkgl.ALPHA_SIZE)
		self._alpha = gtk_config.has_alpha()
		self._double_buffer = gtk_config.is_double_buffered()
		self._stereo = gtk_config.is_stereo()
		self._aux_buffers = attr(gdkgl.AUX_BUFFERS)
		self._depth_size = attr(gdkgl.DEPTH_SIZE)
		self._depth_buffer = gtk_config.has_depth_buffer()
		self._stencil_size = attr(gdkgl.STENCIL_SIZE)
		self._stencil_buffer = gtk_config.has_stencil_buffer()
		self._accum_size = attr(gdkgl.ACCUM_RED_SIZE)
		self._accum_buffer = gtk_config.has_accum_buffer()
		self._multisample = attr(gdkgl.SAMPLE_BUFFERS) <> 0
		self._samples_per_pixel = attr(gdkgl.SAMPLES)
	
	def supported(self, mode = 'both'):
		try:
			gtk_config = self._gtk_get_config()
			pf = GLConfig.__new__(GLConfig)
			pf._gtk_set_config(gtk_config)
			return pf
		except GLConfigError:
			return None

#------------------------------------------------------------------------------

class GLView(GGLView):

	_first_expose = 0

	def __init__(self, config = None, share_group = None, **kwds):
		pf = GLConfig._from_args(config, kwds)
		GLContext.__init__(self, share_group, pf, kwds)
		gtk_share = self._gtk_get_share()
		area = gtkgl.DrawingArea(glconfig = self._gl_config, share_list = gtk_share,
			render_type = gdkgl.RGBA_TYPE)
		area.show()
		self._gtk_connect_after(area, "realize", self._gtk_realize_signal)
		self._gtk_connect(area, "expose-event", self._gtk_expose_event_signal)
		GGLView.__init__(self, _gtk_outer = area, _gtk_input = area,
			_gtk_focus = area)
		self.set(**kwds)

	def _resized(self, delta):
		self.with_context(self._update_viewport)
	
	def _gtk_get_gl_context(self):
		if not self._gl_context:
			self._gtk_inner_widget.realize()
		return self._gl_context
	
	def _gtk_realize_signal(self):
		#print "GLView._gtk_realize_signal" ###
		area = self._gtk_inner_widget
		self._gl_drawable = area.get_gl_drawable()
		self._gl_context = area.get_gl_context()
		self.with_context(self.init_context)
	
	def _gtk_expose_event_signal(self, gtk_event):
		#print "GLView._gtk_expose_event_signal" ###
		if not self._first_expose:
			self.with_context(self._update_viewport)
			self._first_expose = 1
		try:
			self.with_context(self._render, flush = True)
		except:
			import sys, traceback
			sys.stderr.write("\n<<<<<<<<<< Exception while rendering a GLView\n")
			traceback.print_exc()
			sys.stderr.write(">>>>>>>>>>\n\n")
	
	def invalidate(self):
		gtk_window = self._gtk_outer_widget.window
		if gtk_window:
			width, height = self.size
			gtk_window.invalidate_rect((0, 0, width, height), 0)

#------------------------------------------------------------------------------

class GLPixmap(GtkPixmap, GGLPixmap):

	def __init__(self, width, height, config = None, share_group = None, **kwds):
		pf = GLConfig._from_args(config, kwds)
		GLContext.__init__(self, share_group, pf, kwds)
		gl_config = pf._gtk_get_config()
		self._gl_config = gl_config
#		if share:
#			gtk_share = share.shared_context._gtk_get_gl_context()
#		else:
#			gtk_share = None
		gtk_share = self._gtk_get_share()
		GtkPixmap.__init__(self, width, height)
		gdk_pixmap = self._gdk_pixmap
		gdkgl.ext(gdk_pixmap)
		self._gl_drawable = gdk_pixmap.set_gl_capability(glconfig = gl_config)
		print "GLPixmap: self._gl_drawable =", self._gl_drawable ###
		self._gl_context = gdkgl.Context(
			self._gl_drawable,
			direct = False,
			share_list = gtk_share,
			render_type = gdkgl.RGBA_TYPE
		)
		print "GLPixmap: self._gl_context =", self._gl_context ###
		ImageBase.__init__(self, **kwds)
		self.with_context(self._init_context)
		print "GLPixmap: initialised context" ###

#	def _init_context(self):
#		width, height = self.size
#		glViewport(0, 0, int(width), int(height))
#		print "GLPixmap: Set viewport to", width, height ###
#		self.init_context()

	