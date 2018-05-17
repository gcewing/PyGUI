#--------------------------------------------------------------------
#
#   PyGUI - Label - Win32
#
#--------------------------------------------------------------------

from math import ceil
import win32con as wc, win32ui as ui
from GUI import export
from GUI.StdColors import black
from GUI.StdFonts import system_font
from GUI.WinUtils import win_none
from GUI.GLabels import Label as GLabel

win_style = wc.WS_CLIPSIBLINGS | wc.WS_VISIBLE

win_dt_format = wc.DT_NOPREFIX | wc.DT_SINGLELINE | wc.DT_NOCLIP

win_dt_align_map = {
	'l': wc.DT_LEFT | win_dt_format,
	'c': wc.DT_CENTER | win_dt_format,
	'r': wc.DT_RIGHT | win_dt_format,
}

#--------------------------------------------------------------------

class Label(GLabel):

	_win_transparent = True
	
	_font = None
	_color = black
	_just = 'l'
	
	def __init__(self, text = "New Label", **kwds):
		self._set_lines(text)
		lines = self._lines
		font = self._win_predict_font(kwds)
		w = 0
		for line in lines:
			w = max(w, font.width(line))
		w = int(ceil(w))
		h = self._calc_height(font, len(lines))
		win = ui.CreateWnd()
		win.CreateWindow(None, None, win_style, (0, 0, w, h), win_none, 0)
		#win.ModifyStyleEx(0, wc.WS_EX_TRANSPARENT, 0)
		GLabel.__init__(self, _win = win, **kwds)
	
	def get_text(self):
		return "\n".join(self._lines)
	
	def set_text(self, x):
		self._set_lines(x)
		self.invalidate()
	
	def _set_lines(self, x):
		self._lines = x.split("\n")

	def OnPaint(self):
		win = self._win
		dc, paint_struct = win.BeginPaint()
		font = self._font
		win_font = font._win_font
		dc.SetBkMode(wc.TRANSPARENT)
		dc.SelectObject(win_font)
		c = self._color._win_color
		#print "Label.OnPaint: win color = 0x%08x" % c
		dc.SetTextColor(c)
		rm = self.width
		y = 0
		h = font.line_height
		just = self._just[:1]
		dt_format = win_dt_align_map[just]
		for line in self._lines:
			r = (0, y, rm, y + h)
			dc.DrawText(line, r, dt_format)
			y += h
		win.EndPaint(paint_struct)

export(Label)

