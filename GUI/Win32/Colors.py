#--------------------------------------------------------------------
#
#   PyGUI - Color utilities - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32api as api
from GUI import Color

def rgb(red, green, blue, alpha = 1.0):
	color = Color()
	color._red = red
	color._green = green
	color._blue = blue
	color._alpha = alpha
	color._win_color = (
		int(red * 255) |
		int(green * 255) << 8 |
		int(blue * 255) << 16)
	color._win_argb = (
		int(blue * 255) |
		int(green * 255) << 8 |
		int(red * 255) << 16 |
		int(alpha * 255) << 24)
	return color

selection_forecolor = Color._from_win_color(
	api.GetSysColor(wc.COLOR_HIGHLIGHTTEXT))

selection_backcolor = Color._from_win_color(
	api.GetSysColor(wc.COLOR_HIGHLIGHT))
