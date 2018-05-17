#
#   Basic cursor test
#

from GUI import Window, StdCursors, application
from TestViews import TestDrawing
from TestScrollableViews import TestScrollableView
from testing import say

def test():
	cursor = StdCursors.finger
	win = Window(title = "Cursor", width = 500, height = 400)
	view1 = TestDrawing(position = (20, 20), size = (100, 70), cursor = cursor)
	view2 = TestScrollableView(position = (140, 20), size = (200, 200),
		scrolling = 'hv')
	view2.cursor = cursor
	win.add(view1)
	win.place(view2, sticky = 'nsew')
	win.shrink_wrap((20, 20))
	win.show()

instructions = """
There should be a window containing two views. The cursor should be a
pointing finger over both views.

Check that the cursor is properly masked and has the hotspot in the
correct place.

Check that the cursor areas remain correct when the window is resized
and the scrolling view is scrolled.
"""

say(instructions)
test()
application().run()
