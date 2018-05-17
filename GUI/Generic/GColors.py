#
#   Python GUI - Colors - Generic
#

from GUI.Properties import overridable_property

class Color(object):
	"""A drawing color.
	
	Constructors:
		rgb(red, green, blue, alpha = 1.0)
			where red, green, blue, alpha are in the range 0.0 to 1.0
	
	Properties:
		red   -->  float
		green -->  float
		blue  -->  float
		rgb   -->  (red, green, blue)
		rgba  -->  (red, green, blue, alpha)
	"""

	red = overridable_property('red', "Red component (0.0 to 1.0)")
	green = overridable_property('green', "Blue component (0.0 to 1.0)")
	blue = overridable_property('blue', "Blue component (0.0 to 1.0)")
	alpha = overridable_property('alpha', "Alpha (opacity) component")
	rgb = overridable_property('rgb', "Tuple of (red, green, blue) (0.0 to 1.0)")
	rgba = overridable_property('rgba',
		"Tuple of (red, green, blue, alpha) (0.0 to 1.0)")
	
	def get_alpha(self):
		return 1.0

	def get_rgb(self):
		return (self.red, self.green, self.blue)
	
	def set_rgb(self, x):
		self.red, self.green, self.blue = x
	
	def get_rgba(self):
		return (self.red, self.green, self.blue, self.alpha)
	
	def set_rgba(self, x):
		self.red, self.green, self.blue, self.alpha = x

	def __str__(self):
		return "Color(%g,%g,%g,%g)" % self.rgba
