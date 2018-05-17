#
#		Python GUI - Application class - Gtk
#

import sys
from gi.repository import Gtk, Gdk
from GUI.Globals import application
from GUI.GApplications import Application as GApplication

class Application(GApplication):

	_in_gtk_main = 0

	def run(self):
		GApplication.run(self)

	def set_menus(self, menu_list):
		GApplication.set_menus(self, menu_list)
		for window in self._windows:
			window._gtk_update_menubar()
	
#	def handle_events(self):
#		#print "Application.handle_events: entering Gtk.main" ###
#		_call_with_excepthook(Gtk.main, Gtk.main_quit)
#		#print "Application.handle_events: returned from Gtk.main" ###

	def handle_next_event(self, modal_window = None):
		_call_with_excepthook(Gtk.main_iteration)
	
#	def _quit(self):
#		self._quit_flag = True
#		Gtk.main_quit()
	
#	def _exit_event_loop(self):
#		Gtk.main_quit()

	def get_target_window(self):
		for window in self._windows:
			if window._gtk_outer_widget.has_toplevel_focus():
				return window
		return None

	def zero_windows_allowed(self):
		return 0
	
	def query_clipboard(self):
		return _gtk_clipboard.wait_is_text_available()
	
	def get_clipboard(self):
		return _gtk_clipboard.wait_for_text()
	
	def set_clipboard(self, data):
		_gtk_clipboard.set_text(data, len(data))

#------------------------------------------------------------------------------

CLIPBOARD = Gdk.atom_intern("CLIPBOARD", False)

_gtk_clipboard = Gtk.Clipboard.get(CLIPBOARD)

#------------------------------------------------------------------------------

def _call_with_excepthook(proc, breakout = None):
	#  This function arranges for exceptions to be propagated
	#  across calls to the Gtk event loop functions.
	exc_info = []
	def excepthook(*args):
		exc_info[:] = args
		if breakout:
			breakout()
	old_excepthook = sys.excepthook
	try:
		sys.excepthook = excepthook
		proc()
	finally:
		sys.excepthook = old_excepthook
	if exc_info:
		#print "_call_with_excepthook: raising", exc_info ###
		raise exc_info[0], exc_info[1], exc_info[2]

	