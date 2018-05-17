#--------------------------------------------------------------------
#
#   PyGUI - ViewBase - Win32
#
#--------------------------------------------------------------------

import win32gui as gui 
from GUI import export
from GUI import application
from GUI.GViewBases import ViewBase as GViewBase

class ViewBase(GViewBase):
	
	_win_captures_mouse = True
	
	_cursor = None

#	def track_mouse(self):
#		#print "ViewBase.track_mouse: enter" ###
#		self._win_tracking_mouse = True
#		try:
#			while 1:
#				application().event_loop()
#				event = self._win_mouse_event
#				yield event
#				if event.kind == 'mouse_up':
#					break
#		finally:
#			self._win_tracking_mouse = False
#		#print "ViewBase.track_mouse: exit" ###
		
	def track_mouse(self):
		self._win_tracking_mouse = True
		while 1:
			application().event_loop()
			event = self._win_mouse_event
			yield event
			if event.kind == 'mouse_up':
				break
		self._win_tracking_mouse = False

	def get_cursor(self):
		return self._cursor
	
	def set_cursor(self, c):
		self._cursor = c

	def OnSetCursor(self, wnd, hit, message):
		if hit == 1: # HTCLIENT
			cursor = self._cursor
			if cursor:
				gui.SetCursor(cursor._win_cursor)
				return
		self._win.OnSetCursor(wnd._win, hit, message)

export(ViewBase)
