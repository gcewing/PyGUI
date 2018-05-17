#
#   PyGUI - OpenGL Pixmap - Generic
#

from OpenGL.GL import glViewport
from GUI import ImageBase
from GUI.GLContexts import GLContext

class GLPixmap(ImageBase, GLContext):
	"""An offscreen OpenGL drawing area.

	Constructors:
		GLPixmap(width, height, share = None, config_attr = value...)
		GLPixmap(width, height, config, share = None)
	"""

	def destroy(self):
		GLContext.destroy(self)

	def _init_context(self):
		width, height = self.size
		glViewport(0, 0, int(width), int(height))
		self.init_context()
