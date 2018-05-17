#
#   Python GUI - Common code for scrollable components - Gtk
#

import gtk
from GUI import export
from GUI import Globals

gtk_scroll_policies = [gtk.POLICY_NEVER, gtk.POLICY_ALWAYS]


class Scrollable(object):

	gtk_scrollbar_breadth = gtk.VScrollbar().size_request()[0] + 3
	s = gtk.ScrolledWindow().get_style()
	gtk_border_thickness = (s.xthickness, s.ythickness)
	del s

	def get_hscrolling(self):
		return self._gtk_outer_widget.get_property('hscrollbar-policy') <> gtk.POLICY_NEVER
	
	def set_hscrolling(self, value):
		self._gtk_outer_widget.set_property('hscrollbar-policy', gtk_scroll_policies[value])
	
	def get_vscrolling(self):
		return self._gtk_outer_widget.get_property('vscrollbar-policy') <> gtk.POLICY_NEVER
	
	def set_vscrolling(self, value):
		self._gtk_outer_widget.set_property('vscrollbar-policy', gtk_scroll_policies[value])

export(Scrollable)
