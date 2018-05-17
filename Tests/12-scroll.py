from GUI import Window, Button, CheckBox, application
from TestScrollableViews import TestScrollableView
from testing import say

class TestWindow(Window):

	def __init__(self, **kwds):
		Window.__init__(self, **kwds)
		self.view = TestScrollableView(container = self,
			x = 20, y = 20,
			width = 300, height = 300)#, scrolling = 'hv')
		self.view.report_update_rect = True
		if 1: ###
			self.h_scrolling_ctrl = CheckBox("Horizontal Scrolling",
				value = 'h' in self.view.scrolling, 
				action = 'horz_scrolling')
			self.v_scrolling_ctrl = CheckBox("Vertical Scrolling",
				value = 'v' in self.view.scrolling,
				action = 'vert_scrolling')
			self.border_ctrl = CheckBox("Border", value = 1, action = 'change_border')
			CheckBox("Vertical Scrolling", value = 1, action = 'vert_scrolling'),
			buttons = self.create_buttons()
			x = self.view.right + 5
			y = self.view.top
			for b in buttons:
				b.position = (x, y)
				self.add(b)
				y = b.bottom + 5
			#self.shrink_wrap()
			self.view.become_target()
	
	def create_buttons(self):
		return [
			Button("Scroll Left", action = ('scroll', -16, 0)),
			Button("Scroll Right", action = ('scroll', 16, 0)),
			Button("Scroll Up", action = ('scroll', 0, -16)),
			Button("Scroll Down", action = ('scroll', 0, 16)),
			Button("Small Extent", action = ('extent', 100, 100)),
			Button("Medium Extent", action = ('extent', 500, 500)),
			Button("Large Extent", action = ('extent', 1000, 1000)),
			self.h_scrolling_ctrl,
			self.v_scrolling_ctrl,
			self.border_ctrl,
		]
	
	def scroll(self, dx, dy):
		self.view.scroll_by(dx, dy)
	
	def extent(self, w, h):
		self.view.extent = (w, h)
		self.view.invalidate()
		say("Extent =", self.view.extent)
	
	def horz_scrolling(self):
		self.view.hscrolling = self.h_scrolling_ctrl.value

	def vert_scrolling(self):
		self.view.vscrolling = self.v_scrolling_ctrl.value
	
	def change_border(self):
		self.view.border = self.border_ctrl.value

win = TestWindow(size = (500, 500))
win.show()

instructions = """
There should be a scrolling view containing a diagonal row of red
triangles on a white background. All scrolling controls should work
properly.

The extent of the view is marked with a black border. Ensure that the
scrolling range extends exactly to the outer edge of this border in
all directions for Medium and Large extents. For Small extent, the
scroll bars should be disabled.

Buttons down the right side can be used to simulate clicking on the
scroll arrows and to change the extent. Ensure that the scroll bars
are updated accordingly when these buttons are used.
"""

say(instructions)
application().run()
