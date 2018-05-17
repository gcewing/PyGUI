#--------------------------------------------------------------------
#
#   PyGUI - BaseAlert - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32gui as gui, win32api as api
from GUI import export
from GUI import application
from GUI.WinUtils import win_bg_color
from GUI import View
from GUI.GBaseAlerts import BaseAlert as GBaseAlert

win_icon_ids = {
	'stop':    wc.IDI_HAND,
	'caution': wc.IDI_EXCLAMATION,
	'note':    wc.IDI_ASTERISK,
	'query':   wc.IDI_QUESTION,
}

win_icon_size = (
	api.GetSystemMetrics(wc.SM_CXICON),
	api.GetSystemMetrics(wc.SM_CYICON)
)

def win_load_icon(id):
	return gui.LoadIcon(0, id)

class AlertIcon(View):

	_win_transparent = True

	def __init__(self, id, **kwds):
		View.__init__(self, size = win_icon_size, **kwds)
		#hwnd = self._win.GetSafeHwnd()
		self.win_icon = win_load_icon(id)
	
	def draw(self, c, r):
		gfx = c._win_graphics
		hdc = gfx.GetHDC()
		gui.DrawIcon(hdc, 0, 0, self.win_icon)
		gfx.ReleaseHDC(hdc)

#	def draw(self, c, r):
#		dc = c._win_dc
#		dc.DrawIcon((0, 0), self.win_icon)
		
class BaseAlert(GBaseAlert):

	_win_icon = None

	def _layout_icon(self, kind):
		id = win_icon_ids.get(kind)
		if id:
			icon = AlertIcon(id, position = (self._left_margin, self._top_margin))
			self.add(icon)
			return icon.size
		else:
			return (0, 0)

export(BaseAlert)
