#
#   PyGUI - Default control height test
#

import sys
from GUI import Window, Label, TextField, Button, CheckBox, RadioButton, Slider, \
	StdFonts, Font, run
from testing import say

#from AppKit import NSLayoutManager
#nslm = NSLayoutManager.alloc().init()
#
#def showfont(n, f):
#	say("%s: %s" % (n, f))
#	say("height = %s" %   f.height)
#	say("leading = %s" % f._ns_font.leading())
#	say("line height = %s" % nslm.defaultLineHeightForFont_(f._ns_font))

def main():
	f = None
	args = sys.argv[1:]
	if args:
		fontsize = int(args[0])
		sf = StdFonts.system_font
		f = Font(sf.family, fontsize, sf.style)
		#showfont("Using font", f)
	win = Window(title = "Heights")
	if f:
		kwds = {'font': f}
	else:
		kwds = {}
	controls = [
		Label(text = "Label", **kwds),
		TextField(text = "Text", **kwds),
		CheckBox(title = "Check", **kwds),
		RadioButton(title = "Radio", **kwds),
		Slider(orient = 'h', width = 50),
		#Button(title = "Button", **kwds),
	]
	#for ctl in controls:
	#	say("Height of %r is %s" % (ctl, ctl.height))
	win.place_row(controls, left = 10, top = 10)
	win.shrink_wrap(padding = (10, 10))
	win.show()
	run()

instructions = """
The controls should line up horizontally.
"""

say(instructions)
main()
