#
#		Python GUI - Radio buttons - Generic
#

from GUI.Properties import overridable_property
from GUI import Control

class RadioButton(Control):
	"""RadioButtons are used in groups to represent a 1-of-N
	choice. A group of RadioButtons is coordinated by a
	RadioGroup object. The 'group' property indicates the
	RadioGroup to which it belongs, and the 'value' property
	is the value to which the RadioGroup's value is set
	when this RadioButton is selected."""
	
	group = overridable_property('group', """The RadioGroup to
				which this radio button belongs.""")

	value = overridable_property('value', """The value to which
				the associated radio group's 'value' property should be
				set when this radio button is selected.""")

	_group = None
	_value = None

	#
	#		Properties
	#

	def get_group(self):
		return self._group

	def set_group(self, new_group):
		old_group = self._group
		if new_group is not old_group:
			if old_group:
				old_group._remove_item(self)
			self._group = new_group
			if new_group:
				new_group._add_item(self)

	def get_value(self):
		return self._value

	def set_value(self, new_value):
		old_value = self._value
		if new_value != old_value:
			self._value = new_value
			self._value_changed()
	
	def _value_changed(self):
		raise NotImplementedError
