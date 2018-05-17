#
#		Python GUI - Radio groups - PyObjC
#

from GUI import export
from GUI.GRadioGroups import RadioGroup as GRadioGroup

class RadioGroup(GRadioGroup):

	def __init__(self, items = [], **kwds):
		GRadioGroup.__init__(self, items, **kwds)

	def _item_added(self, item):
		item._update()
	
	def _item_removed(self, item):
		pass
	
	def _value_changed(self):
		for item in self._items:
			item._update()

export(RadioGroup)
