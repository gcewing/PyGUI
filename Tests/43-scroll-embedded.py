from GUI import Window, Button, application
from TestScrollableViews import TestScrollableView
from testing import say

class TestWindow(Window):

	def __init__(self, **kwds):
		Window.__init__(self, **kwds)
		view = TestScrollableView(container = self,
			size = (300, 300),
			extent = (1000, 1000),
			scrolling = 'hv',
			anchor = 'ltrb')
		button = Button("Embedded", action = self.click)
		off = (300, 300)
		view.scroll_offset = off
		button.position = off
		view.add(button)
		self.shrink_wrap()

	def click(self):
		say("Embedded button clicked")

win = TestWindow(size = (500, 500))
win.show()

instructions = """
There should be a scrolling view with an embedded button. The
button should initially appear at the top left corner of the visible
part of the view. The button should move with the view's contents
when the view is scrolled.

Check that the button responds to mouse clicks properly before and
after scrolling.

Check that mouse clicks outside the button are reported as clicks in
the view before and after scrolling.

Check that everything works correctly after resizing the window.
"""

say(instructions)
application().run()
