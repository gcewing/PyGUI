#--------------------------------------------------------------------
#
#   PyGUI - Application - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui, win32clipboard as wcb, win32api as api, \
	win32gui as gui, win32process as wp
from GUI import export
from GUI import Component, Window, WinUtils
from GUI.GApplications import Application as GApplication

class Application(GApplication):

	def __init__(self, *args, **kwds):
		self._win_recycle_list = []
		self._win_app = ui.GetApp()
		self._win_app.AttachObject(self)
		self._win_app.SetMainFrame(WinUtils.win_none)
		GApplication.__init__(self, *args, **kwds)
	
	def set_menus(self, x):
		#print "Application.set_menus" ###
		GApplication.set_menus(self, x)
		for window in self.windows:
			window._win_menus_changed()
	
	def _event_loop(self, window):
		if window:
			window._begin_modal()
		try:
			self._win_app.Run()
		finally:
			if window:
				window._end_modal()

	def _exit_event_loop(self):
		api.PostQuitMessage(0)

	def zero_windows_allowed(self):
		return False
	
	def get_target(self):
		try:
			win = ui.GetFocus()
		except ui.error:
			win = None
		if isinstance(win, Component):
			return win
		else:
			return self

	def get_target_window(self):
		win = ui.GetActiveWindow()
		if isinstance(win, Window):
			return win
	
	def OnIdle(self, n):
		#print "Application.OnIdle" ###
		trash = self._win_recycle_list
		while trash:
			trash.pop().DestroyWindow()
		self._win_idle()
		return 0
	
	def _win_idle(self):
		self._check_for_no_windows()
	
	def _check_for_no_windows(self):
		#print "Application._check_for_no_windows" ###
		apid = wp.GetCurrentProcessId()
		#print "... apid =", apid ###
		htop = gui.GetDesktopWindow()
		hwin = gui.GetWindow(htop, wc.GW_CHILD)
		while hwin:
			wpid = wp.GetWindowThreadProcessId(hwin)[1]
			if wpid == apid:
				#print "... hwin", hwin ###
				if gui.GetWindowLong(hwin, wc.GWL_STYLE) & wc.WS_VISIBLE:
					#print "...... is visible" ###
					return
			hwin = gui.GetWindow(hwin, wc.GW_HWNDNEXT)
		#print "... none visible" ###
		self.no_visible_windows()

#	def PreTranslateMessage(self, msg):
#		print "Application.PreTranslateMessage:", msg ###

	def _win_recycle(self, win):
		#  It's not safe to destroy a window inside code called from its
		#  own OnCommand handler, so we use this method to delay it until
		#  a better time.
		self._win_recycle_list.append(win)

	def query_clipboard(self):
		wcb.OpenClipboard()
		result = wcb.IsClipboardFormatAvailable(wc.CF_TEXT)
		wcb.CloseClipboard()
		return result
	
	def get_clipboard(self):
		wcb.OpenClipboard()
		try:
			result = wcb.GetClipboardData()
		except TypeError:
			result = None
		wcb.CloseClipboard()
		return result
	
	def set_clipboard(self, x):
		wcb.OpenClipboard()
		wcb.SetClipboardData(wc.CF_TEXT, x)
		wcb.CloseClipboard()

export(Application)
