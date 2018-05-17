#--------------------------------------------------------------
#
#   PyGUI - Pop-up list control - Generic
#
#--------------------------------------------------------------

from GUI.Properties import overridable_property
from GUI.Actions import Action
from GUI import Control, application

class ListButton(Control, Action):
	"""A button that displays a value and provides a pop-up or
	pull-down list of choices."""

	titles = overridable_property('titles',
		"List of item title strings")
	
	values = overridable_property('values',
		"List of values corresponding to tiles, or None to use item index as value")
	
	def _extract_initial_items(self, kwds):
		titles = kwds.pop('titles', None) or []
		values = kwds.pop('values', None)
		return titles, values

	def get_titles(self):
		return self._titles
	
	def set_titles(self, x):
		self._titles = x
		self._update_items()
	
	def get_values(self):
		return self._values
	
	def set_values(self, x):
		self._values = x
	
	def get_value(self):
		i = self._get_selected_index()
		if i >= 0:
			values = self.values
			if values:
				return values[i]
			else:
				return i

	def set_value(self, value):
		values = self.values
		if values:
			try:
				i = values.index(value)
			except ValueError:
				i = -1
		else:
			if value is None:
				i = -1
			else:
				i = value
		self._set_selected_index(i)

	def do_action(self):
		try:
			Action.do_action(self)
		except:
			application().report_error()
