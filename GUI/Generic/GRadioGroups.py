#
#		Python GUI - Radio groups - Generic
#

from GUI.Properties import Properties, overridable_property
from GUI.Actions import Action

class RadioGroup(Properties, Action):
	"""A RadioGroup coordinates a group of RadioButtons.
	It has a 'value' property which is equal to the value
	of the currently selected RadioButton. It may be given
	an action procedure to execute when its value changes.
	
	Operations:
		iter(group)
			Returns an iterator over the items of the group.
	"""
	
	value = overridable_property('value', """The value of the currently
		selected radio button.""")

	_items = None
	_value = None

	def __init__(self, items = [], **kwds):
		Properties.__init__(self, **kwds)
		self._items = []
		self.add_items(items)
	
	#
	#   Operations
	#
	
	def __iter__(self):
		return iter(self._items)

	#
	#		Properties
	#

	def get_value(self):
		return self._value

	def set_value(self, x):
		if self._value <> x:
			self._value = x
			self._value_changed()
			self.do_action()
	
	#
	#		Adding and removing items
	#

	def add_items(self, items):
		"Add a sequence of RadioButtons to this group."
		for item in items:
			self.add_item(item)
	
	def add_item(self, item):
		"Add a RadioButton to this group."
		item.group = self

	def remove_items(self, items):
		"Remove a sequence of RadioButtons from this group."
		for item in items:
			item.group = None
	
	def remove_item(self, item):
		"Remove a RadioButton from this group."
		item.group = None

	def _add_item(self, item):
		self._items.append(item)
		self._item_added(item)
	
	def _remove_item(self, item):
		self._items.remove(item)
		self._item_removed(item)
	
	def _item_added(self, item):
		raise NotImplementedError

	def _item_removed(self, item):
		raise NotImplementedError

	def _value_changed(self):
		raise NotImplementedError
