#
#		Python GUI - Radio groups - Gtk
#

import gtk
from GUI import export
from GUI.GRadioGroups import RadioGroup as GRadioGroup

class RadioGroup(GRadioGroup):

	def __init__(self, items = [], **kwds):
		self._gtk_dummy_radiobutton = gtk.RadioButton()
		GRadioGroup.__init__(self, items, **kwds)
	
	def _item_added(self, item):
		old_value = self._value
		item._gtk_outer_widget.set_group(self._gtk_dummy_radiobutton)
		self.value = old_value
	
	def _item_removed(self, item):
		item._gtk_outer_widget.set_group(None)
		if item._value == self._value:
			self._value = None
			self._turn_all_off()

	def _value_changed(self):
		new_value = self._value
		for item in self._items:
			if item._value == new_value:
				item._turn_on()
				return
		self._turn_all_off()
	
	def _turn_all_off(self):
		self._gtk_dummy_radiobutton.set_active(1)

export(RadioGroup)
