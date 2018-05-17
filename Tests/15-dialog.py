from GUI import Dialog, Label, Button, application
from GUI.StdButtons import DefaultButton, CancelButton
from testing import say

class TestDialog(Dialog):

	def ok(self):
		say("OK")
	
	def cancel(self):
		say("Cancel")

dlog = TestDialog(width = 250)
lbl = Label(text = "Eject the tomato?")
ok_btn = DefaultButton()
cancel_btn = CancelButton()

dlog.place(lbl, left = 20, top = 20)
dlog.place(ok_btn, left = 20, top = lbl + 20)
dlog.place(cancel_btn, right = -20, top = lbl + 20)
dlog.height = ok_btn.bounds[3] + 20

dlog.show()

instructions = """
There should be a non-modal dialog with two buttons in 'default' and
'cancel' styles. The window should be movable but not resizable.

Messages should be printed when the buttons are pressed (although they
should not dismiss the dialog). Return and Enter should activate the
OK button, and Escape should activate the Cancel button.

On platforms without an application-wide menu bar, the window should
not have a menu bar, but the keyboard equivalent of the Quit command
should still work.
"""

say(instructions)
application().run()
