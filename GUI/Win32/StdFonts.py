#--------------------------------------------------------------------
#
#   PyGUI - Standard Fonts - Win32
#
#--------------------------------------------------------------------

from __future__ import division
import win32con as wc, win32gui as gui, win32ui as ui
from GUI import Font
from GUI.WinUtils import win_none

def _get_win_ppi():
	dc = win_none.GetDC()
	ppi = dc.GetDeviceCaps(wc.LOGPIXELSY)
	win_none.ReleaseDC(dc)
	return ppi

_win_ppi = _get_win_ppi()

def _win_pts_to_pixels(x):
	return int(round(x * _win_ppi / 72))

def _win_stock_font(id):
	h = gui.GetStockObject(id)
	lf = gui.GetObject(h)
	return Font._from_win_logfont(lf)

#system_font = _win_stock_font(wc.SYSTEM_FONT)
#system_font = _win_stock_font(17) # DEFAULT_GUI_FONT
#system_font = Font._from_win(win_none)
#system_font = Font("System", 13)
#system_font = Font("Tahoma", 10)
#system_font = Font("Tahoma", 11)
system_font = Font("Tahoma", _win_pts_to_pixels(8))
#print "StdFonts: System font ascent =", system_font.ascent
#print "StdFonts: System font descent =", system_font.descent
application_font = system_font
