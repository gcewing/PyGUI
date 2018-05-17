#--------------------------------------------------------------------
#
#   PyGUI - ListButton - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui, win32gui as gui
from GUI import export
from GUI.WinUtils import win_none
from GUI.WinComboBox import CreateComboBox
from GUI.GListButtons import ListButton as GListButton

class ListButton(GListButton):

	_pass_key_events_to_platform = True

	def __init__(self, **kwds):
		titles, values = self._extract_initial_items(kwds)
		self._titles = titles
		self._values = values
		win = CreateComboBox(win_none, (0, 0), (100, 320), wc.CBS_DROPDOWNLIST)
		win.ShowWindow()
		self._win_update_items(win)
		GListButton.__init__(self, _win = win, **kwds)
	
	def _update_items(self):
		self._win_update_items(self._win)
	
	def _win_update_items(self, win):
		win.ResetContent()
		for title in self._titles:
			win.AddString(title)

	def _get_selected_index(self):
		return self._win.GetCurSel()
	
	def _set_selected_index(self, x):
		try:
			self._win.SetCurSel(x)
		except ui.error:
			pass
	
	def _cbn_sel_change(self):
		self.do_action()


export(ListButton)
