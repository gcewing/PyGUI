#
#		Python GUI - Radio buttons - PyObjC
#

import AppKit
from AppKit import NSOnState, NSOffState
from GUI import export
from GUI.StdFonts import system_font
from GUI.ButtonBasedControls import ButtonBasedControl
from GUI.GRadioButtons import RadioButton as GRadioButton

class RadioButton(ButtonBasedControl, GRadioButton):
	
	def __init__(self, title = "New Radio Button", font = system_font, **kwds):
		ns_button = self._create_ns_button(title = title, font = font,
			ns_button_type = AppKit.NSRadioButton,
			ns_bezel_style = AppKit.NSRoundedBezelStyle)
		GRadioButton.__init__(self, _ns_view = ns_button, **kwds)

	def do_action(self):
		if self._group:
			self._group.value = self._value
		else:
			self._ns_view.setState_(NSOffState)
	
	def _value_changed(self):
		self._update()
	
	def _update(self):
		if self._group and self._value == self._group._value:
			state = NSOnState
		else:
			state = NSOffState
		self._ns_view.setState_(state)

export(RadioButton)
