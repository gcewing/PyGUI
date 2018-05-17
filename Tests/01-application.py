#
#   Python GUI - Test application and menus
#

import sys
from GUI import Application, Window
from testing import say

class TestApp(Application):

	def __init__(self):
		Application.__init__(self)
	
	def key_down(self, event):
		say("Key down: %s\n" % event)
		if event.char == "E":
			raise Exception("This is a test exception.")
	
	def key_up(self, event):
		say("Key up: %s\n" % event)
	
	def auto_key(self, event):
		say("Auto key: %s\n" % event)

app = TestApp()

#say("Created TestApp")

if not app.zero_windows_allowed():
	#say("Creating window")
	win = Window(title = "TestApp")
	#say("Created window")
	win.show()
	#say("Shown window")

instructions = """
On platforms capable of running an application without windows,
there should be no windows, otherwise there should be a single
window.

If menus have been implemented, the standard menus should be
available, the New, Open and Quit items should be enabled, and
the Quit command should work both by menu selection and keyboard
equivalent. The Page Setup command should be enabled and working
if implemented.

Key down, key up and auto key events should be reported.

Type capital E to test exception handling. Either a dialog
box should appear reporting the exception, or if dialog boxes
are not yet implemented, the message 'Exception while handling
exception' should be printed followed by two tracebacks.
"""

say(instructions)
app.run()
