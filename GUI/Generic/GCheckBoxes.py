#
#		Python GUI - Check boxes - Generic
#

from GUI.Properties import overridable_property
from GUI import Control
from GUI.Actions import Action

class CheckBox(Control, Action):
	"""A CheckBox is a control used to represent a binary choice."""
	
	def __init__(self, **kwds):
		Control.__init__(self, **kwds)
	
	on = overridable_property('on', "Boolean value of the check box.")
	
	auto_toggle = overridable_property('auto_toggle', """If true,
		the check box's 'on' property will automatically be toggled
		before performing the action, if any.""")
	
	mixed = overridable_property('mixed', """If true, the check box
		is capable of displaying a mixed state.""")
	
	_auto_toggle = True
	_mixed = False
	
	def get_auto_toggle(self):
		return self._auto_toggle
	
	def set_auto_toggle(self, v):
		self._auto_toggle = v

	def get_mixed(self):
		return self._mixed
	
	def set_mixed(self, v):
		self._mixed = v

	def get_value(self):
		return self.on
	
	def set_value(self, x):
		self.on = x
