#
#   PyGUI - OpenGL Textures - Gtk
#

from GUI.GGLTextures import Texture as GTexture

class Texture(GTexture):

	def _gl_get_texture_data(self, image):
		raise NotImplementedError("Loading texture from image not yet implemented for Gtk")
