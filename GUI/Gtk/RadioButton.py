#
#		Python GUI - Radio buttons - Gtk
#

import gtk
from GUI import export
from GUI.GRadioButtons import RadioButton as GRadioButton

class RadioButton(GRadioButton):
	
	def __init__(self, title = "New Control", **kwds):
		gtk_radiobutton = gtk.RadioButton(None, title)
		gtk_radiobutton.show()
		self._gtk_connect(gtk_radiobutton, 'toggled', self._gtk_toggled_signal)
		GRadioButton.__init__(self, _gtk_outer = gtk_radiobutton, **kwds)
	
	def _value_changed(self):
		group = self._group
		if group:
			if self._value == group._value:
				self._turn_on()
			else:
				group._turn_all_off()
	
	def _turn_on(self):
		self._gtk_outer_widget.set_active(1)
	
	def _is_on(self):
		return self._gtk_outer_widget.get_active()

	def _gtk_toggled_signal(self):
		if self._is_on():
			group = self._group
			if group and group._value <> self._value:
				group._value = self._value
				group.do_action()

export(RadioButton)
