#
#   PyGUI - OpenGL View - Generic
#

from OpenGL.GL import glViewport, glMatrixMode, glLoadIdentity, \
	GL_PROJECTION, GL_MODELVIEW
from GUI import Component
from GUI import ViewBase
from GUI.GLContexts import GLContext

class GLError(StandardError):
	pass

class GLView(ViewBase, Component, GLContext):
	"""A GLView is a Component providing an OpenGL 3D display area.
	
	Constructors:
		GLView(config_attr = value..., share = None)
		GLView(config, share = None)
	"""
	
	_default_size = (100, 100)

	def __init__(self, **kwds):
		Component.__init__(self, **kwds)
		ViewBase.__init__(self)
	
	def destroy(self):
		ViewBase.destroy(self)
		Component.destroy(self)
	
	def _render(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		self.render()
	
	def render(self):
		"""This method is called when the contents of the view needs to
		be redrawn, with the view's OpenGL context as the current context.
		The modelview matrix has been selected as the current matrix and
		set to an identity matrix. After calling this method, buffers will
		be automatically swapped or drawing flushed as appropriate."""
		pass
	
	def viewport_changed(self):
		"""This method is called when the view's size has changed, with
		the view's OpenGL context as the current context, and the OpenGL
		viewport set to (0, 0, width, height). The default implementation
		loads an identity projection matrix and calls init_projection()."""
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		self.init_projection()
	
	def init_projection(self):
		"""This method is called to establish the projection whenever the
		viewport changes. The projection matrix has been selected as the
		current matrix and set to an identity matrix."""
		pass

	def update(self):
		"""Redraws the contents of the view immediately, without waiting
		for a return to the event loop."""
		self.with_context(self.render, flush = True)

	def _init_context(self):
		self.init_context()
		self._update_viewport()
	
	def _update_viewport(self):
		width, height = self.size
		glViewport(0, 0, int(width), int(height))
		self.viewport_changed()
		
