#
#   Python GUI - Colors - Gtk
#

from gtk import gdk
from GUI import export
from GUI.GColors import Color as GColor

class Color(GColor):

	_alpha = 1.0

	def _from_gdk_color(cls, _gdk_color):
		c = cls.__new__(cls)
		c._gdk_color = _gdk_color
		return c
	
	_from_gdk_color = classmethod(_from_gdk_color)

	def __init__(self, red, green, blue, alpha = 1.0):
		self._rgba = (red, green, blue, alpha)
		gdk_color = gdk.Color()
		gdk_color.red = int(red * 65535)
		gdk_color.green = int(green * 65535)
		gdk_color.blue = int(blue * 65535)
		self._gdk_color = gdk_color
		self._alpha = alpha
	
	def get_red(self):
		return self._gdk_color.red / 65535.0
	
	def get_green(self):
		return self._gdk_color.green / 65535.0

	def get_blue(self):
		return self._gdk_color.blue / 65535.0
	
	def get_alpha(self):
		return self._alpha

export(Color)
