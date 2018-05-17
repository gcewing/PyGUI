#
#   PyGUI - OpenGL Pixel Formats - Generic
#

from GUI.Properties import Properties, overridable_property

class GLPixelFormat(Properties):
	"""Class holding the attributes of an OpenGL pixel format."""
	
	#  NOTE: When adding a property here, also add it to
	#        _pixel_format_attribute_names below.
	
	double_buffer = overridable_property("double_buffer", "True if context is to be double-buffered.")
	alpha = overridable_property("alpha", "True if there is to be an alpha channel.")
	color_size = overridable_property("color_size", "Number of bits per colour buffer component.")
	alpha_size = overridable_property("alpha_size", "Number of bits per alpha channel component.")
	stereo = overridable_property("stereo", "True if stereoscopic context is required.")
	aux_buffers = overridable_property("aux_buffers", "Number of auxiliary colour buffers to allocate.")
	depth_buffer = overridable_property("depth_buffer", "True if a depth buffer is required.")
	depth_size = overridable_property("depth_size", "Number of bits per depth buffer element.")
	stencil_buffer = overridable_property("stencil_buffer", "True if a stencil buffer is required.")
	stencil_size = overridable_property("stencil_size", "Number of bits per stencil buffer element.")
	accum_buffer = overridable_property("accum_buffer", "True if an accumulation buffer is required.")
	accum_size = overridable_property("accum_size", "Number of bits per accumulation buffer component.")
	multisample = overridable_property("multisample", "True if a multisampled context is required.")
	samples_per_pixel = overridable_property("samples_per_pixel", "Number of samples per multisampled pixel.")
	
	_double_buffer = True
	_alpha = True
	_color_size = 8
	_alpha_size = 8
	_stereo = False
	_aux_buffers = 0
	_depth_buffer = True
	_depth_size = 32
	_stencil_buffer = False
	_stencil_size = 8
	_accum_buffer = False
	_accum_size = 8
	_multisample = False
	_samples_per_pixel = False
	
	_pixel_format_attribute_names = (
		'double_buffer', 'alpha', 'color_size', 'alpha_size',
		'stereo', 'aux_buffers', 'depth_buffer', 'depth_size',
		'stencil_buffer', 'stencil_size', 'accum_buffer', 'accum_size',
		'multisample', 'samples_per_pixel',
	)
		
	def _from_args(cls, pixel_format, kwds):
		#  Extract pixel format arguments from arguments of GLView.__init__
		#  or GLPixmap.__init__ and return a GLPixelFormat. Used keyword
		#  arguments are removed from kwds.
		pf_kwds = {}
		for name in cls._pixel_format_attribute_names:
			if name in kwds:
				pf_kwds[name] = kwds.pop(name)
		if pixel_format and pf_kwds:
			raise TypeError("Explicit pixel_format cannot be used with other pixel format keyword arguments")
		if not pixel_format:
			pixel_format = cls(**pf_kwds)
		return pixel_format
	
	_from_args = classmethod(_from_args)
	
	def get_double_buffer(self):
		return self._double_buffer
	
	def set_double_buffer(self, x):
		self._double_buffer = x

	def get_alpha(self):
		return self._alpha
	
	def set_alpha(self, x):
		self._alpha = x

	def get_color_size(self):
		return self._color_size
	
	def set_color_size(self, x):
		self._color_size = x

	def get_alpha_size(self):
		return self._alpha_size
	
	def set_alpha_size(self, x):
		self._alpha_size = x

	def get_stereo(self):
		return self._stereo
	
	def set_stereo(self, x):
		self._stereo = x

	def get_aux_buffers(self):
		return self._aux_buffers
	
	def set_aux_buffers(self, x):
		self._aux_buffers = x

	def get_depth_buffer(self):
		return self._depth_buffer
	
	def set_depth_buffer(self, x):
		self._depth_buffer = x

	def get_depth_size(self):
		return self._depth_size
	
	def set_depth_size(self, x):
		self._depth_size = x

	def get_stencil_buffer(self):
		return self._stencil_buffer
	
	def set_stencil_buffer(self, x):
		self._stencil_buffer = x

	def get_stencil_size(self):
		return self._stencil_size
	
	def set_stencil_size(self, x):
		self._stencil_size = x

	def get_accum_buffer(self):
		return self._accum_buffer
	
	def set_accum_buffer(self, x):
		self._accum_buffer = x

	def get_accum_size(self):
		return self._accum_size
	
	def set_accum_size(self, x):
		self._accum_size = x

	def get_multisample(self):
		return self._multisample
	
	def set_multisample(self, x):
		self._multisample = x

	def get_samples_per_pixel(self):
		return self._samples_per_pixel
	
	def set_samples_per_pixel(self, x):
		self._samples_per_pixel = x

	def supported(self):
		"""Determine whether the combination of attributes requested by this pixel format
		can be satisfied. If successful, a new GLPixelFormat object is returned whose
		attributes reflect those actually allocated. Otherwise, a GLPixelFormatError is
		raised."""
		raise NotImplementedError

#------------------------------------------------------------------------------

class GLPixelFormatError(ValueError):

	def __init__(self):
		ValueError.__init__(self,
			"OpenGL pixel format attribute request cannot be satisfied")
