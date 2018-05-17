#
#   Python GUI - Buttons - Generic
#

from GUI.Properties import overridable_property
from GUI.Actions import Action
from GUI import Control

class Button(Control, Action):
	""" A pushbutton control."""
	
	style = overridable_property('style',
		"One of 'normal', 'default', 'cancel'")

	def activate(self):
		"""Highlight the button momentarily and then perform its action."""
		self.flash()
		self.do_action()

	def flash(self):
		"""Highlight the button momentarily as though it had been clicked,
		without performing the action."""
		raise NotImplementedError
