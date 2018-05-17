#--------------------------------------------------------------------
#
#   PyGUI - RadioGroup - Win32
#
#--------------------------------------------------------------------

from GUI import export
from GUI.GRadioGroups import RadioGroup as GRadioGroup

class RadioGroup(GRadioGroup):

	def _item_added(self, item):
		item._win_update()
	
	def _item_removed(self, item):
		item._win_update()
	
	def _value_changed(self):
		for item in self._items:
			item._win_update()

export(RadioGroup)
