#
#   Python GUI - Colors - PyObjC
#

from AppKit import NSColor, NSCalibratedRGBColorSpace
from GUI import export
from GUI.GColors import Color as GColor

NSColor.setIgnoresAlpha_(False)

class Color(GColor):

	def _from_ns_color(cls, ns_color):
		color = cls.__new__(cls)
		color._ns_color = ns_color.colorUsingColorSpaceName_(
			NSCalibratedRGBColorSpace)
		return color
	
	_from_ns_color = classmethod(_from_ns_color)
	
	def __init__(self, red, green, blue, alpha = 1.0):
		self._ns_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(
			red, green, blue, alpha)

	def get_red(self):
		return self._ns_color.redComponent()
	
	def get_green(self):
		return self._ns_color.greenComponent()

	def get_blue(self):
		return self._ns_color.blueComponent()
	
	def get_alpha(self):
		return self._ns_color.alphaComponent()
	
	def get_rgb(self):
		return self.get_rgba()[:3]
	
	def get_rgba(self):
		m = self._ns_color.getRed_green_blue_alpha_
		try:
			return m()
		except TypeError:
			return m(None, None, None, None)

export(Color)
