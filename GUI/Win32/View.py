#--------------------------------------------------------------------
#
#   PyGUI - View - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui
from GUI import export
from GUI.WinUtils import win_none
from GUI.GViews import View as GView

win_style = wc.WS_VISIBLE
win_default_rect = (0, 0, GView._default_size[0], GView._default_size[1])

class View(GView):
	
	def __init__(self, **kwds):
		win = ui.CreateWnd()
		win.CreateWindow(None, None, win_style, win_default_rect,
			win_none, 0)
		GView.__init__(self, _win = win)
		self.set(**kwds)

export(View)
