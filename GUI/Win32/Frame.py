#--------------------------------------------------------------------
#
#   PyGUI - Frame - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui
from GUI import export
from GUI.WinUtils import win_none
from GUI.GFrames import Frame as GFrame

win_flags = wc.WS_CHILD | wc.WS_VISIBLE

class Frame(GFrame):

	_win_transparent = True

	def __init__(self, **kwds):
		w, h = self._default_size
		win = ui.CreateWnd()
		win.CreateWindow(None, None, win_flags, (0, 0, w, h), win_none, 0)
		GFrame.__init__(self, _win = win, **kwds)

export(Frame)
