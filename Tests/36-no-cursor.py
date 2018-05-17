#
#   Invisible cursor test
#

from GUI import Window, StdCursors, application
from TestViews import TestDrawing
from testing import say

def test():
	cursor = StdCursors.empty_cursor()
	win = Window(title = "No Cursor", width = 500, height = 400)
	view = TestDrawing(position = (20, 20), size = (300, 200),
		cursor = cursor)
	win.add(view)
	win.show()

instructions = """
There should be a window containing a view. The cursor should be
invisible when it is over the view.
"""

say(instructions)
test()
application().run()
