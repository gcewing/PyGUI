#
#   Python GUI - Dialogs - Generic
#

from GUI import Globals
from GUI.Properties import overridable_property
from GUI.Actions import ActionBase, action_property
from GUI import Window

class Dialog(Window, ActionBase):

	_default_keys = "\r"
	_cancel_keys = "\x1b"

	default_button = overridable_property('default_button',
		"Button to be activated by the default key.")
	
	cancel_button = overridable_property('cancel_button',
		"Button to be activated by the cancel key.")
	
	_default_button = None
	_cancel_button = None

	default_action = action_property('default_action',
		"Action to perform when Return or Enter is pressed.")
	
	cancel_action = action_property('cancel_action',
		"Action to perform when Escape is pressed.")
	
	_default_action = 'ok'
	_cancel_action  ='cancel'

	def __init__(self, style = 'nonmodal_dialog', 
			closable = 0, zoomable = 0, resizable = 0, **kwds):
		if 'title' not in kwds:
			kwds['title'] = Globals.application_name
		Window.__init__(self, style = style, 
			closable = closable, zoomable = zoomable, resizable = resizable,
			**kwds)
	
	def get_default_button(self):
		return self._default_button
	
	def set_default_button(self, button):
		self._default_button = button
		if button:
			button.style = 'default'
			if not button.action:
				button.action  = 'do_default_action'
	
	def get_cancel_button(self):
		return self._cancel_button
	
	def set_cancel_button(self, button):
		self._cancel_button = button
		if button:
			button.style = 'cancel'
			if not button.action:
				button.action  = 'do_cancel_action'

	def key_down(self, event):
		#print "GDialog.key_down:", repr(event.char) ###
		c = event.char
		if c:
			if c in self._default_keys:
				self._activate_button(self.default_button) or self.do_default_action()
				return
			elif c in self._cancel_keys:
				self._activate_button(self.cancel_button) or self.do_cancel_action()
				return
		Window.key_down(self, event)

	def do_default_action(self):
		self.do_named_action('default_action')

	def do_cancel_action(self):
		self.do_named_action('cancel_action')

	def _activate_button(self, button):
		#print("GDialog._activate_button:", button)
		if button:
			button.activate()
			return True
		else:
			return False
