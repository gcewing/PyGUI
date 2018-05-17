#
#   Python GUI - Common code for scrollable components - Gtk
#

from gi.repository import Gtk

gtk_scroll_policies = [Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS]

gtk_dummybar = Gtk.VScrollbar()
gtk_scrollbar_breadth = gtk_dummybar.get_preferred_width()
del gtk_dummybar

class Scrollable(object):

	def get_hscrolling(self):
		return self._gtk_outer_widget.get_property('hscrollbar-policy') <> Gtk.PolicyType.NEVER
	
	def set_hscrolling(self, value):
		self._gtk_outer_widget.set_property('hscrollbar-policy', gtk_scroll_policies[value])
	
	def get_vscrolling(self):
		return self._gtk_outer_widget.get_property('vscrollbar-policy') <> Gtk.PolicyType.NEVER
	
	def set_vscrolling(self, value):
		self._gtk_outer_widget.set_property('vscrollbar-policy', gtk_scroll_policies[value])

