#
#   PyGUI - Frame test
#

from GUI import Window, Frame, Label, run
from testing import say

def test():
	win = Window(title = "Frame")
	frm = Frame()
	frm.place_column([
		Label("This is"),
		Label("A frame")],
		left = 0, top = 0)
	frm.shrink_wrap()
	win.place(frm, left = 30, top = 30)
	win.shrink_wrap(padding = (30, 30))
	win.show()

instructions = """
There should be a window containing two labels
spaced 30 pixels from the edge of the window on
all sides.
"""

say(instructions)
test()
run()
