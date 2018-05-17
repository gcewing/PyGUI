#--------------------------------------------------------------------
#
#   PyGUI - Control - Win32
#
#--------------------------------------------------------------------

from math import ceil
import win32con as wc, win32ui as ui
from GUI import export
from GUI.StdColors import black
from GUI.StdFonts import system_font
from GUI.WinUtils import win_none, win_null_hbrush
from GUI.GControls import Control as GControl

class Control(GControl):

	_vertical_padding = 5 # Amount to add when calculating height from font size

	_color = black
	_just = 'left'
	_font = None
	
	def get_title(self):
		return self._win.GetWindowText()
	
	def set_title(self, x):
		self._win.SetWindowText(x)
	
	def get_enabled(self):
		return self._win.IsWindowEnabled()
	
	def set_enabled(self, x):
		self._win.EnableWindow(x)
	
#	def get_visible(self, x):
#		self._win.IsWindowVisible()
#	
#	def set_visible(self, x):
#		if x:
#			self._win.ShowWindow(wc.SW_SHOW)
#		else:
#			self._win.ShowWindow(wc.SW_HIDE)

	def get_font(self):
		return self._font
	
	def set_font(self, x):
		self._font = x
		self._win.SetFont(x._win_font)
		self.invalidate()
	
	def get_color(self):
		return self._color
	
	def set_color(self, x):
		self._color = x
		self.invalidate()
	
	def get_just(self):
		return self._just
	
	def set_just(self, x):
		self._just = x
		self.invalidate()

	def _win_create_button(self, title, style, w, h):
		w = int(ceil(w))
		win = ui.CreateButton()
		win.CreateWindow(title, style, (0, 0, w, h), win_none, 0)
		#if self._win_transparent:
		#	win.ModifyStyleEx(0, wc.WS_EX_TRANSPARENT, 0)
		win.ShowWindow(wc.SW_SHOW)
		return win

	def _win_on_ctlcolor(self, dc, typ):
		#print "Control._win_on_ctlcolor:", self ###
		c = self._color
		if c:
			dc.SetTextColor(c._win_color)
		if self._win_transparent:
			dc.SetBkMode(wc.TRANSPARENT)
			return win_null_hbrush

	def _win_predict_font(self, kwds):
		return kwds.setdefault('font', system_font)

export(Control)
