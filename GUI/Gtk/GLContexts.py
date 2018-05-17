#
#   PyGUI - GL Context - Gtk
#

from GUI.GGLContexts import GLContext as GGLContext

try:
	from OpenGL.GL import glFlush
except ImportError, e:
	raise ImportError("OpenGL support is not available (%s)" % e)

class GLContext(GGLContext):

	_gl_drawable = None
	_gl_context = None
	
	def __init__(self, share_group, config, kwds):
		GGLContext.__init__(self, share_group)
		self._gl_config = config._gtk_get_config()

	def _gtk_get_share(self):
		shared_context = self._get_shared_context()
		if shared_context:
			return shared_context._gtk_get_gl_context()
		else:
			return None

	def _with_context(self, proc, flush):
		drawable = self._gl_drawable
		if drawable:
			if not drawable.gl_begin(self._gl_context):
				raise ValueError(
					"Unable to make %s the current OpenGL context (gl_begin failed)" % self)
			try:
				self._with_share_group(proc)
				if flush:
					if drawable.is_double_buffered():
						#print "GLContext.with_context: swapping buffers" ###
						drawable.swap_buffers()
					else:
						#print "GLContext.with_context: flushing" ###
						glFlush()
			finally:
				drawable.gl_end()
			#return result

