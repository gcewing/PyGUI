#
#   Python GUI - Text Editor - Generic
#

from GUI.Properties import overridable_property
from GUI import Component
from GUI import EditCmdHandler
from GUI.Printing import Printable

class TextEditor(Component, EditCmdHandler, Printable):
	"""A component for editing substantial amounts of text. The text is
	kept internally to the component and cannot be shared between views."""
	
	text = overridable_property('text', "The contents as a string.")
	text_length = overridable_property('text_length', "Number of characters in the text.")
	selection = overridable_property('selection', "Range of text selected.")
	font = overridable_property('font')
	tab_spacing = overridable_property('tab_spacing', "Distance between tab stops")
	
	def setup_menus(self, m):
		Component.setup_menus(self, m)
		EditCmdHandler.setup_menus(self, m)
		Printable.setup_menus(self, m)

	def key_down(self, e):
		if e.key == 'enter':
			self.pass_to_next_handler('key_down', e)
		else:
			Component.key_down(self, e)

	def print_view(self, page_setup):
		from TextEditorPrinting import TextEditorPrintView
		view = TextEditorPrintView(self, page_setup)
		view.print_view(page_setup)
