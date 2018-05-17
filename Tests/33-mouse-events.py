#
#   PyGUI - Mouse event test

from GUI import Window, application
from TestViews import TestDrawing
from TestScrollableViews import TestScrollableDrawing
from TestInput import TestMouseEvents
from testing import say

class TestView(TestMouseEvents, TestDrawing):

	def __init__(self, name, **kwds):
		self.name = name
		TestDrawing.__init__(self, **kwds)
	
	def mouse_down(self, event):
		#self.become_target()
		TestMouseEvents.mouse_down(self, event)
	
	def report_mouse_event(self, mess):
		say("%s: %s" % (self.name, mess))


class TestScrollableView(TestMouseEvents, TestScrollableDrawing):

	def __init__(self, name, **kwds):
		self.name = name
		TestScrollableDrawing.__init__(self, scrolling = 'hv', **kwds)
	
	def mouse_down(self, event):
		#self.become_target()
		TestMouseEvents.mouse_down(self, event)
	
	def report_mouse_event(self, mess):
		say("%s: %s" % (self.name, mess))


win = Window()
view1 = TestView("View 1", width = 320, height = 200)
view2 = TestScrollableView("View 2", width = 320, height = 200)
win.place_row([view1, view2], left = 20, top = 20, spacing = 20)
view2.hstretch = 1
view2.vstretch = 1
win.shrink_wrap(padding = (20, 20))
win.show()
view1.become_target()

say("""
There should be two views. The following events should be reported
in either view: mouse_down, mouse_drag, mouse_up, mouse_move.

The right-hand view should resize with the window. Check that
mouse events are still reported correctly after resizing and after
scrolling the view.
""")

application().run()
