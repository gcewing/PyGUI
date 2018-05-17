#
#		Python GUI - Check boxes - PyObjC
#

import AppKit
from AppKit import NSOnState, NSOffState, NSMixedState
from GUI import export
from GUI.Actions import Action
from GUI.StdFonts import system_font
from GUI.ButtonBasedControls import ButtonBasedControl
from GUI.GCheckBoxes import CheckBox as GCheckBox

class CheckBox(ButtonBasedControl, GCheckBox):

	_ns_mixed = False
	
	def __init__(self, title = "New Check Box", font = system_font, **kwds):
		ns_button = self._create_ns_button(title = title, font = font,
			ns_button_type = AppKit.NSSwitchButton,
			ns_bezel_style = AppKit.NSRoundedBezelStyle)
		#if mixed:
		#	self._ns_mixed = True
		#	ns_button.setAllowsMixedState_(True)
		GCheckBox.__init__(self, _ns_view = ns_button, **kwds)
	
	def get_mixed(self):
		return self._ns_view.allowsMixedState()
	
	def set_mixed(self, x):
		self._ns_view.setAllowsMixedState_(x)
	
	def get_on(self):
		state = self._ns_view.state()
		if state == NSMixedState:
			return 'mixed'
		else:
			return state <> NSOffState
	
	def set_on(self, v):
		if v == 'mixed' and self.mixed:
			state = NSMixedState
		elif v:
			state = NSOnState
		else:
			state = NSOffState
		self._ns_view.setState_(state)

	def do_action(self):
		if not self._auto_toggle:
			self.on = not self.on
		Action.do_action(self)

export(CheckBox)
