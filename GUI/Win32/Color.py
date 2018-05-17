#--------------------------------------------------------------------
#
#   PyGUI - Color - Win32
#
#--------------------------------------------------------------------

from __future__ import division
import win32con as wc, win32ui as ui
from GUI import export
from GUI.GColors import Color as GColor

#--------------------------------------------------------------------

class Color(GColor):
	#  _win_color   00BBGGRR
	#  _win_argb    AARRGGBB

	_win_brush_cache = None

	def get_red(self):
		return self._red
	
	def get_green(self):
		return self._green
	
	def get_blue(self):
		return self._blue
	
	def get_alpha(self):
		return self._alpha

	def _get_win_brush(self):
		b = self._win_brush_cache
		if not b:
			b = ui.CreateBrush(wc.BS_SOLID, self._win_color, 0)
			self._win_brush_cache = b
		return b
	
	_win_brush = property(_get_win_brush)

	def _from_win_color(cls, c):
		self = cls.__new__(cls)
		self._win_color = c
		r = c & 0xff
		g = (c >> 8) & 0xff
		b = (c >> 16) & 0xff
		self._red = r / 255
		self._green = g / 255
		self._blue = b / 255
		self._alpha = 1.0
		self._win_argb = 0xff000000 | (r << 16) | (g << 8) | b
		return self

	_from_win_color = classmethod(_from_win_color)

	def _from_win_argb(cls, c):
		self = cls.__new__()
		self._win_argb = c
		a = (c >> 24) & 0xff
		r = (c >> 16) & 0xff
		g = (c >> 8) & 0xff
		b = c & 0xff
		self._red = r / 255
		self._green = g / 255
		self._blue = b / 255
		self._alpha = a / 255
		self._win_color = (b << 16) | (g << 8) | r

export(Color)
