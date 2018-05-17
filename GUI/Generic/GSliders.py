#
#   Python GUI - Slider - Generic
#

from GUI.Properties import overridable_property
from GUI.Actions import Action
from GUI import Control

class Slider(Control, Action):
	"""A control for entering a value by moving a knob along a scale.
	
	Constructor:
		Slider(orient)
			where orient = 'h' for horizontal or 'v' for vertical.
	"""
	
	_default_length = 100
	
	value = overridable_property('value', "The current value of the control")
	min_value = overridable_property('min_value', "Minimum value of the control")
	max_value = overridable_property('max_value', "Maximum value of the control")
	range = overridable_property('range', "Tuple (min_value, max_value)")
	ticks = overridable_property('ticks', "Number of tick marks")
	discrete = overridable_property('discrete', "Whether to constrain value to ticks")
	live = overridable_property('live', "Whether to invoke action continuously while dragging")

	def get_range(self):
		return (self.min_value, self.max_value)
	
	def set_range(self, x):
		self.min_value = x[0]
		self.max_value = x[1]
