#
#   PyGUI - OpenGL Textures - Generic
#

from weakref import WeakKeyDictionary
from OpenGL.GL import glGenTextures, glBindTexture, glDeleteTextures, \
	glTexImage2D, GL_TEXTURE_2D, GL_RGBA
from OpenGL.GLU import gluBuild2DMipmaps
from GUI.GGLContexts import current_share_group
from GUI.GLDisplayLists import call_when_not_compiling_display_list

#----------------------------------------------------------------------

class TextureIdMap(WeakKeyDictionary):

	def __del__(self):
		#print "GL.TextureIdMap.__del__:", self ###
		def free_texture():
			glDeleteTextures([gl_id])
		for share_group, gl_id in self.items():
			context = share_group._some_member()
			if context:
				#print "...freeing texture id", gl_id, "for", share_group, "using", context ###
				context.with_context(free_texture)

#----------------------------------------------------------------------

class Texture(object):
	"""This class encapsulates an OpenGL texture and maintains a
	representation of it for each OpenGL context with which it is used.
	Allocation and maintentance of texture numbers is handled automatically.
	
	Constructor:
	    Texture(texture_type)
	        where texture_type is the appropriate GL constant for the type
	        of texture (GL_TEXTURE_2D etc.)
	"""
	#
	#   _gl_type   int                 GL_TEXTURE_2D, etc.
	#   _gl_id     ShareGroup -> int   Mapping from OpenGL share group to texture number
	
	def __init__(self, texture_type):
		self._gl_type = texture_type
		self._gl_id = TextureIdMap()
	
	def deallocate(self):
		"""Deallocate any OpenGL resources that have been allocated for this
		texture in any context."""
		self._gl_id.__del__()

	def bind(self):
		"""Makes this texture the current texture for the current context
		by calling glBindTexture. If this texture has not previously been
		used with the current context, do_setup() is called to allocate
		and initialise a representation of the texture."""
		gl_id = self.gl_id()
		glBindTexture(self._gl_type, gl_id)
	
	def gl_id(self):
		"""Returns the OpenGL texture number corresponding to this texture
		in the current context. May trigger allocation of a new texture and
		a call to do_setup(). Does not bind the texture, unless a new texture
		is allocated, in which case the current texture binding may be changed
		as a side effect."""
		share_group = current_share_group()
		gl_id = self._gl_id.get(share_group)
		if gl_id is None:
			gl_id = glGenTextures(1)
			#print "GLTexture: assigned id %d for %s in share group %s" % (
			#	gl_id, self, share_group) ###
			self._gl_id[share_group] = gl_id
			call_when_not_compiling_display_list(lambda: self._setup(gl_id))
		return gl_id
	
	def _setup(self, gl_id):
		glBindTexture(self._gl_type, gl_id)
		self.do_setup()
	
	def do_setup(self):
		"""Subclasses should override this to make the necessary OpenGL
		calls to initialise the texture, assuming that glBindTexture has
		already been called."""
		raise NotImplementedError

	def gl_tex_image_2d(self, image, target = GL_TEXTURE_2D, internal_format = GL_RGBA,
			border = False, with_mipmaps = False):
		"""Load the currently bound texture with data from an image, with automatic
		scaling to power-of-2 size and optional mipmap generation."""
		border = bool(border)
		if border and with_mipmaps:
			raise ValueError("Bordered texture cannot have mipmaps")
		b2 = 2 * border
		width, height = image.size
		twidth = pow2up(width - b2) + b2
		theight = pow2up(height - b2) + b2
		#print "GUI.GGLTextures.Texture.gl_tex_image_2d: before scaling: size =", (width, height) ###
		if width <> twidth or height <> theight:
			#print "GUI.GGLTextures.Texture.gl_tex_image_2d: scaling image to size", (twidth, theight) ###
			from Pixmaps import Pixmap
			image2 = Pixmap(twidth, theight)
			def scale(canvas):
				image.draw(canvas, (0, 0, width, height), (0, 0, twidth, theight))
			image2.with_canvas(scale)
			image = image2
		format, type, data = self._gl_get_texture_data(image)
		if with_mipmaps:
			#print "GUI.GGLTextures.Texture.gl_tex_image_2d: loading mipmaps" ###
			gluBuild2DMipmaps(target, internal_format, twidth, theight,
				format, type, data)
		else:
			#print "GUI.GGLTextures.Texture.gl_tex_image_2d: loading texture" ###
			glTexImage2D(target, 0, internal_format, twidth, theight, border,
				format, type, data)

#----------------------------------------------------------------------

def pow2up(size):
	#  Round size up to a power of 2
	psize = 1
	while psize < size:
		psize <<= 1
	return psize
