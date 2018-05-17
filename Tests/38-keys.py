#
#   Python GUI - Test keys
#

from GUI import Window, run
from testing import say

class TestWindow(Window):

	def key_down(self, event):
		say("char = %r key = %r unichars = %r _keycode = 0x%04x" % (
			event.char, event.key, event.unichars, event._keycode))

instructions = """
Check that the correct 'char' and 'key' values are produced
for all keys.
"""

say(instructions)
win = TestWindow(title = "Test Keys")
win.show()
run()
