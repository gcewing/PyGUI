#--------------------------------------------------------------
#
#   PyGUI - Pop-up list control - Gtk
#
#--------------------------------------------------------------

import gtk
from GUI import export
from GUI.GListButtons import ListButton as GListButton

class ListButton(GListButton):

	_gtk_suppress_action = False
	
	def __init__(self, **kwds):
		titles, values = self._extract_initial_items(kwds)
		self._titles = titles
		self._values = values
		gtk_widget = gtk.combo_box_new_text()
		gtk_widget.connect('changed', self._gtk_changed_signalled)
		gtk_widget.set_property('focus_on_click', False)
		gtk_widget.show()
		self._gtk_update_items(gtk_widget)
		GListButton.__init__(self, _gtk_outer = gtk_widget, **kwds)
	
	def _update_items(self):
		self._gtk_update_items(self._gtk_outer_widget)
	
	def _gtk_update_items(self, gtk_widget):
		self._gtk_suppress_action = True
		n = gtk_widget.get_model().iter_n_children(None)
		for i in xrange(n - 1, -1, -1):
			gtk_widget.remove_text(i)
		for title in self._titles:
			gtk_widget.append_text(title)
		self._gtk_suppress_action = False
	
	def _get_selected_index(self):
		return self._gtk_outer_widget.get_active()

	def _set_selected_index(self, i):
		self._gtk_suppress_action = True
		self._gtk_outer_widget.set_active(i)
		self._gtk_suppress_action = False

	def _gtk_changed_signalled(self, _):
		if not self._gtk_suppress_action:
			self.do_action()

export(ListButton)
