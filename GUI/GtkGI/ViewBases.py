#
#   Python GUI - View Base - Gtk
#

from gi.repository import Gtk
from GUI.GViewBases import ViewBase as GViewBase

class ViewBase(GViewBase):

	def __init__(self, **kwds):
		GViewBase.__init__(self, **kwds)
		self._gtk_connect(self._gtk_inner_widget, 'realize', self._gtk_realize)
	
	def track_mouse(self):
		finished = 0
		while not finished:
			self._mouse_event = None
			while not self._mouse_event:
				Gtk.main_iteration()
			event = self._mouse_event
			if event.kind == 'mouse_up':
				finished = 1
			yield event

	def _cursor_changed(self):
		gtk_widget = self._gtk_inner_widget
		gdk_window = gtk_widget.get_window()
		if gdk_window:
			cursor = self._cursor
			if cursor:
				gdk_window.set_cursor(self._cursor._gtk_cursor)
			else:
				gdk_window.set_cursor(None)
	
	def _gtk_realize(self):
		self._cursor_changed()

	def _targeted(self):
		self.targeted()
	
	def _untargeted(self):
		self.untargeted()
