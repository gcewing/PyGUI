#
#		Python GUI - Application class - Gtk
#

import sys
import gtk
from GUI import export
from GUI import application
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
#		#print "Application.handle_events: entering gtk.main" ###
#		_call_with_excepthook(gtk.main, gtk.main_quit)
#		#print "Application.handle_events: returned from gtk.main" ###

	def handle_next_event(self, modal_window = None):
		_call_with_excepthook(gtk.main_iteration)
		self._check_for_no_windows()
	
#	def _quit(self):
#		self._quit_flag = True
#		gtk.main_quit()
	
#	def _exit_event_loop(self):
#		gtk.main_quit()

	def get_target_window(self):
		for window in self._windows:
			if window._gtk_outer_widget.has_focus:
				return window
		return None

	def zero_windows_allowed(self):
		return 0
	
	def query_clipboard(self):
		return _gtk_clipboard.available()
	
	def get_clipboard(self):
		return _gtk_clipboard.get()
	
	def set_clipboard(self, data):
		_gtk_clipboard.set(data)

#------------------------------------------------------------------------------

class GtkClipboard(gtk.Window):

	data = ""

	def __init__(self):
		gtk.Window.__init__(self)
		self.realize()
		self.connect('selection_get', self.selection_get_signalled)
		self.connect('selection_received', self.selection_received_signalled)
		self.selection_add_target("CLIPBOARD", "STRING", 0)

	def selection_get_signalled(self, w, selection_data, info, time_stamp):
		#print "Clipboard.selection_get_signalled" ###
		selection_data.set_text(self.data, len(self.data))
	
	def selection_received_signalled(self, w, selection_data, info):
		#print "Clipboard.selection_received_signalled:", selection_data ###
		type = str(selection_data.type)
		if type == "STRING":
			data = selection_data.get_text()
		elif type == "ATOM":
			data = selection_data.get_targets()
		else:
			#print "Clipboard.selection_received_signalled: Unknown type: %r" % type
			data = None
		#print "...data =", repr(data) ###
		self.received_data = data
	
	def request(self, target, default):
		#  Get the contents of the clipboard.
		#print "Clipboard.request:", target ###
		self.received_data = -1
		self.selection_convert("CLIPBOARD", target)
		while self.received_data == -1:
			gtk.main_iteration()
		data = self.received_data
		self.received_data = None
		if data is None:
			data = default
		#print "Clipboard.request ->", repr(data) ###
		return data
	
	def available(self):
		targets = self.request("TARGETS", ())
		#print "Clipboard.available: targets =", repr(targets) ###
		return "STRING" in map(str, targets)

	def get(self):
		#  Get the contents of the clipboard.
		text = self.request("STRING", "")
		#print "Clipboard.get ->", repr(text) ###
		return text
		
	def set(self, text):
		#  Put the given text on the clipboard.
		#print "Clipboard.set:", text ###
		self.data = text
		result = self.selection_owner_set("CLIPBOARD")
		#print "...result =", result ###

#------------------------------------------------------------------------------

_gtk_clipboard = GtkClipboard()

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

export(Application)
