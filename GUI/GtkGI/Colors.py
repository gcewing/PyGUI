#
#   Python GUI - Colors - Gtk
#

from gi.repository import Gdk
from gi.repository.Gtk import Style
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
		self._gdk_rgba = Gdk.RGBA(red, green, blue, alpha)
		gdk_color = Gdk.Color(
			int(red * 65535),
			int(green * 65535),
			int(blue * 65535))
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


rgb = Color

s = Style()
selection_forecolor = Color._from_gdk_color(s.fg[3])
selection_backcolor = Color._from_gdk_color(s.bg[3])

#selection_forecolor = rgb(1, 1, 1)
#selection_backcolor = rgb(0, 0, 0)

#s = GtkStyleContext()
