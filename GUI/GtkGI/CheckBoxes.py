#
#		Python GUI - Check boxes - Gtk
#

from gi.repository import Gtk
from GUI.GCheckBoxes import CheckBox as GCheckBox

class CheckBox(GCheckBox):
	
	def __init__(self, title = "New Control", **kwds):
		gtk_checkbox = Gtk.CheckButton(title)
		gtk_checkbox.show()
		self._gtk_connect(gtk_checkbox, 'clicked', self._gtk_clicked_signal)
		self._gtk_inhibit_action = 0
		GCheckBox.__init__(self, _gtk_outer = gtk_checkbox, **kwds)
	
	def get_on(self):
		gtk_checkbox = self._gtk_outer_widget
		if gtk_checkbox.get_inconsistent():
			return 'mixed'
		else:
			return gtk_checkbox.get_active()
	
	def set_on(self, state):
		mixed = state == 'mixed'
		if mixed:
			if not self._mixed:
				raise ValueError("CheckBox state cannot be 'mixed'")
			active = False
		else:
			active = bool(state)
		save = self._gtk_inhibit_action
		self._gtk_inhibit_action = 1
		try:
			gtk_checkbox = self._gtk_outer_widget
			gtk_checkbox.set_active(active)
			gtk_checkbox.set_inconsistent(mixed)
		finally:
			self._gtk_inhibit_action = save

	def _gtk_clicked_signal(self):
		gtk_checkbox = self._gtk_outer_widget
		if not self._gtk_inhibit_action:
			if self._auto_toggle:
				gtk_checkbox.set_inconsistent(False)
			else:
				save = self._gtk_inhibit_action
				self._gtk_inhibit_action = 1
				try:
					gtk_checkbox.set_active(not gtk_checkbox.get_active())
				finally:
					self._gtk_inhibit_action = save
			self.do_action()
