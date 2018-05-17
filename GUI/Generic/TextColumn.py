#-------------------------------------------------------------------------------
#
#		Python GUI - Table Text Column - Generic
#
#-------------------------------------------------------------------------------

from GUI import export
from GUI.Properties import overridable_property
from GUI import TableColumn

class TextColumn(TableColumn):

	font = overridable_property('font', "Font for displaying the data")
	format = overridable_property('format', "Formatting string")
	parser = overridable_property('parser', "Function for converting string to value")

	_format = None
	_parser = None
	_editor = None
	
	def get_format(self):
		return self._format
	
	def set_format(self, x):
		self._format = x
	
	def get_parser(self):
		return self._parser
	
	def set_parser(self, x):
		self._parser = x
	
	def format_value(self, value):
		"""Convert value to string for display, and also for editing with the
		default editor. Default is to perform %-formatting with the format property
		if specified, otherwise apply str to the value."""
		format = self.format
		if format:
			return format % value
		else:
			return str(value)

	def parse_value(self, text):
		"""Convert string to value when using the default editor. Default is to
		return the text unchanged."""
		parser = self.parser
		if parser:
			return parser(text)
		else:
			return text

export(TextColumn)
