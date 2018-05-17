#
#   Python GUI - Labels - PyObjC
#

import AppKit
from AppKit import NSView
from GUI import export
from GUI.StdFonts import system_font
from GUI.TextFieldBasedControls import TextFieldBasedControl
from GUI.GLabels import Label as GLabel

ns_label_autoresizing_mask = (AppKit.NSViewWidthSizable
	| AppKit.NSViewHeightSizable)

class Label(TextFieldBasedControl, GLabel):
	
	def __init__(self, text = "New Label", font = system_font, **kwds):
		ns_textfield = self._create_ns_textfield(editable = False,
			text = text, font = font)
#		width, height = ns_textfield.frame().size
#		ns_view = NSView.alloc().initWithFrame_(((0, 0), (width, height + 5)))
#		ns_view.addSubview_(ns_textfield)
#		ns_textfield.setFrameOrigin_((0, 2))
#		ns_textfield.setAutoresizingMask_(ns_label_autoresizing_mask)
		ns_view = ns_textfield
		GLabel.__init__(self, _ns_view = ns_view, _ns_inner_view = ns_textfield, **kwds)

export(Label)
