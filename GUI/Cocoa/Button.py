#
#   Python GUI - Buttons - PyObjC version
#

import AppKit
from GUI import export
from GUI.StdFonts import system_font
from GUI.ButtonBasedControls import ButtonBasedControl
from GUI.GButtons import Button as GButton

_style_to_ns_key_equivalent = {
	'default': "\x0d",
	'cancel': "\x1b",
}

_ns_key_equivalent_to_style = {
	"\x0d": 'default',
	"\x1b": 'cancel',
}

class Button(ButtonBasedControl, GButton):

	_default_tab_stop = None

	def __init__(self, title = "New Button", font = system_font, **kwds):
		ns_button = self._create_ns_button(title = title, font = font,
			ns_button_type = AppKit.NSMomentaryLight,
			ns_bezel_style = AppKit.NSRoundedBezelStyle,
			padding = (10, 2)
		)
		GButton.__init__(self, _ns_view = ns_button, **kwds)
	
	def get_style(self):
		ns_key = self._ns_view.getKeyEquivalent()
		return _ns_key_equivalent_to_style.get(ns_key, 'normal')
	
	def set_style(self, style):
		ns_key = _style_to_ns_key_equivalent.get(style, "")
		self._ns_view.setKeyEquivalent_(ns_key)

	def activate(self):
		self._ns_view.performClick_(None)

#	def key_down(self, e): ###
#		print "Button.key_down:", e ###

export(Button)
