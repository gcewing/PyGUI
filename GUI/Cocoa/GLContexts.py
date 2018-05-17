#
#   PyGUI - OpenGL Contexts - Cocoa
#

from AppKit import NSOpenGLContext
from GUI.GGLContexts import GLContext as GGLContext

class GLContext(GGLContext):
	#  _ns_context   NSOpenGLContext

	def __init__(self, share_group, _ns_pixel_format):
		GGLContext.__init__(self, share_group)
		shared_context = self._get_shared_context()
		if shared_context:
			ns_share = shared_context._ns_context
		else:
			ns_share = None
		ns_context = NSOpenGLContext.alloc().initWithFormat_shareContext_(
			_ns_pixel_format, ns_share)
		self._ns_context = ns_context

	def _with_context(self, proc, flush):
		#print "GLContext._with_context: Entering context", self._ns_context ###
		old_context = NSOpenGLContext.currentContext()
		self._ns_context.makeCurrentContext()
		try:
			self._with_share_group(proc)
			if flush:
				self._ns_flush()
		finally:
			#print "GL: Restoring previous context" ###
			if old_context:
				old_context.makeCurrentContext()
			else:
				NSOpenGLContext.clearCurrentContext()
