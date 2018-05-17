#--------------------------------------------------------------------
#
#   PyGUI - Win32 - ComboBox
#
#--------------------------------------------------------------------

import win32ui as ui, win32con as wc, win32gui as gui

class ComboBox(object):
	
	def __init__(self, parent, pos, size, style = wc.CBS_DROPDOWNLIST):
		parent_hwnd = parent.GetSafeHwnd()
		self.hwnd = gui.CreateWindow("COMBOBOX", "Blarg",
			wc.WS_CHILD | wc.CBS_DROPDOWNLIST,
			pos[0], pos[1], size[0], size[1],
			parent_hwnd, 0, 0, None)
		self.pycwnd = ui.CreateWindowFromHandle(self.hwnd)
		print "ComboBox: pycwnd =", self.pycwnd ###
	
	def __del__(self):
		gui.DestroyWindow(self.hwnd)

	def ShowWindow(self):
		gui.ShowWindow(self.hwnd, wc.SW_SHOW)

	def AddString(self, text):
		print "ComboBox: Adding string %r" % text ###
		gui.SendMessage(self.hwnd, wc.CB_ADDSTRING, 0, text)


def CreateComboBox(parent, pos, size, style = wc.CBS_DROPDOWNLIST):
	parent_hwnd = parent.GetSafeHwnd()
	hwnd = gui.CreateWindow("COMBOBOX", "Blarg",
		wc.WS_CHILD | wc.CBS_DROPDOWNLIST,
		pos[0], pos[1], size[0], size[1],
		parent_hwnd, 0, 0, None)
	return ui.CreateWindowFromHandle(hwnd)
