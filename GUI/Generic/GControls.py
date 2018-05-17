#
#   Python GUI - Controls - Generic
#

from GUI.Properties import overridable_property
from GUI import Component

class Control(Component):
	"""Abstract base class for components such as buttons, check
	boxes and text entry boxes."""

	title = overridable_property('title', "Title of the control.")
	value = overridable_property('value', "Value of the control.")
	enabled = overridable_property('enabled', "True if user can manipulate the control.")
	font = overridable_property('font')
	color = overridable_property('color')
	just = overridable_property('just', "Justification ('left', 'center' or 'right').")
	lines = overridable_property('lines',
		"Height of the control measured in lines of the current font.")
	tab_stop = overridable_property('tab_stop',
		"Whether tab key can navigate into this control.")
	editable = overridable_property('editable',
	    "Whether the value of the control can be changed by the user.")
	
	_vertical_padding = 0 # Extra height to add when setting 'lines' property
	_default_tab_stop = True
	_user_tab_stop_override = True
	_editable = True
	
	def __init__(self, font = None, lines = None, **kwds):
		Component.__init__(self, **kwds)
		#  If font and lines are both specified, must set font first.
		if font:
			self.font = font
		if lines is not None:
			self.lines = lines
	
	def get_lines(self):
		return int(round((self.height - self._vertical_padding) / self.font.line_height))
	
	def set_lines(self, num_lines):
		self.height = self._calc_height(self.font, num_lines)

	def _calc_height(self, font, num_lines = 1):
		return num_lines * font.line_height + self._vertical_padding

	def _is_targetable(self):
		return self.enabled
	
	def get_editable(self):
	    return self._editable
	
	def set_editable(self, x):
	    self._editable = x
