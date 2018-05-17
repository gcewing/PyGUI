#
#   Python GUI - Text Fields - PyObjC
#

from Foundation import NSRange
from GUI import export
from GUI.StdFonts import system_font #application_font
from GUI import EditCmdHandler
from GUI.TextFieldBasedControls import TextFieldBasedControl
from GUI.GTextFields import TextField as GTextField

class TextField(TextFieldBasedControl, GTextField):

	#_vertical_padding = 5
	_intercept_tab_key = False

	def __init__(self, text = "", font = system_font, 
			multiline = False, password = False, border = True, **kwds):
		ns_textfield = self._create_ns_textfield(editable = True,
			multiline = multiline, password = password,
			text = text, font = font, border = border)
		GTextField.__init__(self, _ns_view = ns_textfield, 
			multiline = multiline, **kwds)

	def get_selection(self):
		ns_editor = self._ns_editor()
		if ns_editor:
			start, length = ns_editor.selectedRange()
			return (start, start + length)
		else:
			return (0, 0)
	
	def set_selection(self, (start, end)):
		self.become_target()
		ns_editor = self._ns_editor()
		if ns_editor:
			ns_editor.setSelectedRange_(NSRange(start, end - start))
	
	def select_all(self):
		self.become_target()
		self._ns_view.selectText_(None)
	
	def get_editable(self):
		return self._ns_view.isEditable()
	
	def set_editable(self, x):
		self._ns_view.setEditable_(x)
		self._ns_view.setSelectable_(x)
		#print "TextField.set_editable: isEditable = %s, isSelectable = %s, isEnabled = %s, acceptsFirstResponder = %s" % (
		#	self._ns_view.isEditable(), self._ns_view.isSelectable(), self._ns_view.isEnabled(), self._ns_view.acceptsFirstResponder())

	def _ns_editor(self):
		return self._ns_view.currentEditor()
	
	def _ns_edit_cmd_target(self):
		return self._ns_editor()
	
export(TextField)
