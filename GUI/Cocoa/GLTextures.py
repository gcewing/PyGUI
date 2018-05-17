#
#   PyGUI - OpenGL Textures - Cocoa
#

from AppKit import NSAlphaFirstBitmapFormat, NSFloatingPointSamplesBitmapFormat
from OpenGL import GL
from GUI.GGLTextures import Texture as GTexture

class Texture(GTexture):

	def _gl_get_texture_data(self, image):
		ns_rep = image._ns_bitmap_image_rep
		if ns_rep.numberOfPlanes() <> 1:
			raise ValueError("Cannot use planar image data as GL texture")
		ns_format = ns_rep.bitmapFormat()
		if ns_format & NSAlphaFirstBitmapFormat:
			raise ValueError("Cannot use alpha-first image data as GL texture")
		fp_samples = ns_format & NSFloatingPointSamplesBitmapFormat <> 0
		bits_per_pixel = ns_rep.bitsPerPixel()
		bytes_per_row = ns_rep.bytesPerRow()
		samples_per_pixel = ns_rep.samplesPerPixel()
		if bits_per_pixel % samples_per_pixel <> 0:
			raise ValueError("Image data format not usable as GL texture")
		bits_per_sample = bits_per_pixel / samples_per_pixel
		try:
			gl_format = format_map[samples_per_pixel]
			gl_type = type_map[bits_per_sample, fp_samples]
		except KeyError:
			raise ValueError("Image data format not usable as GL texture")
		data = ns_rep.bitmapData()
		if 0:
			print "GUI.GLTexture._gl_get_texture_data_and_format:" ###
			print "format =", gl_format_map.get(gl_format) ###
			print "type =", gl_type_map.get(gl_type) ###
			print "data length =", len(data) ###
			print repr(data[:16]) ###
		GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
		return gl_format, gl_type, str(data)

#------------------------------------------------------------------------------

format_map = {
	3: GL.GL_RGB,
	4: GL.GL_RGBA,
	1: GL.GL_LUMINANCE,
	2: GL.GL_LUMINANCE_ALPHA,
}

type_map = {
	(8, 0): GL.GL_UNSIGNED_BYTE,
	(16, 0): GL.GL_UNSIGNED_SHORT,
	(32, 0): GL.GL_UNSIGNED_INT,
	(32, 1): GL.GL_FLOAT,
}

gl_format_map = {
	GL.GL_RGB: 'GL_RGB',
	GL.GL_RGBA: 'GL_RGBA',
	GL.GL_LUMINANCE: 'GL_LUMINANCE',
	GL.GL_LUMINANCE_ALPHA: 'GL_LUMINANCE_ALPHA',
}

gl_type_map = {
	GL.GL_UNSIGNED_BYTE: 'GL_UNSIGNED_BYTE',
	GL.GL_UNSIGNED_SHORT: 'GL_UNSIGNED_SHORT',
	GL.GL_UNSIGNED_INT: 'GL_UNSIGNED_INT',
	GL.GL_FLOAT: 'GL_FLOAT',
}

