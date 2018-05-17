#
#   Python GUI - Test windows
#

from GUI import Window, run
from testing import say

class TestWindow(Window):

	def mouse_down(self, event):
		say(self.name, "Mouse down:", event)
	
	def mouse_drag(self, event):
		say(self.name, "Mouse drag:", event)
	
	def mouse_up(self, event):
		say(self.name, "Mouse up:", event)
		print
	
	def key_down(self, event):
		say(self.name, "Key down:", event)

	def key_up(self, event):
		say(self.name, "Key up:", event)
		print

win1 = TestWindow(title = "Hello PyGUI!", 
	bounds = (50, 70, 250, 270),
	auto_position = False)
win1.name = "Win1"
win1.show()

win2 = TestWindow(title = "Hello Again!",
	auto_position = False, 
	position = (300, 70),
	size = (400, 300),
	resizable = 0)
win2.name = "Win2"
win2.show()

instructions = """
There should be two windows, one titled 'Hello PyGUI!' positioned at (50, 70)
with size (200, 200) and resizable, and one titled 'Hello Again!' positioned
at (300, 70) with size (400, 300) and not resizable. Both should be movable
and closable.

Mouse down, mouse drag, mouse up, key down and key up events in both windows
should be reported. Mouse drag and mouse up events should be reported for the
window in which the preceding mouse down event occurred, and should be reported
even if the mouse is moved outside the original window.
"""

say(instructions)
say("win1 position =", win1.position, "size =", win1.size)
say("win2 position =", win2.position, "size =", win2.size)

run()
