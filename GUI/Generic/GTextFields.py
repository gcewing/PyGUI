#
#   Python GUI - Text fields - Generic
#

from GUI.Properties import overridable_property
from GUI.Actions import ActionBase, action_property
from GUI import application
from GUI import Control
from GUI import EditCmdHandler

class TextField(Control, ActionBase, EditCmdHandler):
	"""A control for entering and editing small amounts of text."""
	
	text = overridable_property('text')
	selection = overridable_property('selection', "Range of text selected.")
	multiline = overridable_property('multiline', "Multiple text lines allowed.")
	password = overridable_property('password', "Display characters obfuscated.")
	enter_action = action_property('enter_action', "Action to be performed "
		"when the Return or Enter key is pressed.")
	escape_action = action_property('escape_action', "Action to be performed "
		"when the Escape key is pressed.")
	tab_action = action_property('tab_action', "Action to be performed "
		"when the Tab key is pressed.")
	text_changed_action = action_property('text_changed_action',
	    "Action to be performed when the text is changed by the user.")
	
	_may_be_password = True

	#_tabbable = True
	_default_tab_stop = True
	_user_tab_stop_override = False
#	_enter_action = 'do_default_action'
#	_escape_action = 'do_cancel_action'
	_tab_action = None
	
	_intercept_tab_key = True
	
	def __init__(self, **kwds):
		self._multiline = kwds.pop('multiline')
		Control.__init__(self, **kwds)
	
	def get_multiline(self):
		return self._multiline
	
	def key_down(self, event):
		#print "GTextField.key_down for", self ###
		c = event.char
		if c == '\r':
			if event.key == 'enter' or not self._multiline:
				if self.do_enter_action() == 'pass':
					self.pass_event_to_next_handler(event)
				return
		if c == '\x1b':
			if self.do_escape_action() == 'pass':
				self.pass_event_to_next_handler(event)
			return
		if c == '\t':
			if self.do_tab_action() == 'pass' or self._intercept_tab_key:
				self.pass_event_to_next_handler(event)
				return
		if not self.multiline:
			k = event.key
			if k == 'up_arrow' or k == 'down_arrow':
				self.pass_event_to_next_handler(event)
				return
		Control.key_down(self, event)		
	
	def setup_menus(self, m):
		Control.setup_menus(self, m)
		EditCmdHandler.setup_menus(self, m)

	def do_enter_action(self):
		return self.do_named_action('enter_action')

	def do_escape_action(self):
		return self.do_named_action('escape_action')
	
	def do_tab_action(self):
		return self.do_named_action('tab_action')
	
	def do_text_changed_action(self):
	    return self.do_named_action('text_changed_action')
	
	def _enter_action(self):
		return 'pass'

	def _escape_action(self):
		return 'pass'
	
	_text_changed_action = None

	def get_text_length(self):
		#  Implementations can override this if they have a more
		#  efficient way of getting the text length.
		return len(self.text)
	
	def get_value(self):
		return self.text
	
	def set_value(self, x):
		self.text = x

