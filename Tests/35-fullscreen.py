#
#   Python GUI - Test fullscreen windows
#

from GUI import Window, Label, run
from testing import say

class TestWindow(Window):

	def mouse_down(self, event):
		say("Mouse down in", self.title)
	
	def key_down(self, event):
		say("Key down in", self.title)
		self.other.show()

win1 = TestWindow(title = "Fullscreen", style = 'fullscreen')
win1.show()

lbl = Label("Fullscreen", x = 300, y = 20)
win1.add(lbl)

win2 = TestWindow(title = "Not Fullscreen")
	
win1.other = win2
win2.other = win1
win2.show()

instructions = """
There should be two windows, one fullscreen and one not fullscreen.
The fullscreen window should have no title bar or other decorations
and should fill the whole screen. Pressing a key should bring one or
the other to the front. On MacOSX, the menu bar should be hidden when
the fullscreen window is frontmost. Menu command key equivalents
should still work.
"""

say(instructions)
run()
